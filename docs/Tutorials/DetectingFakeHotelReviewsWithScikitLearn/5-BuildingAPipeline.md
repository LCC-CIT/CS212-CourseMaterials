## Building a Pipeline

In order to make the vectorizer => transformer => classifier easier to work with, `scikit-learn` provides a <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.pipeline.Pipeline.html#sklearn.pipeline.Pipeline" target="_blank">`Pipeline`</a> class that behaves like a compound classifier:

```python
from sklearn.pipeline import Pipeline
text_clf = Pipeline([
   ('vect', CountVectorizer()),
   ('tfidf', TfidfTransformer()),
   ('clf', MultinomialNB()),
 ])
```

The names `vect`, `tfidf` and `clf` (classifier) are arbitrary. We will use them to perform grid search for suitable hyperparameters[^8] below. We can now train the entire three-step model with a single command:

```python
text_clf.fit(reviews_train, labels_train)
```

When you call `text_clf.fit(...)`, the pipeline automatically calls `fit_transform` on `vect` and `tfidf`, and then calls `fit` on `clf`. When you call `text_clf.predict(...)`, it automatically calls **only** `transform` on `vect` and `tfidf` before calling `predict` on `clf`—preventing data leakage automatically.

**Note:** In scikit-learn 1.7 and later, when you display pipeline objects in Jupyter notebooks, you'll see enhanced HTML representations with comprehensive parameter information and a copy button for easy configuration.

**Estimators and hyperparameters used in the pipeline:**

Each of the estimators in the `text_clf` pipeline has hyperparameters that have default values but can also be set to new values. In our example we are using the default values. Here is one key hyperparameter for each:

- CountVectorizer (`vect`). 
  *ngram_range* is a tuple (min, max) that specifies the minimum and maximum lengths of contiguous word sequences (N-grams) to be extracted as features (tokens). The default is (1, 1).
- TfidfTransformer (`tfidf`).   
  *use_idf* is set to True or False to determine whether the Inverse Document Frequency calculation is used. The default is True.
- MultinomialNB (`clf`)  
  *alpha* is the smoothing parameter. This small value is added to all counts to prevent zero probabilities when a word hasn't been seen in a class. The default value is 1.0.



---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
