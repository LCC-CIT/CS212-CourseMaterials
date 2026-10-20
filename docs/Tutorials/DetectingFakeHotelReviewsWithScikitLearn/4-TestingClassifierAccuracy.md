## Testing Classification Accuracy

[TOC]

Evaluating the predictive accuracy of the model is equally easy. We use the held-out test reviews from `reviews_test` and NumPy (`np.mean`) to calculate the proportion of correct predictions:

```python
import numpy as np
predicted = text_clf.predict(reviews_test)
np.mean(predicted == labels_test)
```

The accuracy score will vary depending on the model and the train/test split.

### Train and Test a Support Vector Machine

While Naïve Bayes treats every word as independent, linear <a href="https://scikit-learn.org/1.7/modules/svm.html#svm" target="_blank">support vector machines (SVMs)</a> optimize a decision hyperplane across all features simultaneously and are widely regarded as one of the best text classification algorithms. We can change the learner by simply plugging a different classifier object into our pipeline. (`SGDClassifier` with `loss='hinge'` trains a linear SVM.)

```python
from sklearn.linear_model import SGDClassifier
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2',
                          alpha=1e-3, random_state=42,
                          max_iter=5, tol=None)),
 ])

text_clf.fit(reviews_train, labels_train)
```

> *Response:*  
> Pipeline(...)

```python
predicted = text_clf.predict(reviews_test)
np.mean(predicted == labels_test)
```

The accuracy score will vary depending on the model and the train/test split.

#### Classification Report

`scikit-learn` provides further utilities for more detailed performance analysis of the results:

```python
from sklearn import metrics
print(metrics.classification_report(labels_test, predicted,
     labels=target_names, target_names=target_names))
```

The columns are showing the following:

- **Precision:** the ratio `tp / (tp + fp)` where `tp` is the number of *true positives* and `fp` the number of *false positives*. For `deceptive`, this measures how often reviews flagged as fake are actually fake.
- **Recall:** the ratio `tp / (tp + fn)` where `tp` is the number of true positives and `fn` the number of false negatives. For `deceptive`, this measures how many of the fake reviews in the test set the classifier finds.
- **F1-score:** A balance between precision and recall (the harmonic mean). 
- **Support:** the number of actual samples of each class in the test set.

#### Confusion Matrix

```python
metrics.confusion_matrix(labels_test, predicted, labels=target_names)
```

The *confusion matrix*[^9] is arranged as follows:

- **Rows** represent the actual classes of the documents (the ground truth).
- **Columns** represent the predicted classes made by the classifier.
- The **diagonal** represents correct classifications: **TP** (True Positive) is the count of reviews correctly classified as in a class.
- Every off-diagonal cell is a mistake, and it counts against two classes:
  - Across a row, it is a **FN** (False Negative) for that row's class: a review that belongs to the class was put in the other one.
  - Down a column, it is a **FP** (False Positive) for that column's class: a review was put in the class but doesn't belong there.

The matrix values show how many reviews of each actual class were assigned to each predicted class. These values depend on the model and train/test split.

#### Inspecting the Most Predictive Features

One major advantage of linear classifiers like `SGDClassifier` is **interpretability**. The learned weight array `text_clf.named_steps['clf'].coef_[0]` contains one weight per word in the vocabulary. Since the classes are ordered alphabetically, negative weights push predictions toward `deceptive` and positive weights push predictions toward `truthful`. We can use `np.argsort` to inspect the top 10 words for each class:

```python
feature_names = text_clf.named_steps['vect'].get_feature_names_out()
weights = text_clf.named_steps['clf'].coef_[0]

print("Top 10 indicators of DECEPTIVE reviews:")
print(feature_names[np.argsort(weights)[:10]])

print("\nTop 10 indicators of TRUTHFUL reviews:")
print(feature_names[np.argsort(weights)[-10:][::-1]])
```

The most predictive words can vary with the training data and split. Often, **truthful indicators** are concrete, spatial, and transactional (such as floor numbers or rates), whereas **deceptive indicators** may include personal pronouns, vague narratives, and superlatives.



---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

[^8]: *Hyperparameter* refers to a configuration setting that is external to the model and whose value can't be estimated from the data. Instead, a hyperparameter's value must be set by the developer.
[^9]: A *confusion matrix* is a table used to evaluate the performance of a classification model on a set of test data for which the true values are known. It visually summarizes the classifier's performance by comparing the predicted categories to the actual categories.
[^10]: A *bigram* is an *n-gram* sequence of two words or characters, for example: "my husband" or "qu".
[^11]: *Cross-validation* is a resampling method that repeatedly splits the data into separate ‘train’ and ‘test’ subsets so model performance can be evaluated on unseen data.
