"""Prints performance metrics calculated by hand (metrics.py) next to scikit-learn's."""

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from metrics import accuracy, count_results, f1, precision, recall


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
