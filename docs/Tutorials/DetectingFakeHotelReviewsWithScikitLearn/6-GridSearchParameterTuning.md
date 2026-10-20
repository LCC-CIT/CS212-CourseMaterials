---
title: Tuning Hyperparameters using Grid Search
---

## Parameter Tuning Using Grid Search

We’ve already encountered some parameters such as `use_idf` in the `TfidfTransformer`. Classifiers tend to have many parameters as well; e.g., `MultinomialNB` includes a smoothing parameter `alpha` and `SGDClassifier` has a regularization penalty parameter `alpha` (which controls how strongly the model penalizes large weights to prevent overfitting).

Instead of tweaking the parameters of the various components of the chain manually, it is possible to run an exhaustive search of the best parameters on a grid of possible values. We try out our classifier on either single words or *bigrams*[^1] (such as `"my husband"` or `"front desk"`), with or without *idf*, and with a penalty parameter of either 0.001 or 0.0001 for the linear SVM. Each key is the pipeline step name, two underscores, and the parameter name:

```python
from sklearn.model_selection import GridSearchCV
parameters = {
     'vect__ngram_range': [(1, 1), (1, 2)],
     'tfidf__use_idf': (True, False),
     'clf__alpha': (1e-3, 1e-4),
 }
```

Obviously, such an exhaustive search can be expensive. If we have multiple CPU cores at our disposal, we can tell the grid searcher to try these eight parameter combinations in parallel with the `n_jobs` parameter. If we give this parameter a value of `-1`, grid search will detect how many cores are installed and use them all:

```python
gs_clf = GridSearchCV(text_clf, parameters, cv=5, n_jobs=-1)
```

Description of parameters:

- `estimator`: An object that fits a model based on some training data and can make predictions for new data. In this case, `text_clf`, the SVM pipeline we built earlier.
- `param_grid`: A dictionary with parameter names as keys and lists of parameter settings to try. In this case, the `parameters` dictionary we defined earlier.
- `n_jobs`: The number of jobs to run in parallel.
- `cv`: Determines the *cross-validation*[^2] splitting strategy. `cv=5` splits the training data into 5 equal folds, training on 4 folds and validating on the 5th fold repeatedly so the test set remains completely untouched during tuning.

The grid search instance behaves like a normal `scikit-learn` model. Let’s fit the grid search across our training reviews:

```python
gs_clf = gs_clf.fit(reviews_train, labels_train)
```

Calling `fit` on a `GridSearchCV` object automatically refits the winning model on the full training set and returns a classifier that we can use to `predict`:

```python
gs_clf.predict(['My husband and I loved this luxurious hotel in Chicago!'])[0]
```

The predicted label can vary depending on the training data and split.

The object’s `best_score_` and `best_params_` attributes store the best mean cross-validation score and the parameter settings corresponding to that score:

```python
gs_clf.best_score_
```

```python
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
```

The best score and settings depend on the data and cross-validation results. You can get a more detailed summary of the search from the `gs_clf.cv_results_` dictionary.



---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---

[^1]: A *bigram* is an *n-gram* sequence of two words or characters, for example: "my husband" or "qu".
[^2]: *Cross-validation* is a resampling method that repeatedly splits the data into separate ‘train’ and ‘test’ subsets so model performance can be evaluated on unseen data.
