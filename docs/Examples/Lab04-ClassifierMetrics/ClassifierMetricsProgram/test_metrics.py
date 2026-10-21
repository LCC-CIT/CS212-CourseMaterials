"""Tests for metrics.py. Run them with:  uv run test_metrics.py
(or with pytest:  uv run pytest)"""

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from metrics import accuracy, count_results, f1, precision, recall

# The results of the spam classifier on 1,394 test messages (1 = spam, 0 = ham).
# 191 messages really are spam. The classifier finds 178 of them and also calls
# 6 of the 1,203 ham messages spam.
TRUE_LABELS = [1] * 191 + [0] * 1203
PREDICTED_LABELS = [1] * 178 + [0] * 13 + [1] * 6 + [0] * 1197


def close(a, b):
    return abs(a - b) < 0.000001


def test_counts():
    assert count_results(TRUE_LABELS, PREDICTED_LABELS) == (178, 6, 13, 1197)


def test_scores_by_hand():
    tp, fp, fn, tn = count_results(TRUE_LABELS, PREDICTED_LABELS)
    assert close(accuracy(tp, fp, fn, tn), 1375 / 1394)
    assert close(precision(tp, fp), 178 / 184)
    assert close(recall(tp, fn), 178 / 191)
    p = 178 / 184
    r = 178 / 191
    assert close(f1(p, r), 2 * p * r / (p + r))


def test_always_ham_does_not_divide_by_zero():
    tp, fp, fn, tn = count_results(TRUE_LABELS, [0] * 1394)
    assert (tp, fp, fn, tn) == (0, 0, 191, 1203)
    assert close(accuracy(tp, fp, fn, tn), 1203 / 1394)
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
    test_always_ham_does_not_divide_by_zero()
    test_matches_scikit_learn()
    print("All tests passed.")
