# Lab 4 example: measuring a classifier with precision, recall and F1.
#
# Run with:  uv run main.py

from sklearn.metrics import (accuracy_score, classification_report, confusion_matrix,
                             f1_score, precision_score, recall_score)

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
