
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


## Feature selection

Greedy feature selection.
Can either start from no features (forward mode),
or all features (backward).
Well supported in standard scikit-learn ecosystem:
 
- https://scikit-learn.org/stable/modules/feature_selection.html#sequential-feature-selection
- http://rasbt.github.io/mlxtend/user_guide/feature_selection/SequentialFeatureSelector/

mlextend additionally supports "floating" versions of forward/backwards,
which samples a few more permutations.

