---
title: Math Concepts for AI
description: Basic algebra concepts needed for this course
keywords: 
generator: Typora
author: Brian Bird
---

<h1>Math Concepts for AI</h1>

**CS 212, AI Programming 1**

| Topics                               |                                   |
| ------------------------------------ | --------------------------------- |
| <mark>Overview, History of AI</mark> | Generative AI                     |
| Machine Learning: Symbolic           | Using LLMs in custom applications |
| Machine Learning: Statistical        | Custom chatbot creation           |
| Neural networks                      | LLM fine-tuning                   |
| Image recognition                    | Social and ethical issues of AI   |



<h2>Contents</h2>

- [Math to Review](#math-to-review)
  - [Equation of the Line](#equation-of-the-line)
- [Math You Might Not Know](#math-you-might-not-know)
  - [Statistics and Probability](#statistics-and-probability)
    - [Descriptive Statistics](#descriptive-statistics)
      - [Mean and Standard Error](#mean-and-standard-error)
    - [Variance and Standard Deviation](#variance-and-standard-deviation)
    - [Median](#median)
  - [Probability Distributioins](#probability-distributioins)
    - [Uniform Distribution](#uniform-distribution)
    - [Normal Distribution](#normal-distribution)
  - [Statistical Tests](#statistical-tests)
    - [Parametric vs. Nonparametric Tests](#parametric-vs-nonparametric-tests)
      - [Parametric Test: t-test](#parametric-test-t-test)
      - [Nonparametric Test: Mann–Whitney U](#nonparametric-test-mannwhitney-u)
    - [Interpreting the p-value](#interpreting-the-p-value)
    - [Thresholds and Significance](#thresholds-and-significance)
- [Linear Algebra](#linear-algebra)
  - [Vectors](#vectors)
  - [Matricies](#matricies)
  - [Matrix Multiplication](#matrix-multiplication)
    - [How It Works](#how-it-works)
    - [Example](#example)
- [References](#references)

## Math to Review

### Equation of the Line

y = mx + b

- Be able to calculate a line based on two points. 
- For a given line and x value, find the y value.



## Math You Might Not Know

### Statistics and Probability

Statistics and probability are vast fields, but in this course we will only focus on a few essential concepts relevant to the machine learning topics we are covering. We'll assume that at this point you're familiar with nothing more than basic ideas like coin flips and dice rolls.

#### Descriptive Statistics

Descriptive statistics are summary values we calculate from data to help us understand patterns, variation, and central tendencies. The most common ones are the **mean**, **median**, and **standard deviation**.

##### Mean and Standard Error

The **mean** (or average) is calculated by adding all measurements and dividing by the number of values. For example, if you're measuring flower lengths, the mean gives you the typical length.

To express how reliable that mean is, we use the **standard error of the mean (SE)**. It’s calculated as:


SE = \frac{\sigma}{\sqrt{n}}


Where:
-  \sigma  is the **standard deviation** (a measure of spread)
-  n  is the number of measurements

A smaller SE means the data points are tightly clustered around the mean, giving us more confidence in that value. We often report results as:

$$
\text{mean} \pm SE
$$
This range estimates where the true mean likely falls.

#### Variance and Standard Deviation

To calculate **standard deviation**, we first compute the **variance**:
1. Subtract each value from the mean
2. Square the result
3. Add all squared differences
4. Divide by  n - 1 

Then take the square root of the variance to get the standard deviation. It tells us how spread out the data is.

---

#### Median

The **median** is the middle value in a sorted dataset:
- If the number of values is odd, it’s the exact middle.
- If even, it’s the average of the two middle values.

The median is especially useful when data is skewed—like income, where a few very high earners can distort the mean. In such cases, the median gives a more representative central value.

### Probability Distributioins

A **probability distribution** describes how likely different values are to occur in a dataset. You can think of it as an oracle that generates numbers—when we train models, we treat our measured data as samples drawn from such a distribution.

This underlying source is called the **parent distribution**—the idealized generator our data approximates.

Probability distributions come in many forms. Two of the most common are *uniform distribution* and *normal distribution*.

#### Uniform Distribution

A uniform distribution assigns equal probability to all values within a range. For example, rolling a fair six-sided die gives each number (1–6) the same chance of appearing.

- **Notation**:


  x \sim U(a, b)


 means  x  is drawn uniformly from the interval between  a  and  b .

- **Range Bracketing**:
  -  U(0, 1) : excludes both bounds
  -  U[0, 1) : includes 0, excludes 1

Unless specified, uniform distributions can return real numbers, not just integers.

#### Normal Distribution

Also known as a **Gaussian distribution**, this is the classic bell curve. It centers around a **mean**  \bar{x} , with probabilities tapering off as values move away from the center. The **standard deviation**  \sigma  controls the spread.

**Notation**:
$$
x \sim N(\bar{x}, \sigma)
$$

 means  x  is sampled from a normal distribution with mean  \bar{x}  and standard deviation  \sigma .

This distribution is fundamental in statistics and machine learning due to its natural occurrence and useful mathematical properties.

Here’s a more concise and structured version of your explanation on statistical tests, broken into clear sections for clarity and precision:

### Statistical Tests

A **statistical test** helps us evaluate whether a hypothesis about data is likely true. Most often, we test whether two sets of measurements come from the same **parent distribution**—the underlying source that generates the data.

If the test statistic falls outside a certain range, we reject the hypothesis and infer that the two datasets likely come from different distributions.

#### Parametric vs. Nonparametric Tests

##### Parametric Test: t-test
- Assumes data is **normally distributed**
- Compares means between two samples
- Known for its simplicity and widespread use

##### Nonparametric Test: Mann–Whitney U
- Makes **no assumption** about data distribution
- Compares ranks rather than means
- Useful when data is skewed or not normally distributed

#### Interpreting the p-value

Both tests yield a **p-value**, which quantifies how likely it is to observe the test statistic (or something more extreme) if the hypothesis is true.

- **Low p-value** → evidence against the hypothesis
- **High p-value** → data is consistent with the hypothesis

#### Thresholds and Significance

- **Traditional cutoff**:  p < 0.05  (5% chance of observing the result by random variation)
- **Stronger evidence**:  p < 0.001 
- **Statistical significance**: When the p-value is low enough to confidently reject the hypothesis

Recent discussions suggest that  p = 0.05  may be too lenient, and more stringent thresholds are often preferred for stronger claims.



## Linear Algebra

Linear algebra is the branch of mathematics that is widely used in machine learning. It involves operations on vectors and matrices called linear transformations, such as multiplying two matricies.

### Vectors

A **mathematical vector** is an object that has both **magnitude** and **direction**. You can think of it as an arrow pointing from one location to another in space. In more practical terms, a vector is often represented as an **ordered list of numbers**, like `[3, 4]` in 2D or `[1, -2, 5]` in 3D, where each number corresponds to a component along an axis.

Vectors are used to describe things like velocity, force, or position in physics, and they’re fundamental in linear algebra, machine learning, and computer graphics. They support operations like addition, scaling, and dot products, which make them powerful tools for modeling and computation.

### Matricies

A **matrix** is a rectangular grid of numbers arranged in rows and columns. It’s a fundamental structure in mathematics used to represent data, perform linear transformations, and solve systems of equations. In Python and machine learning, matrices often model things like images, datasets, or weights in neural networks. You can think of a matrix as a 2D generalization of a vector.

### Matrix Multiplication

Matrix multiplication is a way of combining two matrices to produce a third, where the rows of the first matrix interact with the columns of the second. It’s not just element-by-element multiplication—it’s a structured operation that reflects how linear transformations compose.

#### How It Works

Suppose you have:

- Matrix **A** of size *m × n*
- Matrix **B** of size *n × p*

You can multiply **A × B** only if the **number of columns in A equals the number of rows in B**. The result is a new matrix **C** of size *m × p*.

Each entry in **C** is computed by taking the **dot product** of a row from **A** and a column from **B**.

#### Example

Let’s say:

$$
A = \begin{bmatrix}
1 & 2 \\
3 & 4
\end{bmatrix}
\quad
B =
\begin{bmatrix}
5 & 6 \\
7 & 8
\end{bmatrix}
$$




Then

$$
A \times B = 
\begin{bmatrix}
(1×5 + 2×7) & (1×6 + 2×8) \\
(3×5 + 4×7) & (3×6 + 4×8)
\end{bmatrix}
=
\begin{bmatrix}
19 & 22 \\
43 & 50
\end{bmatrix}
$$

## References

- *Practical Deep Learning: A Python-Based Introduction*, 2nd Edition, Ronald T. Kneusel, 2025, No Starch Press. 
  Chapter 0: Basic Linear Algebra, Statistics and Probability
- *Math for Deep Learning*, Ronald T. Kneusel, 2021, No Starch Press. 

- [Vectrors and Spaces](https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces)&mdash;Khan Academy

- [Matrix Transformations](https://www.khanacademy.org/math/linear-algebra/matrix-transformations)&mdash;Kahn Academy



---

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/) AI Programming 1 lecture notes by [Brian Bird](https://profbird.dev), written in <time>August 2025</time>, are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). 

MS Copilot GPT-4 was used to draft parts of these notes.

[^1]: 
[^2]: 