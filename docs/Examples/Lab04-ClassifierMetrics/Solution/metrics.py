"""Accuracy, precision, recall and F1, calculated by hand from the four counts.

The positive class is 1. Each function returns 0.0 instead of dividing by zero.
"""


def count_results(true_labels, predicted_labels):
    """Count the four kinds of result: true positives, false positives,
    false negatives and true negatives."""
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
