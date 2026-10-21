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

The program `main.py` has a function, `show_scores`, that uses these scikit-learn functions to print the four counts and the four performance metrics. It measures the spam classifier and the "always ham" classifier for comparison, and prints the classification report and confusion matrix that the Spam Detection program printed. At the end it repeats the four-newsgroups example from the scikit-learn text tutorial (Week 3), which has more than two classes and is explained below.

```python
# Lab 4 example: measuring the spam classifier from the Spam Detection example.
#
# Run with:  uv run main.py

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.pipeline import Pipeline

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

# ---------------------------------------------------------------- four classes
# The newsgroups example from the scikit-learn text tutorial (Week 3): posts from four
# newsgroups, classified with the tf-idf and linear SVM pipeline from that tutorial.
# The first run downloads the data, which scikit-learn keeps for later runs.
categories = ["alt.atheism", "soc.religion.christian", "comp.graphics", "sci.med"]
twenty_train = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset="test", categories=categories, shuffle=True, random_state=42)

text_clf = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", alpha=1e-3,
                          random_state=42, max_iter=5, tol=None)),
])
text_clf.fit(twenty_train.data, twenty_train.target)
newsgroup_predictions = text_clf.predict(twenty_test.data)

print("\nFour newsgroups")
print(classification_report(twenty_test.target, newsgroup_predictions,
                            target_names=twenty_test.target_names))
print("Confusion matrix (rows = true, columns = predicted):")
print(twenty_test.target_names)
print(confusion_matrix(twenty_test.target, newsgroup_predictions))
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

Four newsgroups
                        precision    recall  f1-score   support

           alt.atheism       0.95      0.80      0.87       319
         comp.graphics       0.87      0.98      0.92       389
               sci.med       0.94      0.89      0.91       396
soc.religion.christian       0.90      0.95      0.93       398

              accuracy                           0.91      1502
             macro avg       0.91      0.91      0.91      1502
          weighted avg       0.91      0.91      0.91      1502

Confusion matrix (rows = true, columns = predicted):
['alt.atheism', 'comp.graphics', 'sci.med', 'soc.religion.christian']
[[256  11  16  36]
 [  4 380   3   2]
 [  5  35 353   3]
 [  5  11   4 378]]
```

## Reading the Output

**The "always ham" classifier.** Its accuracy is 86.3%, but its recall is 0.0: it found none of the 191 spam messages. Its precision is also reported as 0.0, but really it is undefined, because the classifier never said "spam". When one class is rare, accuracy mostly measures how common the *other* class is, so it can't tell a useful classifier from a useless one. Precision and recall look at the rare class itself.

**The spam classifier.** Its accuracy of 98.6% is far above the 86.3% of "always ham", so the classifier really is useful. Precision and recall show what kind of mistakes it makes. 

- **Precision**: 0.967 because it classified 184 messages as spam, but only 178 were really spam, the other 6 were ham. 
- **Recall**: 0.932 because there were 191 spam messages in the test set, and it found 178 of them. The other 13 got through. 

 The confusion matrix at the bottom of the spam results shows the same counts: the row for really ham is `[1197 6]` and the row for really spam is `[13 178]`.

**Which mistake is worse?** That depends on what the classifier is for. For a spam filter, losing a real message (a false positive) is probably worse than letting some spam through (a false negative), so precision matters more. For a classifier that flags emergency messages, it would be the other way around, and recall would matter more. You choose the performance metrics to watch by thinking about what each kind of mistake costs.

## More Than Two Classes

The spam classifier chooses between two classes. Of the three lab assignment versions, Group B's classifier chooses between six classes (six departments), so if you are in Group B, you will read a report like the one below. When there are more than two classes, scikit-learn calculates precision, recall and F1 for each class in turn, treating that class as the positive one. To show what that looks like, the end of `main.py` repeats the newsgroups example from the scikit-learn text tutorial in Week 3: posts from four newsgroups (atheism, computer graphics, medicine and Christianity), classified with the tf-idf and linear SVM pipeline from the tutorial. The numbers are the same as in the tutorial.

Read the report one row at a time. For `alt.atheism`, the recall is 0.80: there were 319 atheism posts in the test set and the classifier found 256 of them. The precision is 0.95: the classifier put 270 posts in `alt.atheism` (256 + 4 + 5 + 5, the first column of the confusion matrix) and 256 of them belonged there. The other classes work the same way, each one taking its turn as the positive class. In the confusion matrix each row is a true newsgroup and each column is a predicted newsgroup, so the numbers on the diagonal are the correct answers.

At the bottom of the report are two kinds of average:

- **Macro average:** the plain average of the per-class scores. Every class counts the same, however small.
- **Weighted average:** the per-class scores averaged in proportion to the number of posts in each class (the *support* column).

Here the four newsgroups are about the same size (319 to 398 posts), so the macro average, the weighted average and the accuracy are all 0.91. They would be different if one class were much smaller than the others. A class with only 10 test posts would hardly change the weighted average or the accuracy, but it would count as much as any other class in the macro average. When the classes are not the same size, look at both averages and at each class's own row.

The accuracy of 0.91 hides the fact that the recall for `alt.atheism` is only 0.80, the lowest of the four. The confusion matrix shows where those posts went: 36 of the 63 that were missed were put in `soc.religion.christian`. That matches what the tutorial said, that atheism and Christianity posts are confused with each other more often than with the other topics.

## Using a Metric to Tune a Classifier

Performance metrics are also how you decide whether a change made a classifier better. Most classifiers have *hyperparameters*, settings that you choose before training, such as the `alpha` of naive Bayes or whether the word counts include pairs of words. `GridSearchCV` tries every combination of the settings you give it. For each combination it trains and tests the classifier several times with cross-validation, using only the training messages. Then it keeps the combination with the best *score*.

That score is another performance metric, and you choose it with the `scoring` argument. The default for a classifier is accuracy, which has the problem described above: when one class is rare, accuracy can hardly tell a good classifier from a bad one. For a rare class you usually want `scoring="f1"`, which is the F1 of the positive class. For more than two classes, `scoring="f1_macro"` averages the F1 of every class, the same way the macro average in the report does.

The program `tune.py` tunes the spam classifier. It puts the word counts and the classifier in a `Pipeline`, so the grid search can change settings in both, and it tries a small grid with each of the two scores. You can run it with `uv run tune.py`.

```python
# Lab 4 example: using a performance metric to tune the spam classifier.
#
# Run with:  uv run tune.py

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from spam_results import load_spam_data

train_messages, test_messages, train_labels, test_labels = load_spam_data()

# The same steps as before, as a pipeline. The names "counts" and "nb" are used
# in the settings below, for example "nb__alpha" is the alpha setting of "nb".
pipeline = Pipeline([("counts", CountVectorizer()), ("nb", MultinomialNB())])
settings = {
    "counts__ngram_range": [(1, 1), (1, 2)],   # single words, or single words and word pairs
    "nb__alpha": [0.1, 0.5, 1.0],              # how much smoothing naive Bayes does
}

# Try every combination of settings, using 5-fold cross-validation on the training
# messages only. The score decides which combination is "best", so the choice of
# score matters. We try two: accuracy and F1 (the F1 of the positive class, spam).
for score_name in ["accuracy", "f1"]:
    search = GridSearchCV(pipeline, settings, scoring=score_name, cv=5)
    search.fit(train_messages, train_labels)
    print("Best settings when scoring by", score_name)
    print("  ", search.best_params_)
    print("   cross-validation", score_name, "=", round(search.best_score_, 3))

# Only now use the test messages, once, with the model that was best by F1.
print()
predicted_labels = search.predict(test_messages)
print(classification_report(test_labels, predicted_labels, target_names=["ham", "spam"]))
```

Here is the output of `uv run tune.py`:

```
Best settings when scoring by accuracy
   {'counts__ngram_range': (1, 2), 'nb__alpha': 0.1}
   cross-validation accuracy = 0.987
Best settings when scoring by f1
   {'counts__ngram_range': (1, 2), 'nb__alpha': 0.1}
   cross-validation f1 = 0.95

              precision    recall  f1-score   support

         ham       0.99      0.99      0.99      1203
        spam       0.96      0.94      0.95       191

    accuracy                           0.99      1394
   macro avg       0.97      0.97      0.97      1394
weighted avg       0.99      0.99      0.99      1394
```

Both scores picked the same settings, and the tuned classifier is barely different from the untuned one: spam precision went from 0.967 to 0.957 and recall from 0.932 to 0.942, so F1 stayed at about 0.95. That is a normal result. The spam classifier was already good, the test set is small (191 spam messages), and a difference of one or two messages is just noise. Tuning isn't a way to get a big improvement. It helps you pick settings in a systematic way, and it only makes sense if the score you tune for is the one that matters. Here the two scores agree because spam is 13% of the messages. The rarer the class is, the more likely they are to disagree.

Notice that the test messages were used only once, at the end. The grid search chose the settings with cross-validation on the training messages. If you chose the settings by looking at the test results, the test results would no longer tell you how well the classifier works on new messages.

## Running the Code

The code is in the [Lab 4 example](../Examples/Lab04-ClassifierMetrics/CS212_Lab04_Example.md), as a complete Python project and as a Jupyter notebook. That page explains how to download and run them.

## Try It Yourself

- In `main.py`, make a classifier that calls every message spam: `always_spam = [1] * len(test_labels)`. Print its scores with `show_scores`. What are its precision and recall? Why is it useless even though its recall is perfect?
- In `spam_results.py`, change `test_size` from 0.25 to 0.5. Which of the numbers change, and by how much? What does that tell you about how much to trust the result from one test set?
- Which mistake would you rather your spam filter make: sending a real message to the spam folder, or letting a spam message through? What do the precision and recall of spam tell you about that?
- In `tune.py`, add `0.01` to the `nb__alpha` list and `(1, 3)` to the `ngram_range` list. Do the best settings change? Does the F1 on the test messages change? If not, what does that tell you about how much there was to gain from tuning this classifier?
- In the newsgroups example, look at the confusion matrix. Which two newsgroups are confused most often? Calculate the precision and recall of `sci.med` from the matrix, and check your answers against the report.

## Reference

- <a href="https://scikit-learn.org/stable/modules/model_evaluation.html" target="_blank">Metrics and scoring: quantifying the quality of predictions</a>, scikit-learn User Guide.
- <a href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection" target="_blank">SMS Spam Collection</a>, UCI Machine Learning Repository, by Tiago A. Almeida and José María Gómez Hidalgo.



*These notes were drafted by Claude Code and revised by Brian Bird. 10/21/2026*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
