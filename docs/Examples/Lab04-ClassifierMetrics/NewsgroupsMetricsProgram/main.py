# Lab 4 example: measuring a classifier with more than two classes,
# using the newsgroups example from the scikit-learn text tutorial
# (Week 3).
# By Brian Bird 10/21/2026 with assistance from Claude Code
#
# Run with:  uv run main.py

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.pipeline import Pipeline

# ------------------------------------------------ the data
# Posts from four newsgroups. Two of the tutorial's newsgroups (atheism
# and Christianity) are replaced with hockey and religion. The first run
# downloads the data, which scikit-learn keeps for later runs.
categories = ["talk.religion.misc", "rec.sport.hockey", "comp.graphics",
              "sci.med"]
twenty_train = fetch_20newsgroups(subset="train", categories=categories,
                                  shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset="test", categories=categories,
                                 shuffle=True, random_state=42)
group_names = twenty_test.target_names
religion = group_names.index("talk.religion.misc")

# To show what happens when one class is rare, keep only the first 75
# of the 377 religion posts for training. The other newsgroups keep all
# of their posts.
train_posts = []
train_groups = []
religion_count = 0
for i in range(len(twenty_train.data)):
    group = twenty_train.target[i]
    if group == religion:
        religion_count = religion_count + 1
    if group != religion or religion_count <= 75:
        train_posts.append(twenty_train.data[i])
        train_groups.append(group)

# Do the same for testing, keeping only 50 of the 251 religion posts.
test_posts = []
test_groups = []
religion_count = 0
for i in range(len(twenty_test.data)):
    group = twenty_test.target[i]
    if group == religion:
        religion_count = religion_count + 1
    if group != religion or religion_count <= 50:
        test_posts.append(twenty_test.data[i])
        test_groups.append(group)

# ------------------------------------------------ the classifier
# The tf-idf and linear SVM pipeline from the tutorial.
text_clf = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", alpha=1e-3,
                          random_state=42, max_iter=5, tol=None)),
])
text_clf.fit(train_posts, train_groups)
predicted_groups = text_clf.predict(test_posts)

# ------------------------------------------------ measuring it
print("Four newsgroups")
print(classification_report(test_groups, predicted_groups,
                            target_names=group_names))
print("Confusion matrix (rows = true, columns = predicted):")
print(group_names)
print(confusion_matrix(test_groups, predicted_groups))
