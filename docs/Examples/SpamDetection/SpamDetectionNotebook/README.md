# Spam Detection with Naive Bayes

A Jupyter notebook that trains a **naive Bayes** classifier with scikit-learn to sort text messages into **spam** and **ham** (normal messages). It follows the same steps as the scikit-learn *Working With Text Data* tutorial: `CountVectorizer` turns each message into word counts, and `MultinomialNB` learns which words are signs of spam.

---

## Run the Notebook in Google Colab

Open [SpamDetection.ipynb in Colab](https://colab.research.google.com/github/LCC-CIT/CS212-CourseMaterials/blob/main/docs/Examples/SpamDetection/SpamDetectionNotebook/SpamDetection.ipynb), or download the notebook and upload it with **File → Upload notebook**. Colab already has pandas and scikit-learn, and the notebook downloads the data itself, so there's nothing to install.

## Run the Notebook in VS Code with `uv`

[`uv`](https://docs.astral.sh/uv/) reads [`pyproject.toml`](pyproject.toml) and installs the right packages for you. If you don't have it yet, see "Install `uv`" in the [Constraint Solving example](../../ConstraintSolving/README.md).

Open a terminal in the `SpamDetectionNotebook` folder, then run:

```bash
uv sync
```

This creates a `.venv` folder with pandas, scikit-learn, and the Jupyter kernel. Then open [`SpamDetection.ipynb`](SpamDetection.ipynb) in VS Code and choose the `.venv` Python environment as the kernel.

---

## The Data

The [SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) from the UCI Machine Learning Repository has 5,574 real text messages, each labeled `ham` or `spam` by a person. [`sms_spam.csv`](sms_spam.csv) is the same data with a header row added (`label,message`). The notebook reads it from this repository on GitHub, so it works anywhere with an internet connection.

The data was collected by Tiago A. Almeida and José María Gómez Hidalgo, who hold its copyright. Their original readme, including the license, is in [`SMSSpamCollection-readme.txt`](SMSSpamCollection-readme.txt).

---

## File Manifest

| File | Purpose |
|---|---|
| [`SpamDetection.ipynb`](SpamDetection.ipynb) | The notebook, with step-by-step explanations. |
| [`sms_spam.csv`](sms_spam.csv) | The SMS Spam Collection data. |
| [`SMSSpamCollection-readme.txt`](SMSSpamCollection-readme.txt) | The dataset's original readme and license. |
| [`pyproject.toml`](pyproject.toml) | Packages needed to run the notebook locally. |
| [`README.md`](README.md) | This file. |

*This readme file was drafted by Claude Opus 5.5.*
