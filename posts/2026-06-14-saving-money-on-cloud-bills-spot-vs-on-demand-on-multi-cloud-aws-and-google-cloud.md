---
title: "Saving Money on Cloud Bills: Spot vs. On-Demand on Multi-CLoud AWS and Google Cloud"
date: 2026-06-14
slug: saving-money-on-cloud-bills-spot-vs-on-demand-on-multi-cloud-aws-and-google-cloud
tags: [AWS, GCP, FinOps]
minutes: 4
summary: "Spot Instances offer up to 90% off, but providers can reclaim them. How to run a hybrid spot and on-demand setup on AWS and Google Cloud."
---

![](/assets/posts/saving-money-on-cloud-bills-spot-vs-on-demand-on-multi-cloud-aws-and-google-cloud/1.png)

Cloud servers can cost a lot of money. But there is a smart way to save cash: use **Spot Instances** (Google calls them Preemptible VMs). They are leftover servers that the cloud provider sells with a huge discount, often up to 90% off.

**The only problem?** The cloud provider can take them back with almost no warning if a full-paying customer needs them.

Because of this risk, you cannot run your whole website or app on Spot servers. If they disappear, your app crashes. You need a mix: **On-Demand** servers (expensive but they never turn off) for your core services, and **Spot** servers (cheap but risky) for extra scaling.

Both Amazon Web Services (AWS) and Google Cloud (GCP) have built-in tools to handle this automatically.

**Solution** - AWS with Karpenter and GCP with CCC - Custom Compute Classes

##

## **The AWS Way: Karpenter**

**Karpenter** acts like a smart parking attendant for your servers. It watches your app and spins up the exact servers you need in real time.

### **How the Fallback Works**

With Karpenter you can create a list of rules using "weights". You create two different profiles (called NodePools). Karpenter will always check the pool with the highest weight number first.

So, we will create 2 Profiles - spot-pool.yaml and ondemand-pool.yaml

**Spot Config File:**

```
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: primary-spot-pool
spec:
  weight: 100  # <--- High number means try this FIRST
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot"] # Only buy cheap spot servers
```

**OnDemand Config File:**

```
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: backup-ondemand-pool
spec:
  weight: 10   # <--- Low number means use only as a BACKUP
  template:
    spec:
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand"] # Buy safe, standard servers
```

When your app gets busy, Karpenter tries to buy cheap Spot servers because it sees the weight of 100. If AWS is completely sold out of Spot servers in your area, Karpenter instantly switches to the backup plan (Weight 10) and buys On-Demand servers. Your app stays online, and your customers never notice a thing.

### **What Happens During a Spot Shortage?**

Imagine your application suddenly receives more traffic.

1. Karpenter first tries the Spot NodePool because it has a higher weight.
2. AWS says: "Sorry, there is no Spot capacity available right now."
3. Karpenter automatically falls back to the On-Demand NodePool.
4. New On-Demand instances are launched.
5. Your application continues running without any outage.

This is a great design because reliability is never compromised.

##

### **Returning Back to Spot is Not Instant!!**

This is an important detail many people miss. Suppose AWS had no Spot capacity at 10:00 AM, so Karpenter launched expensive On-Demand instances.

At 10:10 AM, Spot capacity becomes available again.

**Will Karpenter immediately delete the On-Demand servers and move everything back to Spot?**

**No.**

Karpenter does not work like a real-time "Spot is back, move everything now" engine.

Instead, Karpenter runs a consolidation process. It checks whether nodes can be safely removed or replaced with cheaper options.

For example, with proper disruption settings:

```
disruption:
  consolidationPolicy: WhenEmptyOrUnderutilized
  consolidateAfter: 5m
```

Karpenter may eventually launch cheaper Spot instances, move workloads, and terminate the expensive On-Demand instances.

However, this depends on multiple factors:

* Consolidation settings.
* Whether moving the workload actually saves money.
* Pod Disruption Budgets (PDBs).
* Scheduling constraints.

So, Karpenter can return to Spot automatically, but it is not immediate.

## **The Google Way: Custom Compute Classes (CCC)**

Instead of creating multiple NodePools with weights, you create a single Compute Class that contains an ordered list of preferences.

For example:

1. First, try new cheap Spot machines.
2. If they are not available, try another Spot machine family.
3. If all Spot capacity is exhausted, fall back to On-Demand machines.

A simple CCC configuration looks like this:

```
apiVersion: cloud.google.com/v1
kind: ComputeClass
metadata:
  name: cost-optimized-compute
spec:
  priorities:
    - machineFamily: n4
      spot: true

    - machineFamily: n2
      spot: true

    - machineFamily: n4
      spot: false
```

When your application scales, GKE checks this list from top to bottom. If the first option is unavailable, it automatically tries the next one.

### **GKE's Power lies in Active Migration Feature**

You can enable Active Migration:

```
activeMigration: 
  optimizeRulePriority: true
```

Now, if GKE had to launch expensive On-Demand servers because Spot capacity was unavailable. Later, when cheaper Spot capacity comes back, GKE actively checks the priority list again. It can automatically:

1. Launch new Spot machines.
2. Move your workloads to those machines.
3. Remove the expensive On-Demand machines.

This gives GKE a more aggressive cost optimization behavior compared to Karpenter.

# AWS EKS vs GKE: Quick Comparison

|  |  |  |
| --- | --- | --- |
| Feature | AWS EKS (Karpenter) | Google GKE (CCC) |
| Spot fallback | Uses NodePool weights | Uses priority order |
| On-Demand backup | Yes | Yes |
| Automatic move back to Spot | Yes, through consolidation | Yes, through Active Migration |
| Immediate move back to Spot | No | More proactive |
| Level of control | More flexible and customizable | More managed and opinionated |

## **Final Thoughts**

Both AWS and Google Cloud have made Spot usage much easier than before.

With Karpenter, AWS gives you very flexible control over how your infrastructure is created and optimized. It can move workloads back to cheaper Spot capacity, but the process depends on consolidation rules and may take time.

With Custom Compute Classes (CCC), Google provides a simpler priority-based model and a built-in Active Migration feature that actively tries to return workloads to cheaper resources.

There is no single winner.

If you want more control and flexibility, Karpenter is an excellent choice.

If you want a more hands-off approach where the platform continuously optimizes your costs, GKE Custom Compute Classes provide a very elegant solution.

The best architecture is not choosing Spot or On-Demand. It is using both together in the right way: cheap capacity when it is available, and reliable capacity when you need it.
