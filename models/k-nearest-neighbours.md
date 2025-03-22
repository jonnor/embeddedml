# k-nearest neighbours
Aka kNN.

Very simple but powerful non-linear classifier.
Trivial to support on-edge learning, as it only requires storing new datapoints.
Main weakness: Poor space and compute complexity for large datasets with many features.

A trivical brute force is O(n_samples*n_features*k)
If computing and storing distances on the fly (requriring O(n_samples) more space),
can get O(n_samples*n_features + k*n_samples), which is faster for k > 1
By additionally using quicksort on the compute distances, one can get O(n_samples*n_features)
https://stats.stackexchange.com/questions/219655/k-nn-computational-complexity/219664

Common query optimizations is to use KD-tree (axis aligned) or Ball-tree (spherical)
kd-tree construction is O(n_samples log(n_samples)),
1-N query is O(log(n_samples)) best case and O(n_samples) worst case -
but is O (C**n_features). 
KD index only makes sense for N >> 2**n_features
Example 2**12 = 4096

## Feature space
As classic kNN does no feature weighting or selection it is important to ensure they are all informative.
The standard distance functions also do not take covariance into account.
So the features should be pre-processed to be infomative, orthogonal and weighted/scaled.
In practice that becomes part of the learning method.
Common approaches is feature selection, PCA transformation.

Several feature weighting approaches and distance metric learning approaches has been proposed.
metrics-learn has methods for learning metrics
that are linear transformation
http://contrib.scikit-learn.org/metric-learn/generated/metric_learn.NCA.html
can return a low-dimensionality transformation
Metric learning is especially useful for one-shot and few-shot learning

## Related methods

Related methods are Radius Neighbour classifier.
The Local Outlier Factor anomaly detection method.
And the DBSCAN clustering/anomaly method.

## Adaptations to embedded devices

[ProtoNN](https://www.microsoft.com/en-us/research/uploads/prod/2017/06/protonn.pdf) by Microsoft Research.
Uses a kNN model, but only storing a much smaller set of "prototypes" instead of the whole training set.

## Embedded implementation

Number of datapoints can easily grow outside of what can be stored in memory.
And when doing on-device learning, need a way to persist things.
Therefore the implementation should support loading instances on-demand.
Should also have an in-RAM and in-PROGMEM standard loaders.

int
read_samples(float *out, int n_features, int n_samples) 

n_samples is an upper limit
May return a lower amount of samples than requested
0 means no more samples.
Negative values means error.

Need to decide whether to do implement KD/ball-trees
Is needed for full scikit-learn compatibility.
For just inference, should be possible to pre-generate the index/trees also.

## Existing implementations

- Very basic example
https://github.com/joaocarvalhoopen/KNN__K_Nearest_Neighbors_in_C_Plus_Plus/blob/master/KNN__K_Nearest_Neighbors.cpp
- Arduino_KNN - Arduino library
https://github.com/arduino-libraries/Arduino_KNN

## Approximate Nearest Neighbours (ANN)

Approximate methods do not guarantee to give the kth nearest neighbour,
but something in the close vicinity.
Widely researched and adopted for information retrieval,
especially in combination with a learned vector embedding.
Known as Vector Similarity Search.

### Approximate kNN

Extension of classic kNN (using kd or ball trees)
Instead of pruning bins which are within "radius",
will prune bins that are within radius/alpha
Where alpha is a hyperparameter.
Significantly reduces query complexity for large alpha,
often with minimal loss in predictive performance

### Locality Sensitive Hashing (LSM)
Alternative to kd-trees
https://www.coursera.org/lecture/ml-clustering-and-retrieval/limitations-of-kd-trees-DA2Hg
https://www.coursera.org/lecture/ml-clustering-and-retrieval/lsh-as-an-alternative-to-kd-trees-HfFv9
https://www.coursera.org/lecture/ml-clustering-and-retrieval/using-random-lines-to-partition-points-KFXqi
Approximate method - not quite kNN
Proabilitist estimation of our approximation
LSM uses binning. BInary binning, using sign of a score
Using a hash-table for lookup.
Can lookup the bin using the relevant 
Then can do kNN only at neighbours inside the bin
How to find good lines? Random can be done
The more lines, the more bins, the fewer datapoints per bin
Can improve search quality by searching neighbouring bins.
Neighbour: 1 bit off current bin index.
Can search until reaching a compute budget threshold,
or until reaching a point within a radius epsilon
Has outlier/anomaly properties built in? Bins are empty - outlier



# Nearest Neighbour models

Canonical example is kNN.
However conventional kNN requires all training points to be stored, which is typically way too much for a microcontroller.

Variants

* Condensed kNN. Data reduction technique.
Selects prototypes for each class and eliminates points that are not needed.
[imbalanced-learn](http://contrib.scikit-learn.org/imbalanced-learn/stable/auto_examples/under-sampling/plot_condensed_nearest_neighbour.html?highlight=condensed)
* Fast condensed nearest neighbor rule. 2005. [Paper](https://dl.acm.org/citation.cfm?id=1102355)
* Approximate nearest neighbours.

References

* [Survey of Nearest Neighbor Condensing Techniques](https://www.thesai.org/Downloads/Volume2No11/Paper%2010-%20Survey%20of%20Nearest%20Neighbor%20Condensing%20Techniques.pdf)
* [Fast Classification with Binary Prototypes](http://users.ices.utexas.edu/~zhongkai/bnc.pdf)


## Attribute weighting / feature weighting for KNN



A feature weighted K-nearest neighbor algorithm based on association rules
https://link.springer.com/article/10.1007/s12652-024-04793-z
2024.
! not available
Researchers propose different feature weightings, such as correlation-based feature selection, mutual information, and chi-square feature selection.
This paper presents a new feature weighting technique based on association rules and information gain.

The Utility of Feature Weighting in Nearest-Neighbor Algorithms
Ron Kohavi, 1997
Proposed DIET. 
Found that either using 0 or 1 as feature weight was difficult to outperform.

A Feature-Weighted Rule for the K-Nearest Neighbor
Mladenova, 2021
! not available
https://www.researchgate.net/publication/356401933_A_Feature-Weighted_Rule_for_the_K-Nearest_Neighbor


Feature importance K-nearest neighbors (FIKNN)
2025
https://www.sciencedirect.com/science/article/pii/S2307410824001494
Uses random forest algorithm to derive importance weights for features
The importance calculated for each feature is normalized such that the sum of all importance scores equals one.

Hybrid dynamic k-nearest-neighbour and distance and attribute weighted method for classiﬁcation
Wu, Cai, 2012
Describes dynamic k-nearest- neighbour with distance and attribute weighted, simply DKNDAW
Refers to existing papers for computing feature/attribute weights.
gain ratio (GR) (Zhang and Sheng, 2005),
correlation-based feature selection (CFS) attribute selection algorithm (Hall, 2000),
mutual information (Jiang and Zhang, 2006)
Hall (2007) the degree to which they depended on the values of other attributes


Dynamic K-Nearest-Neighbor with Distance and attribute weighted for classification
Jia Wu; Zhihua Cai; Zhechao Gao, 2010
! not available
 In DKNDAW, we mixed dynamic selected, distance weighted and attribute weighted methods.
Tested on the whole 36 standard UCI data sets which are downloaded from Weka

Dynamic Feature Scaling for K-Nearest Neighbor Algorithm
https://arxiv.org/abs/1811.05062
Chandrasekaran Anirudh Bhardwaj1, Megha Mishra 1, Kalyani Desikan 2018
Proposes to assign weights to individual feature with the
help of out of bag errors obtained from constructing multiple decision tree models.
Assigning feature weights based on the feature importance obtained while training a Random Forest Model.
Constructing different models on different subsets of dimensions leads to an easy calculation of
out-of-bag error for each particular dimension, which can further be used as a metric for feature
importance.
Feature Importance based Dynamic Scaling method (henceforth abbreviated as FIDS),



