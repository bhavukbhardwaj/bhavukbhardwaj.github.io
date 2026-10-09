---
title: "Linux AWK Commands Practice -1"
date: 2021-02-24
slug: linux-awk-commands-practice-1
tags: [Linux]
minutes: 2
summary: "Practical Linux awk examples to practice, starting with the basics."
---

![](/assets/posts/linux-awk-commands-practice-1/1.jpg)

Hi Readers,

We all know when it comes to Linux, we have to learn commands and there are many commands which we use daily and one such command is "awk".

AWK is a scripting language that allows you to play with data and generate reports. So we will try to cover few practice examples where we can find this command very helpful.

To get more information and syntax, run this command:-

```
$ info awk
```

This will show you a lot of information which you can read at your convenience.

Let's Begin ---

**Case 1: - To Convert the String into Upper Case using awk.**

```
$ randomString="my name is bhavuk."
$ echo $randomString | awk '{print toupper}'
```

```
Output :- MY NAME IS BHAVUK.
```

**Explanation**:- The first line creates a ***variable*** with the name "***randomString***". The Second Line is printing that value in the console using the "***echo***" command and then passing the output into the awk command.

The Awk has many inbuilt functions and one of them is "**toupper**".

**Case 2: - To Convert the String which is in File into Upper Case using awk**

```
$vi toupperfile.txt
```

Add these lines in the file:-

```
my name is bhavuk.
this file contains lower case letters only.
we will use toupper command to print them in uppercase.
```

Run at the console:-

```
$  awk '{print toupper}' toupperfile.txt
```

```
Output :-
MY NAME IS BHAVUK.
THIS FILE CONTAINS LOWER CASE LETTERS ONLY.
WE WILL USE TOUPPER COMMAND TO PRINT THEM IN UPPERCASE.
```

**Explanation**: Here we created a file where we have written all the lines in lowercase. Now, by using awk we can convert this into Upper Case. So this example we passed Filename "toupperfile.txt"

**Case 3: - To Convert the String into Lower Case using awk.**

```
$ randomString="MY NAME IS BHAVUK."
$ echo $randomString | awk '{print tolower}'
```

```
Output :- my name is bhavuk.
```

**Explanation**:- The first line creates a ***variable*** with the name "***randomString***". The Second Line is printing that value in the console using the "***echo***" command and then passing the output into the awk command.

The Awk has many inbuilt functions and one of them is "**tolower**".

**Case 4: - To Convert the String which is in File into Lower Case using awk**

```
$vi tolowerfile.txt
```

Add these lines in the file:-

```
MY NAME IS BHAVUK.
THIS FILE CONTAINS LOWER CASE LETTERS ONLY.
WE WILL USE TOLOWER COMMAND TO PRINT THEM IN LOWERCASE.
```

Run at the console:-

```
$  awk '{print tolower}' tolowerfile.txt
```

```
Output :-
my name is bhavuk.
this file contains lower case letters only.
we will use tolower command to print them in lowercase.
```

**Explanation**: Here we created a file where we have written all the lines in lowercase. Now, by using awk we can convert this into Upper Case. So this example we passed Filename "toupperfile.txt"

**Case 5: Consider a case when you have a file that contains float value and you need data in Integer Format.**

First, create a file with data as follow:

```
$ vi intfile.txt
```

Add the values as follow:

```
23.65
34.87
34.67
232.987
```

Run this command at the console:-

```
awk '{print int($0)}' intfile.txt
```

```
Output:-
23
34
34
232
```

**Explanation**:- At first, we created a file where we stored data that is in decimal.

Later we ran the awk command where "**$0**" represents each line. As awk scans line by line. So before printing each line, we are using the inbuilt ***"int" function*** to convert the decimal data into an integer.

To be continued...
