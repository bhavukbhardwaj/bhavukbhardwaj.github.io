---
title: "Redefining EC2 Connectivity: How EIC Endpoint Surpasses Instance Connect and SSM"
date: 2023-06-17
slug: redefining-ec2-connectivity-how-eic-surpasses-instance-connect-and-ssm
tags: [AWS]
minutes: 2
summary: "EIC Endpoint gives secure connections to instances and other VPC resources from the internet. How it compares with Instance Connect and SSM."
---

![](/assets/posts/redefining-ec2-connectivity-how-eic-surpasses-instance-connect-and-ssm/1.jpg)

## **How many ways are there to connect to an EC2 instance?**

There are several methods, with three being the most commonly utilized:

1. The traditional Jump Box method,
2. EC2 Instance Connect, and
3. Session Manager.

However, AWS has recently introduced a new feature to enhance these connection options: the Amazon EC2 Instance Connect (EIC) Endpoint. This feature enables you to securely connect to your instances and other VPC resources from the internet, further expanding the flexibility and security of managing your AWS resources.

## **EIC Endpoint Overview**

EIC Endpoint is an **identity-aware TCP proxy.**

* **Identity Aware** - It means it uses AWS Identity and Access Management (IAM) credentials to authenticate and authorise requests.
* **TCP Proxy**: It means EIC Endpoint acts as an intermediary for requests from clients seeking resources from other servers. In the context of EIC Endpoint, it allows clients to establish a connection to an EC2 instance through the endpoint, rather than connecting directly.

## **How to create an EIC Endpoint ?**

**Note** - You must have the required IAM permission to connect to an EC2 Instance Connect Endpoint. For more - [here](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/permissions-for-ec2-instance-connect-endpoint.html#iam-OpenTunnel).

1. Open the VPC Console and choose the Endpoints.
2. Choose **Create endpoint**, and then complete the settings in the dialog box and click Create Endpoint, as follows :-

![](/assets/posts/redefining-ec2-connectivity-how-eic-surpasses-instance-connect-and-ssm/2.png)

## **How to connect to an Instance with EIC Endpoint ?**

EC2 Instance Connect Endpoint allows you to connect to an instance without requiring the instance to have a public IPv4 address.

1. Click on EC2 Console and select the EC2.
2. Choose Connect and do the following :-

![](/assets/posts/redefining-ec2-connectivity-how-eic-surpasses-instance-connect-and-ssm/3.png)

**[Max tunnel duration (seconds)**, enter the maximum allowed duration for the SSH connection.**]**

## **Comparison Table**

## **Conclusion**

In a comparison table that evaluated various connection methods based on several factors including the need for a public IP, IGW/NAT Gateway, identity-based access, network-based access, use of ephemeral keys, requirement of an agent, and operational overhead, EIC Endpoint emerged as a superior option.

[#devops](https://www.notfromiit.com/blog/hashtags/devops) [#aws](https://www.notfromiit.com/blog/hashtags/aws) [#ec2](https://www.notfromiit.com/blog/hashtags/ec2) [#recent](https://www.notfromiit.com/blog/hashtags/recent) [#announcements](https://www.notfromiit.com/blog/hashtags/announcements)
