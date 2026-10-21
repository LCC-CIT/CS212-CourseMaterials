# Lab 4 Class Example: Measuring a Classifier

The code for the [Lab 4 class example](../CS212_Lab04_Example.html). It builds on the [Spam Detection example](../../SpamDetection/SpamDetectionProgram/README.md) from class. It takes the results of that spam classifier, calculates accuracy, precision, recall and F1 by hand, checks them against scikit-learn, and shows a three-class `classification_report`. The same steps are in a Jupyter notebook, with an explanation of each one, in the [ClassifierMetricsNotebook](../ClassifierMetricsNotebook/README.md) folder.

| File | What it does |
| --- | --- |
| `metrics.py` | The functions that count the results and calculate the four measures |
| `report.py` | Prints the by-hand and scikit-learn results side by side |
| `spam_results.py` | Repeats the steps of the Spam Detection example and returns the true and predicted labels of its test messages |
| `main.py` | Measures the spam classifier, then shows a made-up three-department example |
| `data/` | The SMS Spam Collection (`sms_spam.csv`) and its readme, which has its description and terms of use |
| `test_metrics.py` | Tests that check `metrics.py` against hand calculations and scikit-learn |
| `pyproject.toml` | The project settings and the packages it needs (scikit-learn, plus pytest for the tests) |
| `uv.lock` | The exact package versions that `uv` installed when this was written |

You need [`uv`](https://docs.astral.sh/uv/). It reads `pyproject.toml` and installs the right packages the first time you run something. Run these commands from this folder:

```bash
uv run main.py
uv run test_metrics.py
uv run pytest           # the same tests, run with pytest
```

Run them from this folder: `spam_results.py` opens `data/sms_spam.csv` using a relative path, and Python starts looking in the folder where the program is *running*.

You don't need pytest for the lab. The test file also runs by itself.
