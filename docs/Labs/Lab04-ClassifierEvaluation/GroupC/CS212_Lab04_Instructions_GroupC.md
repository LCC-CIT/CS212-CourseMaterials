---
title: "Lab 4, Group C"
description: "Instructions for Lab 4, Group C: finding a rare kind of message in disaster response data, with precision and recall."
keywords: classifier, scikit-learn, imbalanced data, precision, recall, threshold, class_weight
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Lab 4: Evaluating Text Classifiers</h1>

<h2>Group C: Finding Medical Requests in Disaster Messages</h2>

<h2>Contents</h2>

[TOC]

## Which Messages Need Medical Help?

After a major disaster, aid organizations receive thousands of messages from people who need help. There are far too many for people to read, so a classifier could pick out the messages that a particular team needs to see first. In this lab you will build a classifier that reads one message and answers a yes/no question: **is this person asking for medical help?**

Most messages are *not* about medical help, so a "yes" is rare. That makes accuracy (the percent correct) a poor measure, and it gives you a chance to work with **precision** and **recall**. By the end of the lab you will have:

- seen a classifier with 92% accuracy that does nothing useful,
- used `class_weight` and the **decision threshold** to trade precision for recall, and
- chosen **hyperparameters** with a grid search that is scored with the right measure.

**A note about the data.** These are real messages from people in Haiti, Chile, Pakistan and other places, sent during earthquakes, floods and storms. Some are frightening or sad. Read them with respect.

**Before you start,** read the lecture notes [Classifier Metrics](../../../LectureNotes/CS212-Unit04-2-ClassifierMetrics.md). They explain the performance metrics you will use in this lab (accuracy, precision, recall and F1) and the confusion matrix. Then look at the [Lab 4 example](../../../Examples/Lab04-ClassifierMetrics/CS212_Lab04_Example.md), which has code that calculates them with scikit-learn.

### The data

The data is the **Disaster Response Messages** data set, which has about 26,000 messages labeled by Appen (formerly Figure Eight) for disaster relief. Each message has a `genre` (`direct` for a message sent by a person, `news`, or `social`) and 36 yes/no categories. We will use five of the categories, which are listed below. Its license is not stated, so you will download it yourself instead of getting it from the course site.

### Set up your project

1. Make a project folder for the lab with `uv init lab04`, and then `cd lab04`.
2. Add scikit-learn: `uv add scikit-learn`
3. Save this program as `fetch_data.py` in your project folder and run it once with `uv run fetch_data.py`. It downloads three CSV files (about 7 MB), removes blank and repeated messages, and saves one CSV file named `disaster_messages.csv` in your project folder. Your own program will read that file.

```python
# fetch_data.py: download the disaster response messages and save them as one CSV file.
# Run it once with:  uv run fetch_data.py
import csv
import os
import socket
from urllib.request import urlretrieve

try:
    import truststore  # only needed if you get a certificate error (see the lab instructions)
    truststore.inject_into_ssl()
except ImportError:
    pass

socket.setdefaulttimeout(60)  # give up with an error instead of waiting forever

URL = "https://s3.amazonaws.com/datasets.huggingface.co/disaster_response_messages_"
PARTS = ["training", "validation", "test"]

# The categories we keep. Every category is 1 (yes) or 0 (no).
CATEGORIES = ["medical_help", "search_and_rescue", "missing_people", "fire", "water"]

rows = []
seen = set()  # the messages we have already kept
count_before = 0
for part in PARTS:
    print("Downloading", part)
    temp_name = part + ".csv"
    urlretrieve(URL + part + ".csv", temp_name)
    # The files start with a "byte order mark", which utf-8-sig removes.
    with open(temp_name, encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            count_before += 1
            message = row["message"].strip()
            # Skip blank and repeated messages.
            if message == "" or message in seen:
                continue
            seen.add(message)
            new_row = {"message": message, "genre": row["genre"]}
            for category in CATEGORIES:
                new_row[category] = row[category]
            rows.append(new_row)
    os.remove(temp_name)

print("Removed", count_before - len(rows), "blank or repeated messages")

with open("disaster_messages.csv", "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["message", "genre"] + CATEGORIES)
    writer.writeheader()
    writer.writerows(rows)

print("Saved", len(rows), "messages to disaster_messages.csv")
for category in CATEGORIES:
    total = 0
    for row in rows:
        total += int(row[category])
    print(category, total, "messages")
```

If the download fails with an error that mentions `CERTIFICATE_VERIFY_FAILED`, run `uv add truststore` and then run the program again. If it stops with a timeout, just run it again.

Output:

```
Downloading training
Downloading validation
Downloading test
Removed 79 blank or repeated messages
Saved 26169 messages to disaster_messages.csv
medical_help 2080 messages
search_and_rescue 724 messages
missing_people 298 messages
fire 282 messages
water 1669 messages
```

You can choose any of the five categories to work on, but **use `medical_help` unless you have a reason not to.** The percentage is the share of the messages that are "yes".

| Category | "Yes" messages | Share | Notes |
| --- | --- | --- | --- |
| `medical_help` | 2,080 | 7.9% | The default for this lab. Enough "yes" messages to get steady results. |
| `water` | 1,669 | 6.4% | The easiest. Water has clear keywords. |
| `search_and_rescue` | 724 | 2.8% | A challenge. The labels are noisy, so expect low scores. |
| `missing_people` | 298 | 1.1% | A challenge. Very few examples. |
| `fire` | 282 | 1.1% | A challenge. Very few examples. |

### Starter code

Put this code at the top of your program. It reads the CSV file and gives you the message texts and the 1/0 labels for the category you choose.

```python
import csv


def load_messages(path, category):
    """Read disaster_messages.csv. Returns two lists with one item per message:
    the message text and its label for the chosen category (1 = yes, 0 = no)."""
    texts = []
    labels = []
    with open(path, encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            texts.append(row["message"])
            labels.append(int(row[category]))
    return texts, labels
```

Now add this to check that it works. It also splits the data three ways: 60% for training, 20% for **validation** and 20% for the **test**. You will use the validation set to compare your ideas. The test set is for one final check at the end.

```python
from sklearn.model_selection import train_test_split

CATEGORY = "medical_help"
texts, labels = load_messages("disaster_messages.csv", CATEGORY)
print(len(texts), "messages,", sum(labels), "are", CATEGORY)

# 60% train, 20% validation, 20% test. stratify keeps the same share of
# "yes" messages in all three parts.
rest_texts, test_texts, rest_labels, test_labels = train_test_split(
    texts, labels, test_size=0.20, random_state=42, stratify=labels)
train_texts, val_texts, train_labels, val_labels = train_test_split(
    rest_texts, rest_labels, test_size=0.25, random_state=42, stratify=rest_labels)
print("train:", len(train_texts), "messages,", sum(train_labels), "yes")
print("validation:", len(val_texts), "messages,", sum(val_labels), "yes")
print("test:", len(test_texts), "messages,", sum(test_labels), "yes")
```

Output:

```
26169 messages, 2080 are medical_help
train: 15701 messages, 1248 yes
validation: 5234 messages, 416 yes
test: 5234 messages, 416 yes
```

### What to do

Write your code in one Python file, and put your answers to the questions in comments. Unless a step says otherwise, train on the training set and measure on the **validation** set.

1. **An "always no" classifier.** Use `DummyClassifier(strategy="most_frequent")`, which ignores the message and always predicts the most common label. Train it and print its accuracy, precision and recall for the "yes" class (`precision_score`, `recall_score` with `zero_division=0`). In your comments, say what the accuracy is and why that number is misleading.

2. **Baseline.** Build a pipeline with a `TfidfVectorizer` and a `LogisticRegression`:

   ```python
   pipe = Pipeline([("tfidf", TfidfVectorizer()),
                    ("clf", LogisticRegression(max_iter=1000))])
   ```

   Use these step names, `"tfidf"` and `"clf"`. A grid search refers to a setting by the name of its step, for example `tfidf__min_df` or `clf__C`, so the names in your grid have to match the names in your pipeline. (The names in the Lab 3 tutorial are different.)

   Train it and print a `classification_report` and a `confusion_matrix`. In your comments, answer:
   - What are the precision and recall of the "yes" class?
   - In words: of the people who needed medical help, how many did the classifier find? Of the messages it flagged, how many really needed it?

3. **Experiment 1: `class_weight`.** Train the same model again with `class_weight="balanced"`. This makes a mistake on a "yes" message count more in training, in proportion to how rare "yes" is. Compare the precision, recall, F1 and accuracy to the baseline. In your comments, say what changed and why accuracy went *down*.

4. **Experiment 2: Move the decision threshold.** A `LogisticRegression` really calculates the *probability* that a message is a "yes", and then says "yes" if that is 0.5 or more. You can pick a different cut-off. Use `model.predict_proba(val_texts)[:, 1]` to get the probabilities for the validation messages from your `class_weight="balanced"` model. For each threshold from 0.2 to 0.8, make a list of predictions (1 if the probability is at least the threshold, else 0) and print the precision, recall and F1. In your comments, answer:
   - What happens to precision and recall as the threshold goes up?
   - Imagine a relief team can read some false alarms, but doesn't want to miss more than four out of ten real requests. Which threshold would you choose, using only the validation results?

5. **Tune the hyperparameters.** Use `GridSearchCV` with `cv=3` and **`scoring="f1"`** to search `tfidf__ngram_range`, `tfidf__min_df`, `clf__C` and `clf__class_weight` (`None` or `"balanced"`). Print the best settings and the cross-validation score. Check the best model on the validation set. In your comments, say why you used `scoring="f1"` and not the default.

6. **Final test.** Choose your best model and a threshold, using only what you learned from the training and validation sets. Run it on the **test** set *once*. Print a `classification_report` and a `confusion_matrix`. In your comments, compare the test scores to the validation scores. If they differ, why might that be?

7. **Error analysis.** From the test set, print five messages that were real "yes" messages that your model missed (false negatives), and five that it flagged but shouldn't have (false positives). Look at them. In your comments, answer: What do the missed messages have in common? Are any of the labels questionable? What does that tell you about how well any classifier could do on this data?

### Hints

- **Use the validation set to decide, the test set to report.** If you make choices (a setting or a threshold) by looking at the test set, then the test results are no longer an honest measure of how the classifier will do on new messages.
- **`scoring="f1"`.** `GridSearchCV` picks the setting with the best score. The default score is accuracy, which would favor a classifier that rarely says "yes". `"f1"` is the F1 score of the positive class.
- **Probabilities.** `predict_proba` returns a table with two columns, the probability of 0 and the probability of 1. `[:, 1]` selects the second column. `LinearSVC` doesn't have `predict_proba`, so use `LogisticRegression` for steps 4 to 6.
- **Run time.** The grid in step 5 has 24 combinations, so 72 training runs. The whole solution runs in about 20 seconds on a laptop.
- **What to expect.** Your scores will be modest, and that's normal. This is a hard problem, partly because people don't always label messages the same way. With `medical_help` the baseline finds only about 1 in 10 of the "yes" messages (recall about 0.10), with high precision. With `class_weight="balanced"` the recall goes up to about 0.60, and the precision drops to about 0.35. A tuned model gets an F1 of about 0.45 to 0.50. The test set results will be a bit different from the validation set results.
- **Your numbers will differ** if you choose another category or change `random_state`.

### References

The data is the Disaster Response Messages data set from Appen (formerly Figure Eight), as published on <a href="https://huggingface.co/datasets/community-datasets/disaster_response_messages" target="_blank">Hugging Face</a>.

The scikit-learn guides to <a href="https://scikit-learn.org/stable/modules/model_evaluation.html" target="_blank">model evaluation</a> and the [Working with Text Data tutorial](../../../Tutorials/scikit-learn-1.7/WorkingWithTextData.md) (see its sections on the classification report, confusion matrix and grid search) are good references for this lab.

## Submitting your lab work on Canvas

**Note**: You only need to submit your code. You <u>do not</u> need to upload your virtual environment (.venv) folder or the data files.

### Beta Version

- Post the beta version of your Python file to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the "Prod." column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The Python (.py) file
2. The code review <u>from your lab partner</u> with the "Prod." column filled out by you.

## Grading Criteria

The main focus of grading will be on use of the scikit-learn classes, on whether you measured your results correctly, and on the explanations in your comments. The accuracy of your classifier will not be graded.

*These lab instructions were drafted by Claude Code and are waiting for review by Brian Bird. 10/20/2026*

------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------
