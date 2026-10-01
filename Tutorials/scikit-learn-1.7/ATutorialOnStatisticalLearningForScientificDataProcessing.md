[scikit-learn tutorials index](ScikitLearnTutorials.md)

# A tutorial on statistical-learning for scientific data processing

Statistical learning

<a href="https://en.wikipedia.org/wiki/Machine_learning" target="_blank">Machine learning</a> is a technique with a growing importance, as the size of the datasets experimental sciences are facing is rapidly growing. Problems it tackles range from building a prediction function linking different observations, to classifying observations, or learning the structure in an unlabeled dataset.

This tutorial will explore *statistical learning*, the use of machine learning techniques with the goal of <a href="https://en.wikipedia.org/wiki/Statistical_inference" target="_blank">statistical inference</a>: drawing conclusions on the data at hand.

Scikit-learn is a Python module integrating classic machine learning algorithms in the tightly-knit world of scientific Python packages (<a href="https://www.numpy.org/" target="_blank">NumPy</a>, <a href="https://scipy.org/" target="_blank">SciPy</a>, <a href="https://matplotlib.org/" target="_blank">matplotlib</a>).

- [Statistical learning: the setting and the estimator object in scikit-learn](StatisticalLearningTheSettingAndTheEstimatorObjectInScikitLearn.md)
  - [Datasets](StatisticalLearningTheSettingAndTheEstimatorObjectInScikitLearn.md#datasets)
  - [Estimators objects](StatisticalLearningTheSettingAndTheEstimatorObjectInScikitLearn.md#estimators-objects)
- [Supervised learning: predicting an output variable from high-dimensional observations](SupervisedLearningPredictingAnOutputVariableFromHighDimensionalObservations.md)
  - [Nearest neighbor and the curse of dimensionality](SupervisedLearningPredictingAnOutputVariableFromHighDimensionalObservations.md#nearest-neighbor-and-the-curse-of-dimensionality)
  - [Linear model: from regression to sparsity](SupervisedLearningPredictingAnOutputVariableFromHighDimensionalObservations.md#linear-model-from-regression-to-sparsity)
  - [Support vector machines (SVMs)](SupervisedLearningPredictingAnOutputVariableFromHighDimensionalObservations.md#support-vector-machines-svms)
- [Model selection: choosing estimators and their parameters](ModelSelectionChoosingEstimatorsAndTheirParameters.md)
  - [Score, and cross-validated scores](ModelSelectionChoosingEstimatorsAndTheirParameters.md#score-and-cross-validated-scores)
  - [Cross-validation generators](ModelSelectionChoosingEstimatorsAndTheirParameters.md#cross-validation-generators)
  - [Grid-search and cross-validated estimators](ModelSelectionChoosingEstimatorsAndTheirParameters.md#grid-search-and-cross-validated-estimators)
- [Unsupervised learning: seeking representations of the data](UnsupervisedLearningSeekingRepresentationsOfTheData.md)
  - [Clustering: grouping observations together](UnsupervisedLearningSeekingRepresentationsOfTheData.md#clustering-grouping-observations-together)
  - [Decompositions: from a signal to components and loadings](UnsupervisedLearningSeekingRepresentationsOfTheData.md#decompositions-from-a-signal-to-components-and-loadings)
- [Putting it all together](PuttingItAllTogether.md)
  - [Pipelining](Pipelining.md)
  - [Face recognition with eigenfaces](PuttingItAllTogether.md#face-recognition-with-eigenfaces)
  - [Open problem: Stock Market Structure](PuttingItAllTogether.md#open-problem-stock-market-structure)



---

This original version of this tutorial was written by scikit-learn developers under the <a href="https://opensource.org/license/BSD-3-clause" target="_blank">BSD License</a>.  

---

The code examples and text were updated for scikit-learn version 1.7 by Brian Bird using Claude Sonet 4, 10/19/2025

---

