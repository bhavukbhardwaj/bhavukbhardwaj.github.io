---
title: "EKS 1.32 → 1.33 Upgrade: Real Production Lessons from Migration"
date: 2026-06-14
slug: eks-1-32-1-33-upgrade-real-production-lessons-from-migration
tags: [EKS]
minutes: 4
summary: "A routine EKS upgrade turned into a major OS transition from Amazon Linux 2 to Amazon Linux 2023. What broke in production and how to avoid it."
---

Upgrading an Amazon EKS cluster is usually seen as a routine maintenance task. You update the Kubernetes version -> upgrade your add-ons -> refresh your worker nodes, and move on.

However, our

**EKS 1.32 → 1.33 upgrade was different.**

This was not just a Kubernetes version upgrade. It was a major operating system transition because EKS 1.33 no longer provides EKS-optimized Amazon Linux 2 (AL2) AMIs. This meant our worker nodes had to move to Amazon Linux 2023 (AL2023) (or another supported option like Bottlerocket).

On paper, this sounds like a simple AMI change. In reality, it introduced multiple infrastructure changes around node bootstrapping, authentication, and access to AWS services.

This blog shares how we approached the upgrade, the problems we found during testing, and the lessons that helped us achieve a smooth production migration.

## **Our Upgrade Strategy**

For any production Kubernetes environment, the biggest mistake is treating the upgrade as a single action.

A safe upgrade follows a controlled sequence:

```
Pre-checks
    ↓
Control Plane Upgrade
    ↓
EKS Managed Add-on Upgrade
    ↓
Worker Node Migration
```

Before touching the cluster version, we first checked for deprecated Kubernetes APIs, validated our add-on compatibility, and ensured that critical applications had proper Pod Disruption Budgets (PDBs).

The goal was simple: find problems before the maintenance window, not during it.

### **Challenge 1: The AL2 → AL2023 Migration**

The biggest change in EKS 1.33 is the worker node operating system migration.

AL2 and AL2023 are not just different AMI versions. They have a different way of initializing Kubernetes nodes.

AL2 relied on the traditional **bootstrap.sh** script to join the cluster. AL2023 introduced **nodeadm**, a newer configuration-based approach.

This means that any custom launch templates or user data scripts that depended on bootstrap.sh needed to be reviewed and updated.

Our approach was to prepare AL2023 nodes first, validate them, and then gradually move workloads from AL2 nodes to AL2023 nodes using a controlled node replacement strategy.

The lesson: do not assume an OS migration is the same as a normal Kubernetes node upgrade.

### **Challenge 2: IMDSv2 and Application Credential Failures**

After moving to AL2023, one of the most unexpected issues was related to AWS credentials.

Many applications, storage drivers, and Kubernetes components communicate with AWS services using the EC2 Instance Metadata Service (IMDS).

With AL2023-based environments, the IMDSv2 configuration becomes much more important. If the IMDS response hop limit is not configured correctly, applications running inside containers may fail to retrieve credentials.

The impact can be surprising:

* EBS or EFS CSI drivers may fail to communicate with AWS APIs.
* Applications using node IAM roles may start failing.
* EKS Pod Identity components may experience credential access issues.

The fix was straightforward: explicitly configure the launch template metadata options and set the **IMDSv2 response hop limit to 2.**

A small infrastructure setting can cause a large production impact.

### **Challenge 3: Legacy IAM Solutions**

Another area we reviewed was our IAM access strategy.

Older tools like kube2iam depend heavily on intercepting metadata requests. The move toward IMDSv2 and newer node architectures makes these approaches difficult to maintain.

The long-term solution was moving workloads toward modern approaches such as EKS Pod Identity or IRSA.

This migration is worth planning before the AL2023 rollout, because IAM failures usually appear only when applications start making AWS API calls.

### **Challenge 4: Add-ons and Cluster Components**

A Kubernetes control plane upgrade does not automatically mean everything in the cluster is ready.

Components such as:

* VPC CNI
* CoreDNS
* kube-proxy
* CSI drivers

must be upgraded to versions compatible with the new Kubernetes release.

However, one important lesson we learned was that compatibility is not only about the Kubernetes version; the underlying server architecture also matters. In our case, we were running ARM-based AWS Graviton nodes. We found that simply choosing the latest add-on versions was not always the right approach, as some versions had compatibility issues or were not stable for our environment.

Instead of assuming the newest version would work, we tested different versions in our lower environments, validated them with our ARM64 workloads, and selected the most stable versions for production.

*The key lesson: "Latest" does not always mean "production-ready". Always validate your add-on versions against your Kubernetes version, operating system, and CPU architecture before deploying them to production.*

### **Challenge 5: Zero-Downtime Node Replacement**

Replacing worker nodes sounds simple: drain old nodes and move workloads to new nodes.

In production, it requires much more planning.

Applications should have:

* Multiple replicas.
* Proper readiness and liveness probes.
* Pod Disruption Budgets to prevent all replicas from being removed at the same time.

Without these protections, a node replacement can become an application outage.

We performed the migration gradually, validated the health of workloads after each step, and only removed the old nodes after confirming that the new AL2023 nodes were stable.

## **Key Lessons Learned**

Looking back, the Kubernetes version upgrade itself was the easiest part of the migration. Most of the effort went into preparing the surrounding infrastructure.

Our biggest lessons were:

* Treat AL2 → AL2023 as an operating system migration, not just an EKS upgrade.
* Validate custom launch templates and user data scripts.
* Configure IMDSv2 correctly before moving workloads.
* Plan migration away from older IAM solutions such as kube2iam.
* Verify whether your cluster components are EKS-managed or self-managed.
* Ensure workloads have proper health checks and Pod Disruption Budgets before draining nodes.

##

![](/assets/posts/eks-1-32-1-33-upgrade-real-production-lessons-from-migration/1.png)
