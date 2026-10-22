# Lab 4 example: using a performance metric to tune the spam classifier and the
# newsgroups classifier.
#
# Run with:  uv run tune.py

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from newsgroups_data import load_newsgroups
from spam_results import load_spam_data

# ---------------------------------------------------------------- spam
train_messages, test_messages, train_labels, test_labels = load_spam_data()

# The same steps as before, as a pipeline. The names "counts" and "nb" are used
# in the settings below, for example "nb__alpha" is the alpha setting of "nb".
pipeline = Pipeline([("counts", CountVectorizer()), ("nb", MultinomialNB())])
settings = {
    "counts__ngram_range": [(1, 1), (1, 2)],   # single words, or single words and word pairs
    "nb__alpha": [0.1, 0.5, 1.0],              # how much smoothing naive Bayes does
}

# Try every combination of settings, using 5-fold cross-validation on the training
# messages only. The score decides which combination is "best", so the choice of
# score matters. We try two: accuracy and F1 (the F1 of the positive class, spam).
for score_name in ["accuracy", "f1"]:
    search = GridSearchCV(pipeline, settings, scoring=score_name, cv=5)
    search.fit(train_messages, train_labels)
    print("Best settings when scoring by", score_name)
    print("  ", search.best_params_)
    print("   cross-validation", score_name, "=", round(search.best_score_, 3))

# Only now use the test messages, once, with the model that was best by F1.
print()
predicted_labels = search.predict(test_messages)
print(classification_report(test_labels, predicted_labels, target_names=["ham", "spam"]))

# ---------------------------------------------------------------- four newsgroups
# The newsgroups classifier from main.py, where talk.religion.misc is the rare class.
train_posts, test_posts, train_groups, test_groups, group_names = load_newsgroups()

pipeline = Pipeline([
    ("vect", CountVectorizer()),
    ("tfidf", TfidfTransformer()),
    ("clf", SGDClassifier(loss="hinge", penalty="l2", random_state=42, max_iter=5, tol=None)),
])
settings = {
    "vect__ngram_range": [(1, 1), (1, 2)],          # single words, or single words and word pairs
    "clf__alpha": [0.01, 0.001, 0.0001, 0.00001],   # how strongly the classifier is kept simple
    "clf__class_weight": [None, "balanced"],        # "balanced" counts each post of a small class for more
}

# This time we compare accuracy with f1_macro, the average of the F1 of each newsgroup.
# To see how the two choices differ, we test both tuned models on the test posts. The
# test results are only for comparing them, not for choosing the settings.
print("Four newsgroups")
for score_name in ["accuracy", "f1_macro"]:
    search = GridSearchCV(pipeline, settings, scoring=score_name, cv=5)
    search.fit(train_posts, train_groups)
    print("Best settings when scoring by", score_name)
    print("  ", search.best_params_)
    print("   cross-validation", score_name, "=", round(search.best_score_, 3))
    print()
    predicted_groups = search.predict(test_posts)
    print(classification_report(test_groups, predicted_groups, target_names=group_names))
