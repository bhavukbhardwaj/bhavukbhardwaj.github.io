---
title: "AWS Verified Access vs. VPN (Securing Access in the Cloud Era)"
date: 2023-06-11
slug: aws-verified-access-vs-vpn-securing-access-in-the-cloud-era
tags: [AWS]
minutes: 4
summary: "Zero Trust access on AWS: how Verified Access compares with a traditional VPN."
---

![](/assets/posts/aws-verified-access-vs-vpn-securing-access-in-the-cloud-era/1.jpg)

**Ever heard of the Zero Trust security framework?** This might sound quite ominous, as if I am suggesting you trust no one. But when it comes to cybersecurity, that's precisely the point! You see, Zero Trust operates on the belief that neither users nor devices should be trusted outright, no matter their location or network environment. This creates an ecosystem where stringent access controls and continuous authentication are the norms, reducing security risks significantly.

Now, let's consider AWS Verified Access, a recent offering from AWS that promises secure access to applications without the need for a VPN. Sounds intriguing, doesn't it? Verified Access evaluates each application request in real time, ensuring users meet specific security requirements before granting access. But what's the real catch? Is it better than the traditional VPN setup?

In terms of benefits, Verified Access boasts an improved security posture, integration with security services, a better user experience, and simplified troubleshooting and audits. It also consists of several components such as Verified Access instances, endpoints, groups, access policies, trust providers, and trust data. All these components work together to evaluate, allow, or deny access to applications based on trust data and access policies.

## **The Question: Can AWS Verified Access be an Overhead?**

But, while AWS Verified Access paints an appealing picture, you might want to weigh it against the trusty VPN. Why, you ask? Let's explore -

### **1. The Load Balancer Conundrum -**

AWS Verified Access implementation requires transitioning applications from Public Application Load Balancers (ALBs) to Internal Load Balancers. However, this migration can be a time-consuming and resource-intensive process. It's crucial to note that AWS Verified Access is incompatible with Public ALBs.

### **2. The Learning Curve: CEDAR Language -**

Next, there's the necessity to learn and master the CEDAR Language in order to write Verified Access Policies. For organizations, this could translate into a significant initial investment in terms of time and effort, especially if they are keen on maintaining internal security standards while writing these new policies.

### **3. Scaling Costs with Applications -**

Each addition to your portfolio of internal applications raises the monthly bill by an estimated $230.

The calculation here is simple = 1 Application \* 31 Days \* 24 Hours \* $0.31(EU Frankfurt Region).

For organizations with a growing number of internal applications, these costs can quickly pile up, making AWS Verified Access a costly venture.

### **4. Suitability for Smaller Organizations -**

For organizations with a limited number of internal applications, the overhead of implementing AWS Verified Access might outweigh its benefits. If an organization already has seasoned infrastructure professionals who are adept at accurately whitelisting VPN IPs in Security Groups, they might not feel the necessity for AWS Verified Access. This service is best suited for large corporations with an abundance of internal tools and applications hosted on AWS, where scaling VPN users and managing an extensive array of Security Groups becomes vital.

### **5. Inter-Cloud Provider Integration Challenges -**

For organizations contemplating hosting internal applications on alternative cloud providers, they should consider potential integration challenges. VPNs have the distinct advantage of working seamlessly across various cloud providers and on-premises infrastructure. This provides consistent access to internal resources, regardless of the hosting environment. If an organization ventures into hosting applications on other Cloud Providers, they might face integration hurdles that a VPN setup could effortlessly navigate.

### **6. Evaluating Past VPN Performance -**

An essential question to ask here is, when was the last time your organization faced issues with your VPN? When did it fail, and what were the circumstances? Reflecting on your VPN's past performance can provide valuable insights into whether it's truly time to seek an alternative or if the existing setup still meets your needs.

### **7. Leveraging Existing VPN Investments -**

For organizations that have already made substantial investments in VPN infrastructure and have a team of experienced professionals managing VPN technologies, it might make more sense, both practically and economically, to continue utilizing VPNs.

### **8. Requirement of Organizational Change Management -**

Introducing a new technology in an organization always requires change management to ensure a smooth transition. Training staff, adapting to new processes, and overcoming resistance to change could add to the overhead cost.

### **9. The Challenge of Legacy Systems -**

Many organizations still operate partially or entirely on legacy systems. These systems may not be compatible with AWS Verified Access or may require significant resources to make them compatible. This factor could increase both the transition time and cost, which are essential considerations when evaluating the practicality of implementing AWS Verified Access.

### **10. Dependability on a Single Provider -**

Relying on a single provider for an important security measure like AWS Verified Access might become a point of failure. If AWS experiences a significant outage or a security incident, it could directly impact the security of the user's applications. In contrast, a VPN could be sourced from multiple vendors, reducing the risk of a single point of failure.

### **11. Incident Response Time -**

With VPNs, your IT team might have built a level of expertise that allows for rapid response to incidents and issues. With a new system like AWS Verified Access, there could be a learning curve that potentially extends incident response times, at least in the initial phases of implementation.

### **12. Global Reach of Service -**

While AWS has a significant global presence, there might be locations where your organization operates but AWS does not, causing issues with implementing Verified Access. VPNs, on the other hand, have a wider reach and might offer a more reliable service in this context.

### **13. Potential Hidden Costs -**

As with any new technology implementation, there might be hidden costs involved with AWS Verified Access, which could include additional training costs, consulting fees, or unforeseen integration expenses. These costs need to be factored into the overall cost assessment.

## **Conclusion**

Remember, technology adoption isn't just about the advanced features a tool brings but about a thorough evaluation of your organization's readiness, the tool's alignment with business needs, and the potential long-term implications of the technology choice.

In conclusion, AWS Verified Access is indeed a compelling solution with its unique features and potential security benefits. However, a careful evaluation of your organization's needs, capabilities, and the considerations mentioned above is critical before making the leap from VPNs to this new mechanism.

> Stay curious, stay informed, and remember, in cybersecurity, trust no one automatically!
