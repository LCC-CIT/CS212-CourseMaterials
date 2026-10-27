# Measuring a Classifier (Jupyter Notebooks)

Two Jupyter notebooks for the [Lab 4 class example](../CS212_Lab04_Example.html):

- `SpamMetrics.ipynb` builds on the [Spam Detection example](../../SpamDetection/CS212_SpamDetection_Overview.md). It trains the same spam classifier, calculates its accuracy, precision, recall and F1 with scikit-learn, and tunes it with a grid search. It does the same steps as the Python project in the [SpamMetricsProgram](../SpamMetricsProgram/README.md) folder, with an explanation of each one.
- `NewsgroupsMetrics.ipynb` shows the `classification_report` and confusion matrix of a four-newsgroups example adapted from the Week 3 tutorial, where one newsgroup is a rare class, and tunes that classifier too. It does the same steps as the Python project in the [NewsgroupsMetricsProgram](../NewsgroupsMetricsProgram/README.md) folder.

Read the spam notebook first.

---

## Run the Notebooks in Google Colab

Open [SpamMetrics.ipynb in Colab](https://colab.research.google.com/github/LCC-CIT/CS212-CourseMaterials/blob/main/docs/Examples/Lab04-ClassifierMetrics/ClassifierMetricsNotebook/SpamMetrics.ipynb) or [NewsgroupsMetrics.ipynb in Colab](https://colab.research.google.com/github/LCC-CIT/CS212-CourseMaterials/blob/main/docs/Examples/Lab04-ClassifierMetrics/ClassifierMetricsNotebook/NewsgroupsMetrics.ipynb), or download a notebook and upload it with **File → Upload notebook**. Colab already has scikit-learn, and the notebooks download the data themselves, so there's nothing to install.

## Run the Notebooks in VS Code with `uv`

[`uv`](https://docs.astral.sh/uv/) reads [`pyproject.toml`](pyproject.toml) and installs the right packages for you. If you don't have it yet, see "Install `uv`" in the [Constraint Solving example](../../ConstraintSolving/README.md).

Open a terminal in the `ClassifierMetricsNotebook` folder, then run:

```bash
uv sync
```

This creates a `.venv` folder with scikit-learn and the Jupyter kernel. Then open [`SpamMetrics.ipynb`](SpamMetrics.ipynb) or [`NewsgroupsMetrics.ipynb`](NewsgroupsMetrics.ipynb) in VS Code and choose the `.venv` Python environment as the kernel.

The spam notebook downloads its data from this repository on GitHub, and the newsgroups notebook downloads the newsgroups data the first time it runs, so they need an internet connection.

---

## The Data

The [SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) from the UCI Machine Learning Repository has 5,574 real text messages, each labeled `ham` or `spam` by a person. The spam notebook reads the copy of the data in the [SpamDetectionNotebook](../../SpamDetection/SpamDetectionNotebook/README.md) folder, so this folder doesn't have its own copy.

The data was collected by Tiago A. Almeida and José María Gómez Hidalgo, who hold its copyright. Their original readme, including the license, is in [`SMSSpamCollection-readme.txt`](../../SpamDetection/SpamDetectionNotebook/SMSSpamCollection-readme.txt) in that folder.

---

## File Manifest

| File | Purpose |
|---|---|
| [`SpamMetrics.ipynb`](SpamMetrics.ipynb) | Measuring and tuning the spam classifier, with step-by-step explanations. |
| [`NewsgroupsMetrics.ipynb`](NewsgroupsMetrics.ipynb) | Measuring and tuning a classifier with four classes, with step-by-step explanations. |
| [`pyproject.toml`](pyproject.toml) | Packages needed to run the notebooks locally. |
| [`README.md`](README.md) | This file. |

*This readme file was drafted by Claude Code.*
