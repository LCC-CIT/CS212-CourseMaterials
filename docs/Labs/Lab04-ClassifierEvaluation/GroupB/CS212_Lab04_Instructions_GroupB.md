---
title: "Lab 4, Group B"
description: "Instructions for Lab 4, Group B: routing customer messages to departments with a multi-class text classifier."
keywords: classifier, scikit-learn, multi-class, imbalanced data, class_weight, confusion matrix
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Lab 4: Evaluating Text Classifiers</h1>

<h2>Group B: Routing Customer Messages to Departments</h2>

<h2>Contents</h2>

[TOC]

## Which Department Should Get This Message?

When you message your bank's help desk, someone has to decide which team should read it. In this lab you will build a classifier that reads a customer's message and routes it to one of **six departments**: Cards, Payments, Transfers, TopUps, Security or Account.

In Lab 3 the classifiers chose between two or three classes of about the same size. Here there are six, and two of them (Security and Account) are much rarer than the others, as they would be in real life. That makes accuracy (the percent correct) a poor measure, and it gives you a chance to see what happens when a classifier mostly learns about the common classes. By the end of the lab you will have:

- read a multi-class `classification_report` and `confusion_matrix`,
- seen how `class_weight` changes the balance between precision and recall for a rare class, and
- chosen **hyperparameters** with a grid search that is scored with the right measure.

**Before you start,** read the lecture notes [Classifier Metrics](../../../LectureNotes/CS212-Unit04-2-ClassifierMetrics.md). They explain the performance metrics you will use in this lab (accuracy, precision, recall and F1) and the confusion matrix. Then look at the [Lab 4 example](../../../Examples/Lab04-ClassifierMetrics/CS212_Lab04_Example.md), which has code that calculates them with scikit-learn.

### The data

The data is **BANKING77**, a collection of 13,083 real-sounding customer service messages written for an online bank (see the References, licensed CC BY 4.0). Each message is labeled with one of 77 *intents*, such as `card_arrival`, `change_pin` or `transfer_fee_charged`. Routing to 77 classes would be hard to read, so we group the intents into six departments. The table gives the number of intents in each department, and a few examples.

| Department | Intents | Some of its intents |
| --- | --- | --- |
| Cards | 21 | `card_arrival`, `change_pin`, `activate_my_card`, `virtual_card_not_working` |
| Payments | 18 | `declined_card_payment`, `request_refund`, `cash_withdrawal_charge` |
| Transfers | 12 | `failed_transfer`, `cancel_transfer`, `transfer_timing` |
| TopUps | 10 | `top_up_failed`, `top_up_limits`, `automatic_top_up` |
| Security | 8 | `lost_or_stolen_card`, `compromised_card`, `verify_my_identity` |
| Account | 8 | `edit_personal_details`, `terminate_account`, `exchange_rate`, `country_support` |

The groups are one person's reasonable guess. A few intents could belong to two departments, and you will see the effect of that in your error analysis.

The data comes in two files, `train.csv` (10,003 messages) and `test.csv` (3,080 messages). Each has two columns: `text` and `category` (the intent).

**Making two departments rare.** The original data has about the same number of messages for every intent. To get a realistic imbalance, the starter code below keeps only about 15% of the Security messages and 25% of the Account messages. It does this to the training set *and* the test set, so the test set looks like the real world the classifier would be used in. It also shuffles the messages, because the files are sorted by intent, and cross-validation does not work well on sorted data.

### Set up your project

1. Make a project folder for the lab with `uv init lab04`, and then `cd lab04`.
2. Add scikit-learn: `uv add scikit-learn`
3. Save this program as `fetch_data.py` in your project folder and run it once with `uv run fetch_data.py`. It downloads the two data files into a folder named `data`.

```python
# fetch_data.py: download the Banking77 files into a folder named data.
# Run it once with:  uv run fetch_data.py
import os
import socket
from urllib.request import urlretrieve

try:
    import truststore  # only needed if you get a certificate error (see the lab instructions)
    truststore.inject_into_ssl()
except ImportError:
    pass

socket.setdefaulttimeout(60)  # give up with an error instead of waiting forever

BASE_URL = "https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/"

os.makedirs("data", exist_ok=True)
for name in ["train.csv", "test.csv"]:
    print("Downloading", name)
    urlretrieve(BASE_URL + name, os.path.join("data", name))
print("Done.")
```

If the download fails with an error that mentions `CERTIFICATE_VERIFY_FAILED`, run `uv add truststore` and then run the program again. If it stops with a timeout, just run it again.

### Starter code

Put this code at the top of your program. It has the grouping of intents into departments, a function that reads a file, and a function that makes some departments rare.

```python
import csv
import random

# The 77 Banking77 intents, grouped into 6 departments.
DEPARTMENTS = {
    "Cards": [
        "activate_my_card", "card_arrival", "card_delivery_estimate", "card_linking",
        "card_not_working", "card_swallowed", "card_about_to_expire", "change_pin",
        "contactless_not_working", "disposable_card_limits", "get_disposable_virtual_card",
        "get_physical_card", "getting_spare_card", "getting_virtual_card",
        "order_physical_card", "pin_blocked", "virtual_card_not_working",
        "apple_pay_or_google_pay", "card_acceptance", "visa_or_mastercard",
        "supported_cards_and_currencies",
    ],
    "Payments": [
        "card_payment_fee_charged", "card_payment_not_recognised",
        "card_payment_wrong_exchange_rate", "declined_card_payment",
        "pending_card_payment", "reverted_card_payment?",
        "direct_debit_payment_not_recognised", "transaction_charged_twice",
        "extra_charge_on_statement", "request_refund", "Refund_not_showing_up",
        "cash_withdrawal_charge", "cash_withdrawal_not_recognised",
        "declined_cash_withdrawal", "pending_cash_withdrawal",
        "wrong_amount_of_cash_received", "wrong_exchange_rate_for_cash_withdrawal",
        "atm_support",
    ],
    "Transfers": [
        "cancel_transfer", "declined_transfer", "failed_transfer", "pending_transfer",
        "transfer_fee_charged", "transfer_into_account", "transfer_not_received_by_recipient",
        "transfer_timing", "beneficiary_not_allowed", "receiving_money",
        "balance_not_updated_after_bank_transfer",
        "balance_not_updated_after_cheque_or_cash_deposit",
    ],
    "TopUps": [
        "automatic_top_up", "pending_top_up", "top_up_by_bank_transfer_charge",
        "top_up_by_card_charge", "top_up_by_cash_or_cheque", "top_up_failed",
        "top_up_limits", "top_up_reverted", "topping_up_by_card", "verify_top_up",
    ],
    "Security": [
        "compromised_card", "lost_or_stolen_card", "lost_or_stolen_phone",
        "unable_to_verify_identity", "verify_my_identity", "why_verify_identity",
        "verify_source_of_funds", "passcode_forgotten",
    ],
    "Account": [
        "age_limit", "country_support", "edit_personal_details", "terminate_account",
        "exchange_charge", "exchange_rate", "exchange_via_app", "fiat_currency_support",
    ],
}

DEPARTMENT_NAMES = list(DEPARTMENTS.keys())

# Look up an intent's department: DEPARTMENT_OF["change_pin"] is "Cards"
DEPARTMENT_OF = {}
for department, intents in DEPARTMENTS.items():
    for intent in intents:
        DEPARTMENT_OF[intent] = department


def load_messages(path):
    """Read a Banking77 CSV file. Returns three lists with one item per message:
    the text, the department it belongs to and its original intent."""
    texts = []
    departments = []
    intents = []
    with open(path, encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            texts.append(row["text"])
            departments.append(DEPARTMENT_OF[row["category"]])
            intents.append(row["category"])
    return texts, departments, intents


def make_imbalanced(texts, departments, intents, keep_fractions, seed=42):
    """Randomly throw away messages so some departments are rare, then shuffle
    what is left. keep_fractions says what fraction of each department to keep,
    for example {"Security": 0.10} keeps about 10% of the Security messages.
    (The files are sorted by intent, so the shuffle is needed for cross-validation.)"""
    generator = random.Random(seed)
    kept = []
    for i in range(len(texts)):
        fraction = keep_fractions.get(departments[i], 1.0)
        if generator.random() < fraction:
            kept.append(i)
    generator.shuffle(kept)

    new_texts = []
    new_departments = []
    new_intents = []
    for i in kept:
        new_texts.append(texts[i])
        new_departments.append(departments[i])
        new_intents.append(intents[i])
    return new_texts, new_departments, new_intents
```

Now add this to check that it works.

```python
from collections import Counter

train_texts, train_departments, train_intents = load_messages("data/train.csv")
test_texts, test_departments, test_intents = load_messages("data/test.csv")
print("Training messages per department:", dict(Counter(train_departments)))

# Make Security and Account rare, in the training AND the test data.
keep = {"Security": 0.15, "Account": 0.25}
train_texts, train_departments, train_intents = make_imbalanced(
    train_texts, train_departments, train_intents, keep)
test_texts, test_departments, test_intents = make_imbalanced(
    test_texts, test_departments, test_intents, keep)
print("After shrinking, training:", dict(Counter(train_departments)))
print("After shrinking, test:    ", dict(Counter(test_departments)))
```

Output:

```
Training messages per department: {'Cards': 2298, 'Account': 945, 'Payments': 2932, 'TopUps': 1232, 'Security': 834, 'Transfers': 1762}
After shrinking, training: {'Payments': 2932, 'Cards': 2298, 'Transfers': 1762, 'TopUps': 1232, 'Account': 214, 'Security': 132}
After shrinking, test:     {'Cards': 840, 'TopUps': 400, 'Payments': 720, 'Transfers': 480, 'Security': 46, 'Account': 93}
```

### What to do

Write your code in one Python file, and put your answers to the questions in comments.

1. **Baseline.** Build a pipeline with a `TfidfVectorizer` and a `LogisticRegression`:

   ```python
   pipe = Pipeline([("tfidf", TfidfVectorizer()),
                    ("clf", LogisticRegression(max_iter=2000))])
   ```

   Use these step names, `"tfidf"` and `"clf"`. A grid search refers to a setting by the name of its step, for example `tfidf__min_df` or `clf__C`, so the names in your grid have to match the names in your pipeline. (The names in the Lab 3 tutorial are different.)

   Train it on the (shrunken) training set. For the test set, print the accuracy, a `classification_report` and a `confusion_matrix`. Pass `labels=DEPARTMENT_NAMES` to `confusion_matrix` so that you know the order of the rows and columns. In your comments, answer:
   - Which departments does the classifier do worst on? Is it the precision or the recall that is low?
   - The accuracy looks good. Why are the macro average and weighted average so different from it and from each other?

2. **Experiment 1: `class_weight`.** Train the same model again with `LogisticRegression(max_iter=2000, class_weight="balanced")`. This makes mistakes on the rare departments count more during training. Print the same report. In your comments, answer:
   - What happened to the precision and recall of Security and Account? Is that what you expected?
   - What happened to the accuracy? What happened to the macro F1 (`f1_score(..., average="macro")`)?
   - If Security messages are about fraud and lost cards, would the bank want the old behavior or the new behavior? Which would you choose for the Cards department?

3. **Experiment 2: Tune the hyperparameters.** Use `GridSearchCV` to search `tfidf__ngram_range`, `tfidf__min_df` and `clf__C`. Use `cv=3` and **`scoring="f1_macro"`**. Print the best settings and the cross-validation score. Then print the report and confusion matrix of the best model on the test set. In your comments, answer:
   - Why use `scoring="f1_macro"` instead of the default? (The default for classifiers is accuracy.)
   - Did the tuned model beat Experiment 1? Did it help the rare departments?

4. **Error analysis.** Print five test messages from the Security department that your tuned model sent somewhere else, with the department it chose and the original intent. Then count which (intent, true department, predicted department) combinations are the most common mistakes. In your comments, answer:
   - What do the mistakes have in common? Are some of them reasonable, or even arguably correct?
   - If you could change one thing in the grouping of intents into departments to reduce mistakes, what would it be?

5. **Think about it.** Sending a message to the wrong department means a delay for the customer. Which is worse: a Security message sent to Cards, or a Cards message sent to Security? Which measure matters more for the Security department, precision or recall? Why?

### Hints

- **`MultinomialNB` has no `class_weight` setting.** Use `LogisticRegression` (or `LinearSVC`) for this lab.
- **The rare departments have few test messages.** The test set has only about 46 Security messages, so each one is worth about two percentage points of recall. Don't read too much into small differences.
- **Why `f1_macro`?** `GridSearchCV` picks the setting with the best score. Accuracy is dominated by the big departments, so it would hardly notice a bad result on Security. Macro F1 averages the six departments equally.
- **A grid is slow if it is big.** Every combination is trained once for each cross-validation fold. The grid in step 3 has 12 combinations, so 36 training runs. The whole solution runs in about 10 seconds on a laptop.
- **What to expect.** The baseline gets about 94% accuracy but only about 60% recall on Security. With `class_weight="balanced"` the Security recall goes up to about 90% and the precision drops to about 70%, and the accuracy hardly changes. After tuning, the macro F1 is about 0.94. Your numbers will be a little different, since your grid and settings may not be the same as ours.
- **Printing a prediction.** The predictions from the model are NumPy strings. If they look odd when you print them inside a tuple, wrap them in `str()`.

### References

Iñigo Casanueva, Tadas Temčinas, Daniela Gerz, Matthew Henderson and Ivan Vulić, "Efficient Intent Detection with Dual Sentence Encoders," 2020. The data is from the <a href="https://github.com/PolyAI-LDN/task-specific-datasets" target="_blank">PolyAI task-specific-datasets repository</a> and is licensed CC BY 4.0.

The scikit-learn guide to <a href="https://scikit-learn.org/stable/modules/model_evaluation.html" target="_blank">model evaluation</a> and the [Working with Text Data tutorial](../../../Tutorials/scikit-learn-1.7/WorkingWithTextData.md) (see its sections on the classification report, confusion matrix and grid search) are good references for this lab.

## Sharing and Submitting Your Lab Work

### What to Submit

For both the beta and production versions you should share or submit the following:

- Python code files (.py files)
- pyproject.toml
- uv.lock

Whoever downloads your code will be able to:

- Create a .venv folder and restore all the packages and python version by running `uv sync`
- Download all the data by runing `uv run fetch_data.py`
- Run your program by running `uv run program_name.py`

### Beta Version

- Post your zipped beta version files to your team channel on Discord.

### Code Review

- Review code from one of your lab partners' and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the "Prod." column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The Zipped code files.
2. The code review <u>from your lab partner</u> with the "Prod." column filled out by you.

## Grading Criteria

The main focus of grading will be on use of the scikit-learn classes, on whether you measured your results correctly, and on the explanations in your comments. The accuracy of your classifier will not be graded.



*These lab instructions were drafted by Claude Code and  revised by Brian Bird. 10/26/2026*

------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------
