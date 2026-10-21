# Lab 4 example: measuring the spam classifier from the Spam Detection example.
#
# Run with:  uv run main.py

from sklearn.metrics import classification_report, confusion_matrix

from report import show_scores
from spam_results import get_spam_results

# ---------------------------------------------------------------- two classes
# The true labels and the predicted labels of the test messages (1 = spam, 0 = ham).
test_labels, predicted_labels = get_spam_results()
print(len(test_labels), "test messages,", sum(test_labels), "of them are spam")
print()
show_scores("Spam classifier", test_labels, predicted_labels)

# For comparison, a "classifier" that calls every message ham.
always_ham = [0] * len(test_labels)
show_scores("Always ham", test_labels, always_ham)

print()
print(classification_report(test_labels, predicted_labels, target_names=["ham", "spam"]))
print("Confusion matrix (rows = true, columns = predicted):")
print(["ham", "spam"])
print(confusion_matrix(test_labels, predicted_labels))

# ---------------------------------------------------------------- three classes
# A made-up example. A help desk sorts 100 messages into three departments.
# Security is the rare one. Each case is (true department, predicted department,
# how many messages).
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

print("\nThree departments (made up)")
names = ["Billing", "Technical", "Security"]
print(classification_report(true_departments, predicted_departments, labels=names))
print("Confusion matrix (rows = true, columns = predicted):")
print(names)
print(confusion_matrix(true_departments, predicted_departments, labels=names))
