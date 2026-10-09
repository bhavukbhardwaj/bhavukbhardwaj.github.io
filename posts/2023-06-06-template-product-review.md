---
title: "Talisman - Security Check (Pre-commit Hook)"
date: 2023-06-06
slug: template-product-review
tags: [DevOps Tool]
minutes: 3
summary: "Pre-commit secret scanning with Talisman: install options and configuration."
---

1. [**Problem Statement**](#viewer-ci7ig)
2. [**Solution - Talisman**](#viewer-cjkah)
3. [**Types of Installation**](#viewer-b5l4h)
4. [**Global Installation**](#viewer-1oqr7)
5. [**How it works ?**](#viewer-aobpi)
6. [**Running Talisman**](#viewer-2k3rj)
7. [**Ignoring the Scan**](#viewer-bod0u)
8. [**References**](#viewer-t396)

## **Problem Statment**

##

How to prevent pushing credentials and secrets or sensitive information to the Github Repos?

## **Solution - Talisman**

![](/assets/posts/template-product-review/1.jpg)

Talisman is a tool that installs a hook to your repository to ensure that potential secrets or sensitive information do not leave the developer's workstation. It validates the outgoing change set for things that look suspicious - such as potential SSH keys, authorization tokens, private keys etc. Talisman can also be used as a repository history scanner to detect secrets that have already been checked in, so that you can take an informed decision to safeguard secrets.

## **Types of Installation**

Talisman can be installed as a **Global Installation** Or as a **hook for Single Repository**. it is recommended that you use Talisman as a **Global Installation**. In this way, Talisman will install as a git hook as a global git hook template on the machine and a CLI utility, which can also be used for git repo scanning. The git hook can be set up for either a pre-commit or a pre-push configuration.

## **Global Installation**

It is a good choice to install Talisman as a global hook template. Talisman will thus be present, not only in your existing git repositories, but also in any new repository that you ‘init’ or ‘clone’.

* Use the below command on terminal to run Talisman as pre-commit hook

```
curl --silent 

https://raw.githubusercontent.com/thoughtworks/talisman/master/global_install_scripts/install.bash > /tmp/install_talisman.bash && /bin/bash /tmp/install_talisman.bash
```

###### **Note** - The above commands will download and install the binary at $HOME/.talisman/bin. If TALISMAN\_HOME not set up in your $PATH, there will be an ask for appropriate place to set it up. Choose the option number where profile source has been set on machine(Select bashrc if using oh-my-zsh in terminal). And don’t forget to restart machine or run the following command:

```
source <profile-source>

Example:
source ~/.zshrc
```

## **How it works ?**

Talisman works based on pattern matching for files, content, patterns, entropy etc. in your commit change sets. If you have installed Talisman as a pre-commit hook, it will scan only the *diff* within each commit. This means that it would only report errors for parts of the file that were changed.

**Validation**

The following detectors execute against the changesets to detect secrets/sensitive information:

* **Encoded values** - scans for encoded secrets in Base64, hex etc.
* **File content** - scans for suspicious content in file that could be potential secrets or passwords
* **File size** - scans for large files that may potentially contain keys or other secrets
* **Entropy** - scans for content with high entropy that are likely to contain passwords
* **Credit card numbers** - scans for content that could be potential credit card numbers
* **File names** - scans for file names and extensions that could indicate them potentially containing secrets, such as keys, credentials etc.

**Note** - You can explore further to add your own [custom configurations](https://thoughtworks.github.io/talisman/docs/configuring-talisman) , such as, checking for [custom patterns](https://thoughtworks.github.io/talisman/docs/configuring-talisman/set-custom-patterns/), set [custom thresholds](https://thoughtworks.github.io/talisman/docs/configuring-talisman/set-custom-patterns/) etc.

## **Running Talisman**

There is no explicit command to run talisman. Whenever you will try to push the Code, it will run automatically behind the scene and will show you the findings. See the below example for details -

* Create a simple file with the name `creds.py` and try to push the code.

![](/assets/posts/template-product-review/2.png)

##

## **Ignoring the Scan**

With the Talisman, you can easily get to know if you are pushing any secrets or sensitive information. Again, if you are absolutely sure that you want to ignore the scan, then for that you can update the talisman config file and add the pattern message shown in the report (for example in above screenshot).

## **References**

[Official Talisman Documentation](https://thoughtworks.github.io/talisman/docs#getting-started)
