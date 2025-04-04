

Variations

* Random Forests
* Extremely Randomized Trees. ExtraTrees
* Gradient Boosted Trees
* Multiple Additive Regression Trees. Lambda-MART. λ-MART. 
* Gradient Boosted Regression Trees (GBRT)

People who need the same

* https://stats.stackexchange.com/questions/208165/generate-code-for-sklearns-gradientboostingclassifier
* https://github.com/ajtulloch/sklearn-compiledtrees/issues/3

Resources

* [Awesome decision tree papers](https://github.com/benedekrozemberczki/awesome-decision-tree-papers).
Large curated list of papers from top conferences from last 30 years.
* [libextratrees](https://github.com/paolo-losi/libextratrees/), C implementation of inference+training. Clean code.
Uses dynamic allocation and floats.
* Standalone example of Random Forest implementation in Python, with results.
[1](https://machinelearningmastery.com/implement-random-forest-scratch-python/), shows the principles well.
* [Current peak based device classification in NILM on a low-cost embedded platform using extra-trees](http://ieeexplore.ieee.org/document/8284200/). Published November 2017. Ran on a Rasperry PI 3, classification of an event was done in 400ms. Events were detected based on a current draw profile of 1 second / 60 current peaks. No details on the code used, probably a standard toolset like Python/sklearn.
Possibly a testcase.

Performance

* MNIST. [Kaggle](https://www.kaggle.com/c/digit-recognizer).
Random Forest with original features seems to peaks out at just under 3% error rate, for 200-1000 trees.
Should be below 5% for 100 trees. Training time should be under 10 minutes.

As execution target for other ML models

* Keywords. Knowledge distillation, model distillation, model compression
* [Distilling a Neural Network Into a Soft Decision Tree](https://www.arxiv-vanity.com/papers/1711.09784/). Hinton, November 2017.
Main motivation is making the decisions of model more explainable.
Could it also be used to get computationally efficient results for problems which classically-trained trees don't perform so well?
"we use the deep neural network to train a decision tree that mimics the input-output function discovered by the neural network
but works in a completely different way".
It is possible to transfer the generalization abilities of the neural net to a decision tree by using a technique called distillation
and a type of decision tree that makes soft decisions.
Soft decision tree is a hierarchical mixture of experts. With probability across learned distributions.
Sigmoid activation function, with heating term.
! Unlike most decision trees, our soft decision trees use decision boundaries that are not aligned with the axes defined by the components of the input vector.
! Trained by first picking the size of the tree and then using mini-batch gradient descent to update all of their parameters simultaneously, rather than the more standard greedy approach that decides the splits one node at a time.
Loss function minimizes the cross entropy between each leaf, weighted by its path probability, and the target distribution.
Using regularization.
* https://github.com/csypeng/nnsdt, Python implementation of Hinton2017 using TensorFlow
* https://github.com/kimhc6028/soft-decision-tree, Python implementation of Hinton2017 using Pytorch




Related methods

* Deep Neural Decision Forests. [Explained](https://topos-theory.github.io/deep-neural-decision-forests/)
* Deep Forest. https://arxiv.org/abs/1702.08835
* [Convolutional Decision Trees for Feature Learning and Segmentation](https://link.springer.com/chapter/10.1007/978-3-319-11752-2_8). Laptev, 2014.
* Multivariate (oblique) trees. 

## Unsupervised

* [Fault Detection using Random Forest Similarity Distance](https://www.sciencedirect.com/science/article/pii/S2405896315017188)

## Kernels

* Original Extremely randomized trees paper includes a kernel-based interpretation
* Random Partition Kernels.
[The Random Forest Kernel and creating other kernels for big data from random partitions](https://arxiv.org/abs/1402.4293). 2014. Alex Davies

Metric Learning / similarity / distance learning

* Similarity Forests
* Random forest distance (RFD)

# Inference optimization


Evaluation strategies
http://tullo.ch/articles/decision-tree-evaluation/ discusses flattening vs compiled
https://github.com/ajtulloch/sklearn-compiledtrees implements compiled regression trees for sklearn

The tree is done as soon as a leaf is reached.
Can we reorder the tree to make this faster for typical data?

QuickScorer (QS). Claims 2-6x speedups over state-of-the-art.
Evaluates the branching nodes of the trees in cache-aware feature-wise order, instead of each tree separately.
Uses a bitvector for the comparison operations.


* Can we reduce number of nodes in a tree? Using pruning?
* Can we eliminate redundant decisions across trees in the forest?
* How to best make use of multithreading?
Split by sample. Only works for batch predictions.
Split by tree. Works also for single sample. 

##

#### Bolt: Fast Inference for Random Forests

Conceptually, Bolt maps every path in each tree to a lookup table which,
if cache were large enough, would allow inference with just one memory access.

Compared with Python Scikit-Learn, Ranger, and Forest Packing.
olt can run 2–14X faster.

## Adaptive inference

Different inputs have different difficulty to classify.
Therefore it is possible to adjust the inference to match the samples.
Can be done at runtime.


- [Adaptive Random Forests for Energy-Efficient Inference on Microcontrollers](https://arxiv.org/abs/2205.13838v1).
Daghero et al. 2022.
Propose an early-stopping mechanism for RF,
which terminates the inference as soon as a high-enough classification confidence is reached,
reducing the number of weak learners executed for easy inputs.
References other existing work on adaptice Random Forests.
Energy reduction from 38% to more than 90% with a drop of less than 0.5% in accuracy.
- [Quit When You Can: Efficient Evaluation of Ensembles with Ordering Optimization](https://arxiv.org/abs/1806.11202).
S. Wang et al. 2018.
Sorts the members of ensemble at training time to get storted paths for easy inputs.
Only for binary classification. 


### Early cutoff in ensamble

Sometimes decisions are easy enough that a smaller amount of trees can do it well enough.

Run first a subset of trees.
If they have a large degree of certainty (low disagreement) on the input,
use their output instead of computing

Could have a fixed threshold for how many trees to consult initially.
Or run until reaching some purity/agreement metric.
Or could model explicitly the "risk" of not evaluation all trees. 

### Reordering for common paths

Sometimes some decision paths are considerably more common than others.
For example with severe class imbalance, where input typically reflects one class.
This happens often for event detection in time-series: typically events are quite rare.
Can be as rare as 1% or 0.01%, depending on usecase.

Reorder feature evaluations such that the common paths are as short as possible.
Possible could try to lay out memory along the paths as well.

Similar concept to Profile Guided Optimization.

Alternative to this is a two-stage classifier chain.
Where the first is optimized for the common case, only

TODO: find references for this

### Subtree de-duplication

With quantization, increased likelihood that

### Quantization

Decreases storage space porportionally.
May also enable node de-duplications?
If two nodes have same threshold (and children).

emlearn can do quantization to 8 bit integer with inline computations.
Not yet implemented for memory models.

Usually need to scale input features.
Can be a linear transform in simple case.
MinMaxScaler can be used.
Could be convenient to have a wrapper/subclass that sets 8, 16 bits etc.

## Unrolled evaluation

Evaluating and fetching one and one node can be wasteful,
due to the large amount of unpredictable branching.
Unrolling is the classical technique for reducing that.
When generating C code from decision trees, compiler should in theory be able to do this by itself.
Should check whether this actually is the case for emlearn output.
And if there are things that can break optimzation.

Benefits a lot from knowing which outcomes cases are likely/not,
to not waste too many computations.

Should be possible to use SIMD.
Cortex M microcontrollers have quad 8 bit operators available.
Tricky part is that the remaining nodes is dependent on first result.

With numeric features each comparison is so simple, that storing the result is not worth it,
must be used right away.
Maybe one can find groups of 4 that

https://github.com/Naveen-Lalwani/High-Performance-ID3-Decision-Trees
implements compiler techniques like loop unrolling, loop fusion,
and also SIMD based kernels.

https://github.com/weliveindetail/DecisionTreeCompiler
considers SIMD for decision trees.
"SIMD-parallelization outweighs its initial overhead only for 7 or more nodes in parallel"

[Exploiting CPU SIMD Extensions to Speed-up Document Scoring with Tree Ensembles]().
V-QuickScorer (vQS).
Extends QuickScorer to use SIMD.
Claims a 3.2x speedup with AVX-2, scoring 8 documents in parallel.

## Histogram binning

Common in gradient boosting ensembles of decision trees.
sklearn.ensemble.HistGradientBoostingClassifier, LightGBM, XGBoost, CatBoost
all implement this. Primarily used for cases with lots of samples, 10k+ region.

It could h

Bin edges can be spaced in different fashions.
Can be seen as an extreme quantization regime, where input features are mapped to discrete bins.

Random Histogram Forest for Unsupervised Anomaly Detection.
A. Putina, M. Sozio, D. Rossi, J.M Navarro. 2020
Compared to iForest.
Creates random splits.
Points that end up in relatively large groups, less likely to be anomalies.
Uses kurtosis score to bin.

Random Forest for Histogram Data, An application in data-driven prognostic models for heavy-duty
trucks. Ram Bahadur Gurung. PhD thesis.

Comparing Histogram Data Using a Mahalanobis–Wasserstein Distance.
R. Verde, A. Irpino. 2008

## Compression

#### Lossless Compression of Random Forests
https://jcst.ict.ac.cn/en/article/pdf/preview/10.1007/s11390-019-1921-0.pdf
Amichai Painsky and Saharon Rosset
2018.

Shows compression rates of 40x for lossless. And 100x or more for lossy.
Using a Zaks sequence for the tree structure.
Models thresholds as per-feature probability distributions.
Uses Huffman coding.
Can predict from the compressed representation.
Tested quantizing the leaf values for regression. Found 8-12 bits sufficient for maxing performance.

## Online learning

Researched very widely for decision-trees.
Often in the context of data-mining.

## On-device learning

Tree/ensemble construction is simple in principle, quite robust and relatively fast.
Bagging requires whole dataset in memory however.
Subsetting of features limits memory a bit, but only by a constant factor.
Boosting does subsets

Histograms are efficient storage mechanisms.
Much reduced complexity over original dataset.
Constant-space over samples.
Linear space over classes.

Challenge: Cannot forget a sample, since the individual sample contribution to the histogram is unknown.
But labeled data tends to be pretty rare. So maybe that is worth also saving in raw features value form.
 
For continious learning cases, maybe one can implement some sort of decay over time.
Using multiple histograms that are summed up to make

Could enable learning 


## Interval-based models

For time-series / sequence classification.
Ideally suited for data like spectra, where a particular section (interval) of the sequence is discriminative.


#### Bake off redux: a review and experimental evaluation of recent time series classification algorithms
https://link.springer.com/article/10.1007/s10618-024-01022-1

contains many interval-based tree-based methods, such as

- Time Series Forest (TSF)
- Random Interval Spectral Ensemble (RISE), from HIVE-COTE
- Supervised Time Series Forest (STSF)
- Randomised STSF (R-STSF)
- Canonical Interval Forest (CIF)
- Diverse Representation Canonical Interval Forest (DrCIF)
- QUANT

Paper shows predictive performance results on UCR UTSC dataset.
All are much better than 1NN-DTW.
QUANT, DrCIF and R-STSF are the best.

CIF and DrCIF have multivariate capabilities.

"QUANT as the best in class because it is significantly faster than DrCIF and RSTSF".

Many of these are implemented in sktime, https://www.sktime.net/en/latest/examples/classification/interval_based_classification.html

And also in aeon, https://www.aeon-toolkit.org/en/latest/examples/classification/interval_based.html

TS-CHIEF comprises an ensemble of trees that embed distance, dictionary, and spectral base features.
At each node, a number of splitting criteria from each of these representations are considered.
The dictionary based splits are based on BOSS, distance splits based on EE and interval splits based on RISE.

HIVE-COTE version 2. Ensemble, consisting of STC, TDE, DrCIF, Arsenal/ROCKET.
Highest performing on 

#### Time Series Forest

> Time Series Forest (TSF)√(Deng et al. 2013) is the simplest interval based tree based ensemble.
> For each tree, sqrt(m) (following the notation from Chapter 2, where m is the length of the series and d is the number of dimensions)
> intervals are selected with a random position and length.
> The same interval offsets are applied to all series. 
> For each interval, three summary statistics (the mean, variance and slope) are extracted and concatenated into a feature vector.>

#### QUANT
https://arxiv.org/abs/2308.00928
https://link.springer.com/article/10.1007/s10618-024-01036-9

Code: https://github.com/angus924/quant

QUANT (Dempster et al. 2023) employs a singular feature type, quantiles, to encapsulate the distribution of a given time series.
The method combines four distinct representations:

- raw time series
- first-order differences
- Fourier coefficients
- second-order differences.

The extraction process involves fixed, dyadic intervals derived from the time series.

These disjoint intervals are constructed through a pyramid structure, where each level successively halves the interval length.
At depths greater than one, an identical set of intervals, shifted by half the interval length, is also included.
Each representation can have up to 120 intervals, resulting in a total of 480 intervals across all four representations.

Computing m ∕ 4 quantiles per interval (where m is interval length),
and subtracting the interval mean from every second quantile.

Used Extratrees classifier, with 200 trees, and 10% max_features, 'entropy' as the splitting criterion.

Two hyperparameters.

- depth, which controls the number of intervals. Default depth=6, for 120 intervals per 4 transform = 420 total
- proportion of quantiles per interval. Default=4. m/v quantiles per interval, where is interval length.
Interval length is dependent on time-series length. So total number of features becomes proportional to time series length.


> We find that it is also beneficial to use the second difference,
> although the improvement in accuracy is marginal: see Sect. 4.2.2.
> We find that it is beneficial to smooth the first difference by applying a simple moving average.
> Again, the effect seems to be relatively small.

> We find that it is beneficial, to subtract the interval mean (that is, the mean of all of the values in the interval) from every second quantile:
> Subtracting the mean from every second quantile allows for capturing both the ‘raw’ distribution of values and the ‘shape’ of the distribution
> (i.e., divorced from mean of the values in a given interval)
> Note, however, that the effect of subtracting the mean from half of the quantiles versus not subtracting the mean is relatively small

> With a sublinear number of candidate features per split,
> as the size of the feature space grows, the probability of any given feature being considered decreases.
> To this end, we find that it is beneficial to increase the number of candidate features per split to a linear proportion of the total number of features
> in particular, 10% of the total number features

> We leave the extension of the method to variable-length and multivariate time series to future work.

Implementation in Python/Pytorch is just 100 lines of code.

Considerably more powerful than catch22 or tsfresh.

! Great candidate for embedded uses.
Simple, computationally efficient, can be used in combination with standard emlearn trees.
Well suited for integer based computation.
Can be done in a reasonable amount of memory.
? should be possible to extract only the features that are used.
?? maybe possible to extract on-demand
Would need to encode: interval (`<120` options typical), transform (4 options), quantile number (typical 4). Fits in 16 bits??
Need to perform a sort - inside the interval.
Might be able to pre-sort or share sorting for efficiency gains?

Can probably drop the second derivative feature.
Depth=4 gives nearly identical average performance as depth=6. Many fewer features.

?? what about a convolutional (FIR) or IIR transform before the interval picking
Alternatively some Wavelet.

Author is also associated with Rocket.
So odd that if a convolutional kernel has not been consided?



