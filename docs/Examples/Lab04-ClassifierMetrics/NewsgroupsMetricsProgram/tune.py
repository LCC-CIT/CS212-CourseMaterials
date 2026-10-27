# Lab 4 example: using a performance metric to tune the newsgroups
# classifier, where talk.religion.misc is the rare class.
#
# Run with:  uv run tune.py

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

# The same posts as main.py: all of the posts from three newsgroups,
# and only 75 training posts and 50 test posts from talk.religion.misc.
categories = ["talk.religion.misc", "rec.sport.hockey", "comp.graphics",
              "sci.med"]
twenty_train = fetch_20newsgroups(subset="train", categories=categories,
                                  shuffle=True, random_state=42)
twenty_test = fetch_20newsgroups(subset="test", categories=categories,
                                 shuffle=True, random_state=42)
group_names = twenty_test.target_names
religion = group_names.index("talk.religion.misc")

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

# The same steps as main.py, as a pipeline, but without alpha, because
# the grid search chooses it. The names "vect" and "clf" are used in
# the settings below, for example "clf__alpha" is the alpha setting of
# "clf".
pipeline = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", random_state=42,
                          max_iter=5, tol=None)),
])
settings = {
    # single words, or single words and word pairs
    "vect__ngram_range": [(1, 1), (1, 2)],
    # how strongly the classifier is kept simple
    "clf__alpha": [0.01, 0.001, 0.0001, 0.00001],
    # "balanced" counts each post of a small class for more
    "clf__class_weight": [None, "balanced"],
}

# Try every combination of settings, using 5-fold cross-validation on
# the training posts only. We compare two scores: accuracy and
# f1_macro, the average of the F1 of each newsgroup. To see how the two
# choices differ, we test both tuned models on the test posts. The test
# results are only for comparing them, not for choosing the settings.
for score_name in ["accuracy", "f1_macro"]:
    search = GridSearchCV(pipeline, settings, scoring=score_name, cv=5)
    search.fit(train_posts, train_groups)
    print("Best settings when scoring by", score_name)
    print("  ", search.best_params_)
    print("   cross-validation", score_name, "=",
          round(search.best_score_, 3))
    print()
    predicted_groups = search.predict(test_posts)
    print(classification_report(test_groups, predicted_groups,
                                target_names=group_names))
