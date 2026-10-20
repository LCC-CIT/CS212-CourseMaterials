---
title: "Lab 4, Part 1"
description: "Part 1 of the assignment is to practice measuring a classifier with precision, recall and F1."
keywords: accuracy, precision, recall, F1, scikit-learn
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Lab 4, Evaluating a Classifier</h1>

<h2>Part 1</h2>

This part of the lab is for everyone. It should take less than an hour.

In Lab 3 you measured a classifier with *accuracy*, the share of test messages it got right. That works when the classes are about the same size. It can be very misleading when one class is rare. In Part 2 you will train a classifier on a real data set, look at it with better measurements, and try to improve it.

<h2>Contents</h2>

[TOC]

## Why Accuracy Isn't Enough

Imagine a program that watches 1,000 text messages and flags the ones that report an emergency. Only 20 of the 1,000 really are emergencies. Here is a "classifier" that never needs any training:

```python
def classify(message):
    return 0   # 0 means "not an emergency"
```

It gets 980 out of 1,000 right, so its accuracy is 98%. It also never finds a single emergency, which makes it useless. To see this, you need to count the different kinds of right and wrong answers.

## The Four Counts

Pick one class to be the *positive* class. Here it is "emergency" (label 1). Every prediction is one of four kinds:

| | Predicted "emergency" | Predicted "not emergency" |
| --- | --- | --- |
| **Really an emergency** | True positive (TP) | False negative (FN) |
| **Really not an emergency** | False positive (FP) | True negative (TN) |

A table like this is called a *confusion matrix*. From the four counts you can calculate:

| Measure | Formula | The question it answers |
| --- | --- | --- |
| Accuracy | (TP + TN) / all messages | How many of all the messages did it get right? |
| Precision | TP / (TP + FP) | When it says "emergency", how often is it right? |
| Recall | TP / (TP + FN) | Of the real emergencies, how many did it find? |
| F1 | 2 × precision × recall / (precision + recall) | One number that is high only when precision *and* recall are both high |

Precision and recall pull against each other. A classifier that flags everything has perfect recall and terrible precision. One that only flags the messages it is very sure about has high precision and poor recall. Which one you want depends on the cost of each kind of mistake. A missed emergency costs more than a false alarm.

When there are more than two classes, scikit-learn calculates precision, recall and F1 for each class in turn (treating that class as the positive one). It then reports two kinds of average:

- **Macro average:** the plain average of the per-class scores. Every class counts the same, however small. A weak score on a rare class pulls it down.
- **Weighted average:** the per-class scores averaged in proportion to the number of messages in each class. A rare class barely moves it.

## Step A: Calculate the Measures Yourself

Write a Python file named `metrics_practice.py` with these functions. Use plain `for` loops, not scikit-learn, to do the counting and the arithmetic.

- `count_results(true_labels, predicted_labels)` returns the four counts (TP, FP, FN, TN) as a tuple. The positive class is 1.
- `accuracy(tp, fp, fn, tn)`, `precision(tp, fp)`, `recall(tp, fn)` and `f1(precision_value, recall_value)` each return one number.

Be careful about dividing by zero. For example, a classifier that never says "yes" has `tp + fp == 0`. Return 0.0 in that case.

Then test your functions on this data:

```python
# 1000 messages. The first 20 really are emergencies (1), the other 980 are not (0).
true_labels = [1] * 20 + [0] * 980

# The classifier found 15 of the 20 emergencies and raised 10 false alarms.
predicted_labels = [1] * 15 + [0] * 5 + [1] * 10 + [0] * 970

# A "classifier" that always says no.
always_no = [0] * 1000
```

## Step B: Check Your Work with scikit-learn

scikit-learn has functions that do the same calculations: `accuracy_score`, `precision_score`, `recall_score`, `f1_score` and `confusion_matrix`, all in `sklearn.metrics`. They take `(true_labels, predicted_labels)`. For `precision_score`, add `zero_division=0` so it returns 0 instead of a warning when the classifier never says "yes".

Print your results and scikit-learn's side by side for both sets of predictions. They should match. The way you lay out the output is up to you, but your numbers should be the same as these:

```
Classifier
  counts:     TP = 15  FP = 10  FN = 5  TN = 970
  by hand:    accuracy 0.985 | precision 0.6 | recall 0.75 | F1 0.667
  scikit-learn: accuracy 0.985 | precision 0.6 | recall 0.75 | F1 0.667
Always no
  counts:     TP = 0  FP = 0  FN = 20  TN = 980
  by hand:    accuracy 0.98 | precision 0.0 | recall 0.0 | F1 0.0
  scikit-learn: accuracy 0.98 | precision 0.0 | recall 0.0 | F1 0.0
```

(To use scikit-learn, you need it in your project. Make a project folder for Lab 4 with `uv init lab04`, `cd lab04` and `uv add scikit-learn`. You will use the same project for Part 2.)

## Step C: Answer Two Questions

Put your answers in comments at the end of your file.

1. The "always no" classifier has 98% accuracy. What are its precision and recall, and what does that tell you about accuracy?
2. The first classifier has a precision of 0.60 and a recall of 0.75. Describe in your own words what each number means for the 1,000 messages. Which kind of mistake is it making more often, missing emergencies or raising false alarms?

## Submitting your lab work on Canvas

For Part 1, upload your `metrics_practice.py` file to the Lab 4 Part 1 assignment on Canvas. (No code review is needed.)

### Grading Criteria

The main focus of grading will be on correct coding and understanding of the measures.

## Part 2

There are three versions of part 2.

- [Group A: ChatGPT vs. Human](GroupA/CS212_Lab04_Part2_Instructions_GroupA.md)
- [Group B: Routing Customer Messages to Departments](GroupB/CS212_Lab04_Part2_Instructions_GroupB.md)
- [Group C: Finding Medical Requests in Disaster Messages](GroupC/CS212_Lab04_Part2_Instructions_GroupC.md)

*These lab instructions were drafted by Claude Code and are waiting for review by Brian Bird. 10/20/2026*

------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------
