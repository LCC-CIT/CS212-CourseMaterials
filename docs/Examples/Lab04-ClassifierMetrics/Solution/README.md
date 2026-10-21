# Lab 4 Class Example: Measuring a Classifier

The code for the [Lab 4 class example](../CS212_Lab04_Example.html). It calculates accuracy, precision, recall and F1 by hand, checks the results against scikit-learn, and shows a three-class `classification_report`.

| File | What it does |
| --- | --- |
| `metrics.py` | The functions that count the results and calculate the four measures |
| `main.py` | Runs the examples and prints the by-hand and scikit-learn results side by side |
| `test_metrics.py` | Tests that check `metrics.py` against hand calculations and scikit-learn |
| `pyproject.toml` | The project settings and the packages it needs (scikit-learn, plus pytest for the tests) |
| `uv.lock` | The exact package versions that `uv` installed when this was written |

You need [`uv`](https://docs.astral.sh/uv/). It reads `pyproject.toml` and installs the right packages the first time you run something. Run these commands from this folder:

```bash
uv run main.py
uv run test_metrics.py
uv run pytest           # the same tests, run with pytest
```

You don't need pytest for the lab. The test file also runs by itself.
