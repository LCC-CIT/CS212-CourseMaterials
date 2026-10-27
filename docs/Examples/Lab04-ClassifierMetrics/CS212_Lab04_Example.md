---
title: "Lab 4, Example"
description: "Class example for Lab 4: measuring a classifier with the performance metrics accuracy, precision, recall and F1, building on the spam detection example."
keywords: performance metrics, accuracy, precision, recall, F1, confusion matrix, spam detection, scikit-learn
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Example for Lab 4: Measuring and Improving a Classifier</h1>

<h2>Example for Lab 4</h2>

This example builds on the [Spam Detection example](../SpamDetection/CS212_SpamDetection_Overview.md). It takes the results of the spam classifier from that example and uses scikit-learn to calculate its *performance metrics*: accuracy (the percent correct), precision, recall and F1. It also prints a classification report and a confusion matrix. A second example, adapted from the four-newsgroups example in the scikit-learn text tutorial (Week 3), shows what the report looks like when there are more than two classes. For each example, a second program, `tune.py`, uses a grid search to tune the classifier with a performance metric as the score.

The explanations of what the numbers mean and how they are calculated are in the lecture notes, [Classifier Metrics](../../LectureNotes/CS212-Unit04-2-ClassifierMetrics.md). Read them first, then run the code.

<h2>Contents</h2>

[TOC]

## The Code

There are two examples, the spam classifier and the newsgroups classifier, and two versions of the code for each: a Python project and a Jupyter notebook. To get them all, [download them as a zip file](https://download-directory.github.io/?url=https://github.com/LCC-CIT/CS212-CourseMaterials/tree/main/docs/Examples/Lab04-ClassifierMetrics) and unzip it. The unzipped folder has three subfolders:

| Folder | What it is |
| --- | --- |
| `SpamMetricsProgram` | A Python project that measures and tunes the spam classifier. You run it from the command line with `uv` |
| `NewsgroupsMetricsProgram` | A Python project that measures and tunes the newsgroups classifier, which has four classes |
| `ClassifierMetricsNotebook` | Two Jupyter notebooks that do the same steps as the two projects, with an explanation of each one |

## Running the Python Projects

You need [`uv`](https://docs.astral.sh/uv/). It reads `pyproject.toml` and installs scikit-learn the first time you run something. Both projects have these files:

| File | What it does |
| --- | --- |
| `main.py` | Trains the classifier and measures it with scikit-learn's metrics functions |
| `tune.py` | Uses `GridSearchCV` to tune the classifier, comparing two scores: accuracy and an F1 score |
| `pyproject.toml` | The project settings and the packages it needs |
| `uv.lock` | The exact package versions that `uv` installed when this was written |
| `README.md` | A short description of the project |

`SpamMetricsProgram` also has a `data/` folder with the SMS Spam Collection data file and its readme.

To run either project, open a terminal in its folder and run these commands:

```bash
uv run main.py
uv run tune.py
```

The spam programs have to run from inside the `SpamMetricsProgram` folder, because they open `data/sms_spam.csv` using a relative path, and Python starts looking in the folder where the program is *running*. The first run of the newsgroups programs downloads the newsgroups data, so it needs an internet connection. The newsgroups `tune.py` takes about a minute.

## Running the Jupyter Notebooks

The `ClassifierMetricsNotebook` folder has two notebooks: `SpamMetrics.ipynb` for the spam classifier and `NewsgroupsMetrics.ipynb` for the newsgroups classifier. Start with the spam notebook. Both download their data, so they need an internet connection.

- **In Google Colab:** open the [spam notebook](https://colab.research.google.com/github/LCC-CIT/CS212-CourseMaterials/blob/main/docs/Examples/Lab04-ClassifierMetrics/ClassifierMetricsNotebook/SpamMetrics.ipynb) or the [newsgroups notebook](https://colab.research.google.com/github/LCC-CIT/CS212-CourseMaterials/blob/main/docs/Examples/Lab04-ClassifierMetrics/ClassifierMetricsNotebook/NewsgroupsMetrics.ipynb) in Colab. Colab already has scikit-learn, so there is nothing to install.
- **In VS Code:** open a terminal in the `ClassifierMetricsNotebook` folder and run `uv sync`. Then open a notebook and choose the `.venv` Python environment as the kernel.

## Experimenting

- In the spam `main.py`, make a classifier that calls every message spam: `always_spam = [1] * len(test_labels)`. Copy the "always ham" part of the program and change it to print the scores of `always_spam`. What are its precision and recall? Why is it useless even though its recall is perfect?
- In the spam `main.py`, change `test_size` from 0.25 to 0.5. Which of the numbers change, and by how much? What does that tell you about how much to trust the result from one test set?
- Which mistake would you rather your spam filter make: sending a real message to the spam folder, or letting a spam message through? What do the precision and recall of spam tell you about that?
- In the spam `tune.py`, add `0.01` to the `nb__alpha` list and `(1, 3)` to the `counts__ngram_range` list. Do the best settings change? Does the F1 on the test messages change? If not, what does that tell you about how much there was to gain from tuning this classifier?
- In the output of the newsgroups `main.py`, look at the confusion matrix. Which two newsgroups are confused most often? Calculate the precision and recall of `sci.med` from the matrix, and check your answers against the report.
- In the newsgroups `main.py`, change the 75 and the 50 to 377 and 251, so that all of the religion posts are used. How do the recall of `talk.religion.misc` and the macro average change? Make the same change in the newsgroups `tune.py` and run it again: does tuning still make as much difference? Try 150 and 100 as well.



*These lab materials were drafted by Claude Code and revised by Brian Bird. 10/21/2026*

------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------
