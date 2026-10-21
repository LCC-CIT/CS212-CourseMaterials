# Lab 4 Class Example: Measuring a Classifier

The code for the [Lab 4 class example](../CS212_Lab04_Example.html). It builds on the [Spam Detection example](../../SpamDetection/SpamDetectionProgram/README.md) from class. It takes the results of that spam classifier, calculates accuracy, precision, recall and F1 with scikit-learn, shows the `classification_report` of a four-newsgroups example adapted from the Week 3 tutorial, and uses a grid search to tune the classifier with a performance metric. The same steps are in a Jupyter notebook, with an explanation of each one, in the [ClassifierMetricsNotebook](../ClassifierMetricsNotebook/README.md) folder.

| File | What it does |
| --- | --- |
| `spam_results.py` | Repeats the steps of the Spam Detection example and returns the true and predicted labels of its test messages |
| `main.py` | Measures the spam classifier with scikit-learn's metrics functions, then shows a four-newsgroups example adapted from the Week 3 tutorial |
| `tune.py` | Uses `GridSearchCV` to tune the spam classifier, scoring by accuracy and by F1 |
| `data/` | The SMS Spam Collection (`sms_spam.csv`) and its readme, which has its description and terms of use |
| `pyproject.toml` | The project settings and the packages it needs (scikit-learn) |
| `uv.lock` | The exact package versions that `uv` installed when this was written |

You need [`uv`](https://docs.astral.sh/uv/). It reads `pyproject.toml` and installs the right packages the first time you run something. Run these commands from this folder:

```bash
uv run main.py
uv run tune.py
```

Run them from this folder: `spam_results.py` opens `data/sms_spam.csv` using a relative path, and Python starts looking in the folder where the program is *running*. The first run of `main.py` downloads the newsgroups data, so it needs an internet connection.
