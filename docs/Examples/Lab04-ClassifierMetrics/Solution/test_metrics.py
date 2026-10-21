"""Tests for metrics.py. Run them with:  uv run test_metrics.py
(or with pytest:  uv run pytest)"""

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from metrics import accuracy, count_results, f1, precision, recall

# 1000 messages: 20 real emergencies. The classifier finds 15 and raises 10 false alarms.
TRUE_LABELS = [1] * 20 + [0] * 980
PREDICTED_LABELS = [1] * 15 + [0] * 5 + [1] * 10 + [0] * 970


def close(a, b):
    return abs(a - b) < 0.000001


def test_counts():
    assert count_results(TRUE_LABELS, PREDICTED_LABELS) == (15, 10, 5, 970)


def test_scores_by_hand():
    tp, fp, fn, tn = count_results(TRUE_LABELS, PREDICTED_LABELS)
    assert close(accuracy(tp, fp, fn, tn), 0.985)
    assert close(precision(tp, fp), 0.6)
    assert close(recall(tp, fn), 0.75)
    assert close(f1(0.6, 0.75), 2 * 0.6 * 0.75 / 1.35)


def test_always_no_does_not_divide_by_zero():
    tp, fp, fn, tn = count_results(TRUE_LABELS, [0] * 1000)
    assert (tp, fp, fn, tn) == (0, 0, 20, 980)
    assert close(accuracy(tp, fp, fn, tn), 0.98)
    assert precision(tp, fp) == 0.0   # the classifier never said "yes"
    assert recall(tp, fn) == 0.0
    assert f1(0.0, 0.0) == 0.0


def test_matches_scikit_learn():
    cases = [
        (TRUE_LABELS, PREDICTED_LABELS),
        ([1, 0, 1, 1, 0, 0, 1, 0], [1, 1, 0, 1, 0, 0, 1, 1]),
        ([1, 1, 1, 0], [1, 1, 1, 0]),   # a perfect classifier
    ]
    for true_labels, predicted_labels in cases:
        tp, fp, fn, tn = count_results(true_labels, predicted_labels)
        p = precision(tp, fp)
        r = recall(tp, fn)
        assert close(accuracy(tp, fp, fn, tn), accuracy_score(true_labels, predicted_labels))
        assert close(p, precision_score(true_labels, predicted_labels))
        assert close(r, recall_score(true_labels, predicted_labels))
        assert close(f1(p, r), f1_score(true_labels, predicted_labels))


if __name__ == "__main__":
    test_counts()
    test_scores_by_hand()
    test_always_no_does_not_divide_by_zero()
    test_matches_scikit_learn()
    print("All tests passed.")
