---
title: "Infrastructure Coding Made Simple: Using GitHub Copilot and  Terraform"
date: 2023-04-10
slug: infrastructure-coding-made-simple-using-github-copilot-and-terraform
tags: [Terraform, DevOps Tool]
minutes: 3
summary: "Using GitHub Copilot to write Terraform: what works and what to double-check."
---

* [Introduction](#viewer-a6lun)
* [Integrating Github Copilot in VSCode](#viewer-8k6i2)
* [Examples of Using GitHub Copilot with Terraform](#viewer-f3ouv)
* [Advantages of Using GitHub Copilot](#viewer-a3h69)
* [Limitations of GitHub Copilot](#viewer-6ln84)
* [Conclusion](#viewer-clh29)

#### **Introduction**

[](https://media0.giphy.com/media/3oFzmerJ9kykSR92jm/giphy.mp4?cid=e2a3cbde2jx40eb6e50j5glf6s26vswn3kztvm4oewgjkrzx&rid=giphy.mp4&ct=g)

Have you ever found yourself stuck while writing code? Maybe you're not sure what syntax to use or how to structure your code. Fortunately, GitHub Copilot is here to help. Developed in collaboration with OpenAI, GitHub Copilot is an artificial intelligence (AI) tool that assists developers in writing code. By suggesting relevant snippets, functions, and entire code blocks based on the context and language used in the code, Copilot can save developers time and make their coding experience more efficient.

#### **Integrating GitHub Copilot in VSCode**

Integrating GitHub Copilot in Visual Studio Code (VSCode) is easy. Simply install the Copilot extension from the VSCode marketplace and sign in with your GitHub account. Once installed, Copilot will automatically start suggesting code as you type.

**Steps to Integrate Github Copilot in VSCode:**

* **Install the Github Copilot Extension**: Open VSCode and navigate to the Extensions tab. Search for the Github Copilot extension and click on Install.

![](/assets/posts/infrastructure-coding-made-simple-using-github-copilot-and-terraform/1.png)

* **Sign in to Github**: Once the extension is installed, you will be prompted to sign in to your Github account. You will need to authorize the extension to access your Github repositories and other data.
* **Enable Copilot**: After signing in, you will need to enable Copilot by clicking on the Github Copilot icon in the VSCode toolbar. You can also use the keyboard shortcut `Ctrl + Shift + P` to open the command palette and search for "Github Copilot: Enable".
* **Use Copilot**: Once Copilot is enabled, you can start using it by typing code in any supported language in a new or existing file. Github Copilot will provide suggestions in real-time based on the context of the code.

At the end, you should see this Copilot button in your VSCode. (Let it be as it is, You don't have to disable it)

![](/assets/posts/infrastructure-coding-made-simple-using-github-copilot-and-terraform/2.png)

#### **Examples of Using GitHub Copilot with Terraform**

Now let's explore how Github Copilot can be used with Terraform. Suppose we want to create an Elastic Compute Cloud (EC2) instance using Terraform.

* Give a try by typing the below statement and it will automatically start generating the code:

```
# create an EC2 resource
```

* Give a try with other prompts such as :-

```
#Create a Load Balancer
#Create a Target Group
#Create a Listener
```

![](/assets/posts/infrastructure-coding-made-simple-using-github-copilot-and-terraform/3.png)

#### **Advantages of Using GitHub Copilot**

There are numerous benefits to using GitHub Copilot, including:

1. **Accelerated coding**: Spend less time searching for code snippets or debugging syntax errors.
2. **Improved productivity**: Focus on the logic and design of your code, while GitHub Copilot handles the mundane tasks.
3. **Continuous learning**: GitHub Copilot learns from your code and adapts its suggestions over time.

#### **Limitations of Using GitHub Copilot**

Here are some limitations of GitHub Copilot that developers should be aware of:

1. **Code Quality**: Although GitHub Copilot is designed to assist developers in writing code, the quality of the generated code may vary depending on the context and complexity of the task. Therefore, developers should still review and test the generated code to ensure it meets the required standards.
2. **Limited Support for Debugging**: GitHub Copilot is primarily designed for generating code, rather than helping developers debug existing code. It may not provide helpful suggestions for identifying and fixing bugs in the code.
3. **Dependency on training data**: GitHub Copilot's effectiveness depends heavily on the quality and relevance of the training data it was trained on. So, overtime it will become great.

#### **Conclusion**

In conclusion, GitHub Copilot is an incredibly useful tool for developers, particularly those working with Python and Terraform (or other supported languages / frameworks).

By suggesting relevant code snippets and automating portions of the coding process, Copilot can save developers time and help them write more efficient code.

However, it's important to remember the limitations of AI-powered coding assistants and use Copilot as a tool to assist in coding rather than relying on it completely. I encourage readers to try out GitHub Copilot and share their experiences. Happy coding!
