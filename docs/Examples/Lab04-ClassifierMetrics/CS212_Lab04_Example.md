---
title: "Lab 4, Example"
description: "Class example for Lab 4: measuring a classifier with accuracy, precision, recall and F1."
keywords: accuracy, precision, recall, F1, confusion matrix, scikit-learn
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Lab 4, Measuring a Classifier</h1>

<h2>Example</h2>

In Lab 3 you measured a classifier with *accuracy*, the share of test messages it got right. That works when the classes are about the same size. It can be very misleading when one class is rare. The Lab 4 assignments (all three groups) are about measuring a classifier well and then improving it, so read this example before you start your lab. The complete program is [metrics_example.py](metrics_example.py).

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

## Calculating the Measures in Python

The program below counts the four results with a plain `for` loop and calculates the four measures from the counts. It then asks scikit-learn (`sklearn.metrics`) for the same numbers, so you can see that they agree. The functions are careful about dividing by zero. For example, a classifier that never says "yes" has `tp + fp == 0`, so its precision can't be calculated and the function returns 0.0.

```python
# Lab 4 example: measuring a classifier with precision, recall and F1.
#
# Run with:  uv run metrics_example.py

from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)


def count_results(true_labels, predicted_labels):
    """Count the four kinds of result. The positive class is 1."""
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0
    for i in range(len(true_labels)):
        if predicted_labels[i] == 1 and true_labels[i] == 1:
            true_positives += 1
        elif predicted_labels[i] == 1 and true_labels[i] == 0:
            false_positives += 1
        elif predicted_labels[i] == 0 and true_labels[i] == 1:
            false_negatives += 1
        else:
            true_negatives += 1
    return true_positives, false_positives, false_negatives, true_negatives


def accuracy(tp, fp, fn, tn):
    return (tp + tn) / (tp + fp + fn + tn)


def precision(tp, fp):
    if tp + fp == 0:
        return 0.0  # the classifier never said "yes"
    return tp / (tp + fp)


def recall(tp, fn):
    if tp + fn == 0:
        return 0.0  # there were no real "yes" messages
    return tp / (tp + fn)


def f1(precision_value, recall_value):
    if precision_value + recall_value == 0:
        return 0.0
    return 2 * precision_value * recall_value / (precision_value + recall_value)


def show_scores(name, true_labels, predicted_labels):
    tp, fp, fn, tn = count_results(true_labels, predicted_labels)
    p = precision(tp, fp)
    r = recall(tp, fn)
    print(name)
    print("  counts:       TP =", tp, " FP =", fp, " FN =", fn, " TN =", tn)
    print("  by hand:      accuracy", round(accuracy(tp, fp, fn, tn), 3),
          "| precision", round(p, 3), "| recall", round(r, 3), "| F1", round(f1(p, r), 3))
    print("  scikit-learn: accuracy", round(accuracy_score(true_labels, predicted_labels), 3),
          "| precision", round(precision_score(true_labels, predicted_labels, zero_division=0), 3),
          "| recall", round(recall_score(true_labels, predicted_labels), 3),
          "| F1", round(f1_score(true_labels, predicted_labels), 3))


# ---------------------------------------------------------------- two classes
# 1000 messages. The first 20 really are emergencies (1), the other 980 are not (0).
true_labels = [1] * 20 + [0] * 980

# This classifier found 15 of the 20 emergencies and raised 10 false alarms.
predicted_labels = [1] * 15 + [0] * 5 + [1] * 10 + [0] * 970
show_scores("Classifier", true_labels, predicted_labels)

# A "classifier" that always says no.
always_no = [0] * 1000
show_scores("Always no", true_labels, always_no)

# ---------------------------------------------------------------- three classes
# A help desk sorts 100 messages into three departments. Security is the rare one.
# Each case is (true department, predicted department, how many messages).
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

print("\nThree departments")
names = ["Billing", "Technical", "Security"]
print(classification_report(true_departments, predicted_departments, labels=names))
print("Confusion matrix (rows = true, columns = predicted):")
print(names)
print(confusion_matrix(true_departments, predicted_departments, labels=names))
```

To run it, use `uv run metrics_example.py` in the example's folder. Here is the output:

```
Classifier
  counts:       TP = 15  FP = 10  FN = 5  TN = 970
  by hand:      accuracy 0.985 | precision 0.6 | recall 0.75 | F1 0.667
  scikit-learn: accuracy 0.985 | precision 0.6 | recall 0.75 | F1 0.667
Always no
  counts:       TP = 0  FP = 0  FN = 20  TN = 980
  by hand:      accuracy 0.98 | precision 0.0 | recall 0.0 | F1 0.0
  scikit-learn: accuracy 0.98 | precision 0.0 | recall 0.0 | F1 0.0

Three departments
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

**The "always no" classifier.** Its accuracy is 98%, but its recall is 0.0: it found none of the 20 emergencies. Its precision is also reported as 0.0, but really it is undefined, because the classifier never said "yes". When one class is rare, accuracy mostly measures how common the *other* class is, so it can't tell a useful classifier from a useless one. Precision and recall look at the rare class itself.

**The first classifier.** Its accuracy is 98.5%, which hardly beats "always no". But look at the other measures. The precision of 0.60 means that it said "emergency" 25 times (15 + 10), and 15 of those were right, so 6 out of 10 alarms are real. The recall of 0.75 means that of the 20 real emergencies it found 15 and missed 5. It makes more false-alarm mistakes (10) than missed-emergency mistakes (5). To get fewer false alarms it would have to be more cautious, and then it would probably miss more emergencies.

## More Than Two Classes

In the labs, some of the classifiers choose between several classes. scikit-learn then calculates precision, recall and F1 for each class in turn, treating that class as the positive one. The `classification_report` in the output above shows this for a help desk that sorts 100 messages into three departments. Security is the rare one: it gets only 10 of the 100 messages.

At the bottom of the report are two kinds of average, and they tell different stories:

- **Macro average:** the plain average of the per-class scores. Every class counts the same, however small. Security's recall of 0.50 pulls the macro F1 down to 0.80.
- **Weighted average:** the per-class scores averaged in proportion to the number of messages in each class. The big departments dominate it, so the weighted F1 is 0.89, the same as the accuracy.

If you only looked at the accuracy, you wouldn't notice that half of the Security messages were sent to the wrong department. The confusion matrix shows where they went: 3 to Billing and 2 to Technical. Each row is a true department and each column is a predicted department, so the numbers on the diagonal are the correct answers.

## Try It Yourself

- Change the `predicted_labels` list so that the classifier finds all 20 emergencies but raises 100 false alarms. What happens to the precision and the recall?
- Change it again so that the classifier says "emergency" only once, and is right. What are the precision and recall now?
- In the three-department example, move one of the Security messages that was sent to Billing so it is predicted correctly. How much does the accuracy change? How much does the Security recall change?

*These lab materials were drafted by Claude Code and are waiting for review by Brian Bird. 10/20/2026*

------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------
