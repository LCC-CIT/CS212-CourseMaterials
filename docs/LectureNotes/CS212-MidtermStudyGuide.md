---
title: Midterm Study Guide
description: A two-page cheat sheet covering weeks 1 through 4 of CS 212.
keywords: midterm, study guide, cheat sheet
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>CS 212 Midterm Study Guide</h1>

[TOC]

## What is AI?

- **Dartmouth workshop** (1956, John McCarthy, who coined "AI"): "every aspect of learning... can in principle be so precisely described that a machine can be made to simulate it."[^ai]
- **Symbolic AI / GOFAI** ("Good Old Fashioned AI", Haugeland): explicit rules and logic on human-readable *symbols*. `IF feathers AND flies THEN bird`.
- **Modern (US 2020 law) definition:** a machine-based system that makes **predictions, recommendations or decisions**. It *perceives* input, *abstracts* it into a model (**training**), and uses the model to choose options (**inference**).
- **Categories:** Symbolic (GOFAI) | Machine learning (statistical, ANN).

## Python Basics[^py]

- No braces (**indentation** makes blocks), no `;`, **dynamically typed**, interpreted, style guide = **PEP 8**.
- Multi-paradigm; **duck typing**; first-class functions. OOP: **composition** (has-a), **inheritance** (is-a), **encapsulation**.

| Type | Syntax | Ordered | Mutable | Duplicates |
|---|---|---|---|---|
| list | `[1, 2]` | yes | yes | yes |
| tuple | `(1, 2)` | yes | **no** | yes |
| set | `{1, 2}` | no | yes | **no** |
| dict | `{"k": 1}` | insertion | yes | keys unique |

Dict keys must be immutable (a tuple can be a key; a list can't).[^coll]

```python
d = {"apples": 50}
d["apples"]            # 50     d["kiwi"] -> KeyError
d.get("kiwi", 0)       # 0 (default instead of KeyError)
unique = set([1, 2, 2, 3])        # {1, 2, 3}
name, age = ("Alice", 30)         # tuple unpacking
```

**Loops:** `for x in iterable:` (known items; `range(3)` gives 0,1,2) | `while condition:` (unknown count; change the condition or loop forever). `break` exits the loop; `continue` skips to next pass; loop `else` runs only if no `break`.[^loop]

```python
for i in range(1, 4):
    if i == 2:
        continue
    print(i)           # prints 1, then 3
```

## Python Projects[^proj]

- Each project gets its own **virtual environment** (`.venv`): avoids version conflicts, documents dependencies, protects system Python. Don't commit `.venv`.
- **venv/pip:** `python -m venv .venv`, activate (`.venv\Scripts\Activate.ps1` Windows, `source .venv/bin/activate` Mac), `python -m pip install pkg`, `pip freeze > requirements.txt`.
- **uv**:

| Command | Does |
|---|---|
| `uv init` | new project (`pyproject.toml`, `.python-version`, `main.py`) |
| `uv add pkg` | install + record in `pyproject.toml` + update `uv.lock` |
| `uv sync` | rebuild `.venv` from `uv.lock` (cloned project) |
| `uv run main.py` | run in project's environment |

- `pyproject.toml` : project settings and dependencies (TOML format). `uv.lock` = exact versions of everything.

## Constraint Solving[^cs]

- **Declarative**: describe *what* a correct answer looks like, not *how* to find it. Part of symbolic AI; **deterministic**; answer is guaranteed to obey the rules and it can prove none exists.
- **Three inputs:** **variables** (unknowns), **domains** (allowed values), **constraints** (rules).
- **Results:** `sat` (solution found), `unsat` (rules contradict), `unknown` (gave up/timeout).
- Why not loops? Combinations explode (20 guests have about 2.4 quintillion seatings); solvers prune whole branches.
- Fits scheduling, gates, delivery, timetables, Sudoku. Key question: *"What are the unknowns and what are the rules?"*

## Z3 (SMT solver)[^z3]

Five steps: **create variables, create solver, add constraints, check, read model.**

```python
from z3 import Ints, Solver, Distinct, Abs, sat
ana, ben, cat, dev = Ints('ana ben cat dev')
s = Solver()
for f in (ana, ben, cat, dev):
    s.add(f >= 1, f <= 4)         # always bound Ints
s.add(Distinct(ana, ben, cat, dev))
s.add(Abs(ana - ben) > 1, cat == 1, ana < ben)
if s.check() == sat:              # check BEFORE model()
    m = s.model()
    print(m[ana].as_long())       # 2 (Python int)
```

- Z3 variables are **symbols**, not numbers: `Int`, `Real`, `Bool`, `Ints('a b')`. Package `z3-solver`, import `z3`.
- `==` is a constraint; `=` is assignment and destroys your symbol. Operators are overloaded to build rules.
- Use `And Or Not Implies If Distinct Sum Abs`, **not** Python `and/or/not/if`. `If(c, 1, 0)` counts.
- `Implies(a, b)` only restricts when `a` is true.
- Solver: `add`, `check`, `model`, `push`/`pop` (what-if), `reset`, `set("timeout", ms)`. `unsat_core()` (with tracking flags) shows conflicting rules; `Optimize` has `minimize`/`maximize`.
- Z3 gives *a* solution, not *the* only one.

## Machine Learning Basics[^ml]

- ML = models trained on data sets to **predict** and **classify**. A **model** = algorithm + what it learned from training data.
- **Feature**: one piece of input info. **Label**: target output. **Training data** teaches; **test data** (unseen) evaluates.
- **Supervised** (labeled data; spam filter) | **Unsupervised** (unlabeled, finds structure; k-means customer groups) | **Reinforcement** (agent learns by trial, rewards/penalties).

| Model | Idea |
|---|---|
| **Naive Bayes** | Bayes' rule, assumes features independent; fast |
| **Bayesian network** | directed graph; models feature dependencies |
| **k-NN** | classify by majority vote of *k* nearest feature vectors; no real training step, just stores data |
| **Linear regression** | `y = mx + b`; predicts a continuous value |
| **Logistic regression** | sigmoid squeezes to 0&ndash;1; binary classification (multinomial = unordered 3+, ordinal = ordered 3+) |
| **Decision tree** | flowchart: decision nodes test features, leaves are outcomes |
| **Random forest** | many trees on random samples; majority vote (or average); reduces overfitting |
| **ANN** | weighted connected neurons; weights adjusted in training |

## Bayes' Rule[^bayes]

- **Probability** = happens / total (die 6: 1/6). **Odds** = happens : doesn't (1:5). Odds *o* to probability: *o* / (1 + *o*).
- **Prior odds**: before new evidence (rain in Eugene 146:219).
- **Likelihood ratio**: P(observation | event) / P(observation | no event) (morning clouds: 7).
- **Posterior odds = prior odds &times; likelihood ratio** = 146:219 &times; 7 = 1022:219 (82.4%).
- **Naive Bayes sentiment:** label posts, count word frequencies per class, then `likelihood = (negFreq/negTotal) / (posFreq/posTotal)` (e.g. fine: 10/500 &divide; 50/1000 = 0.40).
- **Inference:** prior &times; likelihood<sub>1</sub> &times; ... &times; likelihood<sub>n</sub>, compare to a **decision threshold** found from training data.

- 

## scikit-learn Text Pipeline[^sk]

- **Bag of words:** each word gets a column; cell = count. High-dimensional and **sparse** (mostly zeros).
- **`CountVectorizer`** builds vocabulary + counts. **tf** = counts scaled by doc length; **tf-idf** = also down-weights words common to many documents.
- **`fit`/`fit_transform` on training data only; `transform` on new data** (reuse the learned vocabulary).
- **`Pipeline`** chains steps; `step__param` names a setting.

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split, GridSearchCV
tr_x, te_x, tr_y, te_y = train_test_split(msgs, labels,
                         test_size=0.25, random_state=42)
pipe = Pipeline([("vect", CountVectorizer()),
                 ("tfidf", TfidfTransformer()),
                 ("clf", MultinomialNB())])
pipe.fit(tr_x, tr_y)             # train
pred = pipe.predict(te_x)        # inference
grid = {"vect__ngram_range": [(1, 1), (1, 2)],
        "clf__alpha": [0.1, 1.0]}
gs = GridSearchCV(pipe, grid, cv=5, scoring="f1")
gs.fit(tr_x, tr_y)               # best_params_, best_score_
```

## Classifier Metrics[^met]

Pick a **positive** class (spam = 1). **Confusion matrix** (rows = true, cols = predicted); sklearn 2-class order is `[[TN, FP], [FN, TP]]`.

| | Pred. spam | Pred. ham |
|---|---|---|
| **Is spam** | TP | FN |
| **Is ham** | FP | TN |

| Metric | Formula | Asks |
|---|---|---|
| Accuracy | (TP+TN) / all | % right overall |
| Precision | TP / (TP+FP) | when it says spam, how often right? |
| Recall | TP / (TP+FN) | of real spam, how much found? |
| F1 | 2PR / (P+R) | high only if both high |

- **Accuracy misleads with a rare class:** "always ham" scores 1203/1394 = 86.3% but recall 0. Spam model: TP 178, FP 6, FN 13, TN 1197 &rarr; precision 178/184 = 0.967, recall 178/191 = 0.932.
- Precision and recall trade off; choose by cost of each mistake (spam filter: false positives worse &rarr; precision; emergency alerts: recall).
- **Multiclass:** each class takes a turn as positive. Row total = **support**; diagonal / row = recall; diagonal / column = precision. **Macro avg** = plain average of classes; **weighted avg** = by support.
- **Hyperparameters** are set *before* training (`alpha` smoothing, `ngram_range`, `class_weight="balanced"`). Tune with `GridSearchCV`; for a rare class use `scoring="f1"` (or `"f1_macro"`), not accuracy.

```python
from sklearn.metrics import (accuracy_score, precision_score,
    recall_score, f1_score, confusion_matrix, classification_report)
tn, fp, fn, tp = confusion_matrix(te_y, pred).ravel()
precision_score(te_y, pred, zero_division=0)
print(classification_report(te_y, pred))
```

[^ai]: [Overview of AI](../LectureNotes/CS212-Unit01-1-IntroToAI.md): Dartmouth, McCarthy, GOFAI, the 2020 definition, categories.
[^py]: [Intro to Python](../LectureNotes/CS212-Unit01-1-Python.md): Python distinctives, paradigms, OOP concepts.
[^coll]: [Python Collection Types](../LectureNotes/CS212-Unit02-3-PythonCollectionTypes.md): lists, dictionaries, `get()`, sets, tuples.
[^loop]: [Python Loops](../LectureNotes/CS212-Unit02-4-PythonLoops.md): `for`, `while`, `break`, `continue`, `else`.
[^proj]: [Python Projects](../LectureNotes/CS212-Unit02-5-PythonProjects.md): `.venv`, pip, `requirements.txt`, uv, `pyproject.toml`.
[^cs]: [Constraint Solvers](../LectureNotes/CS212-Unit02-1-ConstraintSolvers.md): variables, domains, constraints, sat/unsat, real-world uses.
[^z3]: [The Z3 Constraint Solver](../LectureNotes/CS212-Unit02-2-TheZ3ConstraintSolver.md): five steps, Z3 functions, solver methods, pitfalls, cheat sheet.
[^ml]: [Machine Learning](../LectureNotes/CS212-Unit03-1-MachineLearning.md): terminology, types of ML, supervised models.
[^bayes]: [Machine Learning: Bayes' Rule](../LectureNotes/CS212-Unit03-2-Bayes.md): odds, prior, likelihood ratio, posterior, sentiment example.
[^data]: [Data Set Concepts and Preparation](../LectureNotes/CS212-Unit04-1-DataSetPrep.md): features, dataset quality, scaling, splitting, k-fold, inspection.
[^sk]: [Working with Text Data](../Tutorials/scikit-learn-1.7/WorkingWithTextData.md) (week 3 scikit-learn tutorial): bag of words, tf-idf, pipeline, grid search.
[^met]: [Classifier Metrics](../LectureNotes/CS212-Unit04-2-ClassifierMetrics.md): confusion matrix, accuracy/precision/recall/F1, multiclass reports, tuning.



*Drafted using Claude Sonnet 5.5, reviewed and revised by Brian Bird 10/28/26*

---

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 Course Materials by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in 2026 are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 
