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
