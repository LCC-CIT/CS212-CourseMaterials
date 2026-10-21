"""The results of the spam classifier from the Spam Detection example.

load_spam_data() and get_spam_results() repeat the steps of spam_detection.py in that example: the same
data, the same 75/25 split and a naive Bayes classifier on word counts. See that example
for how the steps work. The only differences are that the data is read with the csv
module and the labels are numbers: 1 is spam and 0 is ham.
"""

import csv

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB


def load_spam_data():
    """Returns the training and test messages and their labels (75/25 split)."""
    messages = []
    labels = []
    with open("data/sms_spam.csv", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            messages.append(row["message"])
            if row["label"] == "spam":
                labels.append(1)
            else:
                labels.append(0)

    return train_test_split(messages, labels, test_size=0.25, random_state=42)


def get_spam_results():
    """Returns the true labels and the predicted labels of the test messages."""
    train_messages, test_messages, train_labels, test_labels = load_spam_data()

    vectorizer = CountVectorizer()
    train_counts = vectorizer.fit_transform(train_messages)
    test_counts = vectorizer.transform(test_messages)

    classifier = MultinomialNB()
    classifier.fit(train_counts, train_labels)
    predicted_labels = classifier.predict(test_counts)
    return test_labels, predicted_labels
