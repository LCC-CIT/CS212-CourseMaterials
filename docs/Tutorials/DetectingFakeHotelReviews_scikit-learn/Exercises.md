## Exercises

### Setup for All the Exercises

For each exercise, start with the KaggleHub download, CSV-loading, and train/test-splitting code from this tutorial. Use the same `reviews_train`, `labels_train`, `reviews_test`, and `labels_test` lists so you can compare your models on the same held-out test data.

### Exercise 1: Stylometry and Stopwords

In topic classification, removing English stopwords (`stop_words='english'`) often reduces noise. In this exercise, you will test whether removing stopwords helps or hurts when detecting deceptive hotel reviews.

- Write a text classification pipeline using `CountVectorizer(stop_words='english')`, `TfidfTransformer`, and `SGDClassifier`, and compare its test set accuracy against the default `CountVectorizer(stop_words=None)`.
- Inspect the top 10 deceptive words of both models using `np.argsort` and explain why pronouns and function words matter in deception detection.

#### Hints

- Setting up a vectorizer that strips English stopwords:

  ```python
  vectorizer = CountVectorizer(
      stop_words='english',  # Remove common English function words and pronouns
      ngram_range=(1, 1)
  )
  ```

### Exercise 2: Incorporating Character and Word N-grams

In this exercise, you will explore whether character N-grams or multi-word phrases (bigrams and trigrams) better capture the formulaic writing style of fake reviewers.

- Write a text classification pipeline using `TfidfVectorizer` and `SGDClassifier`.
- Use `GridSearchCV` to compare word N-grams (`analyzer='word'`, `ngram_range=(1, 3)`) against character N-grams within word boundaries (`analyzer='char_wb'`, `ngram_range=(3, 5)`).
- Evaluate the winning model on the held-out test set (`reviews_test`).

### Exercise 3: CLI fake review detector utility

Using the results of the previous exercises and the `pickle` module of the standard library, write a command line utility that reads a hotel review provided on `stdin` and predicts whether the review is `'truthful'` or `'deceptive'`.

Bonus point if the utility is able to give a confidence level for its predictions (hint: use `loss='log_loss'` in `SGDClassifier` or use `MultinomialNB` to enable `.predict_proba()`).