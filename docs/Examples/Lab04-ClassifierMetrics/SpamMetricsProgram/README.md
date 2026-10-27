# Lab 4 Class Example: Measuring the Spam Classifier

Part of the code for the [Lab 4 class example](../CS212_Lab04_Example.html). It builds on the [Spam Detection example](../../SpamDetection/SpamDetectionProgram/README.md) from class. It trains the same spam classifier, calculates its accuracy, precision, recall and F1 with scikit-learn, and uses a grid search to tune it with a performance metric. The same steps are in a Jupyter notebook, with an explanation of each one, in the [ClassifierMetricsNotebook](../ClassifierMetricsNotebook/README.md) folder. The second half of the example, a classifier with more than two classes, is in the [NewsgroupsMetricsProgram](../NewsgroupsMetricsProgram/README.md) folder.

| File | What it does |
| --- | --- |
| `main.py` | Trains the spam classifier from the Spam Detection example and measures it with scikit-learn's metrics functions, comparing it with a classifier that calls every message ham |
| `tune.py` | Uses `GridSearchCV` to tune the spam classifier, comparing accuracy with F1 as the score |
| `data/` | The SMS Spam Collection (`sms_spam.csv`) and its readme, which has its description and terms of use |
| `pyproject.toml` | The project settings and the packages it needs (scikit-learn) |
| `uv.lock` | The exact package versions that `uv` installed when this was written |

You need [`uv`](https://docs.astral.sh/uv/). It reads `pyproject.toml` and installs the right packages the first time you run something. Run these commands from this folder:

```bash
uv run main.py
uv run tune.py
```

Run them from this folder: both programs open `data/sms_spam.csv` using a relative path, and Python starts looking in the folder where the program is *running*.
