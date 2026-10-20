---
title: Loading and Exploring the Data
---

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



[^1]: *Text preprocessing* is the initial set of steps to clean and standardize raw text data before analysis. This often includes converting all text to lowercase, removing punctuation, and handling special characters to ensure consistency. ↩
[^2]: *Tokenizing* is the process of breaking down a text document into smaller units called *tokens*. Tokens are usually words, but can also be individual characters or parts of words.
[^3]: *Stopwords* are common words (like "the," "a," "is," "my," "and," "of") that often don't carry topic meaning, though in deception detection they provide useful stylistic clues. (`CountVectorizer` only removes them if you set its `stop_words` parameter; by default it keeps them.)



---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

---
