---
title: Data Set Concepts and Prep
description: Concepts related to data and how to prepare a data set
generator: Typora
author: Brian Bird
---

<h1>Data Set Concepts and Preperation</h1>

**CS 210, Intro to AI Programming**

| Topics                                                  |                                                  |
| ------------------------------------------------------- | ------------------------------------------------ |
| 1. What is AI, Python                                   | 6. Artificial Neural Networks: Image recognition |
| 2.  Symbolic AI: rule-based                             | 7. Generative AI                                 |
| 3.  Classical Machine Learning<br />Bayes' Rule         | 8. Custom chatbot                                |
| 4. <mark>scikit-learn<br />Working withData Sets</mark> | 9. LLM fine-tuning                               |
| 5. ML: Scikit Learn Part 2                              | 10. Ethics                                       |

<h2>Table of Contents</h2>

[TOC]

# Working with Data

Developing a proper dataset is the most crucial part of building a successful machine learning model, as performance depends entirely on the quality of the data ("garbage in, garbage out").

## I. Core Components of a Dataset

### A. Classes and Labels

- **Classes:** Discrete categories (e.g., dog breed, flower type) that the model predicts.
- **Labels:** Identifiers assigned to each input to represent its class.
  - Usually represented as **integers** starting with 0 (e.g., 0, 1, 2, ...).

### B. Features and Feature Vectors

- **Features:** The numerical inputs the model takes (e.g., pixels, measurements, sound frequencies).
- **Feature Vector:** The set of numbers (features) used as the input for a single sample.
- The goal of training is for the model to learn the relationship between input features and the output label.

### C. Types of Features

1. **Floating-Point Numbers (Continuous):** Numbers with a decimal point (real numbers), used directly by most models (e.g., `2.33 cm`).
2. **Interval Values (Discrete):** Integers where the difference (interval) between values is meaningful and equal (e.g., pixel intensity, number of petals).
3. **Ordinal Values:** Express an ordering, but the difference between the values is **not** necessarily the same (e.g., educational level encoded as 1, 2, 3).
4. **Categorical Values:** Numbers used as codes to express a category, with no inherent relationship between them (e.g., 0 for male, 1 for female, 0 for red).
   - **One-Hot Encoding:** A technique to make categorical values ordinal by mapping them to a binary vector (one feature per category), where only one element is `1` (e.g., male $\to [1, 0]$, female $\to [0, 1]$).

## II. Feature Selection and Dimensionality

### A. Feature Selection Rule of Thumb

- The feature vector should contain **only** features that help the model separate the classes and generalize to new data.

### B. The Curse of Dimensionality

- As the number of features (**dimensions**) increases, the amount of training data required to get a representative sampling of the feature space increases **dramatically** (approximately as $10^d$).
- This makes it impossible to fully sample high-dimensional spaces (like a full-resolution color image).

## III. Features of a Good Dataset

### A. Interpolation vs. Extrapolation

- **Interpolation:** Estimating within the known range of the training data. Models are generally accurate here.
- **Extrapolation:** Estimating outside the known range of the training data. Models often fail or perform poorly here.
- A good dataset must be a **comprehensive representation** of the full range of variations within the classes the model will encounter.

### B. The Parent Distribution

- The dataset is assumed to be a sample from an **unknown data generator** (the parent distribution).
- The training data, test data, and data used for prediction **must all come from the same parent distribution**.

### C. Prior Class Probabilities

- The dataset should generally **match the probability** with which each class appears "in the wild."
- **Exception:** For **rare classes** (imbalanced data), the ratio in the training set may be intentionally balanced (e.g., 10:1 instead of 5000:1) to give the model enough examples to learn the key features.

### D. Confusers (Hard Negatives)

- The dataset should include **confusers** (or **hard negatives**)—examples that are similar enough to a target class to be mistaken for it, but are actually in the "not class" category (e.g., including images of wolves in a "not dog" class when training a "dog vs. not dog" classifier).

### E. Dataset Size

- The ideal answer is "all of it," but a practical size involves a trade-off between **accuracy** and the **time/expense** of data acquisition.
- Larger models (more parameters) require more training data.

## IV. Data Preparation Techniques

### A. Scaling Features

- **Problem:** Some features may dominate others due to a wider range, causing problems for certain models.
- **Mean Centering:** Subtracting the mean (average) value of the feature from every sample, resulting in a new mean of 0.
- **Standardization/Normalizing:** Subtracting the mean and dividing by the standard deviation ($\sigma$) so that the features have **0 mean and a standard deviation of 1**.

### B. Missing Features

- Most models cannot accept missing data.
- **Solution (Simple Imputation):** Replacing missing features with the **mean value** of that feature over the entire dataset.

## V. Splitting the Dataset

We split the full dataset into three non-overlapping subsets:

| **Subset**          | **Purpose**                                                  | **Typical Size** |
| ------------------- | ------------------------------------------------------------ | ---------------- |
| **Training Data**   | Used to train the model and adjust its parameters.           | 90%              |
| **Validation Data** | Used **during training** to tune the model's architecture (hyperparameters) and decide when to stop. | 5%               |
| **Test Data**       | Used **only once** at the very end to evaluate the final, complete model's performance. | 5%               |

### A. Partitioning Methods

1. **Partitioning by Class (Exact Split):** Manually ensuring that the class ratios (prior probabilities) are preserved exactly in each subset. (Tedious, but useful for small or severely imbalanced datasets).
2. **Random Sampling:** Randomizing the full dataset and slicing off the sections for training, validation, and test. (Simpler, and generally sufficient for large datasets).

### B. k-Fold Cross Validation

- **Use Case:** Ideal for **small datasets** intended for traditional machine learning models.
- **Process:** Partition the full dataset into $k$ non-overlapping groups (folds). Train $k$ models, each time using one fold for testing and the remaining $k-1$ folds for training.
- **Benefit:** Ensures every sample is used for both training and testing, and the averaged results give a better estimate of model performance.

## VI. Data Inspection

- It is essential to **look at your data** to check for problems.
- **Mislabeled Data:** Avoid label noise, especially in large datasets collected from external sources.
- **Missing or Outlier Data:** Check for features with large percentages of missing values (eliminate the feature) or extreme outliers (consider removing the samples).
- **Statistical Tools:** Use the **mean**, **standard deviation** ($\sigma$), **median**, and **standard error** ($SE$) to summarize the data.
- **Visualization:** Use a **box plot** to visualize the distribution, median, quartiles (Q1, Q3), and easily spot **outliers** (values outside the whiskers).
- **Cautionary Tales:** Be mindful of **unintended consequences**; models might learn confounding factors instead of the desired features (e.g., learning the difference between sunny and cloudy days instead of tanks and non-tanks).

## Reference

- Ch. 4, "Working with Data", *Practical Deep Learning*, First Edition, by Ronald T. Kneusel, No Starch Press, 2021.
- [Build and test your first machine learning model using Python and scikit-learn](https://developer.ibm.com/tutorials/build-and-test-your-first-machine-learning-model-using-python-and-scikit-learn/) by Samaya Madhavan and Mark Sturdevant, IBM Developer, accessed 10/20/2025.
- [Working with Categorical Data](https://developers.google.com/machine-learning/crash-course/categorical-data) in Machine Learning Crash Course, Google, accessed 10/20/2025.

---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) Intro to AI Programming lecture notes by [Brian Bird](https://profbird.dev), written in <time>2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

---
Google Gemini Flash 2.5 Pro was used to draft these notes.