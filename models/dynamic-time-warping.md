
# Dynamic Time Warping (DTW)

Elastic distance metric between sequences / time-series.

Has been used in several applications, such as

- Speech Command recognition
- Gesture recognition

Since 2015 many uses have been replaced by deep learning approaches,
such as CNNs and RNNs.

A non-elastic measure such as Euclidian distance,
used in Matrix Profile etc, can be seen as a special case of the DTW.

### DTW KNN

For classification DTW is often used as a distance function inside KNN.
This is a conceptually very simple framework which can form a suprisingly strong baseline.
The KNN classifier makes it trivial to support on-device learning, for example to allow end-user customization.

How well KNN works is dependent on how representative the stored prototypes are (in addition to the distance function).

### Combining with deep learning

How well DTW performs depends a lot on how good the input features are.
Situations with high-dimensionality and noisy input data might not do so well,
such as noisy speech.
Deep learning approaches have shown to be able to learn noise-resistant feature representations.

Q: How could we use deep learning to extract better features for a DTW, and how well would it work?

For speech command recognition, one could try to learn a time-series of phoneme representation.
The goal would be to significantly outperform a MFCC (or HFCC-ENS) baseline,
and be competitive with a pure deep learning approach when data is abundant,
and outperform deep learning on small datasets (few shot learning).

Targetting a vector of 2-6 dimensions.

Differentiable DTW.

[Soft DTW loss in tslearn](https://tslearn.readthedocs.io/en/stable/auto_examples/autodiff/plot_soft_dtw_loss_for_pytorch_nn.html).


[Two-Dimensional Embeddings for Low-Resource Keyword Spotting Based on Dynamic Time Warping](https://www.wilkinghoff.com/publications/itg21_2d_embedding.pdf)
(Wilkinghoff et.al., 2021).

Tested a combination of deep learning for embeddings and DTW.
Used an 2D AdaCos loss function.
Suggests using Soft DTW in a follow up work.
Used an internal dataset recorded by Fraunhofer FKIE.
37 keywords and an additional class Silence.
12 male and 7 female speakers.
Mentions an HFCC-ENS as a baseline. Supposed to be better than MFCC.

[TempAdaCos: Learning Temporally Structured Embeddings for Few-Shot Keyword Spotting with Dynamic Time Warping](https://www.researchgate.net/publication/370869755_TempAdaCos_Learning_Temporally_Structured_Embeddings_for_Few-Shot_Keyword_Spotting_with_Dynamic_Time_Warping/fulltext/6466e7ea9533894cac7c6baa/TempAdaCos-Learning-Temporally-Structured-Embeddings-for-Few-Shot-Keyword-Spotting-with-Dynamic-Time-Warping.pdf) (Wilkinghoff et.al., 2023).

Proposes an KWS dataset called KWS-DailyTalk, based on the ASR dataset DailyTalk.
https://github.com/wilkinghoff/kws-dailytalk
In contrast to existing KWS datasets such as SpeechCommands,
KWS-DailyTalk is an open-set classification dataset with isolated keywords as training data and complete spoken sentences as validation and test data.

Uses an TempAdaCos loss function.
! no mention of SoftDTW loss?
Uses a modified ResNet architecture.
Mel spectrogram as input feature representation.
? Still a 2d embedding?

TACos: Learning Temporally Structured Embeddings for Few-Shot Keyword Spotting with Dynamic Time Warping
(Wilkinghoff et.al., 2024).

HFCC-ENS. Perceptual audio features for unsupervised key-phrase detection. (Zeddelmann et al, 2010).
Claims better than MFCC on key-phrase detection.

### Advanced feature extraction with DTW

WHEN: A Wavelet-DTW Hybrid Attention Network for Heterogeneous Time Series Analysis
https://dl.acm.org/doi/abs/10.1145/3580305.3599549
KDD 2023.


### Efficient implementations

The naive DTW KNN is .

Limiting the possible warping path is a key optimization.
For example to the Sakoe-Chiba Band or Itakura Parallelogram.
Can reduce computation by 10-100x.
Limiting warping path also tends to improve accuracy, as very odd warping paths are unlikely to be true matches.

Ref: Everything you know about Dynamic Time Warping is Wrong (Ratanamahatana & Keogh, 2004).


Ref: Extracting Optimal Performance from Dynamic Time Warping (Mueen & Keogh, 2016).
Also discussed in https://www.youtube.com/watch?v=LnQneYvg84M
MATLAB (pseudo) code for implementation.

- Constrained warping path.
- Memoization.
- SIMD.
- Piecewise Aggregate Approximation (PAA)
- Length-encoding approximation
- 1-NN. Prune using lower-bound for distance
- 1-NN. Early abandonment
- Just in Time Z-normalization
- PrunedDTW: all-pair distance matrix

? what would be a good lower bound distance for multi-dimensional case ?

In KNN should do most frequent class first. Establish the distance that other classes must beat.
For keyword recognition, "silence" / "noise" classes.


### Existing implementations of DTW

Especially low-level and/or high performance.

https://github.com/wannesm/dtaidistance/blob/master/dtaidistance/lib/DTAIDistanceC/DTAIDistanceC/dd_dtw.c

Wearable Real-time Air-writing System Employing KNN and Constrained Dynamic Time Warping
https://ieeexplore.ieee.org/document/10118944
Constrained dynamic time warping (cDTW) algorithm for the distance measure and K-nearest neighbors (KNN) as the classifier

tslearn implements DTW and KNN with DTW.
Has a very pedagogical description of how it works.
https://tslearn.readthedocs.io/en/stable/user_guide/dtw.html

librosa implements DTW
https://librosa.org/doc/latest/generated/librosa.sequence.dtw.html
Supports Sakoe-Chiba constraints.
Also backtracking?

### Variations

#### Amerced Dynamic Time Warping (ADTW)

https://arxiv.org/abs/2111.13314
November 2021.

https://www.sciencedirect.com/science/article/pii/S0031320323000341
May 2023.

> Introduction of a novel constraint, amercing — the application of a simple additive penalty every time an alignment is warped (i-j changes).
> ...
> This addresses the following problems:
> - DTWFull can be too flexible in its alignments;
> - DTW uses a crude step function — any flexibility is allowed within the window and none beyond it;
> - WDTW applies a multiplicative weight, and hence promotes large degrees of warping if they lead to low cost alignments

Implemented in Aeon: [Amercing Dynamic Time Warping](https://www.aeon-toolkit.org/en/stable/api_reference/distances.html#amerced-dynamic-time-warping-adtw)


#### Time Series Alignment with Global Invariances (DTW GI)
https://arxiv.org/abs/2002.03848
Feb 2020

https://rtavenar.github.io/hdr/parts/01/dtw/dtw_gi.html

Considered for implementation in https://github.com/aeon-toolkit/aeon/issues/444


#### ProximityForest

https://arxiv.org/abs/1808.10594
August 2018.

> Whereas conventional decision trees branch on attribute values (and usually perform poorly on time series)
> Proximity Trees branch on the proximity of time series to one exemplar time series or another;
> allowing us to leverage the decades of work into developing relevant measures for time series.
> ...
> Our experiments demonstrate that Proximity Forest is highly competitive on the UCR archive:
> it ranks among the most accurate classifiers while being significantly faster.

Implementations

- sktime. Implemented https://www.sktime.net/en/stable/api_reference/auto_generated/sktime.classification.distance_based.ProximityForest.html
- aeon. Planned. https://github.com/aeon-toolkit/aeon/issues/159
- https://github.com/moradabaz/ProximityForests-python - uses dtaidistances - unmaintained since 2020

Splits based on the similarity of instances to chosen time series exemplars.
Each splitter consists of a set of exemplar time series for each class and a parameterized similarity measure, both chosen randomly.

!! should be much faster than KNN-DTW. And potentially more powerful
Not as easy learn on-device though.

#### ProximityForest 2.0
Similarity-based classifier.
Extends the original ProximityForest.
Builds on Amerced Dynamic Time Warping (ADTW). Also uses constrained DTW for speedups.

Predictive performance on UCR slightly better than ProximityForest 1.0.
A little bit lower than MultiRocket, HIVE COTE and TS-CHIEF.
Slightly faster than ProximityForest 1.0 for higher complexity tasks.

https://github.com/monashts/proximityforest2.0
Implemented in C++, with Python bindings.
Looks primarily to reproduce their paper/benchmarks.
Not much documentation for how to use for other things?


### Practical hints

Using for speech recognition.
https://stackoverflow.com/questions/30159072/compare-two-spoken-words-with-mfcc-and-dtw-using-aquila-library

> feature extraction pipeline should include lifter for cepstrum and cepstral mean normalization (essentially volume normalization).
> Audio you use should not include silence, you need to use Voice Activity Detection to strip it


Extracting Optimal Performance from Dynamic Time Warping (Mueen & Keogh, 2016).

Primarily about univariate time-series.
Explaining how to get DTW down to amortized O(n) space and time complexity.
Discusses warping constraint. Basis for most speedup tricks.
Notes that with different length inputs, the endpoint warping can skew results a lot.
Says that *each subsequence* must be Z-normalized. Normalizing the entire series not sufficient.
Discusses two ways of extending DTW to multi-dimensional data.
Independent: Just compute the DTW score for each dimension independently, and sum up each score.
Dependent: Create a single distance matrix that reflect the distance between each corresponding pair of time series,
then find the single warping path and distance as per normal.

If the physical process affects the time series simultaneously (at same time steps),
then DTW Dependent will probably be best. We call this the tightly coupled case.
If the physical process affects the time series with varying lags,
then DTW Indepedent will probably be best. We call this the loosely coupled case.

> Critical Point: You can generalize DTW to 2,3,4,…1,000 dimensions.
> However, it is very unlikely that more than 2 to 4 is useful, after that,
> you are almost certainly condemned to the curse of dimensionality.

Example PAMAP. DTW-KNN with w=0. All 9 dimensions failed. Best 3 dimensions combined gave better than best 1 dimension.

