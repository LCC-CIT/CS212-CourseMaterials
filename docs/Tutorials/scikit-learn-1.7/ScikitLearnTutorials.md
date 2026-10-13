# scikit-learn Tutorials

- [An introduction to machine learning with scikit-learn](AnIntroductionToMachineLearningWithScikitLearn.md)
  - [Machine learning: the problem setting](AnIntroductionToMachineLearningWithScikitLearn.md#machine-learning-the-problem-setting)
  - [Loading an example dataset](AnIntroductionToMachineLearningWithScikitLearn.md#loading-an-example-dataset)
  - [Learning and predicting](AnIntroductionToMachineLearningWithScikitLearn.md#learning-and-predicting)
  - [Conventions](AnIntroductionToMachineLearningWithScikitLearn.md#conventions)
- [A tutorial on statistical-learning for scientific data processing](ATutorialOnStatisticalLearningForScientificDataProcessing.md)
  - [Statistical learning: the setting and the estimator object in scikit-learn](StatisticalLearningTheSettingAndTheEstimatorObjectInScikitLearn.md)
  - [Supervised learning: predicting an output variable from high-dimensional observations](SupervisedLearningPredictingAnOutputVariableFromHighDimensionalObservations.md)
  - [Model selection: choosing estimators and their parameters](ModelSelectionChoosingEstimatorsAndTheirParameters.md)
  - [Unsupervised learning: seeking representations of the data](UnsupervisedLearningSeekingRepresentationsOfTheData.md)
  - [Putting it all together](PuttingItAllTogether.md)
- [Working With Text Data](WorkingWithTextData.md)
  - [Tutorial setup](WorkingWithTextData.md#tutorial-setup)
  - [Loading the 20 newsgroups dataset](WorkingWithTextData.md#loading-the-20-newsgroups-dataset)
  - [Extracting features from text files](WorkingWithTextData.md#extracting-features-from-text-files)
  - [Training a classifier](WorkingWithTextData.md#training-a-classifier)
  - [Building a pipeline](WorkingWithTextData.md#building-a-pipeline)
  - [Evaluation of the performance on the test set](WorkingWithTextData.md#evaluation-of-the-performance-on-the-test-set)
  - [Parameter tuning using grid search](WorkingWithTextData.md#parameter-tuning-using-grid-search)
  - [Exercise 1: Language identification](WorkingWithTextData.md#exercise-1-language-identification)
  - [Exercise 2: Sentiment Analysis on movie reviews](WorkingWithTextData.md#exercise-2-sentiment-analysis-on-movie-reviews)
  - [Exercise 3: CLI text classification utility](WorkingWithTextData.md#exercise-3-cli-text-classification-utility)
  - [Where to from here](WorkingWithTextData.md#where-to-from-here)
- [Choosing the right estimator](ChoosingTheRightEstimatorScikitLearn142Documentation.html)
- <a href="https://scikit-learn.org/1.7/presentations.html" target="_blank">External Resources, Videos and Talks</a>
  - <a href="https://scikit-learn.org/1.7/presentations.html#new-to-scientific-python" target="_blank">New to Scientific Python?</a>
  - <a href="https://scikit-learn.org/1.7/presentations.html#external-tutorials" target="_blank">External Tutorials</a>
  - <a href="https://scikit-learn.org/1.7/presentations.html#videos" target="_blank">Videos</a>

## Note on IPython

Some of the tutorials have code blocks start with >>> and are intended to be executed in <a href="https://ipython.org/" target="_blank">IPython</a> using doctest_mode. IPPython has not been updated since 2020 (it is replaced by Jupyter notbooks).  But you can simply execute the code in the Python interactive console by copying the code in a way that omits the >>> at the beginning of the line.  


---

These tutorials are updated from "scikit-learn Tutorials" by scikit-learn developers. Original Source: https://scikit-learn.org/1.4/tutorial/index.html under the <a href="https://opensource.org/license/BSD-3-clause" target="_blank">BSD License</a>.  

---

The code examples and text in this tutorial were updated for scikit-learn version 1.7 by Brian Bird using Claude Sonnet 4, 10/19/2025

---

[^1]:The `%doctest_mode` command in IPython is particularly useful for developers who work with Python documentation. It allows for easy copying and pasting of code snippets that start with >>> into IPython, even if they have extra leading whitespace. This is particularly helpful for doctests, where you might have docstrings that start with >>>. By using %doctest_mode, you can directly paste these snippets into your code without leaving the IPython session, ensuring that your documentation is up-to-date and correctly formatted.
