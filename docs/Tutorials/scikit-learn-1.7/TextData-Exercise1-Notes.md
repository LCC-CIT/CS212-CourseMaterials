### Exercises

To do the exercises, copy the content of the ‘skeletons’ folder as a new folder named ‘workspace’:

```python
cp -r skeletons sklearn_tut_workspace
```

You can then edit the content of the workspace without fear of losing the original exercise instructions.

Then start the Python interpreter and run the work-in-progress script with:

```python
[1] %run workspace/exercise_XX_script.py arg1 arg2 arg3
```

If an exception is triggered, use `%debug` to fire-up a post mortem ipdb session.

Refine the implementation and iterate until the exercise is solved.

**For each exercise, the skeleton file provides all the necessary import statements, boilerplate code to load the data and sample code to evaluate the predictive accuracy of the model.**

## Exercise 1: Language identification

- Write a text classification pipeline using a custom preprocessor and `TfidfVectorizer` set up to use character based n-grams, using data from Wikipedia articles as the training set.
- Evaluate the performance on some held out test set.

ipython command line:

```python
%run workspace/exercise_01_language_train_model.py data/languages/paragraphs/
```

### Tasks in Code Comments

### 1. Build a vectorizer

> TASK: Build a vectorizer that splits strings into sequence of 1 to 3 characters instead of word tokens

**What it means**:
This task requires creating a [TfidfVectorizer](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) (or similar text vectorizer) configured to tokenize text into n-grams of 1 to 3 consecutive characters (e.g., "the" becomes "t", "th", "the", "h", "he", "e"). This is instead of the default word-based tokenization (splitting on spaces/punctuation).

**Why?**:
Character n-grams capture language-specific patterns (like frequent letter combinations) as "fingerprints" for classification, rather than relying on words. This is useful for language detection where vocabulary might vary but character sequences are distinctive.

**How to implement**:
Use [TfidfVectorizer(analyzer='char', ngram_range=(1, 3))](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) to achieve this. Assign it to a variable (e.g., `vectorizer`) for use in the pipeline.

This vectorizer will be part of the [Pipeline](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) (clf) built in the next task.

### Definitions

#### Vectorizer

- **General**: A tool or process that converts unstructured data (like text) into numerical vectors (arrays of numbers) that machine learning algorithms can process. This transforms qualitative data into quantitative features.
- **In scikit-learn (sklearn)**: Refers to classes like [TfidfVectorizer](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) or `CountVectorizer` from [sklearn.feature_extraction.text](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). These build feature matrices from text by tokenizing and weighting terms (e.g., TF-IDF scores). In the exercise, the vectorizer will create vectors based on character sequences.

#### Word Tokens

- **General**: Individual units (typically words) extracted from text during tokenization, where text is split into meaningful elements (e.g., "hello world" → ["hello", "world"]).
- **In scikit-learn (sklearn)**: The default analyzer in vectorizers like [TfidfVectorizer](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) tokenizes text into word tokens by splitting on whitespace and punctuation. The exercise task requires switching from word tokens to character-based tokens.

#### N-grams

- **General**: Contiguous sequences of n items (e.g., words, characters, or syllables) from a text. Examples: unigrams (n=1: single items), bigrams (n=2: pairs), trigrams (n=3: triples). Used to capture context or patterns.
- **In scikit-learn (sklearn)**: Configured via the `ngram_range` parameter in vectorizers (e.g., `ngram_range=(1, 3)` for 1-3 item sequences). In the exercise, this applies to characters (e.g., "the" → "t", "th", "the") instead of words, enabling language "fingerprints" based on frequent character combos.

#### 2. Build a pipeline

> TASK: Build a vectorizer / classifier pipeline using the previous analyzer the pipeline instance should stored in a variable named clf

**What it means**:
This task requires creating a [Pipeline](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) object that combines the character-based vectorizer (from the prior task) with a linear classifier (e.g., [Perceptron](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)). The pipeline integrates text vectorization and classification into a single model for training and prediction. Store the pipeline instance in a variable named [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html).

**Why?**:
Pipelines streamline the workflow by chaining preprocessing (vectorization) and modeling steps, ensuring consistent application during fit/predict. This builds a complete language detector using character n-gram features.

**How to implement**:
Use [Pipeline([('vectorizer', your_vectorizer), ('classifier', Perceptron())\])](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) and assign to [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). The vectorizer should be the one configured for 1-3 character n-grams. This [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) will be used for fitting and predicting in subsequent tasks.

#### 3. Fit the pipeline

> TASK: Fit the pipeline on the training set

**What it means**:
This task requires training (fitting) the [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) pipeline on the training data ([docs_train](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) and [y_train](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)). Fitting learns the model parameters, including vectorizing the text into character n-grams and training the classifier to predict languages.

**Why?**:
Fitting builds the model using labeled training data, enabling it to generalize and make predictions on unseen data. This step is essential before evaluation or prediction.

**How to implement**:
Call [clf.fit(docs_train, y_train)](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) after defining [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). This applies the vectorizer to transform text and trains the [Perceptron](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) classifier on the resulting features. The fitted [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) can then be used for predictions.

#### 4. Test

> TASK: Predict the outcome on the testing set in a variable named y_predicted

**What it means**:
This task requires using the fitted [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) pipeline to predict language labels for the test data ([docs_test](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)). Store the predictions in a variable named [y_predicted](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html).

**Why?**:
Predictions on the test set evaluate the model's performance by comparing [y_predicted](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html) to the true labels ([y_test](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html)). This assesses how well the model generalizes to unseen data.

**How to implement**:
After fitting [clf](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html), call [y_predicted = clf.predict(docs_test)](vscode-file://vscode-app/c:/Users/Brian/AppData/Local/Programs/Microsoft VS Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html). This applies the vectorizer and classifier to generate predictions, which are then used in the classification report and confusion matrix.



Note: This document was drafted using Grok Code Fast 1, 10/22/2025

