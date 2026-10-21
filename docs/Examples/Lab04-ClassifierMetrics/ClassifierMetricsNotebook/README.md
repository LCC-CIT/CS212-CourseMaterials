# Measuring a Classifier (Jupyter Notebook)

A Jupyter notebook for the [Lab 4 class example](../CS212_Lab04_Example.html). It builds on the [Spam Detection example](../../SpamDetection/CS212_SpamDetection_Overview.md): it takes the results of the spam classifier, calculates accuracy, precision, recall and F1 with scikit-learn, and shows the `classification_report` of the four-newsgroups example from the Week 3 tutorial. It does the same steps as the Python project in the [ClassifierMetricsProgram](../ClassifierMetricsProgram/README.md) folder, with an explanation of each one.

---

## Run the Notebook in Google Colab

Open [ClassifierMetrics.ipynb in Colab](https://colab.research.google.com/github/LCC-CIT/CS212-CourseMaterials/blob/main/docs/Examples/Lab04-ClassifierMetrics/ClassifierMetricsNotebook/ClassifierMetrics.ipynb), or download the notebook and upload it with **File → Upload notebook**. Colab already has scikit-learn, and the notebook downloads the data itself, so there's nothing to install.

## Run the Notebook in VS Code with `uv`

[`uv`](https://docs.astral.sh/uv/) reads [`pyproject.toml`](pyproject.toml) and installs the right packages for you. If you don't have it yet, see "Install `uv`" in the [Constraint Solving example](../../ConstraintSolving/README.md).

Open a terminal in the `ClassifierMetricsNotebook` folder, then run:

```bash
uv sync
```

This creates a `.venv` folder with scikit-learn and the Jupyter kernel. Then open [`ClassifierMetrics.ipynb`](ClassifierMetrics.ipynb) in VS Code and choose the `.venv` Python environment as the kernel.

The notebook downloads the data from this repository on GitHub, so it needs an internet connection.

---

## The Data

The [SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) from the UCI Machine Learning Repository has 5,574 real text messages, each labeled `ham` or `spam` by a person. The notebook reads the copy of the data in the [SpamDetectionNotebook](../../SpamDetection/SpamDetectionNotebook/README.md) folder, so this folder doesn't have its own copy.

The data was collected by Tiago A. Almeida and José María Gómez Hidalgo, who hold its copyright. Their original readme, including the license, is in [`SMSSpamCollection-readme.txt`](../../SpamDetection/SpamDetectionNotebook/SMSSpamCollection-readme.txt) in that folder.

---

## File Manifest

| File | Purpose |
|---|---|
| [`ClassifierMetrics.ipynb`](ClassifierMetrics.ipynb) | The notebook, with step-by-step explanations. |
| [`pyproject.toml`](pyproject.toml) | Packages needed to run the notebook locally. |
| [`README.md`](README.md) | This file. |

*This readme file was drafted by Claude Code.*
