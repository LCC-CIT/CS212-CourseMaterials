# Program Structure: Classifier Metrics Lab

This document provides a visual overview of the structure and data flow of the Classifier Metrics program.

## Module Structure & Dependencies

```mermaid
graph TD
    subgraph entryPoints["Entry points (run with uv)"]
        main["main.py<br/>'uv run main.py'"]
        tune["tune.py<br/>'uv run tune.py'"]
    end

    subgraph helpers["Shared helpers"]
        spam["spam_results.py<br/>load_spam_data()<br/>get_spam_results()"]
        ng["newsgroups_data.py<br/>load_newsgroups()<br/>keep_fewer()"]
    end

    dataCsv[("data/sms_spam.csv")]
    dataWeb[("20 newsgroups<br/>(downloaded)")]

    main -->|get_spam_results| spam
    main -->|load_newsgroups| ng
    tune -->|load_spam_data| spam
    tune -->|load_newsgroups| ng

    spam -->|reads CSV| dataCsv
    ng -->|fetch_20newsgroups| dataWeb
```

## Data Flow

```mermaid
graph LR
    csv["sms_spam.csv"] -->|load_spam_data| split["75/25 split"]
    split --> nb["MultinomialNB on word counts"]
    nb -->|test labels| mainM["main.py: show_scores<br/>accuracy/precision/recall/F1"]
    nb -->|train only| tuneSpam["tune.py: GridSearchCV<br/>accuracy vs F1"]

    web["20 newsgroups"] -->|keep_fewer: 75 train / 50 test| svm["TF-IDF + SGD linear SVM"]
    svm --> mainM
    svm --> tuneNg["tune.py: GridSearchCV<br/>accuracy vs f1_macro"]
```

## Summary

- **`spam_results.py`** and **`newsgroups_data.py`** are the reusable helpers — both entry points import from them.
- **`main.py`** shows the *measured* results; **`tune.py`** *tunes* the same two classifiers with `GridSearchCV`, comparing accuracy vs F1.
- The spam classifier is `CountVectorizer → MultinomialNB`; the newsgroups classifier is `CountVectorizer → TfidfTransformer → SGDClassifier` (a linear SVM pipeline).
- `talk.religion.misc` is deliberately kept small (75/50 posts) to create an imbalanced/rare class — the core learning objective of the lab.
