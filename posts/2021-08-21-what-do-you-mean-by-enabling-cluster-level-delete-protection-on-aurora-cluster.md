---
title: "What do you mean by Enabling Cluster Level Delete Protection on Aurora Cluster?"
date: 2021-08-21
slug: what-do-you-mean-by-enabling-cluster-level-delete-protection-on-aurora-cluster
tags: [AWS]
minutes: 2
summary: "What cluster-level delete protection does on an Aurora cluster, and why you want it enabled."
---

![](/assets/posts/what-do-you-mean-by-enabling-cluster-level-delete-protection-on-aurora-cluster/1.png)

Hi Readers,

Ever wonder what is the meaning of enabling Cluster Level Delete Protection on RDS Aurora Cluster?

Or you have been advised by your Technical Architect to enable it for all Production Clusters.

Let me try to explain it here in this blog...

**First, we need to understand, What is the meaning of Cluster?**

- Usually when we club more than one resource and packed them together that forms a cluster.

**Does one resource can be called a Cluster?**

- Yes, it is more like saying "All squares are like rectangles". But also it depends on the context. Here we are speaking about RDS and in the case of the RDS Cluster, you can have one Instance and it will be considered as a Cluster.

**How to create a single rds instance in the cluster?**

![](/assets/posts/what-do-you-mean-by-enabling-cluster-level-delete-protection-on-aurora-cluster/2.png)

- While creating the RDS Aurora Cluster, you have to choose

***"Don't" create an Aurora Replica.***

This will only launch one RDS Instance and the type will be Cluster. But to be honest, nobody uses a single Instance in Production. The purpose of having a cluster is to fulfill the requirement of "High Availability". In production, you will be requiring at least 2 Instances that are

1. As a Writer &
2. As a Reader

So, here is the interesting part that starts. Once you enable the Delete Protection, what will happen. Let us try to understand with an example :

Suppose you have 1 Cluster which contains 2 RDS Instances (one is the reader & the other is the writer).

So, when we delete the writer, what happens while you are having Delete Protection ON?

1. Writer Instance will be promoted to Reader.
2. This means the DB Instance will get restarted and marked as Reader.
3. Then this Reader Instance gets Shutdown and deleted.

But at the same time, what will happen to the Reader Instance which was already present?

1. First, it will get shut down and
2. Then it will be started as a Writer and marked as same - Writer Instance.

So, in the end, **Delete Protection allows you to have at least one RDS Instance which will be the writer only. I mean that is correct, in a cluster, you should have at least One Writer Instance and from that writer Instance, you can launch multiple Replica/Reader.**

Regards,

Bhavuk

AWS DevOps Engineer
