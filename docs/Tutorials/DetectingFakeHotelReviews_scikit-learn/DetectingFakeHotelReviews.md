<h1>Detecting Fake Hotel Reviews with Text Classification</h1>

[TOC]

The goal of this guide is to explore the main `scikit-learn` text processing tools on a single practical task: analyzing a collection of hotel reviews to detect whether each review is **truthful** (real) or **deceptive** (fake). Unlike topic classification—where specific subject nouns like `"gpu"` or `"atheism"` reveal the category—deception detection requires recognizing subtle stylistic patterns, pronoun usage, and hyperbolic phrasing.

In this section we will see how to:

- Load the review text and labels from a CSV file and split them into training and test sets.
- Extract numerical feature vectors suitable for machine learning while avoiding *data leakage*[^12].
- Train probabilistic (Naïve Bayes) and linear (Support Vector Machine) models to perform classification.
- Interpret model decisions by inspecting feature weights and confusion matrices.
- Use a grid search strategy to find a good configuration of both the feature extraction components and the classifier.

## Tutorial setup

To get started with this tutorial, create a virtual environment and install KaggleHub, NumPy, and scikit-learn. Run these commands from the tutorial folder:

```bash
uv venv --python 3.14
uv pip install kagglehub numpy scikit-learn
# Activate the venv using commands for your os and shell
```

In VS Code, select the `.venv` environment as the Python interpreter.


### Loading the Deceptive Opinion Spam dataset

The dataset is called the “Deceptive Opinion Spam Corpus”, originally collected by Myle Ott et al. at Cornell University. Here is a description of the collection:

> The Deceptive Opinion Spam Corpus consists of 1,600 hotel reviews for 20 of the most popular hotels in Chicago. Half of the reviews (800) are **truthful** opinions scraped from verified customer reviews on TripAdvisor, and the other half (800) are **deceptive** (fake) opinions written by human workers on Amazon Mechanical Turk who were instructed to write convincing fake reviews for hotels they had never actually visited.

The corpus is not included with scikit-learn. Download it from [Kaggle](https://www.kaggle.com/datasets/rtatman/deceptive-opinion-spam-corpus) using KaggleHub:

```python
import kagglehub

# Download the latest version into the tutorial's data folder
path = kagglehub.dataset_download(
    "rtatman/deceptive-opinion-spam-corpus",
    output_dir="data/hotel_reviews"
)

print("Path to dataset files:", path)
```

Because the fake reviews were written by humans trying to sound persuasive rather than by simple bots, human judges perform barely better than a coin flip (around 55%–60% accuracy) when trying to spot the fakes. However, statistical machine learning models can detect recurring psycholinguistic cues that humans miss.

The downloaded dataset contains one CSV file, `deceptive-opinion.csv`, with the review text in the `text` column and the label (`deceptive` or `truthful`) in the `deceptive` column. We will read it with Python's built-in `csv` module and split the reviews and labels into training and test sets. The `stratify` setting keeps the proportion of each label about the same in both sets:

```python
import csv
from sklearn.model_selection import train_test_split

reviews = []
labels = []
with open('data/hotel_reviews/deceptive-opinion.csv',
          encoding='utf-8', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        reviews.append(row['text'])
        labels.append(row['deceptive'])

reviews_train, reviews_test, labels_train, labels_test = train_test_split(
    reviews,
    labels,
    test_size=0.2,
    random_state=42,
    stratify=labels)

target_names = ['deceptive', 'truthful']
```

This creates an 80% training set and a 20% test set. We will use the training set to fit our models and hold the test set aside until we evaluate them.

#### Exploring the Data

Now that the reviews are in `reviews_train`, let's explore the training data. (This isn't part of the training process—it's just to help you understand the dataset.)

```python
print(len(reviews_train))
```

Let's print the first 3 reviews with their labels

```python
for i in range(3):
    print(labels_train[i], "-", reviews_train[i][:100])
```

Research shows that truthful reviewers naturally include concrete **spatial and verifiable details** (floors, prices, bathroom layouts), whereas deceptive reviewers—who haven't visited the hotel—compensate by using more **first-person pronouns** (`"I"`, `"my"`, `"we"`), **emotional superlatives** (`"amazing"`, `"luxurious"`), and **generalized narratives** (`"my husband and I"`, `"vacation"`).

Supervised learning algorithms require a category label for each review. In this case, we store the label (`deceptive` or `truthful`) in the `labels_train` list.

Here are the first ten labels:

```python
labels_train[:10]
```

You can also print them one at a time:

```python
for label in labels_train[:10]:
    print(label)
```

`train_test_split` shuffles the rows by default.

## Building Feature Vectors and Training

### Extracting features from review text

In order to perform machine learning on text documents, we first need to turn the text content into *numerical* *feature vectors*[^4].

#### Bags of words and N-grams

The most intuitive way to do so is to use a "bag of words" representation:

1. Assign a fixed integer id to each word occurring in any document of the training set (for instance, by building a dictionary from words to integer indices).
2. For each document `i`, count how many times each word `w` occurs and store the count in `X[i, j]`, where `i` is the document's row number and `j` is the column number for word `w` in the dictionary.

It is called a "bag" of words because the order of words in a sentence is discarded—only their occurrence counts are kept. However, if we also extract **N-grams**[^5] (contiguous sequences of 2 or 3 words, such as `"my husband"` or `"front desk"`), we can preserve local word order and capture multi-word stylistic phrases.

The bag of words representation implies that `n_features` is the number of distinct words in the corpus: across large text collections, this number is typically larger than 100,000.

If `n_samples == 10000`, storing `X` as a standard NumPy array of type `float32` would require 10000 x 100000 x 4 bytes = 4GB in RAM which is a lot for the average consumer computer.

Fortunately, <u>most values in `X` will be zeros</u> since for a given hotel review only a hundred or so distinct words will be used. For this reason we say that bags of words are typically *high-dimensional sparse* datasets. We can save a lot of memory by only storing the non-zero parts of the feature vectors in memory.

`scipy.sparse` matrices are data structures that do exactly this, and `scikit-learn` has built-in support for these structures. 

#### Tokenize the Text and Build Feature Vectors

Text preprocessing[^1], tokenizing[^2] and filtering (removal) of stopwords[^3] are all included in <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a>, which:

- Builds a dictionary of features in which each unique token (word) found across all training documents is assigned a specific index (a column number in the resulting matrix).
- Transforms documents to feature vectors[^4]. Each document is transformed into a vector (a row in the matrix) where the value at each position corresponds to the count (*frequency*) of a specific word (*feature*) from the dictionary in that document.

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

<a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a> supports counts of words (or *N-grams*[^5] of words or consecutive characters). Once fitted, our vectorizer object will have built a dictionary of feature indices:

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

**Note:** In scikit-learn 1.7, when you display pipeline objects in Jupyter notebooks, you'll see enhanced HTML representations with comprehensive parameter information and a copy button for easy configuration.

**Estimators and hyperparameters used in the pipeline:**

Each of the estimators in the `text_clf` pipeline has hyperparameters that have default values but can also be set to new values. In our example we are using the default values. Here is one key hyperparameter for each:

- CountVectorizer (`vect`). 
  *ngram_range* is a tuple (min, max) that specifies the minimum and maximum lengths of contiguous word sequences (N-grams) to be extracted as features (tokens). The default is (1, 1).
- TfidfTransformer (`tfidf`).   
  *use_idf* is set to True or False to determine whether the Inverse Document Frequency calculation is used. The default is True.
- MultinomialNB (`clf`)  
  *alpha* is the smoothing parameter. This small value is added to all counts to prevent zero probabilities when a word hasn't been seen in a class. The default value is 1.0.

## Testing Classification Accuracy

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

## Parameter Tuning Using Grid Search

We’ve already encountered some parameters such as `use_idf` in the `TfidfTransformer`. Classifiers tend to have many parameters as well; e.g., `MultinomialNB` includes a smoothing parameter `alpha` and `SGDClassifier` has a regularization penalty parameter `alpha` (which controls how strongly the model penalizes large weights to prevent overfitting).

Instead of tweaking the parameters of the various components of the chain manually, it is possible to run an exhaustive search of the best parameters on a grid of possible values. We try out our classifier on either single words or *bigrams*[^10] (such as `"my husband"` or `"front desk"`), with or without *idf*, and with a penalty parameter of either 0.001 or 0.0001 for the linear SVM. Each key is the pipeline step name, two underscores, and the parameter name:

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
- `cv`: Determines the *cross-validation*[^11] splitting strategy. `cv=5` splits the training data into 5 equal folds, training on 4 folds and validating on the 5th fold repeatedly so the test set remains completely untouched during tuning.

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



<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

*This tutorial was drafted by Gemini 4.0 Argon and revised by Brian Bird*

[^1]: *Text preprocessing* is the initial set of steps to clean and standardize raw text data before analysis. This often includes converting all text to lowercase, removing punctuation, and handling special characters to ensure consistency. ↩
[^2]: *Tokenizing* is the process of breaking down a text document into smaller units called *tokens*. Tokens are usually words, but can also be individual characters or parts of words.
[^3]: *Stopwords* are common words (like "the," "a," "is," "my," "and," "of") that often don't carry topic meaning, though in deception detection they provide useful stylistic clues. (`CountVectorizer` only removes them if you set its `stop_words` parameter; by default it keeps them.)
[^4]: A *feature vector* in the context of scikit-learn is a one-dimensional array of numerical values that represents a single data point (or sample) to be used by a machine learning algorithm.
[^5]: An *n-gram* is a contiguous sequence of N characters or words from a given sample of text.
[^6]: *Estimators* are objects in scikit-learn that can learn parameters from data by implementing a `.fit()` method. These include: *Predictors* (Models): like `MultinomialNB` or `LinearRegression` and *Transformers* (Preprocessing Tools) like `CountVectorizer` or `StandardScaler` that learn rules to transform or process data.
[^7]: *Multinomial* in this context means the classifier models each document's word counts with a *multinomial distribution*: for each category, it learns how often each word in the vocabulary tends to appear, and it predicts the category whose word frequencies best match the document.
[^8]: *Hyperparameter* refers to a configuration setting that is external to the model and whose value can't be estimated from the data. Instead, a hyperparameter's value must be set by the developer.
[^9]: A *confusion matrix* is a table used to evaluate the performance of a classification model on a set of test data for which the true values are known. It visually summarizes the classifier's performance by comparing the predicted categories to the actual categories.
[^10]: A *bigram* is an *n-gram* sequence of two words or characters, for example: "my husband" or "qu".
[^11]: *Cross-validation* is a resampling method that repeatedly splits the data into separate ‘train’ and ‘test’ subsets so model performance can be evaluated on unseen data.
