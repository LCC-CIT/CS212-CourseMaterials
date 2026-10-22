# Spam Detection with Naive Bayes (Python Program)

A Python program that trains a **naive Bayes** classifier with scikit-learn to sort text messages into **spam** and **ham** (normal messages). It does the same steps as the notebook in the [SpamDetectionNotebook](../SpamDetectionNotebook/README.md) folder, which has step-by-step explanations of each one.

---

## Run the Program with `uv`

[`uv`](https://docs.astral.sh/uv/) installs the right packages for you. If you don't have it yet, see "Install `uv`" in the [Constraint Solving example](../../ConstraintSolving/README.md).

Open a terminal in the `SpamDetectionProgram` folder, then run:

```bash
uv run spam_detection.py
```

The packages the program needs are listed in a comment block at the top of `spam_detection.py`. `uv` reads that list and installs the packages in its own cache, so it doesn't create a `.venv` folder.

### Using the `pyproject.toml` File

The `SpamDetectionProgram` folder includes a `pyproject.toml` file that lists the required packages. To use it instead of the inline script dependencies, delete the comment block at the top of `spam_detection.py` (the lines from `# /// script` to `# ///`). If a script has that block, `uv run` uses it and ignores `pyproject.toml`.

Then run the program with the same command, `uv run spam_detection.py`. This time `uv` installs the packages in a `.venv` folder inside the project folder.

## Run the Program without `uv`

If you already have Python 3.11 or newer, install the packages with pip and run the program with Python:

```bash
pip install numpy pandas scikit-learn
```

```bash
python spam_detection.py
```

(On macOS and Linux, you may need to type `pip3` and `python3`.)

---

## The Data

[`sms_spam.csv`](sms_spam.csv) is the [SMS Spam Collection](https://archive.ics.uci.edu/dataset/228/sms+spam+collection) from the UCI Machine Learning Repository: 5,574 real text messages, each labeled `ham` or `spam` by a person. The program reads it from this folder.

The data was collected by Tiago A. Almeida and José María Gómez Hidalgo, who hold its copyright. Their original readme, including the license, is in [`SMSSpamCollection-readme.txt`](SMSSpamCollection-readme.txt).

---

## File Manifest

| File | Purpose |
|---|---|
| [`spam_detection.py`](spam_detection.py) | The program. |
| [`sms_spam.csv`](sms_spam.csv) | The SMS Spam Collection data. |
| [`SMSSpamCollection-readme.txt`](SMSSpamCollection-readme.txt) | The dataset's original readme and license. |
| [`README.md`](README.md) | This file. |

*This readme file was drafted by Claude Opus 5.5.*
