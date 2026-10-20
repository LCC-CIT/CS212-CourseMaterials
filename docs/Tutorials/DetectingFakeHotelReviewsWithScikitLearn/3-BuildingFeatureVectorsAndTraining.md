---
title: Building Feature Vectors and Training the Model
---

## Building Feature Vectors and Training

### Extracting features from review text

In order to perform machine learning on text documents, we first need to turn the text content into *numerical* *feature vectors*[^1].

#### Bags of words and N-grams

The most intuitive way to do so is to use a "bag of words" representation:

1. Assign a fixed integer id to each word occurring in any document of the training set (for instance, by building a dictionary from words to integer indices).
2. For each document `i`, count how many times each word `w` occurs and store the count in `X[i, j]`, where `i` is the document's row number and `j` is the column number for word `w` in the dictionary.

It is called a "bag" of words because the order of words in a sentence is discarded—only their occurrence counts are kept. However, if we also extract **N-grams**[^2] (contiguous sequences of 2 or 3 words, such as `"my husband"` or `"front desk"`), we can preserve local word order and capture multi-word stylistic phrases.

The bag of words representation implies that `n_features` is the number of distinct words in the corpus: across large text collections, this number is typically larger than 100,000.

If `n_samples == 10000`, storing `X` as a standard NumPy array of type `float32` would require 10000 x 100000 x 4 bytes = 4GB in RAM which is a lot for the average consumer computer.

Fortunately, <u>most values in `X` will be zeros</u> since for a given hotel review only a hundred or so distinct words will be used. For this reason we say that bags of words are typically *high-dimensional sparse* datasets. We can save a lot of memory by only storing the non-zero parts of the feature vectors in memory.

`scipy.sparse` matrices are data structures that do exactly this, and `scikit-learn` has built-in support for these structures. 

#### Tokenize the Text and Build Feature Vectors

Text preprocessing[^3], tokenizing[^4] and filtering (removal) of stopwords[^5] are all included in <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a>, which:

- Builds a dictionary of features in which each unique token (word) found across all training documents is assigned a specific index (a column number in the resulting matrix).
- Transforms documents to feature vectors[^1]. Each document is transformed into a vector (a row in the matrix) where the value at each position corresponds to the count (*frequency*) of a specific word (*feature*) from the dictionary in that document.

**Concept — Why keep stopwords for fake review detection?**  
In topic classification, common words like `"i"`, `"my"`, `"we"`, and `"the"` are often removed as noise. In deception detection, however, psycholinguistic studies show that **pronouns and function words are strong signals of deception** (fake reviewers use significantly more first-person pronouns to make their stories sound personal). By default, `CountVectorizer()` keeps stopwords (`stop_words=None`), which is ideal for our task.

This code does all that:

```python
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(reviews_train)
```

##### Code Explanation

- `from sklearn.feature_extraction.text import CountVectorizer`
  Imports the `CountVectorizer` class from the scikit-learn library. `CountVectorizer` is a feature extractor.
- `count_vect = CountVectorizer()`
  Creates an instance of the `CountVectorizer`. This object holds the logic for the entire text-to-numerical conversion process. It doesn't have a vocabulary yet; it learns one in the next step.
- `X_train_counts = count_vect.fit_transform(reviews_train)`
  This is the main operation, which performs two main steps: `fit` and *`transform`*
  - *fit*: the vectorizer learns from the input text data (`reviews_train`) by scanning all the documents to identify every unique word, performing text preprocessing and tokenizing in the process. This builds an internal dictionary of features.
  - *transform*: The vectorizer then uses the internal dictionary of features to convert the text documents into a numerical matrix. Each document is converted into a *feature vector* (a row) where the values are the counts of each word in the dictionary. The resulting feature vector matrix, `X_train_counts`, is the numerical representation of the training data.

##### Explore the Feature Vector Matrix

The feature vectors are now stored in `X_train_counts` which is a scipy sparse matrix. Let's take a look at it. It has one row for each training review and one column for each word in the vocabulary.

```python
print(X_train_counts)
```

The first number is the number of training reviews. The second is the number of unique word features and can vary with the training data.

<a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a> supports counts of words (or *N-grams*[^2] of words or consecutive characters). Once fitted, our vectorizer object will have built a dictionary of feature indices:

```python
count_vect.vocabulary_.get('chicago')
```

- `count_vect` is the `CountVectorizer` object we fitted to `reviews_train`.
- `.vocabulary_` is an attribute that holds a dictionary mapping terms to feature indices. (Words are the keys and the values are column indices in the feature matrix, `X_train_counts`.)
- `.get('chicago')` gets the column index for the word `"chicago"`. It is *not* a count; the counts for that word are stored in that column of `X_train_counts`, one per document.

#### Transform Occurrence Counts to Frequencies

The values in `X_train_counts` are the number of times each word occurs in each document. Occurrence count is a good start but there are two issues:

1. **Document length discrepancy:** Longer reviews will have higher average count values than shorter reviews, even though they might share the same writing style and authenticity.
2. **Ubiquitous domain words:** Words like `"hotel"`, `"room"`, and `"stay"` appear in almost every review—both truthful and deceptive—so high counts for those words provide very little informative signal.

We can avoid the first discrepancy by dividing the number of occurrences of each unique word in a document by the total number of words in the document: these new features are called `tf` for *Term Frequencies*. (By default, scikit-learn actually scales each document's row of counts to a length of 1 using L2 normalization instead, which has the same effect of making long and short reviews comparable.)

##### Calculating Term Frequency

The scipy sparse matrix of *term frequencies* can be computed using <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer" target="_blank">`TfidfTransformer`</a>. (Run this code to see term frequencies. It's an intermediate step, so we won't use `X_train_tf` later.)

```python
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape
```

In the above code, we first used the `fit(..)` method to fit our estimator[^6] to the data and then the `transform(..)` method to transform our count matrix to a `tf` representation. 

##### Calculating Term Frequency and Inverse Document Frequency

Another refinement on top of `tf` solves our second issue: giving a lower weight to ubiquitous words (like `"hotel"`) that occur across many documents in the corpus and are therefore less informative than distinctive words (like `"priceline"`, `"elevator"`, or `"luxurious"`) that occur only in a smaller portion of the corpus.

This weight reduction is called <a href="https://en.wikipedia.org/wiki/Tf-idf" target="_blank">tf–idf</a> for “*Term Frequency* times *Inverse Document Frequency*”:

$$\text{tfidf}(t, d) = \text{tf}(t, d) \times \left(\ln\frac{1 + n}{1 + \text{df}(t)} + 1\right)$$

where $n$ is the total number of training documents and $\text{df}(t)$ is the number of training documents containing term $t$. The fit and transform steps can be combined into one call using the `fit_transform(..)` method, as shown below:

```python
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape
```

`X_train_tfidf` is the scipy sparse matrix containing the new feature vectors.

### Training a classifier

Now that we have our features in `X_train_tfidf`, we can train a classifier to try to predict whether a review is truthful or deceptive. Let's start with a <a href="https://scikit-learn.org/1.7/modules/naive_bayes.html#naive-bayes" target="_blank">naïve Bayes</a> classifier, which provides a nice baseline for this task. `scikit-learn` includes several variants of this classifier, and the one most suitable for word counts and TF-IDF weights is the *multinomial*[^7] variant:

```python
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, labels_train)
```

**How `MultinomialNB` learns:** For each class (`deceptive` and `truthful`), the classifier estimates the conditional probability $P(w \mid \text{class})$ of every word $w$ in the vocabulary based on its TF-IDF weights in `X_train_tfidf`. When given a new review, it multiplies the probabilities of the words present in that review to determine which class is most likely.

### Making Predictions

To try to predict the outcome on a new review we need to extract the features using almost the same feature extracting chain as before. The difference is that we call `transform` instead of `fit_transform` on the transformers, since they have already been fit to the training set (any brand-new words not seen during training are safely ignored):

```python
docs_new = [
    'Room 812 on the 8th floor had a small bathroom and street noise, '
    'but the $145 AAA rate and 2 block walk to the L train made it worth it.',
    'My husband and I had the most amazing magical stay at this luxurious hotel! '
    'Everything was wonderful and I would definitely recommend it to everyone!'
]
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc[:55] + '...', category))
```

The predicted labels can vary depending on the training data and split.

**Explanation:**

- `docs_new = [...]`
  Creates a list of new hotel review strings that the classifier will attempt to categorize.

- `X_new_counts = count_vect.transform(docs_new)`
  Tokenizes the new reviews and converts them into a feature matrix of word counts. It uses the 8,432-word vocabulary that the `count_vect` object learned from the training data.

- `X_new_tfidf = tfidf_transformer.transform(X_new_counts)`
  Converts the new count matrix into a normalized *Term Frequency* times *Inverse Document Frequency* representation using the IDF weights learned from the training data.

- `predicted = clf.predict(X_new_tfidf)`
  **The prediction happens here!** The previously trained classifier *predicts* a category label (`truthful` or `deceptive`) for each of the new reviews. Which label it predicts can vary with the training data and split.

- `for doc, category in zip(docs_new, predicted):`
  Starts a loop to iterate through the original new review strings and their corresponding predicted category labels.

- `print('%r => %s' % (doc[:55] + '...', category))`
  **Prints the result** by showing the first 55 characters of the review string followed by the predicted category label (`truthful` or `deceptive`).


---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---

[^1]: A *feature vector* in the context of scikit-learn is a one-dimensional array of numerical values that represents a single data point (or sample) to be used by a machine learning algorithm.
[^2]: An *n-gram* is a contiguous sequence of N characters or words from a given sample of text.
[^3]: *Text preprocessing* is the initial set of steps to clean and standardize raw text data before analysis. This often includes converting all text to lowercase, removing punctuation, and handling special characters to ensure consistency.
[^4]: *Tokenizing* is the process of breaking down a text document into smaller units called *tokens*. Tokens are usually words, but can also be individual characters or parts of words.
[^5]: *Stopwords* are common words (like "the," "a," "is," "my," "and," "of") that often don't carry topic meaning, though in deception detection they provide useful stylistic clues. (`CountVectorizer` only removes them if you set its `stop_words` parameter; by default it keeps them.)
[^6]: *Estimators* are objects in scikit-learn that can learn parameters from data by implementing a `.fit()` method. These include: *Predictors* (Models): like `MultinomialNB` or `LinearRegression` and *Transformers* (Preprocessing Tools) like `CountVectorizer` or `StandardScaler` that learn rules to transform or process data.
[^7]: *Multinomial* in this context means the classifier models each document's word counts with a *multinomial distribution*: for each category, it learns how often each word in the vocabulary tends to appear, and it predicts the category whose word frequencies best match the document.
