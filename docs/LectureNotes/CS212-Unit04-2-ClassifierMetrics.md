---
title: Classifier Metrics
description: Performance metrics for classifiers (accuracy, precision, recall, F1 and the confusion matrix) and how to calculate them with scikit-learn.
keywords: performance metrics, accuracy, precision, recall, F1, confusion matrix, macro average, scikit-learn
generator: Typora
author: Brian Bird
---

<h1>Classifier Metrics</h1>

**CS 212, AI Programming 1**

In Lab 3 you measured a classifier with *accuracy*, the percent of test messages it got right. That works when the classes are all about the same size. It can be very misleading when the number of samples for one class is small.

The Lab 4 assignments (all three groups) are about measuring how well a classifier performs and then improving it. *Accuracy*, *precision*, *recall* and *F1* are all *performance metrics*, which are numbers that measure how well a classifier does its job. These notes build on the [Spam Detection example](../Examples/SpamDetection/CS212_SpamDetection_Overview.md): they take its spam classifier and show what its performance metrics mean and how they are calculated. The code is in the [Lab 4 example](../Examples/Lab04-ClassifierMetrics/CS212_Lab04_Example.md).

<h2>Contents</h2>

[TOC]

## Starting Point: The Spam Detection Example

The [Spam Detection example](../Examples/SpamDetection/CS212_SpamDetection_Overview.md) loads the data, splits it into training and test messages, counts the words, trains the classifier and tests it. After testing, it prints three things about the classifier: its accuracy, a classification report and a confusion matrix.

This example starts where that program ends. It takes the classifier's results and explains what the numbers mean, how they are calculated, and how to judge whether they are good.

The data is the SMS Spam Collection, collected by Tiago Almeida and José María Gómez Hidalgo. It has 5,574 real text messages, and people labeled each one as spam or ham. In the file `data/sms_spam.csv` in the Python project folder (the notebook reads the same data from GitHub), each row has a `label` and a `message`. The file `data/SMSSpamCollection-readme.txt` describes the collection and its terms of use. Only 747 of the messages (13%) are spam.

## What We Are Measuring

To find out how well a classifier works, you compare its answers with the right answers for the same messages. Both are needed:

- The *true labels* are the correct classes in the test data set. Someone read each message and marked it as spam or ham.
- The *predicted labels* are the classes the classifier chose for the same messages.

You measure the classifier on the *test* messages, which it did not learn from. In this example the true labels and the predicted labels are lists of numbers, where 1 means spam and 0 means ham.

In your lab you will do something similar with a different data set. The true labels come from a data set that your group's lab instructions describe, and the predicted labels come from a classifier that you train with scikit-learn.

## Why Accuracy Isn't Enough

The spam classifier's accuracy is 98.6%. That sounds excellent, but how good is it really? Here is a "classifier" that never needs any training:

```python
def classify(message):
    return "ham"
```

Most messages are ham: 1,203 of the 1,394 test messages. So this classifier gets 86.3% of them right. It also never finds a single spam message, which makes it useless as a spam filter. The spam classifier's 98.6% has to be compared with that 86.3%. And if spam were much rarer than 13%, the problem would be worse. A classifier that is 99% accurate when 99% of the messages are ham is no better than the one above.

To see how well a classifier does on the rare class (in this case the spam), you need to count the different kinds of right and wrong clasifications.

## The Four Counts

Pick one class to be the *positive* class. Here it is spam (label 1). Every prediction is one of four kinds:

| | Predicted spam | Predicted ham |
| --- | --- | --- |
| **Really spam** | True positive (TP) | False negative (FN) |
| **Really ham** | False positive (FP) | True negative (TN) |

A table like this is called a *confusion matrix*. From the four counts you can calculate these performance metrics:

| Measure | Formula | The question it answers |
| --- | --- | --- |
| Accuracy | (TP + TN) / all messages | What percent of all the messages did it get right? |
| Precision | TP / (TP + FP) | When it says "spam", how often is it right? |
| Recall | TP / (TP + FN) | Of the real spam messages, how many did it find? |
| F1 | 2 × precision × recall / (precision + recall) | A number that is high only when precision *and* recall are both high |

*Precision* and *recall* pull against each other. A classifier that calls every message spam has perfect recall and terrible precision. One that only says "spam" for only the most obvious spam has high precision and poor recall. Which one you want depends on the *cost* of each kind of mistake. For a spam filter, a real message lost in the spam folder (a false positive) is usually worse than a spam message that gets through (a false negative).

## Calculating the Measures in Python

You don't need to write code to calculate these numbers. The module `sklearn.metrics` has a function for each one: `accuracy_score`, `precision_score`, `recall_score` and `f1_score`. You give each of them the true labels and the predicted labels. The function `confusion_matrix` gives you the four counts. For two classes, its result is `[[TN, FP], [FN, TP]]`, so `.ravel()` flattens it into the four numbers in that order.

If a classifier never says "spam", then TP + FP is 0, and precision (TP / (TP + FP)) would divide by zero. The argument `zero_division=0` tells `precision_score` to return 0.0 in that case instead of printing a warning.

The function `get_spam_results` in `spam_results.py` repeats the steps of the Spam Detection program (the same data, the same 75/25 split, and a naive Bayes classifier on word counts) and returns the true labels and the predicted labels of the test messages. You can read that program to see how those steps work.

The program `main.py` has a function, `show_scores`, that uses these scikit-learn functions to print the four counts and the four performance metrics. It measures the spam classifier and the "always ham" classifier for comparison, and prints the classification report and confusion matrix that the Spam Detection program printed. At the end it has a made-up example with three classes, which is explained below.

```python
# Lab 4 example: measuring the spam classifier from the Spam Detection example.
#
# Run with:  uv run main.py

from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)

from spam_results import get_spam_results


def show_scores(name, true_labels, predicted_labels):
    """Print the four counts and the four performance metrics. The positive class is 1."""
    # For two classes, the confusion matrix has the four counts: [[TN, FP], [FN, TP]].
    tn, fp, fn, tp = confusion_matrix(true_labels, predicted_labels, labels=[0, 1]).ravel()
    print(name)
    print("  counts:  TP =", tp, " FP =", fp, " FN =", fn, " TN =", tn)
    print("  accuracy ", round(accuracy_score(true_labels, predicted_labels), 3))
    # zero_division=0 is the score to use if the classifier never says "spam"
    print("  precision", round(precision_score(true_labels, predicted_labels, zero_division=0), 3))
    print("  recall   ", round(recall_score(true_labels, predicted_labels), 3))
    print("  F1       ", round(f1_score(true_labels, predicted_labels), 3))


# ---------------------------------------------------------------- two classes
# The true labels and the predicted labels of the test messages (1 = spam, 0 = ham).
test_labels, predicted_labels = get_spam_results()
print(len(test_labels), "test messages,", sum(test_labels), "of them are spam")
print()
show_scores("Spam classifier", test_labels, predicted_labels)
print()

# For comparison, a "classifier" that calls every message ham.
always_ham = [0] * len(test_labels)
show_scores("Always ham", test_labels, always_ham)

print()
print(classification_report(test_labels, predicted_labels, target_names=["ham", "spam"]))
print("Confusion matrix (rows = true, columns = predicted):")
print(["ham", "spam"])
print(confusion_matrix(test_labels, predicted_labels))

# ---------------------------------------------------------------- three classes
# A made-up example. A help desk sorts 100 messages into three departments.
# Security is the rare one. Each case is (true department, predicted department,
# how many messages).
cases = [
    ("Billing", "Billing", 57), ("Billing", "Technical", 3),
    ("Technical", "Technical", 27), ("Technical", "Billing", 1), ("Technical", "Security", 2),
    ("Security", "Security", 5), ("Security", "Billing", 3), ("Security", "Technical", 2),
]
true_departments = []
predicted_departments = []
for true_department, predicted_department, count in cases:
    for i in range(count):
        true_departments.append(true_department)
        predicted_departments.append(predicted_department)

print("\nThree departments (made up)")
names = ["Billing", "Technical", "Security"]
print(classification_report(true_departments, predicted_departments, labels=names))
print("Confusion matrix (rows = true, columns = predicted):")
print(names)
print(confusion_matrix(true_departments, predicted_departments, labels=names))
```

Here is the output of `uv run main.py`:

```
1394 test messages, 191 of them are spam

Spam classifier
  counts:  TP = 178  FP = 6  FN = 13  TN = 1197
  accuracy  0.986
  precision 0.967
  recall    0.932
  F1        0.949

Always ham
  counts:  TP = 0  FP = 0  FN = 191  TN = 1203
  accuracy  0.863
  precision 0.0
  recall    0.0
  F1        0.0

              precision    recall  f1-score   support

         ham       0.99      1.00      0.99      1203
        spam       0.97      0.93      0.95       191

    accuracy                           0.99      1394
   macro avg       0.98      0.96      0.97      1394
weighted avg       0.99      0.99      0.99      1394

Confusion matrix (rows = true, columns = predicted):
['ham', 'spam']
[[1197    6]
 [  13  178]]

Three departments (made up)
              precision    recall  f1-score   support

     Billing       0.93      0.95      0.94        60
   Technical       0.84      0.90      0.87        30
    Security       0.71      0.50      0.59        10

    accuracy                           0.89       100
   macro avg       0.83      0.78      0.80       100
weighted avg       0.89      0.89      0.89       100

Confusion matrix (rows = true, columns = predicted):
['Billing', 'Technical', 'Security']
[[57  3  0]
 [ 1 27  2]
 [ 3  2  5]]
```

## Reading the Output

**The "always ham" classifier.** Its accuracy is 86.3%, but its recall is 0.0: it found none of the 191 spam messages. Its precision is also reported as 0.0, but really it is undefined, because the classifier never said "spam". When one class is rare, accuracy mostly measures how common the *other* class is, so it can't tell a useful classifier from a useless one. Precision and recall look at the rare class itself.

**The spam classifier.** Its accuracy of 98.6% is far above the 86.3% of "always ham", so the classifier really is useful. Precision and recall show what kind of mistakes it makes. 

- **Precision**: 0.967 because it classified 184 messages as spam, but only 178 were really spam, the other 6 were ham. 
- **Recall**: 0.932 because there were 191 spam messages in the test set, and it found 178 of them. The other 13 got through. 

 The confusion matrix at the bottom of the spam results shows the same counts: the row for really ham is `[1197 6]` and the row for really spam is `[13 178]`.

**Which mistake is worse?** That depends on what the classifier is for. For a spam filter, losing a real message (a false positive) is probably worse than letting some spam through (a false negative), so precision matters more. For a classifier that flags emergency messages, it would be the other way around, and recall would matter more. You choose the performance metrics to watch by thinking about what each kind of mistake costs.

## More Than Two Classes

The spam classifier chooses between two classes. Of the three lab assignment versions, Group B's classifier chooses between six classes (six departments), so if you are in Group B, you will read a report like the one below. When there are more than two classes, scikit-learn calculates precision, recall and F1 for each class in turn, treating that class as the positive one. To show what that looks like, the end of `main.py` has a made-up example: a help desk that sorts 100 messages into three departments. Security is the rare one: it gets only 10 of the 100 messages.

At the bottom of the report are two kinds of average, and they tell different stories:

- **Macro average:** the plain average of the per-class scores. Every class counts the same, however small. Security's recall of 0.50 pulls the macro F1 down to 0.80.
- **Weighted average:** the per-class scores averaged in proportion to the number of messages in each class. The big departments dominate it, so the weighted F1 is 0.89, the same as the accuracy.

If you only looked at the accuracy, you wouldn't notice that half of the Security messages were sent to the wrong department. The confusion matrix shows where they went: 3 to Billing and 2 to Technical. Each row is a true department and each column is a predicted department, so the numbers on the diagonal are the correct answers.

## Running the Code

The code is in the [Lab 4 example](../Examples/Lab04-ClassifierMetrics/CS212_Lab04_Example.md), as a complete Python project and as a Jupyter notebook. That page explains how to download and run them.

## Try It Yourself

- In `main.py`, make a classifier that calls every message spam: `always_spam = [1] * len(test_labels)`. Print its scores with `show_scores`. What are its precision and recall? Why is it useless even though its recall is perfect?
- In `spam_results.py`, change `test_size` from 0.25 to 0.5. Which of the numbers change, and by how much? What does that tell you about how much to trust the result from one test set?
- Which mistake would you rather your spam filter make: sending a real message to the spam folder, or letting a spam message through? What do the precision and recall of spam tell you about that?
- In the three-department example, move one of the Security messages that was sent to Billing so it is predicted correctly. How much does the accuracy change? How much does the Security recall change?

## Reference

- <a href="https://scikit-learn.org/stable/modules/model_evaluation.html" target="_blank">Metrics and scoring: quantifying the quality of predictions</a>, scikit-learn User Guide.
- <a href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection" target="_blank">SMS Spam Collection</a>, UCI Machine Learning Repository, by Tiago A. Almeida and José María Gómez Hidalgo.



*These notes were drafted by Claude Code and revised by Brian Bird. 10/21/2026*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
