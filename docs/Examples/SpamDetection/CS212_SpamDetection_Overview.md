---
title: "Spam Detection Example"
description: "Overview of the spam detection example: the problem of sorting text messages into spam and ham, and the strategy of training a naive Bayes classifier."
keywords: spam detection, classification, naive Bayes, scikit-learn, machine learning
material: Lecture Notes
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Spam Detection with Naive Bayes</h1>

<h2>Example Overview</h2>

This page describes the problem that the spam detection example solves and the strategy it uses. It is not a tutorial. The step-by-step explanations are in the notebook, and the instructions for running each version are in its readme file (see [Two Versions of the Solution](#two-versions-of-the-solution)).

<h2>Contents</h2>

[TOC]

## The Problem

Most text messages are ones you want to read. Some are not: unwanted ads and scams, such as "Free entry in a weekly competition to win FA Cup final tickets". In this example the unwanted messages are called *spam*, and the normal messages are called *ham*.

The goal is a program that reads a message and decides whether it is spam or ham. In machine learning this is a *classification* problem with two *classes*.

It is hard to solve this by writing rules. Spammers change their wording all the time, and plenty of normal messages mention prizes or phone numbers too. Instead, the program *learns* from examples: it is shown many messages that people have already labeled, and it works out for itself which words are signs of spam. Learning from labeled examples is called *supervised learning*.

## The Data

The data is the **SMS Spam Collection** from the UCI Machine Learning Repository. It has 5,574 real text messages, and a person labeled each one `ham` or `spam`. Only 747 of the messages (about 13%) are spam, so the two classes are not the same size. The data is a CSV file with two columns, `label` and `message`.

The data was collected by Tiago A. Almeida and José María Gómez Hidalgo, who hold its copyright. Each version of the example has a copy of the data and of the original readme, which includes the license. The collection is described on the <a href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection" target="_blank">UCI Machine Learning Repository</a> web page.

## The Strategy

The steps follow the scikit-learn [Working With Text Data](../../Tutorials/scikit-learn-1.7/WorkingWithTextData.md) tutorial, with a last step that looks inside the classifier:

1. **Load and explore the data.** Read the messages and labels, and count how many of each kind there are.
2. **Split the data into training and test sets.** Hold back 25% of the messages. The classifier never learns from the test messages, so how well it does on them is an honest estimate of how well it would do on new messages.
3. **Turn the text into numbers.** A classifier can't read words, so each message is turned into a list of word counts. This is called a *bag of words*, because it keeps the counts and ignores the order of the words.
4. **Train the classifier.** A *naive Bayes* classifier counts how often each word appears in spam messages and in ham messages. To classify a message, it uses Bayes' rule to combine the evidence from all of the message's words into a probability that the message is spam. (It is called "naive" because it treats the words as if they were independent of each other, which is not quite true, but works well anyway.) See [Machine Learning: Bayes' Rule](../../LectureNotes/CS212-Unit03-2-Bayes.md) for the idea behind it.
5. **Test the classifier.** Classify the test messages and compare the predictions with the true labels. The results are reported as an accuracy, a classification report and a confusion matrix. The [Lab 4 example](../Lab04-ClassifierMetrics/CS212_Lab04_Example.md) builds on this step and explains what those numbers mean.
6. **Classify new messages.** Use the trained classifier on messages that are not in the data, and look at the probability that each is spam.
7. **See which words signal spam.** Compare how likely each word is in spam and in ham, to find the words that the classifier relies on most.

On the test messages the classifier's accuracy is about 98.6%.

## Two Versions of the Solution

There are two versions of the solution. They do the same steps.

| Version | What it is | Folder |
| --- | --- | --- |
| Notebook | A Jupyter notebook with an explanation of each step. It runs in Google Colab or in VS Code. | <a href="https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Examples/SpamDetection/SpamDetectionNotebook" target="_blank">SpamDetectionNotebook</a> |
| Program | A single Python script, `spam_detection.py`, that you run from the command line with `uv`. | <a href="https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Examples/SpamDetection/SpamDetectionProgram" target="_blank">SpamDetectionProgram</a> |

Each folder has a readme file that describes its files and tells you how to run that version.

*This overview was drafted by Claude Code and is waiting for review by Brian Bird. 10/21/2026*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
