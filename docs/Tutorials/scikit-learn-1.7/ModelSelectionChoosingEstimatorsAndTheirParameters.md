[scikit-learn tutorials index](ScikitLearnTutorials.md)

# Model selection: choosing estimators and their parameters

## Score, and cross-validated scores

As we have seen, every estimator exposes a `score` method that can judge the quality of the fit (or the prediction) on new data. **Bigger is better**.

```python
>>> from sklearn import datasets, svm
>>> X_digits, y_digits = datasets.load_digits(return_X_y=True)
>>> svc = svm.SVC(C=1, kernel='linear')
>>> svc.fit(X_digits[:-100], y_digits[:-100]).score(X_digits[-100:], y_digits[-100:])
0.98
```

To get a better measure of prediction accuracy (which we can use as a proxy for goodness of fit of the model), we can successively split the data in *folds* that we use for training and testing:

```python
>>> import numpy as np
>>> X_folds = np.array_split(X_digits, 3)
>>> y_folds = np.array_split(y_digits, 3)
>>> scores = list()
>>> for k in range(3):
...     # We use 'list' to copy, in order to 'pop' later on
...     X_train = list(X_folds)
...     X_test = X_train.pop(k)
...     X_train = np.concatenate(X_train)
...     y_train = list(y_folds)
...     y_test = y_train.pop(k)
...     y_train = np.concatenate(y_train)
...     scores.append(svc.fit(X_train, y_train).score(X_test, y_test))
>>> print(scores)
[0.934..., 0.956..., 0.939...]
```

This is called a <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.KFold.html#sklearn.model_selection.KFold" target="_blank">`KFold`</a> cross-validation.

## Cross-validation generators

Scikit-learn has a collection of classes which can be used to generate lists of train/test indices for popular cross-validation strategies.

They expose a `split` method which accepts the input dataset to be split and yields the train/test set indices for each iteration of the chosen cross-validation strategy.

This example shows an example usage of the `split` method.

```python
>>> from sklearn.model_selection import KFold, cross_val_score
>>> X = ["a", "a", "a", "b", "b", "c", "c", "c", "c", "c"]
>>> k_fold = KFold(n_splits=5)
>>> for train_indices, test_indices in k_fold.split(X):
...      print('Train: %s | test: %s' % (train_indices, test_indices))
Train: [2 3 4 5 6 7 8 9] | test: [0 1]
Train: [0 1 4 5 6 7 8 9] | test: [2 3]
Train: [0 1 2 3 6 7 8 9] | test: [4 5]
Train: [0 1 2 3 4 5 8 9] | test: [6 7]
Train: [0 1 2 3 4 5 6 7] | test: [8 9]
```

The cross-validation can then be performed easily:

```python
>>> [svc.fit(X_digits[train], y_digits[train]).score(X_digits[test], y_digits[test])
...  for train, test in k_fold.split(X_digits)]
[0.963..., 0.922..., 0.963..., 0.963..., 0.930...]
```

The cross-validation score can be directly calculated using the <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score" target="_blank">`cross_val_score`</a> helper. Given an estimator, the cross-validation object and the input dataset, the <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.cross_val_score.html#sklearn.model_selection.cross_val_score" target="_blank">`cross_val_score`</a> splits the data repeatedly into a training and a testing set, trains the estimator using the training set and computes the scores based on the testing set for each iteration of cross-validation.

By default the estimator’s `score` method is used to compute the individual scores.

Refer the <a href="https://scikit-learn.org/1.7/modules/metrics.html#metrics" target="_blank">metrics module</a> to learn more on the available scoring methods.

```python
>>> cross_val_score(svc, X_digits, y_digits, cv=k_fold, n_jobs=-1)
array([0.96388889, 0.92222222, 0.9637883 , 0.9637883 , 0.93036212])
```

`n_jobs=-1` means that the computation will be dispatched on all the CPUs of the computer.

Alternatively, the `scoring` argument can be provided to specify an alternative scoring method.

```python
>>> cross_val_score(svc, X_digits, y_digits, cv=k_fold,
...                 scoring='precision_macro')
array([0.96578289, 0.92708922, 0.96681476, 0.96362897, 0.93192644])
```

**Cross-validation generators**

| <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.KFold.html#sklearn.model_selection.KFold" target="_blank">`KFold`</a> **(n_splits, shuffle, random_state)** | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.StratifiedKFold.html#sklearn.model_selection.StratifiedKFold" target="_blank">`StratifiedKFold`</a> **(n_splits, shuffle, random_state)** | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.GroupKFold.html#sklearn.model_selection.GroupKFold" target="_blank">`GroupKFold`</a> **(n_splits)** |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Splits it into K folds, trains on K-1 and then tests on the left-out. | Same as K-Fold but preserves the class distribution within each fold. | Ensures that the same group is not in both testing and training sets. |

| <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.ShuffleSplit.html#sklearn.model_selection.ShuffleSplit" target="_blank">`ShuffleSplit`</a> **(n_splits, test_size, train_size, random_state)** | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.StratifiedShuffleSplit.html#sklearn.model_selection.StratifiedShuffleSplit" target="_blank">`StratifiedShuffleSplit`</a> | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.GroupShuffleSplit.html#sklearn.model_selection.GroupShuffleSplit" target="_blank">`GroupShuffleSplit`</a> |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Generates train/test indices based on random permutation.    | Same as shuffle split but preserves the class distribution within each iteration. | Ensures that the same group is not in both testing and training sets. |

| <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html#sklearn.model_selection.LeaveOneGroupOut" target="_blank">`LeaveOneGroupOut`</a> **()** | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.LeavePGroupsOut.html#sklearn.model_selection.LeavePGroupsOut" target="_blank">`LeavePGroupsOut`</a>  **(n_groups)** | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.LeaveOneOut.html#sklearn.model_selection.LeaveOneOut" target="_blank">`LeaveOneOut`</a> **()** |
| ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Takes a group array to group observations.                   | Leave P groups out.                                          | Leave one observation out.                                   |

| <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.LeavePOut.html#sklearn.model_selection.LeavePOut" target="_blank">`LeavePOut`</a> **(p)** | <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.PredefinedSplit.html#sklearn.model_selection.PredefinedSplit" target="_blank">`PredefinedSplit`</a> |
| ------------------------------------------------------------ | ------------------------------------------------------------ |
| Leave P observations out.                                    | Generates train/test indices based on predefined splits.     |

**Exercise**

On the digits dataset, plot the cross-validation score of a <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.svm.SVC.html#sklearn.svm.SVC" target="_blank">`SVC`</a> estimator with a linear kernel as a function of parameter `C` (use a logarithmic grid of points, from 1 to 10).

```python
>>> import numpy as np
>>> from sklearn import datasets, svm
>>> from sklearn.model_selection import cross_val_score
>>> X, y = datasets.load_digits(return_X_y=True)
>>> svc = svm.SVC(kernel="linear")
>>> C_s = np.logspace(-10, 0, 10)
>>> scores = list()
>>> scores_std = list()
```
```

```

![../../_images/model_selection-1.png](https://scikit-learn.org/1.7/_images/model_selection-1.png)
## Grid-search and cross-validated estimators

### Grid-search

scikit-learn provides an object that, given data, computes the score during the fit of an estimator on a parameter grid and chooses the parameters to maximize the cross-validation score. This object takes an estimator during the construction and exposes an estimator API:

```python
>>> from sklearn.model_selection import GridSearchCV, cross_val_score
>>> Cs = np.logspace(-6, -1, 10)
>>> clf = GridSearchCV(estimator=svc, param_grid=dict(C=Cs),
...                    n_jobs=-1)
>>> clf.fit(X_digits[:1000], y_digits[:1000])
GridSearchCV(cv=None,...
>>> clf.best_score_
0.925...
>>> clf.best_estimator_.C
0.0077...

>>> # Prediction performance on test set is not as good as on train set
>>> clf.score(X_digits[1000:], y_digits[1000:])
0.943...
```

By default, the <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV" target="_blank">`GridSearchCV`</a> uses a 5-fold cross-validation. However, if it detects that a classifier is passed, rather than a regressor, it uses a stratified 5-fold.

Nested cross-validation

```python
>>> cross_val_score(clf, X_digits, y_digits)
array([0.938..., 0.963..., 0.944...])
```

Two cross-validation loops are performed in parallel: one by the <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.model_selection.GridSearchCV.html#sklearn.model_selection.GridSearchCV" target="_blank">`GridSearchCV`</a> estimator to set `gamma` and the other one by `cross_val_score` to measure the prediction performance of the estimator. The resulting scores are unbiased estimates of the prediction score on new data.

Warning

You cannot nest objects with parallel computing (`n_jobs` different than 1).

### Cross-validated estimators

Cross-validation to set a parameter can be done more efficiently on an algorithm-by-algorithm basis. This is why, for certain estimators, scikit-learn exposes <a href="https://scikit-learn.org/1.7/modules/cross_validation.html#cross-validation" target="_blank">Cross-validation: evaluating estimator performance</a> estimators that set their parameter automatically by cross-validation:

```python
>>> from sklearn import linear_model, datasets
>>> lasso = linear_model.LassoCV()
>>> X_diabetes, y_diabetes = datasets.load_diabetes(return_X_y=True)
>>> lasso.fit(X_diabetes, y_diabetes)
LassoCV()
>>> # The estimator chose automatically its lambda:
>>> lasso.alpha_
0.00375...
```

These estimators are called similarly to their counterparts, with ‘CV’ appended to their name.

**Exercise**

On the diabetes dataset, find the optimal regularization parameter alpha.

**Bonus**: How much can you trust the selection of alpha?

```python
import numpy as np

from sklearn import datasets
from sklearn.linear_model import Lasso
from sklearn.model_selection import GridSearchCV

X, y = datasets.load_diabetes(return_X_y=True)
X = X[:150]
```

**Solution:** <a href="https://scikit-learn.org/1.7/auto_examples/exercises/plot_cv_diabetes.html#sphx-glr-auto-examples-exercises-plot-cv-diabetes-py" target="_blank">Cross-validation on diabetes Dataset Exercise</a>

## Enhanced Model Selection Features in scikit-learn 1.7

Since this tutorial was originally written for scikit-learn 1.4, several enhancements have been made to model selection and cross-validation capabilities:

### Enhanced Array API Support for Model Selection

scikit-learn 1.7 now supports Array API-compliant inputs in model selection functions, making it easier to work with data from libraries like PyTorch and CuPy:

```python
>>> import torch
>>> from sklearn.model_selection import cross_val_score, GridSearchCV
>>> from sklearn.svm import SVC
>>>
>>> # Works with PyTorch tensors
>>> X = torch.tensor([[1, 2], [3, 4], [5, 6], [7, 8]])
>>> y = torch.tensor([0, 1, 0, 1])
>>> svc = SVC()
>>>
>>> # Cross-validation with PyTorch tensors
>>> scores = cross_val_score(svc, X, y, cv=3)
>>>
>>> # Grid search with PyTorch tensors
>>> param_grid = {'C': [0.1, 1, 10]}
>>> grid_search = GridSearchCV(svc, param_grid, cv=3)
>>> grid_search.fit(X, y)
```

### Enhanced Sparse Data Support in Cross-Validation

All model selection functions now support both traditional sparse matrices (`scipy.sparse.spmatrix`) and the newer sparse arrays (`scipy.sparse.sparray`):

```python
>>> from scipy.sparse import csr_array
>>> from sklearn.model_selection import cross_val_score, GridSearchCV
>>> from sklearn.linear_model import LogisticRegression
>>>
>>> X_sparse = csr_array([[0, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 0]])
>>> y = [0, 1, 1, 0]
>>>
>>> # Cross-validation with sparse arrays
>>> lr = LogisticRegression()
>>> scores = cross_val_score(lr, X_sparse, y, cv=3)
>>>
>>> # Grid search with sparse arrays
>>> param_grid = {'C': [0.1, 1, 10]}
>>> grid_search = GridSearchCV(lr, param_grid, cv=3)
>>> grid_search.fit(X_sparse, y)
```

### Enhanced ROC Curve Visualization from Cross-Validation

The new `from_cv_results()` method in `RocCurveDisplay` allows automatic generation of ROC curves from cross-validation results, making model evaluation more comprehensive:

```python
>>> from sklearn.model_selection import cross_validate
>>> from sklearn.metrics import RocCurveDisplay
>>> from sklearn.svm import SVC
>>>
>>> # Perform cross-validation with return_estimator=True
>>> cv_results = cross_validate(svc, X, y, cv=5, return_estimator=True)
>>>
>>> # Generate ROC curves from cross-validation results
>>> RocCurveDisplay.from_cv_results(cv_results, X, y)
```

### Enhanced Metadata Routing for Model Selection

scikit-learn 1.7 includes improved metadata routing that ensures proper handling of metadata (like sample weights) when used within cross-validation and grid search:

```python
>>> from sklearn.model_selection import cross_val_score
>>> from sklearn.ensemble import HistGradientBoostingClassifier
>>> import numpy as np
>>>
>>> # Sample weights
>>> sample_weights = np.array([1.0, 2.0, 1.5, 0.8, 1.2])
>>>
>>> # Cross-validation with sample weights
>>> clf = HistGradientBoostingClassifier(enable_metadata_routing=True)
>>> scores = cross_val_score(clf, X, y, cv=3,
...                         params={'sample_weight': sample_weights})
```

These enhancements maintain full backward compatibility while providing more flexibility and power for model selection and cross-validation tasks.





---

This original version of this tutorial was written by scikit-learn developers under the <a href="https://opensource.org/license/BSD-3-clause" target="_blank">BSD License</a>.  

---

The code examples and text were updated for scikit-learn version 1.7 by Brian Bird using Claude Sonet 4, 10/19/2025

---

