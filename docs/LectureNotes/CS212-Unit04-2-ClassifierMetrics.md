---
title: Classifier Metrics
description: Performance metrics for classifiers (accuracy, precision, recall, F1 and the confusion matrix) and how to calculate them with scikit-learn.
keywords: performance metrics, accuracy, precision, recall, F1, confusion matrix, macro average, scikit-learn
generator: Typora
author: Brian Bird
---

<h1>Classifier Metrics</h1>

**CS 212, AI Programming 1**

<h2>Contents</h2>

[TOC]

## Introduction

Last week we briefly looked at classifier with *accuracy*, the percent of test messages it got right. There are other *performance metrics* that matter as well *precision*, *recall* and *F1*. We will learn to use tools to make these performance assessments and discuss their importance. We will also learn how to improve the performance of our models.

## Review

Lets review by looking at a [spam detection example](../Examples/SpamDetection/CS212_SpamDetection_Overview.md). Last week we looked at similar code in [the twenty newsgroups tutorial](https://colab.research.google.com/drive/1FBrABO2L1DFKRn1v0zRknHS57eiktzgm?usp=sharing). In both of these programs, these are the things that are done:

- Prepare the data
  - Download a data set.
  - Load the data into a 
  - Split the data set into training and test sets.
  - Get word frequency counts from both data sets.
    (These are the feature vectors.)
- Training
  - Use the training data word counts to train the model.
- Testing
  - Use the model for prediction (inference).
    Generate a set of predicted labels for the test data.
  - Extract feature vectors from the training set.
  - Calculate an accuracy score (percent right) by comparing the actual labels to the predicted labels.

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

## Calculating the Measures with scikit-learn

You don't need to write code to calculate these numbers. The module `sklearn.metrics` has a function for each one: `accuracy_score`, `precision_score`, `recall_score` and `f1_score`. You give each of them the true labels and the predicted labels. The function `confusion_matrix` gives you the four counts. For two classes, its result is `[[TN, FP], [FN, TP]]`, so `.ravel()` flattens it into the four numbers in that order.

If a classifier never says "spam", then TP + FP is 0, and precision (TP / (TP + FP)) would divide by zero. The argument `zero_division=0` tells `precision_score` to return 0.0 in that case instead of printing a warning.

The program `main.py` has a function, `show_scores`, that uses these scikit-learn functions to print the four counts and the four performance metrics. The program measures two examples: first the spam classifier, which has two classes, then a newsgroups classifier, which has four.

### The Spam Example

The function `get_spam_results` in `spam_results.py` repeats the steps of the Spam Detection program (the same data, the same 75/25 split, and a naive Bayes classifier on word counts) and returns the true labels and the predicted labels of the test messages. You can read that program to see how those steps work.

The first part of `main.py` measures the spam classifier and the "always ham" classifier for comparison, and prints the classification report and confusion matrix that the Spam Detection program printed:

```python
# Lab 4 example: measuring the spam classifier from the Spam Detection
# example.
# By Brian Bird 10/21/2026 with assistance from Claude Code
#
# Run with:  uv run main.py

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.pipeline import Pipeline

from newsgroups_data import load_newsgroups
from spam_results import get_spam_results


def show_scores(name, true_labels, predicted_labels):
    """Print the four counts and the four performance metrics.

    The positive class is 1.
    """
    # For two classes, the confusion matrix has the four counts:
    # [[TN, FP], [FN, TP]].
    matrix = confusion_matrix(true_labels, predicted_labels, labels=[0, 1])
    tn, fp, fn, tp = matrix.ravel()
    print(name)
    print("  counts:  TP =", tp, " FP =", fp, " FN =", fn, " TN =", tn)
    accuracy = accuracy_score(true_labels, predicted_labels)
    # zero_division=0 is the score to use if the classifier never says
    # "spam"
    precision = precision_score(true_labels, predicted_labels, zero_division=0)
    recall = recall_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels)
    print("  accuracy ", round(accuracy, 3))
    print("  precision", round(precision, 3))
    print("  recall   ", round(recall, 3))
    print("  F1       ", round(f1, 3))


# ------------------------------------------------ two classes
# The true labels and the predicted labels of the test messages
# (1 = spam, 0 = ham).
test_labels, predicted_labels = get_spam_results()
print(len(test_labels), "test messages,", sum(test_labels), "of them are spam")
print()
show_scores("Spam classifier", test_labels, predicted_labels)
print()

# For comparison, a "classifier" that calls every message ham.
always_ham = [0] * len(test_labels)
show_scores("Always ham", test_labels, always_ham)

print()
print(classification_report(test_labels, predicted_labels,
                            target_names=["ham", "spam"]))
print("Confusion matrix (rows = true, columns = predicted):")
print(["ham", "spam"])
print(confusion_matrix(test_labels, predicted_labels))
```

Here is the output of this part of `uv run main.py`:

> 1394 test messages, 191 of them are spam
>
> Spam classifier<br>
> counts:  TP = 178  FP = 6  FN = 13  TN = 1197<br>
> accuracy  0.986<br>
> precision 0.967<br>
> recall    0.932<br>
> F1        0.949
>
> Always ham<br>
> counts:  TP = 0  FP = 0  FN = 191  TN = 1203<br>
> accuracy  0.863<br>
> precision 0.0<br>
> recall    0.0<br>
> F1        0.0
>
> | | precision | recall | f1-score | support |
> | --- | ---: | ---: | ---: | ---: |
> | ham | 0.99 | 1.00 | 0.99 | 1203 |
> | spam | 0.97 | 0.93 | 0.95 | 191 |
> | accuracy | | | 0.99 | 1394 |
> | macro avg | 0.98 | 0.96 | 0.97 | 1394 |
> | weighted avg | 0.99 | 0.99 | 0.99 | 1394 |
>
> Confusion matrix (rows = true, columns = predicted):<br>
> ['ham', 'spam']<br>
> [[1197    6]<br>
> [  13  178]]

#### Reading the Output

**The "always ham" classifier.** Its accuracy is 86.3%, but its recall is 0.0: it found none of the 191 spam messages. Its precision is also reported as 0.0, but really it is undefined, because the classifier never found "spam". When one class is rare, accuracy mostly measures how common the *other* class is, so it can't tell a useful classifier from a useless one. Precision and recall look at the rare class itself.

**The spam classifier.** Its accuracy of 98.6% is far above the 86.3% of "always ham", so the classifier really is useful. Precision and recall show what kind of mistakes it makes. 

- **Precision**: 0.967 because it classified 184 messages as spam, but only 178 were really spam, the other 6 were ham. 
- **Recall**: 0.932 because there were 191 spam messages in the test set, and it found 178 of them. The other 13 got through. 

**The confusion matrix.** The confusion matrix at the bottom of the spam results shows the same four counts. Each *row* is a true class (what the message really is), and each *column* is a predicted class (what the classifier said it is). scikit-learn puts the classes in order of their labels, so ham (0) comes first and spam (1) second. That is the opposite order from the table in [The Four Counts](#the-four-counts), so be careful when you read it. Here is the matrix `[[1197 6] [13 178]]` with each cell labeled:

| | Predicted ham | Predicted spam |
| --- | --- | --- |
| **Really ham** | **1197**: true negatives (TN), real messages correctly left in the inbox | **6**: false positives (FP), real messages wrongly sent to the spam folder |
| **Really spam** | **13**: false negatives (FN), spam messages that got through | **178**: true positives (TP), spam messages correctly caught |

- **Row 1, really ham:** 1197 + 6 = 1,203, all of the ham messages in the test set.
- **Row 2, really spam:** 13 + 178 = 191, all of the spam messages. Each row adds up to the number of messages in that class, the *support* column of the classification report. Recall uses this row: 178 / 191 = 0.932.
- **Column 1, predicted ham:** 1197 + 13 = 1,210, all of the messages the classifier called ham.
- **Column 2, predicted spam:** 6 + 178 = 184, all of the messages the classifier called spam. Precision uses this column: 178 / 184 = 0.967.

The numbers on the diagonal, from the top left to the bottom right (1197 and 178), are the right answers. The other two numbers (6 and 13) are the mistakes.

**Which mistake is worse?** That depends on what the classifier is for. For a spam filter, losing a real message (a false positive) is probably worse than letting some spam through (a false negative), so precision matters more. For a classifier that flags emergency messages, it would be the other way around, and recall would matter more. You choose the performance metrics to watch by thinking about what each kind of mistake costs.

### The Newsgroups Example

The spam classifier chooses between two classes. Of the three lab assignment versions, Group B's classifier chooses between six classes (six departments), so if you are in Group B, you will read a report like the one below. When there are more than two classes, scikit-learn calculates precision, recall and F1 for each class in turn, treating that class as the positive one.

To show what that looks like, the end of `main.py` uses the newsgroups example from the scikit-learn text tutorial in Week 3: posts from four newsgroups (computer graphics, hockey, medicine and religion), classified with the tf-idf and linear SVM pipeline from the tutorial. Two of the tutorial's newsgroups (atheism and Christianity) are replaced with hockey and religion. To show what happens when one class is rare, the function `keep_fewer` in `newsgroups_data.py` throws away most of the religion posts: it keeps only 75 of the 377 for training and 50 of the 251 for testing. The other three newsgroups keep all of their posts, about 600 each for training and 390 each for testing.

The imports for the pipeline are at the top of `main.py`, shown above. Here is the rest of `main.py`:

```python
# ------------------------------------------------ four classes
# The newsgroups example from the scikit-learn text tutorial (Week 3),
# with two of its newsgroups changed and only a few posts from one of
# them (see newsgroups_data.py). The posts are classified with the
# tf-idf and linear SVM pipeline from that tutorial.
(train_posts, test_posts, train_groups, test_groups,
 group_names) = load_newsgroups()

text_clf = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", alpha=1e-3,
                          random_state=42, max_iter=5, tol=None)),
])
text_clf.fit(train_posts, train_groups)
newsgroup_predictions = text_clf.predict(test_posts)

print("\nFour newsgroups")
print(classification_report(test_groups, newsgroup_predictions,
                            target_names=group_names))
print("Confusion matrix (rows = true, columns = predicted):")
print(group_names)
print(confusion_matrix(test_groups, newsgroup_predictions))
```

Here is the rest of the output (the newsgroups part):

> Four newsgroups
>
> | | precision | recall | f1-score | support |
> | --- | ---: | ---: | ---: | ---: |
> | comp.graphics | 0.90 | 0.97 | 0.93 | 389 |
> | rec.sport.hockey | 0.97 | 0.99 | 0.98 | 399 |
> | sci.med | 0.93 | 0.90 | 0.92 | 396 |
> | talk.religion.misc | 0.96 | 0.52 | 0.68 | 50 |
> | accuracy | | | 0.94 | 1234 |
> | macro avg | 0.94 | 0.84 | 0.88 | 1234 |
> | weighted avg | 0.94 | 0.94 | 0.93 | 1234 |
>
> Confusion matrix (rows = true, columns = predicted):<br>
> ['comp.graphics', 'rec.sport.hockey', 'sci.med', 'talk.religion.misc']<br>
> [[377   3   9   0]<br>
> [  3 394   2   0]<br>
> [ 35   3 357   1]<br>
> [  4   6  14  26]]

#### Reading the Output

Read the report one row at a time. For `talk.religion.misc`, the recall is 0.52: there were 50 religion posts in the test set and the classifier found only 26 of them. The precision is 0.96: the classifier put 27 posts in `talk.religion.misc` (0 + 0 + 1 + 26, the last column of the confusion matrix) and 26 of them belonged there. The other classes work the same way, each one taking its turn as the positive class. In the confusion matrix each row is a true newsgroup and each column is a predicted newsgroup, so the numbers on the diagonal are the correct answers.

The rows and columns are in the same order as the list of names printed above the matrix: `comp.graphics`, `rec.sport.hockey`, `sci.med` and `talk.religion.misc` (shortened to graphics, hockey, medicine and religion below). Here is the matrix with each cell labeled:

| | Predicted graphics | Predicted hockey | Predicted medicine | Predicted religion |
| --- | --- | --- | --- | --- |
| **Really graphics** | **377**: correct | **3**: graphics posts called hockey | **9**: graphics posts called medicine | **0**: graphics posts called religion |
| **Really hockey** | **3**: hockey posts called graphics | **394**: correct | **2**: hockey posts called medicine | **0**: hockey posts called religion |
| **Really medicine** | **35**: medicine posts called graphics | **3**: medicine posts called hockey | **357**: correct | **1**: medicine post called religion |
| **Really religion** | **4**: religion posts called graphics | **6**: religion posts called hockey | **14**: religion posts called medicine | **26**: correct |

- **Each row** is all the test posts from one newsgroup, and it adds up to that newsgroup's *support* in the report. For example, the religion row is 4 + 6 + 14 + 26 = 50. The number on the diagonal divided by the row total is that newsgroup's recall: 26 / 50 = 0.52 for religion.
- **Each column** is all the posts the classifier put in one newsgroup. The number on the diagonal divided by the column total is that newsgroup's precision: for religion, 26 / (0 + 0 + 1 + 26) = 26 / 27 = 0.96.
- **The diagonal** (377, 394, 357 and 26) is the right answers. Every other cell is a mistake, and it tells you which two newsgroups were confused. The biggest one is the 35 medicine posts that were called graphics.

With more than two classes, the words true positive, false positive and false negative only make sense after you pick one class to be the positive one. If religion is the positive class, then 26 is TP, the other three numbers in its row (4, 6 and 14) are FN, and the other three numbers in its column (0, 0 and 1) are FP. All of the other cells are TN for religion. Each class takes its turn as the positive class in the same way.

At the bottom of the report are two kinds of average:

- **Macro average:** the plain average of the per-class scores. Every class counts the same, however small.
- **Weighted average:** the per-class scores averaged in proportion to the number of posts in each class (the *support* column).

Here the religion class is much smaller than the others: 50 test posts, compared with 389 to 399. In the weighted average it counts for only 50 of the 1234 posts, so the weighted average F1 is 0.93, close to the scores of the three big classes. In the macro average it counts as one class out of four, so its low recall pulls the macro average recall down to 0.84 and the macro average F1 down to 0.88. When the classes are not the same size, look at both averages and at each class's own row.

The accuracy of 0.94 hides the fact that the classifier misses about half of the religion posts. It is the same problem as the "always ham" classifier: a rare class hardly changes the accuracy, so the accuracy can't tell you how well that class is classified. The confusion matrix shows where the missed posts went: 14 of the 24 were put in `sci.med`. With only 75 religion posts to learn from, the classifier rarely predicts that class. When it does, it is almost always right (high precision), but it misses many of the religion posts (low recall). The best fix is to collect more examples of the rare class. When you can't, you can at least choose a classifier's settings with a score that counts every class equally, as the next section shows.

## Using a Metric to Tune a Classifier

Performance metrics are also how you decide whether a change made a classifier better. Most classifiers have *hyperparameters*, settings that you choose before training, such as the `alpha` of naive Bayes or whether the word counts include pairs of words. `GridSearchCV` tries every combination of the settings you give it. For each combination it trains and tests the classifier several times with cross-validation, using only the training messages. Then it keeps the combination with the best *score*.

### Choosing a Metric to Optimize for

That score is another performance metric, and you choose it with the `scoring` argument. The default for a classifier is accuracy, which has the problem described above: when one class is rare, accuracy can hardly tell a good classifier from a bad one. For a rare class you usually want `scoring="f1"`, which is the F1 of the positive class. For more than two classes, `scoring="f1_macro"` averages the F1 of every class, the same way the macro average in the report does.

### Hyperparameters Being Tuned

These are the hyperparameters that `tune.py` tries. In the code, each name starts with the name of a pipeline step and two underscores, so `nb__alpha` means the `alpha` setting of the step named `nb`.

- **`ngram_range`** (`counts__ngram_range` for spam, `vect__ngram_range` for the newsgroups): which word groups `CountVectorizer` counts. `(1, 1)` counts single words only. `(1, 2)` also counts pairs of words that are next to each other, such as "free entry" or "call now", so the classifier can learn from short phrases as well as single words. Pairs make many more features, so training is slower.
- **`alpha` of naive Bayes** (`nb__alpha`): how much *smoothing* naive Bayes does. Before calculating its probabilities, naive Bayes adds `alpha` to the count of every word in every class. Without smoothing, a word that never appeared in a spam message during training would make the probability of spam zero for any message that contains it. A small `alpha` (0.1) affects the training counts less, and a large one (1.0) affects them more (smooths them more).
- **`alpha` of the linear SVM** (`clf__alpha`): how strongly the classifier is kept simple (this is called *regularization*). A large `alpha` (0.01) keeps the classifier's weights small, so it may miss real patterns. A small `alpha` (0.00001) lets it fit the training posts very closely, so it may learn details that don't carry over to new posts. This is a different setting from the `alpha` of naive Bayes, even though it has the same name.
- **`class_weight`** (`clf__class_weight`): how much each training post counts. With `None`, every post counts the same, so a small class has little effect on what the classifier learns. With `"balanced"`, each post counts for more if its class is small and less if its class is big, so every class has the same total effect.

```python
# Lab 4 example: using a performance metric to tune the spam classifier
# and the newsgroups classifier.
#
# Run with:  uv run tune.py

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from newsgroups_data import load_newsgroups
from spam_results import load_spam_data

# ------------------------------------------------ spam
(train_messages, test_messages,
 train_labels, test_labels) = load_spam_data()

# The same steps as before, as a pipeline. The names "counts" and "nb"
# are used in the settings below, for example "nb__alpha" is the alpha
# setting of "nb".
pipeline = Pipeline([("counts", CountVectorizer()),
                     ("nb", MultinomialNB())])
settings = {
    # single words, or single words and word pairs
    "counts__ngram_range": [(1, 1), (1, 2)],
    # how much smoothing naive Bayes does
    "nb__alpha": [0.1, 0.5, 1.0],
}

# Try every combination of settings, using 5-fold cross-validation on
# the training messages only. The score decides which combination is
# "best", so the choice of score matters. We try two: accuracy and F1
# (the F1 of the positive class, spam).
for score_name in ["accuracy", "f1"]:
    search = GridSearchCV(pipeline, settings, scoring=score_name, cv=5)
    search.fit(train_messages, train_labels)
    print("Best settings when scoring by", score_name)
    print("  ", search.best_params_)
    print("   cross-validation", score_name, "=",
          round(search.best_score_, 3))

# Only now use the test messages, once, with the model that was best
# by F1.
print()
predicted_labels = search.predict(test_messages)
print(classification_report(test_labels, predicted_labels,
                            target_names=["ham", "spam"]))

# ------------------------------------------------ four newsgroups
# The newsgroups classifier from main.py, where talk.religion.misc is
# the rare class.
(train_posts, test_posts, train_groups, test_groups,
 group_names) = load_newsgroups()

pipeline = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", random_state=42,
                          max_iter=5, tol=None)),
])
settings = {
    # single words, or single words and word pairs
    "vect__ngram_range": [(1, 1), (1, 2)],
    # how strongly the classifier is kept simple
    "clf__alpha": [0.01, 0.001, 0.0001, 0.00001],
    # "balanced" counts each post of a small class for more
    "clf__class_weight": [None, "balanced"],
}

# This time we compare accuracy with f1_macro, the average of the F1 of
# each newsgroup. To see how the two choices differ, we test both tuned
# models on the test posts. The test results are only for comparing
# them, not for choosing the settings.
print("Four newsgroups")
for score_name in ["accuracy", "f1_macro"]:
    search = GridSearchCV(pipeline, settings, scoring=score_name, cv=5)
    search.fit(train_posts, train_groups)
    print("Best settings when scoring by", score_name)
    print("  ", search.best_params_)
    print("   cross-validation", score_name, "=",
          round(search.best_score_, 3))
    print()
    predicted_groups = search.predict(test_posts)
    print(classification_report(test_groups, predicted_groups,
                                target_names=group_names))
```

Here is the output of `uv run tune.py`:

> Best settings when scoring by accuracy<br>
> `{'counts__ngram_range': (1, 2), 'nb__alpha': 0.1}`<br>
> cross-validation accuracy = 0.987<br>
> Best settings when scoring by f1<br>
> `{'counts__ngram_range': (1, 2), 'nb__alpha': 0.1}`<br>
> cross-validation f1 = 0.95
>
> | | precision | recall | f1-score | support |
> | --- | ---: | ---: | ---: | ---: |
> | ham | 0.99 | 0.99 | 0.99 | 1203 |
> | spam | 0.96 | 0.94 | 0.95 | 191 |
> | accuracy | | | 0.99 | 1394 |
> | macro avg | 0.97 | 0.97 | 0.97 | 1394 |
> | weighted avg | 0.99 | 0.99 | 0.99 | 1394 |
>
> Four newsgroups<br>
> Best settings when scoring by accuracy<br>
> `{'clf__alpha': 0.0001, 'clf__class_weight': 'balanced', 'vect__ngram_range': (1, 2)}`<br>
> cross-validation accuracy = 0.976
>
> | | precision | recall | f1-score | support |
> | --- | ---: | ---: | ---: | ---: |
> | comp.graphics | 0.91 | 0.97 | 0.94 | 389 |
> | rec.sport.hockey | 0.97 | 0.99 | 0.98 | 399 |
> | sci.med | 0.96 | 0.90 | 0.93 | 396 |
> | talk.religion.misc | 0.82 | 0.72 | 0.77 | 50 |
> | accuracy | | | 0.94 | 1234 |
> | macro avg | 0.91 | 0.89 | 0.90 | 1234 |
> | weighted avg | 0.94 | 0.94 | 0.94 | 1234 |
>
> Best settings when scoring by f1_macro<br>
> `{'clf__alpha': 0.0001, 'clf__class_weight': 'balanced', 'vect__ngram_range': (1, 1)}`<br>
> cross-validation f1_macro = 0.966
>
> | | precision | recall | f1-score | support |
> | --- | ---: | ---: | ---: | ---: |
> | comp.graphics | 0.91 | 0.97 | 0.94 | 389 |
> | rec.sport.hockey | 0.98 | 0.99 | 0.98 | 399 |
> | sci.med | 0.96 | 0.89 | 0.93 | 396 |
> | talk.religion.misc | 0.82 | 0.84 | 0.83 | 50 |
> | accuracy | | | 0.94 | 1234 |
> | macro avg | 0.92 | 0.92 | 0.92 | 1234 |
> | weighted avg | 0.95 | 0.94 | 0.94 | 1234 |



The tuning results for the newsgroups classifier is different from the spam classifier: its religion class is rare, and the grid has one more setting, `class_weight`. Normally every training post counts the same, so a class with only 75 posts has little effect on what the classifier learns. The setting `class_weight="balanced"` makes each post of a small class count for more, in proportion to how rare the class is.

Tuning made a much bigger difference here than it did for spam. Before tuning, in the output of `main.py`, the classifier found 26 of the 50 religion posts (recall 0.52). Both tuned classifiers use a smaller `alpha` and `class_weight="balanced"`, and they find many more: 36 with the settings chosen by accuracy (recall 0.72) and 42 with the settings chosen by `f1_macro` (recall 0.84). The two scores disagree about word pairs. The F1 of the religion class went from 0.68 to 0.77 and 0.83, and the macro average F1 from 0.88 to 0.90 and 0.92. There is a cost: the precision of the religion class went down from 0.96 to 0.82, because the classifier now puts more posts in that class that don't belong there.

Now look at the accuracy on the test posts: it is 0.94 for both tuned classifiers, the same as before tuning. If accuracy were the only number you looked at, you would think tuning had done nothing. Keep in mind that there are only 50 religion posts in the test set, so the difference between the two tuned classifiers is 6 posts. It is a real difference but not a big one. The lesson is that the score you tune for decides which settings you get, so it should be the score that measures what you care about.

Notice that the test messages and posts were not used to choose the settings. The grid search chose them with cross-validation on the training data, and the test data was used only at the end, to see how well the tuned classifiers work. (For the newsgroups, both tuned classifiers are tested so that you can compare them.) If you chose the settings by looking at the test results, the test results would no longer tell you how well the classifier works on new messages.



## Reference

- <a href="https://scikit-learn.org/stable/modules/model_evaluation.html" target="_blank">Metrics and scoring: quantifying the quality of predictions</a>, scikit-learn User Guide.
- <a href="https://archive.ics.uci.edu/dataset/228/sms+spam+collection" target="_blank">SMS Spam Collection</a>, UCI Machine Learning Repository, by Tiago A. Almeida and José María Gómez Hidalgo.



*These notes were drafted by Claude and revised by Brian Bird. 10/21/2026*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lecture notes by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
