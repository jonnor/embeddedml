
# Feature engineering
Feature extraction/engineering critical to model performance.
Both predictive accuracy, as well as.
May need to create new features from raw data.
One approach is to generate a large set of potentially-useful candidates,
and then use Feature Selection to find a good subset.

Some auto generation approaches exist.

## TODO

On-line DSP tools:

    Streaming summarizers/estimators. min/max, mean/std, median
    Reservoir sampling.
    Voice Activity Detection
    Sound level. Incl IEC A-weighting

Transformers:

    Scalers: Standard,MinMax
    Dimensionality: PCA,NMF


## Generic features

### catch22
https://github.com/chlubba/catch22
Defines 22 features for dynamical aspects of univariate time-series.
Has implementations in C. However using doubles and malloc.
The features are explained here:
https://feature-based-time-series-analys.gitbook.io/catch22-features/
They are relatively complex, consisting of several steps, online "estimation"
z-score, histogram, Welch method with rectangular window,
Note: no fetures for "static" aspects, such as mean,std etc

### Matrix profile
Especially for finding common motifs, or anomalies (discords)
https://matrixprofile.org/
https://stumpy.readthedocs.io/en/latest/index.html
How is it in terms of CPU and RAM requirements for typical embedded tasks?

### tsfresh
https://github.com/blue-yonder/tsfresh
Time-series feature generation, with integrated feature selection.
Extracts 100s of features automatically
Provided as scikit-learn transformers
Overview of features:
https://tsfresh.readthedocs.io/en/latest/text/list_of_features.html

## featuretools
https://featuretools.alteryx.com/
composes a set of primitives by stacking them.
Primitives can be either transformations or aggregators
Gives new feature names that include description of calculations

### autofeat
https://github.com/cod3licious/autofeat
Linear Prediction Models with Automated Feature Engineering and Selection

## MiniRocket
MiniRocket: A Very Fast (Almost) Deterministic Transform for Time Series Classification
August 2021
KDD '21: Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data MiningAugust 2021 Pages 248–257https://doi.org/10.1145/3447548.3467231
https://arxiv.org/pdf/2012.08791.pdf
https://github.com/angus924/minirocket

Transforms time-series using a set of convolution kernels.
And then classifies using a linear classifier.


MiniRocket uses a small, fixed set of kernels, and is almost entirely deterministic.
Uses dilation , sampled on an exponential scale
Uses ‘proportion of positive values’ pooling (PPV)

Weights constrained to two values
Similarities with binary and quantised convolutional neural networks

MiniRocket exploits various properties of the kernels, and of PPV,
in order to massively reduce the time required for the transform.
Precomputing the product of the kernel weights and the input,
and using those precomputed values to construct the convolution output


Trained 109 datasets from UCR in 10 minutes.
Compares against other methods
- cBOSS. dictionary methods
- Temporal Dictionary Ensemble (TDE) is a recent dictionary method
based on the frequency of occurrence of patterns in time series. TDE combines aspects of earlier dictionary methods including cBOSS
- Proximity Forest, an ensemble of decision trees using distance measures as splitting criteria
- Canonical Interval Forest (CIF) is a recent method which adapts the Time Series Forest (TSF)
to use catch22 features. CIF is significantly more accurate than either catch22 or TSF.
- TS-CHIEF builds on Proximity Forest.
In addition to distance measures, it uses interval-based and spectralbased splitting criteria [36]
- HIVE-COTE is an ensemble of other methods including BOSS and TSF.

MosquitoSound, InsectSound, FruitFlies

84 different kernels
With different dilations. 119 dialations = 10k features

linear in the number of kernels/features (𝑘),
linear the number of examples (𝑛),
and linear time series length (input),
tin total, 𝑂(𝑘 · 𝑛 · input)

2**9 = 512 possible two-valued kernels of length 9.
Uses a subset of 84 of these kernels, all combinations with 3 values of B (and 6 values of A)
Uses kernels of length 9 with 2 values, 𝛼 = −1 and 𝛽 = 2.
Choice of 𝛼 and 𝛽 is arbitrary, since the scale of these values is unimportant.
It is only important that the sum of the weights should be zero or, equivalently, that 𝛽 = −2A

PPV is bounded between 0 and 1

Take [0.25, 0.5, 0.75] quantiles from 𝑊𝑑 ∗ 𝑋 as bias values, to be used in computing PPV

Wespecify dilations in the range 𝐷 = {2**0, ..., 2**max⌋},
such that the maximum effective length of a kernel, including dilation,
is the length of the input time series.
Default limit the maximum number of dilations per kernel to 32

Padding is alternated for each kernel/dilation combination such that,
overall, half the kernel/dilation combinations use padding, and half do not.

reuse the convolution output, 𝐶, to compute multiple features, with different bias values

it is only necessary to compute 𝛼𝑋 and 𝛽𝑋 once for each input time series,
and then reuse the results to complete the convolution operation for each kernel by addition


3.2.3 Avoiding Multiplications.
Restricting the kernel weights to two values allows us to,
in effect, ‘factor out’ the multiplications from the convolution operation,
and to perform the convolution operation using only addition.

#### Notes

Transforms are not integrated with the classifier.
Likely overcomplete.

? What would the execution time of MiniRocket be, on a microcontroller?

? how sparse are the feature weights. How many can be dropped for each problem?

? what if to use trees rather than linear methods

TSC-RTF is example of using Random Forest to select features, from random temporal features.
"Time series classification with random temporal features"
https://www.sciencedirect.com/science/article/pii/S1319157823003373

"Random subsequence forests"
https://www.sciencedirect.com/science/article/abs/pii/S0020025524003918
The experimental results on 15 real datasets show that our method can outperform those state-of-the-art classification algorithms in terms of the predictive accuracy.

#### Evaluations of MiniRocket

"Evaluating ROCKET and Catch22 features for calf behaviour classification from accelerometer data using Machine Learning models"
https://arxiv.org/abs/2404.18159
April 2024.

ROCKET with RidgeClassifier to work the best overall.
!Ridge did better than RF on ROCKET.
!!Very wide and sparse set of hyperparameters attempted for RF.
Found catch22 with RF to work second best overall.
Both considerably better than a set of hand-selected features.

## MultiRocket

Paper.
"MultiRocket: multiple pooling operators and transformations for fast and effective time series classification"
https://link.springer.com/article/10.1007/s10618-022-00844-1
2022.

Builds on MiniRocket.
Does a first-order difference transformation on the input.
And uses 4 pooling operators.
Percentage of positive values (PPV); Mean of Positive Values (MPV); Mean of Indices of Positive Values (MIPV); and Longest Stretch of Positive Values (LSPV).
Defaults to 50k features. Also tested with 10k features.

> 

Implementations

- sktime [RocketClassifier](https://www.sktime.net/en/stable/api_reference/auto_generated/sktime.classification.kernel_based.RocketClassifier.html), supports transform=multirocket
- aeon [MultiRocket](https://www.aeon-toolkit.org/en/stable/api_reference/auto_generated/aeon.transformations.collection.convolution_based.MultiRocket.html)
- tsai [MultiRocketPlus](https://timeseriesai.github.io/tsai//models.multirocketplus.html)
- Official. https://github.com/ChangWeiTan/MultiRocket


#### Further extensions of MultiRocket

CEEMD-MultiRocket: Integrating CEEMD with Improved MultiRocket for Time Series Classification
CEEMD = Complementary Ensemble Empirical Mode Decomposition

POCKET: Pruning random convolution kernels for time series classification from a feature selection perspective
https://www.sciencedirect.com/science/article/abs/pii/S0950705124008876
https://arxiv.org/abs/2309.08499
September 2024.

> To efficiently prune models, this paper eliminates feature groups contributing minimally to the classifier,
> thereby discarding the associated random kernels without direct evaluation.
> To this end, we incorporate both group-level (-norm) and element-level (-norm) regularizations to the classifier,
> formulating the pruning challenge as a group elastic net classification problem.
> An ADMM-based algorithm is initially introduced to solve the problem, but it is computationally intensive.
> Building on the ADMM-based algorithm, we then propose our core algorithm, POCKET, which significantly speeds up the process by dividing the task into two sequential stages.
> ...
> POCKET prunes up to 60% of kernels without a significant reduction in accuracy and performs 11× faster than its counterparts

Detach-ROCKET: Sequential feature selection for time series classification with random convolutional kernels
https://arxiv.org/abs/2309.14518

> Testing on the UCR archive shows that SFD can produce models with better test accuracy using only 10\% of the original features

Still a few thousand features. Heavily over-parametrized.

HIERVAR: A HIERARCHICAL FEATURE SELECTION METHOD FOR TIME SERIES ANALYSIS

Left with 500-1000 features, down from 10k+

#### Random and Fixed Covolutional filters

Deep Learning For Time Series Classification Using New Hand-Crafted Convolution Filters
https://ieeexplore.ieee.org/abstract/document/10020496
> Experiments reveal that adding our manually created filters increase the prediction accuracy on a majority of the 128 datasets of the UCR Archive


Reducing the Computational Complexity of Learning with Random Convolutional Features
https://ieeexplore.ieee.org/abstract/document/10095893
ICASSP 2023.
Convolutional Kitchen Sinks-based method.
Simple and efficient feature selection method based on knee/elbow detection in the curve of ordered coefficients in linear regression.
Our empirical studies show that without significant loss in accuracy, the proposed feature selector,
on average, prunes more than 84 percent of randomly generated features.

HIERVAR: A Hierarchical Feature Selection Method for Time Series Analysis
https://arxiv.org/abs/2407.16048
July 2024.

Weighted Sums of Random Kitchen Sinks (RKS), (mini)ROCKET,

Hierarchical feature selection method aided by ANOVA variance analysis to address this challenge. Through meticulous experimentation, we demonstrate that our method substantially reduces features by over 94% while preserving accuracy -- a significant advancement in the field of time series analysis and feature selection

Raster: Representation Learning for Time Series Classification using Scatter Score and Randomized Threshold Exceedance Rate
https://ieeexplore.ieee.org/abstract/document/10285973

> Randomized machine learning is gaining interest as many cases it can outperform deep learning.
> However, it often requires many features, which can be an issue with high-dimensional training data and low-sample sizes.
> To address this issue, we propose a novel and efficient approach that utilizes a new and fast metric to evaluate features,
> called the Scatter Score (SS), and a new temporal-aware down-sampling strategy, called randomized threshold exceedance rate (rTER).
> Our method achieves significant improvements in classification performance compared to state-of-the-art methods such as
> ROCKET, miniROCKET, ResNet, and InceptionTime, as demonstrated on 30 different datasets.


#### Adacket: ADAptive Convolutional KErnel Transform for Multivariate Time Series Classification
https://link.springer.com/chapter/10.1007/978-3-031-43424-2_12
September 2023

> automatically design efficient 1D dilated convolutional kernels for various MTSC scenarios (multivariate time series classification)
> Adacket formulates the design problem as a multi-objective optimization problem,
> with a focus on performance and resource efficiency jointly. 


#### Back to Basics: A Sanity Check on Modern Time Series Classification Algorithms
https://link.springer.com/chapter/10.1007/978-3-031-49896-1_14

Found that tabular methods actually outperformed time-series for nearly 20% of the
"time series" benchmarks. In another 20% tabular was within 10% of the time-series performance.

Takeaway: Highlights importance of checking with simple baselines.

UCR multivariate datasets have 9 Human Action Recognition datasets.
Time-series methods (ROCKET) did considerably better than tabular.


## Feature selection

Greedy feature selection.
Can either start from no features (forward mode),
or all features (backward).
Well supported in standard scikit-learn ecosystem:
 
- https://scikit-learn.org/stable/modules/feature_selection.html#sequential-feature-selection
- http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/

mlextend additionally supports "floating" versions of forward/backwards,
which samples a few more permutations.

