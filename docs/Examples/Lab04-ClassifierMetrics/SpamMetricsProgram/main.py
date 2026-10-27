# Lab 4 example: measuring the spam classifier from the Spam Detection
# example.
# By Brian Bird 10/21/2026 with assistance from Claude Code
#
# Run with:  uv run main.py

import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, precision_score,
                             recall_score)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# ------------------------------------------------ the spam classifier
# These steps are the same as in the Spam Detection example: the same
# data, the same 75/25 split, and a naive Bayes classifier on word
# counts. The only differences are that the data is read with the csv
# module and the labels are numbers: 1 is spam and 0 is ham.
messages = []
labels = []
with open("data/sms_spam.csv", encoding="utf-8", newline="") as file:
    for row in csv.DictReader(file):
        messages.append(row["message"])
        if row["label"] == "spam":
            labels.append(1)
        else:
            labels.append(0)

train_messages, test_messages, train_labels, test_labels = train_test_split(
    messages, labels, test_size=0.25, random_state=42)

vectorizer = CountVectorizer()
train_counts = vectorizer.fit_transform(train_messages)
test_counts = vectorizer.transform(test_messages)

classifier = MultinomialNB()
classifier.fit(train_counts, train_labels)
predicted_labels = classifier.predict(test_counts)

print(len(test_labels), "test messages,", sum(test_labels), "of them are spam")
print()

# ------------------------------------------------ measuring it
# For two classes, the confusion matrix has the four counts:
# [[TN, FP], [FN, TP]]. The positive class is 1 (spam).
matrix = confusion_matrix(test_labels, predicted_labels, labels=[0, 1])
tn, fp, fn, tp = matrix.ravel()
print("Spam classifier")
print("  counts:  TP =", tp, " FP =", fp, " FN =", fn, " TN =", tn)
accuracy = accuracy_score(test_labels, predicted_labels)
precision = precision_score(test_labels, predicted_labels)
recall = recall_score(test_labels, predicted_labels)
f1 = f1_score(test_labels, predicted_labels)
print("  accuracy ", round(accuracy, 3))
print("  precision", round(precision, 3))
print("  recall   ", round(recall, 3))
print("  F1       ", round(f1, 3))
print()

# ------------------------------------------------ always ham
# For comparison, a "classifier" that calls every message ham.
always_ham = [0] * len(test_labels)

matrix = confusion_matrix(test_labels, always_ham, labels=[0, 1])
tn, fp, fn, tp = matrix.ravel()
print("Always ham")
print("  counts:  TP =", tp, " FP =", fp, " FN =", fn, " TN =", tn)
accuracy = accuracy_score(test_labels, always_ham)
# This classifier never says "spam", so precision would divide by zero.
# zero_division=0 makes precision_score return 0 instead of a warning.
precision = precision_score(test_labels, always_ham, zero_division=0)
recall = recall_score(test_labels, always_ham)
f1 = f1_score(test_labels, always_ham)
print("  accuracy ", round(accuracy, 3))
print("  precision", round(precision, 3))
print("  recall   ", round(recall, 3))
print("  F1       ", round(f1, 3))

# ------------------------------------------------ report and matrix
print()
print(classification_report(test_labels, predicted_labels,
                            target_names=["ham", "spam"]))
print("Confusion matrix (rows = true, columns = predicted):")
print(["ham", "spam"])
print(confusion_matrix(test_labels, predicted_labels))
