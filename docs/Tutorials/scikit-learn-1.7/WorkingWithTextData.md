[scikit-learn tutorials index](ScikitLearnTutorials.md)

<h1>Working With Text Data</h1>

- [Tutorial setup](#tutorial-setup)
  - [Loading the 20 newsgroups dataset](#loading-the-20-newsgroups-dataset)
    - [Exploring the Data](#exploring-the-data)
- [Building Feature Vectors and Training](#building-feature-vectors-and-training)
  - [Extracting features from text files](#extracting-features-from-text-files)
    - [Bags of words](#bags-of-words)
    - [Tokenize the Text and Build Feature Vectors](#tokenize-the-text-and-build-feature-vectors)
      - [Code Explanation](#code-explanation)
      - [Explore the Feature Vector Matrix](#explore-the-feature-vector-matrix)
    - [Transform Occurrence Counts to Frequencies](#transform-occurrence-counts-to-frequencies)
      - [Calculating Term Frequency](#calculating-term-frequency)
      - [Calculating Term Frequency and Inverse Document Frequency](#calculating-term-frequency-and-inverse-document-frequency)
  - [Training a classifier](#training-a-classifier)
  - [Making Predictions](#making-predictions)
- [Building a Pipeline](#building-a-pipeline)
- [Testing Classification Accuracy](#testing-classification-accuracy)
  - [Train and Test a Support Vector Machine](#train-and-test-a-support-vector-machine)
    - [Classification Report](#classification-report)
    - [Confusion Matrix](#confusion-matrix)
- [Parameter Tuning Using Grid Search](#parameter-tuning-using-grid-search)
- [Exercises](#exercises)
  - [Setup for All the Exercises](#setup-for-all-the-exercises)
  - [Exercise 1: Language identification](#exercise-1-language-identification)
    - [Hints](#hints)
  - [Exercise 2: Sentiment Analysis on movie reviews](#exercise-2-sentiment-analysis-on-movie-reviews)
  - [Exercise 3: CLI text classification utility](#exercise-3-cli-text-classification-utility)
  - [Where to from here](#where-to-from-here)
- [What's New in scikit-learn 1.7 for Text Processing](#whats-new-in-scikit-learn-17-for-text-processing)

The goal of this guide is to explore some of the main `scikit-learn` tools on a single practical task: analyzing a collection of text documents (newsgroups posts) on twenty different topics.

In this section we will see how to:

- Load the file contents and the categories.
- Extract feature vectors suitable for machine learning.
- Train a linear model to perform categorization.
- Use a grid search strategy to find a good configuration of both the feature extraction components and the classifier.

## Tutorial setup

To get started with this tutorial, you must first install *scikit-learn* and all of its required dependencies.

Please refer to the <a href="https://scikit-learn.org/1.7/install.html#installation-instructions" target="_blank">installation instructions</a> page for more information and for system-specific instructions. (Note: this tutorial was updated for scikit-learn 1.7, but has been tested with 1.6 through 1.9.)

### Loading the 20 newsgroups dataset

The dataset is called “Twenty Newsgroups”. Here is the official description, quoted from the <a href="http://qwone.com/~jason/20Newsgroups/" target="_blank">website</a>:

> The 20 Newsgroups data set is a collection of approximately 20,000 newsgroup documents, partitioned (nearly) evenly across 20 different newsgroups. To the best of our knowledge, it was originally collected by Ken Lang, probably for his paper "<a href="http://qwone.com/~jason/20Newsgroups/lang95.bib" target="_blank">Newsweeder: Learning to filter netnews</a>", though he does not explicitly mention this collection. The 20 newsgroups collection has become a popular data set for experiments in text applications of machine learning techniques, such as text classification and text clustering.

In the following we will use the built-in dataset loader for 20 newsgroups from scikit-learn. Alternatively, it is possible to download the dataset manually from the website and use the <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.datasets.load_files.html#sklearn.datasets.load_files" target="_blank">`sklearn.datasets.load_files`</a> function by pointing it to the `20news-bydate-train` sub-folder of the uncompressed archive folder.

In order to get faster execution times for this first example, we will work on a partial dataset with only 4 categories out of the 20 available in the dataset:

```python
categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
```

We can now load the list of files matching those categories as follows:
***(This will take a minute or more to load.)***

```python
from sklearn.datasets import fetch_20newsgroups
twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=42)
```

#### Exploring the Data

Now that the 4 newsgroups are loaded into `twenty_train` (note that it's just the four specified in `categories`, not twenty), let's explore the dataset. (This isn't part of the training process&mdash; it's just to help you understand the dataset.)

The returned dataset is a `scikit-learn` “bunch”: a simple holder object with fields that can be both accessed as python `dict` keys or `object` attributes for convenience, for instance the `target_names` holds the list of the requested category names:

```python
twenty_train.target_names
```
> *response:*  
>['alt.atheism', 'comp.graphics', 'sci.med', 'soc.religion.christian']

The files themselves are loaded in memory in the `data` attribute. For reference the filenames are also available:

```python
print(len(twenty_train.data))
print(len(twenty_train.filenames))
```

> *response:*  
> 2257
> 2257

Let’s print the first lines of the first loaded file:

```python
print("\n".join(twenty_train.data[0].split("\n")[:3]))
```
>*response:*  
>From: sd345@city.ac.uk (Michael Collier)
>Subject: Converting images to HP LaserJet III?
>Nntp-Posting-Host: hampton

```python
print(twenty_train.target_names[twenty_train.target[0]])
```
>*response:*
>comp.graphics

Supervised learning algorithms will require a category label for each document in the training set. In this case the category is the name of the newsgroup which also happens to be the name of the folder holding the individual documents.

For speed and space efficiency reasons, `scikit-learn` loads the target attribute as an array of integers that correspond to the index of the category name in the `target_names` list. The category integer id of each sample is stored in the `target` attribute:

```python
twenty_train.target[:10]
```

> *response:*  
> array([1, 1, 3, 3, 3, 3, 3, 2, 2, 2])

It is possible to get back the category names as follows:

```python
for t in twenty_train.target[:10]:
    print(twenty_train.target_names[t])
```

> *response:*  
> comp.graphics
> comp.graphics
> soc.religion.christian
> soc.religion.christian
> soc.religion.christian
> soc.religion.christian
> soc.religion.christian
> sci.med
> sci.med
> sci.med

You might have noticed that the samples were shuffled randomly when we called `fetch_20newsgroups(..., shuffle=True, random_state=42)`: this is useful if you wish to select only a subset of samples to quickly train a model and get a first idea of the results before re-training on the complete dataset later.

## Building Feature Vectors and Training

### Extracting features from text files

In order to perform machine learning on text documents, we first need to turn the text content into *numerical* *feature vectors*.

#### Bags of words

The most intuitive way to do so is to use a "bags of words" representation:

1. Assign a fixed integer id to each word occurring in any document of the training set (for instance, by building a dictionary from words to integer indices).
2. For each document `#i`, count the number of occurrences of each word `w` and store it in `X[i, j]` as the value of feature `#j` where `j` is the index of word `w` in the dictionary.

The bags of words representation implies that `n_features` is the number of distinct words in the corpus: this number is typically larger than 100,000.

If `n_samples == 10000`, storing `X` as a NumPy array of type float32 would require 10000 x 100000 x 4 bytes = 4GB in RAM which is a lot for the average consumer computer.

Fortunately, <u>most values in `X` will be zeros</u> since for a given document less than a few thousand distinct words will be used. For this reason we say that bags of words are typically *high-dimensional sparse* datasets. We can save a lot of memory by only storing the non-zero parts of the feature vectors in memory.

`scipy.sparse` matrices are data structures that do exactly this, and `scikit-learn` has built-in support for these structures. 

**Note:** In scikit-learn 1.7, all text processing estimators now also accept the new sparse arrays (`sparray`) in addition to traditional sparse matrices, ensuring compatibility with future versions of SciPy as it transitions from sparse matrices to sparse arrays.

#### Tokenize the Text and Build Feature Vectors

Text preprocessing[^1], tokenizing[^2] and filtering (removal) of stopwords[^3] are all included in <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a>, which:

- Builds a dictionary of features in which each unique token (word) found across all documents is assigned a specific index (a column number in the resulting matrix).
-  Transforms documents to feature vectors[^4]. Each document is transformed into a vector (a row in the matrix) where the value at each position corresponds to the count (*frequency*) of a specific word (*feature*) from the dictionary in that document.

This code does all that:

```python
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(twenty_train.data)
```

##### Code Explanation

- `from sklearn.feature_extraction.text import CountVectorizer`
  Imports the `CountVectorizer` class from the scikit-learn library. `CountVectorizer` is a feature extractor.
- `count_vect = CountVectorizer()`
  Creates an instance of the `CountVectorizer`. This object holds the logic for the entire text-to-numerical conversion process. It doesn't have a vocabulary yet; it learns one in the next step.
- `X_train_counts = count_vect.fit_transform(twenty_train.data)`
  This is the main operation, which performs two main steps: `fit` and *`transform`*
  - *fit*: the vectorizer learns from the input text data (`twenty_train.data`) by scanning all the documents to identify every unique word, performing text preprocessing and tokenizing in the process. This builds an internal dictionary of features.
  - *transform*: The vectorizer then uses the internal dictionary of features to convert the text documents into a numerical matrix. Each document is converted into a *feature vector* (a row) where the values are the counts of each word in the dictionary. The resulting feature vector matrix, `X_train_counts`, is the numerical representation of the training data.

##### Explore the Feature Vector Matrix

The feature vectors are now stored in `X_train_counts` which is a scipy sparse matrix. Let's take a look at it. It has one row for each document and one column for each word in the vocabulary.

```python
X_train_counts.shape
```

> *response:*  
> (2257, 35788)

<a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a> supports counts of words (or *N-grams*[^5] of words or consecutive characters). Once fitted, our vectorizer object will have built a dictionary of feature indices:

```python
count_vect.vocabulary_.get('algorithm')
```

> *response*  
> 4690

- `count_vect` is the `CountVectorizer` object we fitted to `twenty_train`.
- `.vocabulary_` is an attribute that holds a dictionary mapping terms to feature indices. (Words are the keys and the values are column indices in the feature matrix, `X_train_counts`.)
- `.get('algorithm')` gets the column index for the word "algorithm". It is *not* a count; the counts for that word are stored in that column of `X_train_counts`, one per document.

#### Transform Occurrence Counts to Frequencies

The values in `X_train_counts` are the number of times each word occurs in each document. Occurrence count is a good start but there is an issue: longer documents will have higher average count values than shorter documents, even though they might be about the same topics.

We can avoid this potential discrepancy by dividing the number of occurrences of each unique word in a document by the total number of words in the document: these new features are called `tf` for *Term Frequencies*. (By default, scikit-learn actually scales each document's row of counts to a length of 1 instead, which has the same effect of making long and short documents comparable.)

##### Calculating Term Frequency

The scipy sparse matrix of *term frequencies* can be computed using <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.TfidfTransformer.html#sklearn.feature_extraction.text.TfidfTransformer" target="_blank">`TfidfTransformer`</a>. (This code is just an example; we won't use `X_train_tf` after this.)

```python
from sklearn.feature_extraction.text import TfidfTransformer
tf_transformer = TfidfTransformer(use_idf=False).fit(X_train_counts)
X_train_tf = tf_transformer.transform(X_train_counts)
X_train_tf.shape
```

> *response:*  
> (2257, 35788)

In the above example code, we first used the `fit(..)` method to fit our estimator[^6] to the data and then the `transform(..)` method to transform our count matrix to a `tf` representation. 

##### Calculating Term Frequency and Inverse Document Frequency

Another refinement on top of `tf` is to give a lower weight to words that occur across many documents in the corpus and are therefore less informative than those that occur only in a smaller portion of the corpus.

This weight reduction is called <a href="https://en.wikipedia.org/wiki/Tf-idf" target="_blank">tf–idf</a> for “*Term Frequency* times *Inverse Document Frequency*”. The fit and transform steps can be combined into one call using the `fit_transform(..)` method, as shown below:

```python
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
X_train_tfidf.shape
```

> *response:*  
> (2257, 35788)

`X_train_tfidf` is the scipy sparse matrix containing the new feature vectors.

### Training a classifier

Now that we have our features in `X_train_tfidf`, we can train a classifier to try to predict the category of a post. Let's start with a <a href="https://scikit-learn.org/1.7/modules/naive_bayes.html#naive-bayes" target="_blank">naïve Bayes</a> classifier, which provides a nice baseline for this task. `scikit-learn` includes several variants of this classifier, and the one most suitable for word counts is the *multinomial*[^7] variant:

```python
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
```

### Making Predictions

To try to predict the outcome on a new document we need to extract the features using almost the same feature extracting chain as before. The difference is that we call `transform` instead of `fit_transform` on the transformers, since they have already been fit to the training set:

```python
docs_new = ['God is love', 'OpenGL on the GPU is fast']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

predicted = clf.predict(X_new_tfidf)

for doc, category in zip(docs_new, predicted):
    print('%r => %s' % (doc, twenty_train.target_names[category]))
```

> *response:*  
> 'God is love' => soc.religion.christian
> 'OpenGL on the GPU is fast' => comp.graphics

**Explanation:**

- `docs_new = ['God is love', 'OpenGL on the GPU is fast']`
  Creates a list of new text documents that the classifier will attempt to categorize.

- `X_new_counts = count_vect.transform(docs_new)`
  Tokenizes the new documents and converts them into a feature matrix of word counts. It uses the vocabulary that the `count_vect` object learned from the training data.

- `X_new_tfidf = tfidf_transformer.transform(X_new_counts)`

  Converts the new count matrix into a normalized *Term Frequency* times *Inverse Document Frequency* representation.

- `predicted = clf.predict(X_new_tfidf)`

  **The prediction happens here!** The previously trained classifier *predicts* the category (topic) for each of the new documents.

- `for doc, category in zip(docs_new, predicted):`

  Starts a loop to iterate through the original new documents and their corresponding predicted category indices.

- `print('%r => %s' % (doc, twenty_train.target_names[category]))`

  **Prints the result** by showing the original document string (`doc`) followed by the category name, which is retrieved from the list of target names using the predicted numerical index (`category`).

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

The names `vect`, `tfidf` and `clf` (classifier) are arbitrary. We will use them to perform grid search for suitable hyperparameters[^8] below. We can now train the model with a single command:

```python
text_clf.fit(twenty_train.data, twenty_train.target)
```

> *response:*  
> Pipeline(steps=[('vect', CountVectorizer()), ('tfidf', TfidfTransformer()),
>                 ('clf', MultinomialNB())])

**Note:** In scikit-learn 1.7, when you display pipeline objects in Jupyter notebooks, you'll see enhanced HTML representations with comprehensive parameter information and a copy button for easy configuration.

**Estimators and hyperparameters used in the pipeline:**

Each of the estimators in the `text_clf` pipeline has hyperparameters that have default values but can also be set to new values. In our example we are using the default values. Here is one key hyperparameter for each:

- CountVectorizer (`vect`). 
  *ngram_range* is a tuple (min, max) that specifies the minimum and maximum lengths of contiguous word sequences (N-grams) to be extracted as features (tokens). The default is (1, 1).
- TfidfTransformer (`tfidf`).   
  *use_idf* is set to True or False to determine whether the Inverse Document Frequency calculation is used. The default is True.
- MultinomialNB (`clf`)  
  *alpha* is the smoothing parameter. This small value is added to all counts to prevent zero probabilities. The default value is 1.0.

## Testing Classification Accuracy

Evaluating the predictive accuracy of the model is equally easy. The newsgroup posts that `fetch_20newsgroups` loads are split into *training* and *test* sets. To evaluate the performance of the classifier we will use the test posts.

```python
import numpy as np
twenty_test = fetch_20newsgroups(subset='test',
    categories=categories, shuffle=True, random_state=42)
docs_test = twenty_test.data
predicted = text_clf.predict(docs_test)
np.mean(predicted == twenty_test.target)
```

> *response:*  
> np.float64(0.8348868175765646)

We achieved 83.5% accuracy. 

### Train and Test a Support Vector Machine

Let's see if we can do better with a linear <a href="https://scikit-learn.org/1.7/modules/svm.html#svm" target="_blank">support vector machine (SVM)</a>, which is widely regarded as one of the best text classification algorithms (although it's also a bit slower than naïve Bayes). We can change the learner by simply plugging a different classifier object into our pipeline. (`SGDClassifier` with `loss='hinge'` trains a linear SVM.)

```python
from sklearn.linear_model import SGDClassifier
text_clf = Pipeline([
    ('vect', CountVectorizer()),
    ('tfidf', TfidfTransformer()),
    ('clf', SGDClassifier(loss='hinge', penalty='l2',
                          alpha=1e-3, random_state=42,
                          max_iter=5, tol=None)),
 ])

text_clf.fit(twenty_train.data, twenty_train.target)
```

> *Response:*  
> Pipeline(...)

```python
predicted = text_clf.predict(docs_test)
np.mean(predicted == twenty_test.target)
```
> *Response:*  
> np.float64(0.9101198402130493)

We achieved 91.0% accuracy using the SVM.

#### Classification Report

 `scikit-learn` provides further utilities for more detailed performance analysis of the results:

```python
from sklearn import metrics
print(metrics.classification_report(twenty_test.target, predicted,
     target_names=twenty_test.target_names))
```

>*Response:*  
>                                      precision    recall  f1-score   support
>                    alt.atheism       0.95      0.80      0.87       319
>              comp.graphics       0.87      0.98      0.92       389
>                           sci.med       0.94      0.89      0.91       396
>  soc.religion.christian      0.90      0.95      0.93       398
>
>     ​                     accuracy                                  0.91     1502
>     ​                   macro avg      0.91      0.91      0.91     1502
>     ​             weighted avg       0.91      0.91      0.91      1502

The columns are showing the following:

- **Precision:** the ratio `tp / (tp + fp)` where `tp` is the number of *true positives* and `fp` the number of *false positives*. The precision is intuitively the ability of the classifier not to label a negative sample as positive.
- **Recall:** the ratio `tp / (tp + fn)` where `tp` is the number of true positives and `fn` the number of false negatives. The recall is intuitively the ability of the classifier to find all the positive samples.
- **F1-score:** A balance between precision and recall (the harmonic mean). 
- **Support:** the number of actual samples of each class in the test set.

#### Confusion Matrix

```python
metrics.confusion_matrix(twenty_test.target, predicted)
```
>*Response:*  
>array([
>    [256,  11,  16,  36],
>    [  4, 380,   3,   2],
>    [  5,  35, 353,   3],
>    [  5,  11,   4, 378]
>])

The  *confusion matrix*[^9] is arranged as follows:

- **Rows** represent the actual classes of the documents (the ground truth).
- **Columns** represent the predicted classes made by the classifier.
- The **diagonal** represents correct classifications: **TP** (True Positive) is the count of posts correctly classified as in a class.
- Every off-diagonal cell is a mistake, and it counts against two classes:
  - Across a row, it is a **FN** (False Negative) for that row's class: a post that belongs to the class was put in a different one.
  - Down a column, it is a **FP** (False Positive) for that column's class: a post was put in the class but doesn't belong there.

|                         | **Predicted Atheism** | **Predicted Graphics** | **Predicted Medical** | **Predicted Christianity** | **Total FN** |
| ----------------------- | --------------------- | ---------------------- | --------------------- | -------------------------- | ------------ |
| **Actual Atheism**      | **256** (TP)          | 11                     | 16                    | 36                         | 63           |
| **Actual Graphics**     | 4                     | **380** (TP)           | 3                     | 2                          | 9            |
| **Actual Medical**      | 5                     | 35                     | **353** (TP)          | 3                          | 43           |
| **Actual Christianity** | 5                     | 11                     | 4                     | **378** (TP)               | 20           |
| **Total FP**            | 14                    | 57                     | 23                    | 41                         |              |

As expected, this shows that posts from the newsgroups on atheism and Christianity are more often confused for one another than with computer graphics.

## Parameter Tuning Using Grid Search

We’ve already encountered some parameters such as `use_idf` in the `TfidfTransformer`. Classifiers tend to have many parameters as well; e.g., `MultinomialNB` includes a smoothing parameter `alpha` and `SGDClassifier` has a penalty parameter `alpha` and configurable loss and penalty terms in the objective function (see the module documentation, or use the Python `help` function to get a description of these).

Instead of tweaking the parameters of the various components of the chain, it is possible to run an exhaustive search of the best parameters on a grid of possible values. We try out all classifiers on either words or *bigrams*[^10], with or without *idf*, and with a penalty parameter of either 0.01 or 0.001 for the linear SVM. Each key is the pipeline step name, two underscores, and the parameter name:

```python
from sklearn.model_selection import GridSearchCV
parameters = {
     'vect__ngram_range': [(1, 1), (1, 2)],
     'tfidf__use_idf': (True, False),
     'clf__alpha': (1e-2, 1e-3),
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
- `cv`: Determines the *cross-validation*[^11] splitting strategy. `cv=5` splits the data into 5 parts.

The grid search instance behaves like a normal `scikit-learn` model.

Let’s perform the search on a smaller subset of the training data to speed up the computation:

```python
gs_clf = gs_clf.fit(twenty_train.data[:400], twenty_train.target[:400])
```

Calling `fit` on a `GridSearchCV` object returns a classifier that we can use to `predict`:

```python
twenty_train.target_names[gs_clf.predict(['God is love'])[0]]
```

> *Response:*  
> 'soc.religion.christian'

The object’s `best_score_` and `best_params_` attributes store the best mean score and the parameter settings corresponding to that score:

```python
gs_clf.best_score_
```
> *Response:*  
> np.float64(0.9175000000000001)

```python
for param_name in sorted(parameters.keys()):
    print("%s: %r" % (param_name, gs_clf.best_params_[param_name]))
```

> *Response:*  
> `clf__alpha: 0.001`  
> `tfidf__use_idf: True`  
> `vect__ngram_range: (1, 1)`

You can get a more detailed summary of the search from `gs_clf.cv_results_`.

The `cv_results_` attribute can be easily imported into pandas as a `DataFrame` for further inspection.

## Exercises

### Setup for All the Exercises

The source code for these exercises is <a href="https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Tutorials/scikit-learn-1.7/text_analytics" target="_blank">on GitHub</a>.

The tutorial folder on GitHub should contain the following sub-folders:

- `*.rst files` - the source of the tutorial document written with sphinx.
- `data` - folder to put the datasets used during the tutorial.
- `skeletons` - sample incomplete scripts for the exercises.
- `solutions` - solutions of the exercises.

Copy the skeletons folder into a new folder somewhere on your hard-drive named `sklearn_TextAnalyaticsTutorial`, where you can edit your own files for the exercises while keeping the original skeletons intact:

```python
cp -r skeletons your_path/sklearn_TextAnalyaticsTutorial
```

Machine learning algorithms need data. Go to each `sklearn_TextAnalyaticsTutorial` sub-folder and run the `fetch_data.py` script from there (after having read them first).

Note: `fetch_data.py` imports the `lxml` module for XML processing.  You will need to install that package with the command: `pip install lxml`.

Now run `fetch_data.py` in the languages and movie_reviews folders.

Then  run the work-in-progress script from `sklearn_TextAnalyaticsTutorial` with:

```python
python exercise_XX_script.py arg1 # arg1 is the training data folder
```

Or run the script in an IDE where you can edit and debug more easily.

Refine the implementation and iterate until the exercise is solved.

**For each exercise, the skeleton file provides all the necessary import statements and boilerplate code to load the data as well as sample code to evaluate the predictive accuracy of the model.**

### Exercise 1: Language identification

In this exercise, you will train a classifier to tell which language a piece of text is written in. The earlier sections of this tutorial used whole words as features. Here you will use short sequences of *characters* instead, because the letter patterns in a language, such as common pairs and triplets of letters, are a good clue to which language it is.

- Write a text classification pipeline using a custom preprocessor and `TfidfVectorizer` set up to use *character based* *n-grams*, using data from Wikipedia articles as the training set.
- Evaluate the performance on some held out test set.

#### Hints

- Setting up a vectorizer for a character instead of word sequence.  
  This code specifies *n-grams* of 1, 2, or 3 character sequences.

  ```python
  vectorizer = TfidfVectorizer(
      analyzer='char',      # Use individual characters as features
      ngram_range=(1, 3)    # Extract unigrams (1), bigrams (2), and trigrams (3)
  )
  ```

  

### Exercise 2: Sentiment Analysis on movie reviews

In this exercise, you will train a classifier to decide whether a movie review is positive or negative. It's a chance to use everything from this tutorial in one project: build a pipeline, use grid search to choose good parameters, and then check how well the result works on reviews it hasn't seen.

- Write a text classification pipeline to classify movie reviews as either positive or negative.
- Find a good set of parameters using grid search.
- Evaluate the performance on a held out test set.

### Exercise 3: CLI text classification utility

Using the results of the previous exercises and the `cPickle` module of the standard library, write a command line utility that detects the language of some text provided on `stdin` and estimate the polarity (positive or negative) if the text is written in English.

Bonus point if the utility is able to give a confidence level for its predictions.

### Where to from here

Here are a few suggestions to help further your scikit-learn intuition upon the completion of this tutorial:

- Try playing around with the `analyzer` and `token normalisation` under <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a>.
- If you don't have labels, try using <a href="https://scikit-learn.org/1.7/auto_examples/text/plot_document_clustering.html#sphx-glr-auto-examples-text-plot-document-clustering-py" target="_blank">Clustering</a> on your problem.
- If you have multiple labels per document, e.g. categories, have a look at the <a href="https://scikit-learn.org/1.7/modules/multiclass.html#multiclass" target="_blank">Multiclass and multilabel section</a>.
- Try using <a href="https://scikit-learn.org/1.7/modules/decomposition.html#lsa" target="_blank">Truncated SVD</a> for <a href="https://en.wikipedia.org/wiki/Latent_semantic_analysis" target="_blank">latent semantic analysis</a>.
- Have a look at using <a href="https://scikit-learn.org/1.7/auto_examples/applications/plot_out_of_core_classification.html#sphx-glr-auto-examples-applications-plot-out-of-core-classification-py" target="_blank">Out-of-core Classification</a> to learn from data that would not fit into the computer main memory.
- Have a look at the <a href="https://scikit-learn.org/1.7/modules/feature_extraction.html#hashing-vectorizer" target="_blank">Hashing Vectorizer</a> as a memory efficient alternative to <a href="https://scikit-learn.org/1.7/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html#sklearn.feature_extraction.text.CountVectorizer" target="_blank">`CountVectorizer`</a>.

## What's New in scikit-learn 1.7 for Text Processing

scikit-learn 1.7 introduces several enhancements that improve the text processing workflow:

- **Enhanced Estimator Visualization**: In Jupyter notebooks, estimators now display comprehensive parameter information with non-default parameters highlighted, and include a copy button for easy configuration of nested pipelines and hyperparameter searches.

- **Sparse Array Compatibility**: All text processing estimators now support both traditional `scipy.sparse` matrices and the new sparse arrays (`sparray`), ensuring future compatibility as SciPy transitions to sparse arrays.

- **Extended Array API Support**: Several metrics used in text classification now support Array API-compatible data structures from libraries like PyTorch or CuPy, with the `array-api-compat` module now natively integrated.

- **Improved Pipeline Configuration**: The enhanced HTML representation makes it easier to configure complex text processing pipelines with multiple transformers and classifiers.



---

This <a href="https://scikit-learn.org/1.4/tutorial/text_analytics/working_with_text_data.html" target="_blank">original version</a> of this tutorial was written by scikit-learn developers under a <a href="https://opensource.org/license/BSD-3-clause" target="_blank">BSD License</a>.  

The code examples and text were updated for scikit-learn version 1.7 by Brian Bird, 10/23/2025

Note: Claude Sonet 4 and Gemini Flash 2.5 were used to assist in drafting the revisions to this tutorial.

Claude Opus 5.5 was used to correct errors in this tutorial and convert it to a Jupyter notebook, 10/12/2026.

[^1]: *Text preprocessing* is the initial set of steps to clean and standardize raw text data before analysis. This often includes converting all text to lowercase, removing punctuation, and handling special characters to ensure consistency. ↩
[^2]: *Tokenizing* is the process of breaking down a text document into smaller units called *tokens*. Tokens are usually words, but can also be individual characters or parts of words.
[^3]: *Stopwords* are common words (like "the," "a," "is," "and," "of") that generally don't carry significant meaning for classification or analysis. Removing them helps reduce the size of the feature set and can improve model performance. (`CountVectorizer` only removes them if you set its `stop_words` parameter; by default it keeps them.)
[^4]: A *feature vector* in the context of scikit-learn is a one-dimensional array of numerical values that represents a single data point (or sample) to be used by a machine learning algorithm.
[^5]: An *n-gram* is a contiguous sequence of N characters or words from a given sample of text.
[^6]: *Estimators* are objects in scikit-learn that can learn parameters from data by implementing a `.fit()` method. These include: *Predictors* (Models): like `MultinomialNB` or `LinearRegression` and *Transformers* (Preprocessing Tools) like `CountVectorizer` or `StandardScaler` that learn rules to transform or process data.
[^7]: *Multinomial* in this context means the classifier models each document's word counts with a *multinomial distribution*: for each topic, it learns how often each word in the vocabulary tends to appear, and it predicts the topic whose word frequencies best match the document.
[^8]: *Hyperparameter* refers to a configuration setting that is external to the model and whose value can't be estimated from the data. Instead, a hyperparameter's value must be set by the developer.

[^9]: A *confusion matrix* is a table used to evaluate the performance of a classification model on a set of test data for which the true values are known. It visually summarizes the classifier's performance by comparing the predicted categories to the actual categories.
[^10]: A *bigram* is an *n-gram* sequence of two words or characters, for example: "quick brown" or "qu".
[^11]: *Cross-validation* is a resampling method that repeatedly splits the data into separate ‘train’ and ‘test’ subsets so model performance can be evaluated on unseen data.



