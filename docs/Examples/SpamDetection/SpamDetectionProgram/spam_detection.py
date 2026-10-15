# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy>=2.4.0",
#     "pandas>=3.0.0",
#     "scikit-learn>=1.9.0",
# ]
# ///
"""Spam Detection with Naive Bayes

CS 212 AI Programming 1

Trains a naive Bayes classifier to sort text messages into spam (unwanted
ads and scams) and ham (normal messages). This program does the same steps
as SpamDetection.ipynb in the SpamDetectionNotebook folder.

Run it with:  uv run spam_detection.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# --- 1. Load and explore the data ---
# The data file is in the same folder as this program.
data_file = Path(__file__).parent / "sms_spam.csv"
messages = pd.read_csv(data_file)

print("First five messages:")
print(messages.head())
print()
print("Number of each kind of message:")
print(messages["label"].value_counts())
print()

# --- 2. Split the data into training and test sets ---
# Hold back 25% of the messages for testing. random_state makes the
# shuffle the same every time you run the program.
train_text, test_text, train_labels, test_labels = train_test_split(
    messages["message"], messages["label"], test_size=0.25, random_state=42)

print("Training messages:", len(train_text))
print("Test messages:", len(test_text))

# --- 3. Turn the text into word counts ---
# fit_transform builds the word dictionary from the training messages and
# counts their words. transform counts the test messages' words using that
# same dictionary.
count_vect = CountVectorizer()
train_counts = count_vect.fit_transform(train_text)
test_counts = count_vect.transform(test_text)

print("Words in the dictionary:", train_counts.shape[1])
print()

# --- 4. Train the classifier ---
clf = MultinomialNB()
clf.fit(train_counts, train_labels)

# --- 5. Test the classifier ---
predicted = clf.predict(test_counts)
print("Accuracy:", metrics.accuracy_score(test_labels, predicted))
print()
print(metrics.classification_report(test_labels, predicted))

# Rows are the real labels and columns are the predictions (ham, spam).
print("Confusion matrix:")
print(metrics.confusion_matrix(test_labels, predicted))
print()

# --- 6. Classify new messages ---
# Try adding your own messages to the list!
new_messages = [
    "Hey, are we still meeting for lunch tomorrow?",
    "WINNER! You have won a free cruise. Call now to claim your prize!",
    "Can you send me the notes from today's class?",
    "URGENT: your account has been selected for a cash reward. Text CLAIM to 80082",
]

new_counts = count_vect.transform(new_messages)
new_predictions = clf.predict(new_counts)
new_probabilities = clf.predict_proba(new_counts)

print("New messages:")
for i in range(len(new_messages)):
    spam_chance = new_probabilities[i][1]  # column 1 is the chance of spam
    print(f"{new_predictions[i]:4}  ({spam_chance:.1%} spam)  {new_messages[i]}")
print()

# --- 7. Which words signal spam? ---
# feature_log_prob_ holds each word's probability (as a logarithm) in ham
# (row 0) and spam (row 1). Dividing them gives the likelihood ratio.
words = count_vect.get_feature_names_out()
ham_probs = np.exp(clf.feature_log_prob_[0])
spam_probs = np.exp(clf.feature_log_prob_[1])
ratios = spam_probs / ham_probs

# argsort lists the positions of the ratios from smallest to largest,
# so we take the last 10 positions and go through them backward.
print("Strongest signs of spam:")
top_ten = np.argsort(ratios)[-10:]
for i in reversed(top_ten):
    print(f"{words[i]:10} {ratios[i]:6.1f} times more likely in spam")
