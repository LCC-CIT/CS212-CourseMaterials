# Lab 4 example: measuring the spam classifier from the Spam Detection example.
# By Brian Bird 10/21/2026 with assistance from Claude Code
#
# Run with:  uv run main.py

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)
from sklearn.pipeline import Pipeline

from newsgroups_data import load_newsgroups
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
# The newsgroups example from the scikit-learn text tutorial (Week 3), with two of its
# newsgroups changed and only a few posts from one of them (see newsgroups_data.py).
# The posts are classified with the tf-idf and linear SVM pipeline from that tutorial.
train_posts, test_posts, train_groups, test_groups, group_names = load_newsgroups()

text_clf = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", alpha=1e-3,
                          random_state=42, max_iter=5, tol=None)),
])
text_clf.fit(train_posts, train_groups)
newsgroup_predictions = text_clf.predict(test_posts)

print("\nFour newsgroups")
print(classification_report(test_groups, newsgroup_predictions, target_names=group_names))
print("Confusion matrix (rows = true, columns = predicted):")
print(group_names)
print(confusion_matrix(test_groups, newsgroup_predictions))
