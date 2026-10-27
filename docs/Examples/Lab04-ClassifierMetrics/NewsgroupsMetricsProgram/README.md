# Lab 4 Class Example: Measuring a Classifier with More Than Two Classes

Part of the code for the [Lab 4 class example](../CS212_Lab04_Example.html). It uses the newsgroups example from the Week 3 scikit-learn text tutorial, with posts from four newsgroups, and keeps only a few posts from one of them so that it is a rare class. It prints the `classification_report` and confusion matrix of the classifier, and uses a grid search to tune it with a performance metric. The same steps are in a Jupyter notebook, with an explanation of each one, in the [ClassifierMetricsNotebook](../ClassifierMetricsNotebook/README.md) folder. The first half of the example, measuring the spam classifier, is in the [SpamMetricsProgram](../SpamMetricsProgram/README.md) folder.

| File | What it does |
| --- | --- |
| `main.py` | Loads the newsgroups posts, trains the tf-idf and linear SVM classifier from the tutorial, and prints its classification report and confusion matrix |
| `tune.py` | Uses `GridSearchCV` to tune the newsgroups classifier, comparing accuracy with `f1_macro` as the score |
| `pyproject.toml` | The project settings and the packages it needs (scikit-learn) |
| `uv.lock` | The exact package versions that `uv` installed when this was written |

You need [`uv`](https://docs.astral.sh/uv/). It reads `pyproject.toml` and installs the right packages the first time you run something. Run these commands from this folder:

```bash
uv run main.py
uv run tune.py
```

The first run downloads the newsgroups data, so it needs an internet connection. scikit-learn keeps the data for later runs. `tune.py` takes about a minute.
