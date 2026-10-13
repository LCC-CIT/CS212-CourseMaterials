---
title: Lab 3, Group C
description: Instructions for doing text classification
keywords: classifier, scikit-learn
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Lab 3: Working with Text Data</h1>

<h2>Group C</h2>

[TOC]

## Part 1: The scikit-learn "Working with Text Data" Tutorial

The instructions for part 1 are [here](../CS212_Lab03_Part1_Instructions.html).
Part 1 has its own assignment submission on Canvas.



## Part 2: Predicting Star Ratings from Movie Reviews

In the tutorial's sentiment exercise, a review is either positive or negative. Real reviews are messier: a critic might give three stars, which is neither good nor bad. In this part you will train a classifier to predict one of **three** classes from the text of a movie review: negative (0), neutral (1) or positive (2).

### The data

The data is the Cornell "scale dataset", which has about 5,000 movie review excerpts by four film critics. Each review is labeled with the rating the critic gave the movie.

1. Download <a href="https://www.cs.cornell.edu/people/pabo/movie-review-data/scale_data.tar.gz" target="_blank">scale_data.tar.gz</a> (4 MB) from the <a href="https://www.cs.cornell.edu/people/pabo/movie-review-data/" target="_blank">Cornell movie review data page</a>.
2. Extract it into your project folder. This works on Windows 10 and later, macOS and Linux: open a terminal in your project folder and run `tar -xzf scale_data.tar.gz`. You will get a folder named `scaledata` with one sub-folder for each critic.

Each critic's folder has these files, with one review on each line. Line 5 of one file matches line 5 of every other file in the same folder.

| File | What is on each line |
| --- | --- |
| `subj.<critic>` | The text of the review |
| `label.3class.<critic>` | The class: 0 = negative, 1 = neutral, 2 = positive |
| `label.4class.<critic>` | A four-class version of the label (you can ignore it for now) |
| `rating.<critic>` | The critic's rating, scaled to a number from 0 to 1 |
| `id.<critic>` | An ID number for the review |

Here is code to load the reviews and the 3-class labels. It uses relative paths, so Python looks for the `scaledata` folder in the folder where you run the program. The files contain a few unusual characters, so they are opened with `encoding="latin-1"`.

```python
import os

CRITICS = ["Dennis+Schwartz", "James+Berardinelli", "Scott+Renshaw", "Steve+Rhodes"]


def read_lines(path):
    lines = []
    with open(path, encoding="latin-1") as file:
        for line in file:
            lines.append(line.strip())
    return lines


def load_reviews(folder):
    texts = []
    labels = []
    for critic in CRITICS:
        text_lines = read_lines(os.path.join(folder, critic, "subj." + critic))
        label_lines = read_lines(os.path.join(folder, critic, "label.3class." + critic))
        for i in range(len(text_lines)):
            texts.append(text_lines[i])
            labels.append(int(label_lines[i]))
    return texts, labels


texts, labels = load_reviews("scaledata")
print(len(texts), "reviews")
print("Negative:", labels.count(0), "Neutral:", labels.count(1), "Positive:", labels.count(2))
```

Output:

```
5006 reviews
Negative: 1197 Neutral: 1915 Positive: 1894
```

### What to do

1. **Split the data.** Use `train_test_split` to hold out 25% of the reviews for testing. Use `random_state=42` so your results are repeatable, and `stratify=labels` so each class has the same share in both sets.
2. **Build a pipeline.** Use a `TfidfVectorizer` and a classifier of your choice, such as `MultinomialNB` or `LinearSVC`, as you did in the tutorial.
3. **Check the accuracy.** Train on the training set and print the accuracy on the test set. Also print a `classification_report` and a `confusion_matrix`.
4. **Improve it with a grid search.** Use `GridSearchCV` to look for better settings. Some ideas: `ngram_range` (single words or also pairs of words), `min_df`, `sublinear_tf` (which makes a word that repeats many times count for less) and the `C` value of `LinearSVC`. Print the best parameters you find and the accuracy of the best model on the test set.
5. **Explain your results.** Put a few comments at the top of your file that answer these questions:
   - Which class did your classifier predict best, and which was hardest? Use the confusion matrix to back up your answer.
   - What kinds of mistakes did it make most often? Do they make sense?
   - Why do you think it can't reach 100% on this data?

**Hints**

- Only use the test set to measure your final results. Use the grid search (which does its own cross-validation on the training set) to choose settings.
- A good result for `LinearSVC` is about 70% accuracy. `MultinomialNB` does a few points worse (about 65%). Don't worry if you get a little more or less.
- `C` is a setting of `LinearSVC`. If you use `MultinomialNB`, try its `alpha` setting instead (for example 0.01, 0.1 and 1.0), or you will get an error about an invalid parameter.
- Keep your grid small. The grid search trains the model once for every combination of settings, times 3 for the cross-validation. A grid with 32 combinations (2 `ngram_range` values, 2 `min_df` values, 2 `sublinear_tf` values and 4 `C` values) took about a minute and a half to run on a laptop.
- The tutorial's Exercise 2 and its grid search section show how the pipeline and `GridSearchCV` fit together.

### Alternative Exercise

Alternatively, you can do a classification project of your own design.  You can browse the <a href="https://scikit-learn.org/stable/datasets.html" target="_blank">scikit-learn datset loaders</a> page for ideas. Let me know if you would have something to propose. It would be very cool to see some of you do a mini-project of your own choosing!

## References

The data is from Bo Pang and Lillian Lee, "Seeing stars: Exploiting class relationships for sentiment categorization with respect to rating scales," *Proceedings of the ACL*, 2005.

## Submitting your lab work on Canvas

**Note**: You only need to submit your code. You <u>do not</u> need to upload your virtual environment (.venv) folder.

### Beta Version

- Post the beta version of your Python file to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the “Prod.” column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The Python (.py) file
2. The code review <u>from your lab partner</u> with the “Prod.” column filled out by you.



## Grading Criteria

The main focus of grading will be on use of the sckit-learn classes and problem solving skills.



------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2025</time>, are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------

