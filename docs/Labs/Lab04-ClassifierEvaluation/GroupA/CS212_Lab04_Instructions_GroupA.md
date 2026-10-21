---
title: "Lab 4, Group A"
description: "Instructions for Lab 4, Group A: Distinguishing ChatGPT answers from human answers with a text classifier."
keywords: classifier, scikit-learn, TF-IDF, cross-validation, grid search
material: Lab Instructions
generator: Typora
author: Brian Bird
---

**CS 212, AI Programming 1**

<h1>Lab 4: Evaluating Text Classifiers</h1>

<h2>Group A: ChatGPT vs. Human</h2>

<h2>Contents</h2>

[TOC]

## Can a Classifier Tell ChatGPT from a Person?

Teachers, editors and websites all want to know whether a piece of writing came from a person or from a chatbot. In this lab you will build a classifier that reads an answer to a question about computers or science and decides: human (0) or ChatGPT (1).

You will use the same tools as in Lab 3. This time the focus is on *measuring* your classifier and on *improving* its accuracy (the percent correct). By the end of the lab you will have:

- compared different *features* (words, word pairs, characters) and seen how the choice affects the result,
- measured your classifier so you can tell a real improvement from luck and see if it does better on one class than the other, and
- chosen *hyperparameters* with a grid search.

You will also test your classifier on a different kind of question than the one it was trained on. That test shows how far you can trust a classifier like this.

**Before you start,** read the lecture notes [Classifier Metrics](../../../LectureNotes/CS212-Unit04-2-ClassifierMetrics.md). They explain the performance metrics you will use in this lab (accuracy, precision, recall and F1) and the confusion matrix. Then look at the [Lab 4 example](../../../Examples/Lab04-ClassifierMetrics/CS212_Lab04_Example.md), which has code that calculates them with scikit-learn.

### The data

The data is the **Human ChatGPT Comparison Corpus (HC3)**, a collection of questions, each with an answer written by a person and an answer written by ChatGPT. It was collected in early 2023 by Guo and colleagues (see the References) and is licensed under CC BY-SA 4.0. You will use two of its files:

| File | The questions are about | Questions |
| --- | --- | --- |
| `wiki_csai.jsonl` | Computer science and AI concepts. The human answers come from Wikipedia. | 842 |
| `open_qa.jsonl` | General knowledge questions. The human answers come from a question-answering data set. | 1,187 |

Each line of a file is one question, written as a JSON object with three parts: `question`, `human_answers` and `chatgpt_answers`. The last two are lists, because some questions have more than one answer. To keep the classes balanced, you will use only the first human answer and the first ChatGPT answer for each question.

### Set up your project

1. Make a project folder for the lab with `uv init lab04`, and then `cd lab04`.
2. Add scikit-learn: `uv add scikit-learn`
3. Save this program as `fetch_data.py` in your project folder and run it once with `uv run fetch_data.py`. It downloads the two data files into a folder named `data` (about 5 MB in all).

```python
# fetch_data.py: download the HC3 files into a folder named data.
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

BASE_URL = "https://huggingface.co/datasets/Hello-SimpleAI/HC3/resolve/main/"

os.makedirs("data", exist_ok=True)
for name in ["wiki_csai.jsonl", "open_qa.jsonl"]:
    print("Downloading", name)
    urlretrieve(BASE_URL + name, os.path.join("data", name))
print("Done.")
```

If the download fails with an error that mentions `CERTIFICATE_VERIFY_FAILED`, run `uv add truststore` and then run the program again. If it stops with a timeout, just run it again.

### Starter code

Put this code at the top of your program. The first function reads a data file. The second builds a list of answers and a list of labels for the questions you choose.

```python
import json


def load_hc3(path):
    """Read an HC3 file. Returns three lists with one item per question:
    the questions, the first human answer and the first ChatGPT answer."""
    questions = []
    human_answers = []
    chatgpt_answers = []
    with open(path, encoding="utf-8") as file:
        for line in file:
            item = json.loads(line)
            questions.append(item["question"])
            human_answers.append(item["human_answers"][0])
            chatgpt_answers.append(item["chatgpt_answers"][0])
    return questions, human_answers, chatgpt_answers


def make_samples(human_answers, chatgpt_answers, question_numbers):
    """Build the texts and labels (0 = human, 1 = ChatGPT) for the chosen questions."""
    texts = []
    labels = []
    for number in question_numbers:
        texts.append(human_answers[number])
        labels.append(0)
        texts.append(chatgpt_answers[number])
        labels.append(1)
    return texts, labels
```

Now add this to check that it works. It also splits the data into a training set (75%) and a test set (25%).

```python
from sklearn.model_selection import train_test_split

questions, human_answers, chatgpt_answers = load_hc3("data/wiki_csai.jsonl")
print(len(questions), "questions")

# Split by question number, so both answers to a question stay together.
question_numbers = list(range(len(questions)))
train_numbers, test_numbers = train_test_split(
    question_numbers, test_size=0.25, random_state=42)

train_texts, train_labels = make_samples(human_answers, chatgpt_answers, train_numbers)
test_texts, test_labels = make_samples(human_answers, chatgpt_answers, test_numbers)
print(len(train_texts), "training answers,", len(test_texts), "test answers")
print("A human answer:  ", human_answers[0][:70])
print("A ChatGPT answer:", chatgpt_answers[0][:70])
```

Output:

```
842 questions
1262 training answers, 422 test answers
A human answer:   Animal cognition encompasses the mental capacities of non-human animal
A ChatGPT answer: Animal cognition refers to the mental capacities of non-human animals.
```

**Why split by question?** Each question has two answers, one from a person and one from ChatGPT. If one of the two ended up in the training set and the other in the test set, the classifier could pick up clues from the *topic* of the question instead of the *style* of the writing. Splitting the question numbers first keeps both answers to a question on the same side.

### What to do

Write your code in one Python file, and put your answers to the questions in comments.

1. **Baseline.** Build a pipeline with a `TfidfVectorizer` and a `LogisticRegression`:

   ```python
   pipe = Pipeline([("tfidf", TfidfVectorizer()),
                    ("clf", LogisticRegression(max_iter=1000))])
   ```

   Use these step names, `"tfidf"` and `"clf"`. A grid search refers to a setting by the name of its step, for example `tfidf__min_df` or `clf__C`, so the names in your grid have to match the names in your pipeline. (The names in the Lab 3 tutorial are different.)

   Train it on the training set. For the test set, print the accuracy, a `classification_report` and a `confusion_matrix`. Write down the numbers. Every later step needs to beat them.

2. **Experiment 1: Which features work best?** Compare at least these four ways of turning text into features:
   - words (the default `TfidfVectorizer()`),
   - words and word pairs (`ngram_range=(1, 2)`),
   - characters (`analyzer="char", ngram_range=(2, 4)`), and
   - words with the common English words removed (`stop_words="english"`).

   For each one, use `cross_val_score(pipeline, train_texts, train_labels, cv=5)` and print the mean and standard deviation (`scores.mean()` and `scores.std()`) of the five scores. Cross-validation only uses the training set, so the test set stays untouched. In your comments, answer:
   - Which features were best? Is the difference bigger than the standard deviation? If not, you can't say one is really better.
   - What happened when you removed the stop words? Does that surprise you? (Think about what kind of words are in the list.)

3. **Look inside the classifier.** Print the 15 words with the strongest "human" weight and the 15 with the strongest "ChatGPT" weight. See the hints for how. Which words are about *style*, and which are *artifacts* of how the data was collected? An artifact is something that gives the answer away but wouldn't be there in real writing.

4. **Tune the hyperparameters.** Use `GridSearchCV` with your pipeline and `cv=5` to search `tfidf__ngram_range`, `tfidf__min_df` and `clf__C`. Print the best settings and their cross-validation score. Then print the accuracy of the best model on the test set. Use the test set for this only once.

5. **Experiment 2: A new topic.** Load `data/open_qa.jsonl` and use *all* of its questions (it isn't training data, so there is no need to split it). Use your tuned model to predict the label of each answer. Print the accuracy, a `classification_report` and a `confusion_matrix`. In your comments, answer:
   - How much did the accuracy drop compared with the wiki_csai test set?
   - Which of the two classes did the model get wrong more often? Compare the lengths of the human and ChatGPT answers in the two files (the median number of words is a good measure) and explain what you see.

6. **Error analysis.** Print five answers from the wiki_csai test set that your tuned model got wrong, and the true and predicted labels. Look at them. What do the mistakes have in common? Are any of them hard even for you to judge?

7. **Optional: your own text.** Use your tuned model's `predict_proba` to rate a paragraph you wrote yourself and a paragraph you got from a chatbot today. Is the model fooled? Why do you think so?

### Hints

- **Top words.** For a `LogisticRegression` in a pipeline named `pipe` with steps called `"tfidf"` and `"clf"`:

  ```python
  import numpy as np

  words = pipe.named_steps["tfidf"].get_feature_names_out()
  weights = pipe.named_steps["clf"].coef_[0]
  order = np.argsort(weights)   # positions of the words, from most "human" to most "ChatGPT"
  print(list(words[order[:15]]))     # the 15 most human-like words
  print(list(words[order[-15:]]))    # the 15 most ChatGPT-like words
  ```

  Use `LogisticRegression` or `LinearSVC` for this step, since `coef_` is what holds the weights. To do the same with `MultinomialNB`, you would need `feature_log_prob_`, which this lab doesn't cover.

- **Don't trust a small difference.** The test set only has 422 answers, so one extra mistake changes the accuracy by about a quarter of a percent. Differences of one or two percentage points between settings are often just luck. That is why Experiment 1 uses cross-validation and looks at the standard deviation.

- **`C`.** `C` controls how closely a `LogisticRegression` is allowed to fit the training data. A larger `C` means a closer fit. The default of 1 is too small for TF-IDF features, so include values up to 1000 in your grid. If the best value is the largest in your grid, try an even larger one.

- **Use a `Pipeline`.** `cross_val_score` and `GridSearchCV` train a new model for each fold. If the vectorizer is part of the pipeline, it learns its vocabulary from the training part of each fold only, as it should.

- **Run time.** The character n-gram experiment is the slowest. The whole solution runs in about 20 seconds on a laptop. If your grid search takes more than a minute or two, shrink the grid.

- **What to expect.** With the settings above, the baseline gets about 89% accuracy and a tuned model about 94% on the wiki_csai test set. On open_qa the accuracy drops to about 79%. Your numbers will be a little different.

- **Think about it.** Tools that claim to detect AI writing are used on student essays. What would a false positive (flagging a person's writing as AI) cost the student? Your classifier was trained on answers written by one version of ChatGPT in early 2023. How much would you trust it today?

### References

Biyang Guo, Xin Zhang, Ziyuan Wang, Minqi Jiang, Jinran Nie, Yuxuan Ding, Jianwei Yue and Yupeng Wu, "How Close is ChatGPT to Human Experts? Comparison Corpus, Evaluation, and Detection," 2023. The data is at <a href="https://huggingface.co/datasets/Hello-SimpleAI/HC3" target="_blank">Hello-SimpleAI/HC3 on Hugging Face</a>.

The scikit-learn guide to <a href="https://scikit-learn.org/stable/modules/model_evaluation.html" target="_blank">model evaluation</a> and the [Working with Text Data tutorial](../../../Tutorials/scikit-learn-1.7/WorkingWithTextData.md) (see its sections on the classification report, confusion matrix and grid search) are good references for this lab.

## Submitting your lab work on Canvas

**Note**: You only need to submit your code. You <u>do not</u> need to upload your virtual environment (.venv) folder or the data files.

### Beta Version

- Post the beta version of your Python file to your team channel in Discord.

### Code Review

- Review one of your lab partners' code and post the review in your team channel on Discord.
- Submit a copy of the code review <u>you did</u> to the code review assignment on Canvas.

### Production Version

Based on the code review and helpful advice from your lab partners, you may revise your code. On the code review from your lab partner, complete the "Prod." column to show what you revised. Upload the following to the *Lab Production Version* assignment on Canvas:

1. The Python (.py) file
2. The code review <u>from your lab partner</u> with the "Prod." column filled out by you.

## Grading Criteria

The main focus of grading will be on use of the scikit-learn classes, on whether you measured your results correctly, and on the explanations in your comments. The accuracy of your classifier will not be graded.

*These lab instructions were drafted by Claude Code and are waiting for review by Brian Bird. 10/20/2026*

------

<a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank"><img src="https://i.creativecommons.org/l/by-sa/4.0/88x31.png" alt="Creative Commons License"></a> AI Programming 1 lab instructions by <a href="https://profbird.dev" target="_blank">Brian Bird</a>, written in <time>2026</time> are licensed under a <a href="http://creativecommons.org/licenses/by-sa/4.0/" target="_blank">Creative Commons Attribution-ShareAlike 4.0 International License</a>. 

------------
