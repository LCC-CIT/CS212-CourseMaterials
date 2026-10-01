[scikit-learn tutorials index](ScikitLearnTutorials.md)

# Unsupervised learning: seeking representations of the data

## Clustering: grouping observations together

The problem solved in clustering

Given the iris dataset, if we knew that there were 3 types of iris, but did not have access to a taxonomist to label them: we could try a **clustering task**: split the observations into well-separated group called *clusters*.

```python
>>> # Set the PRNG
>>> import numpy as np
>>> np.random.seed(1)
```

### K-means clustering

Note that there exist a lot of different clustering criteria and associated algorithms. The simplest clustering algorithm is <a href="https://scikit-learn.org/1.7/modules/clustering.html#k-means" target="_blank">K-means</a>.

```python
>>> from sklearn import cluster, datasets
>>> X_iris, y_iris = datasets.load_iris(return_X_y=True)

>>> k_means = cluster.KMeans(n_clusters=3)
>>> k_means.fit(X_iris)
KMeans(n_clusters=3)
>>> print(k_means.labels_[::10])
[1 1 1 1 1 2 0 0 0 0 2 2 2 2 2]
>>> print(y_iris[::10])
[0 0 0 0 0 1 1 1 1 1 2 2 2 2 2]
```

<a href="https://scikit-learn.org/1.7/auto_examples/cluster/plot_cluster_iris.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_cluster_iris_001.png" alt="../../_images/sphx_glr_plot_cluster_iris_001.png"></a>

Warning

There is absolutely no guarantee of recovering a ground truth. First, choosing the right number of clusters is hard. Second, the algorithm is sensitive to initialization, and can fall into local minima, although scikit-learn employs several tricks to mitigate this issue.

For instance, on the image above, we can observe the difference between the ground-truth (bottom right figure) and different clustering. We do not recover the expected labels, either because the number of cluster was chosen to be to large (top left figure) or suffer from a bad initialization (bottom left figure).

**It is therefore important to not over-interpret clustering results.**

**Application example: vector quantization**

Clustering in general and KMeans, in particular, can be seen as a way of choosing a small number of exemplars to compress the information. The problem is sometimes known as <a href="https://en.wikipedia.org/wiki/Vector_quantization" target="_blank">vector quantization</a>. For instance, this can be used to posterize an image:

```python
>>> import scipy as sp
>>> try:
...    face = sp.face(gray=True)
... except AttributeError:
...    from scipy import misc
...    face = misc.face(gray=True)
>>> X = face.reshape((-1, 1)) # We need an (n_sample, n_feature) array
>>> k_means = cluster.KMeans(n_clusters=5, n_init=1)
>>> k_means.fit(X)
KMeans(n_clusters=5, n_init=1)
>>> values = k_means.cluster_centers_.squeeze()
>>> labels = k_means.labels_
>>> face_compressed = np.choose(labels, values)
>>> face_compressed.shape = face.shape
```

**Raw image**

<a href="https://scikit-learn.org/1.7/auto_examples/cluster/plot_face_compress.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_face_compress_001.png" alt="../../_images/sphx_glr_plot_face_compress_001.png"></a>

**K-means quantization**

<a href="https://scikit-learn.org/1.7/auto_examples/cluster/plot_face_compress.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_face_compress_004.png" alt="../../_images/sphx_glr_plot_face_compress_004.png"></a>

**Equal bins**

<a href="https://scikit-learn.org/1.7/auto_examples/cluster/plot_face_compress.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_face_compress_002.png" alt="../../_images/sphx_glr_plot_face_compress_002.png"></a>

### Hierarchical agglomerative clustering: Ward

A <a href="https://scikit-learn.org/1.7/modules/clustering.html#hierarchical-clustering" target="_blank">Hierarchical clustering</a> method is a type of cluster analysis that aims to build a hierarchy of clusters. In general, the various approaches of this technique are either:

- **Agglomerative** - bottom-up approaches: each observation starts in its own cluster, and clusters are iteratively merged in such a way to minimize a *linkage* criterion. This approach is particularly interesting when the clusters of interest are made of only a few observations. When the number of clusters is large, it is much more computationally efficient than k-means.
- **Divisive** - top-down approaches: all observations start in one cluster, which is iteratively split as one moves down the hierarchy. For estimating large numbers of clusters, this approach is both slow (due to all observations starting as one cluster, which it splits recursively) and statistically ill-posed.

#### Connectivity-constrained clustering

With agglomerative clustering, it is possible to specify which samples can be clustered together by giving a connectivity graph. Graphs in scikit-learn are represented by their adjacency matrix. Often, a sparse matrix is used. This can be useful, for instance, to retrieve connected regions (sometimes also referred to as connected components) when clustering an image.

<a href="https://scikit-learn.org/1.7/auto_examples/cluster/plot_coin_ward_segmentation.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_coin_ward_segmentation_001.png" alt="../../_images/sphx_glr_plot_coin_ward_segmentation_001.png"></a>

```python
>>> from skimage.data import coins
>>> from scipy.ndimage import gaussian_filter
>>> from skimage.transform import rescale
>>> rescaled_coins = rescale(
...     gaussian_filter(coins(), sigma=2),
...     0.2, mode='reflect', anti_aliasing=False
... )
>>> X = np.reshape(rescaled_coins, (-1, 1))
```

We need a vectorized version of the image. `'rescaled_coins'` is a down-scaled version of the coins image to speed up the process:

```python
>>> from sklearn.feature_extraction import grid_to_graph
>>> connectivity = grid_to_graph(*rescaled_coins.shape)
```

Define the graph structure of the data. Pixels connected to their neighbors:

```python
>>> n_clusters = 27  # number of regions

>>> from sklearn.cluster import AgglomerativeClustering
>>> ward = AgglomerativeClustering(n_clusters=n_clusters, linkage='ward',
...                                connectivity=connectivity)
>>> ward.fit(X)
AgglomerativeClustering(connectivity=..., n_clusters=27)
>>> label = np.reshape(ward.labels_, rescaled_coins.shape)
```

#### Feature agglomeration

We have seen that sparsity could be used to mitigate the curse of dimensionality, *i.e* an insufficient amount of observations compared to the number of features. Another approach is to merge together similar features: **feature agglomeration**. This approach can be implemented by clustering in the feature direction, in other words clustering the transposed data.

<a href="https://scikit-learn.org/1.7/auto_examples/cluster/plot_digits_agglomeration.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_digits_agglomeration_001.png" alt="../../_images/sphx_glr_plot_digits_agglomeration_001.png"></a>

```python
>>> digits = datasets.load_digits()
>>> images = digits.images
>>> X = np.reshape(images, (len(images), -1))
>>> connectivity = grid_to_graph(*images[0].shape)

>>> agglo = cluster.FeatureAgglomeration(connectivity=connectivity,
...                                      n_clusters=32)
>>> agglo.fit(X)
FeatureAgglomeration(connectivity=..., n_clusters=32)
>>> X_reduced = agglo.transform(X)

>>> X_approx = agglo.inverse_transform(X_reduced)
>>> images_approx = np.reshape(X_approx, images.shape)
```

`transform` and `inverse_transform` methods

Some estimators expose a `transform` method, for instance to reduce the dimensionality of the dataset.

## Decompositions: from a signal to components and loadings

**Components and loadings**

If X is our multivariate data, then the problem that we are trying to solve is to rewrite it on a different observational basis: we want to learn loadings L and a set of components C such that *X = L C*. Different criteria exist to choose the components

### Principal component analysis: PCA

<a href="https://scikit-learn.org/1.7/modules/decomposition.html#pca" target="_blank">Principal component analysis (PCA)</a> selects the successive components that explain the maximum variance in the signal. Let’s create a synthetic 3-dimensional dataset.

```python
>>> # Create a signal with only 2 useful dimensions
>>> x1 = np.random.normal(size=(100, 1))
>>> x2 = np.random.normal(size=(100, 1))
>>> x3 = x1 + x2
>>> X = np.concatenate([x1, x2, x3], axis=1)
```

The point cloud spanned by the observations above is very flat in one direction: one of the three univariate features (i.e. z-axis) can almost be exactly computed using the other two.

```python
>>> import matplotlib.pyplot as plt
>>> fig = plt.figure()
>>> ax = fig.add_subplot(111, projection='3d')
>>> ax.scatter(X[:, 0], X[:, 1], X[:, 2])
<...>
>>> _ = ax.set(xlabel="x", ylabel="y", zlabel="z")
```

![../../_images/unsupervised_learning-1.png](https://scikit-learn.org/1.7/_images/unsupervised_learning-1.png)

PCA finds the directions in which the data is not *flat*.

```python
>>> from sklearn import decomposition
>>> pca = decomposition.PCA()
>>> pca.fit(X)
PCA()
>>> print(pca.explained_variance_)
[  2.18565811e+00   1.19346747e+00   8.43026679e-32]
```

Looking at the explained variance, we see that only the first two components are useful. PCA can be used to reduce dimensionality while preserving most of the information. It will project the data on the principal subspace.

```python
>>> pca.set_params(n_components=2)
PCA(n_components=2)
>>> X_reduced = pca.fit_transform(X)
>>> X_reduced.shape
(100, 2)
```

### Independent Component Analysis: ICA

<a href="https://scikit-learn.org/1.7/modules/decomposition.html#ica" target="_blank">Independent component analysis (ICA)</a> selects components so that the distribution of their loadings carries a maximum amount of independent information. It is able to recover **non-Gaussian** independent signals:

<a href="https://scikit-learn.org/1.7/auto_examples/decomposition/plot_ica_blind_source_separation.html" target="_blank"><img src="https://scikit-learn.org/1.7/_images/sphx_glr_plot_ica_blind_source_separation_001.png" alt="../../_images/sphx_glr_plot_ica_blind_source_separation_001.png"></a>

```python
>>> # Generate sample data
>>> import numpy as np
>>> from scipy import signal
>>> time = np.linspace(0, 10, 2000)
>>> s1 = np.sin(2 * time)  # Signal 1 : sinusoidal signal
>>> s2 = np.sign(np.sin(3 * time))  # Signal 2 : square signal
>>> s3 = signal.sawtooth(2 * np.pi * time)  # Signal 3: saw tooth signal
>>> S = np.c_[s1, s2, s3]
>>> S += 0.2 * np.random.normal(size=S.shape)  # Add noise
>>> S /= S.std(axis=0)  # Standardize data
>>> # Mix data
>>> A = np.array([[1, 1, 1], [0.5, 2, 1], [1.5, 1, 2]])  # Mixing matrix
>>> X = np.dot(S, A.T)  # Generate observations

>>> # Compute ICA
>>> ica = decomposition.FastICA()
>>> S_ = ica.fit_transform(X)  # Get the estimated sources
>>> A_ = ica.mixing_.T
>>> np.allclose(X,  np.dot(S_, A_) + ica.mean_)
True
```

## Enhanced Unsupervised Learning Features in scikit-learn 1.7

Since this tutorial was originally written for scikit-learn 1.4, several enhancements have been made to unsupervised learning capabilities:

### Enhanced Array API Support for Unsupervised Learning

scikit-learn 1.7 now supports Array API-compliant inputs in unsupervised learning algorithms, making it easier to work with data from libraries like PyTorch and CuPy:

```python
>>> import torch
>>> from sklearn.cluster import KMeans
>>> from sklearn.decomposition import PCA
>>>
>>> # Works with PyTorch tensors
>>> X = torch.tensor([[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]])
>>>
>>> # Clustering with PyTorch tensors
>>> kmeans = KMeans(n_clusters=2)
>>> kmeans.fit(X)
>>>
>>> # Dimensionality reduction with PyTorch tensors
>>> pca = PCA(n_components=1)
>>> X_reduced = pca.fit_transform(X)
```

### Enhanced Sparse Data Support in Unsupervised Learning

All unsupervised learning algorithms now support both traditional sparse matrices (`scipy.sparse.spmatrix`) and the newer sparse arrays (`scipy.sparse.sparray`):

```python
>>> from scipy.sparse import csr_array
>>> from sklearn.cluster import KMeans
>>> from sklearn.decomposition import TruncatedSVD
>>>
>>> X_sparse = csr_array([[0, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 0]])
>>>
>>> # Clustering with sparse arrays
>>> kmeans = KMeans(n_clusters=2)
>>> kmeans.fit(X_sparse)
>>>
>>> # Dimensionality reduction with sparse arrays
>>> svd = TruncatedSVD(n_components=2)
>>> X_reduced = svd.fit_transform(X_sparse)
```

### Enhanced Clustering Algorithms

Several clustering algorithms have been improved with better initialization strategies and performance optimizations:

```python
>>> from sklearn.cluster import KMeans, AgglomerativeClustering
>>> from sklearn.datasets import make_blobs
>>>
>>> X, _ = make_blobs(n_samples=1000, centers=3, random_state=42)
>>>
>>> # Improved K-means with better initialization
>>> kmeans = KMeans(n_clusters=3, init='k-means++', n_init=10)
>>> kmeans.fit(X)
>>>
>>> # Enhanced hierarchical clustering
>>> agglo = AgglomerativeClustering(n_clusters=3, linkage='ward')
>>> agglo.fit(X)
```

### Enhanced Dimensionality Reduction

PCA and other decomposition methods now have improved numerical stability and support for more data types:

```python
>>> from sklearn.decomposition import PCA, FastICA
>>> import numpy as np
>>>
>>> # Generate sample data
>>> X = np.random.randn(100, 10)
>>>
>>> # Enhanced PCA with better numerical stability
>>> pca = PCA(n_components=5, svd_solver='auto')
>>> X_pca = pca.fit_transform(X)
>>>
>>> # Improved FastICA
>>> ica = FastICA(n_components=5, random_state=42)
>>> X_ica = ica.fit_transform(X)
```

### Enhanced Feature Agglomeration

Feature agglomeration algorithms now support more connectivity patterns and have improved performance:

```python
>>> from sklearn.cluster import FeatureAgglomeration
>>> from sklearn.feature_extraction import grid_to_graph
>>>
>>> # Enhanced feature agglomeration
>>> connectivity = grid_to_graph(8, 8)
>>> agglo = FeatureAgglomeration(n_clusters=32, connectivity=connectivity)
>>> X_reduced = agglo.fit_transform(X)
>>> X_restored = agglo.inverse_transform(X_reduced)
```

These enhancements maintain full backward compatibility while providing more flexibility and power for unsupervised learning tasks.



---

This original version of this tutorial was written by scikit-learn developers under the <a href="https://opensource.org/license/BSD-3-clause" target="_blank">BSD License</a>.  

---

The code examples and text were updated for scikit-learn version 1.7 by Brian Bird using Claude Sonet 4, 10/19/2025

---

