
## Gaussian Mixture Models

### For outlier detection
The regular GMM formulation is vunerable to outliers
that do not fit into Gaussian clusters.

#### Software

pygmmis implements an uniform background component, in pure Python
https://github.com/pmelchior/pygmmis

pomegranate has a GeneralMixtureModel,
and supporting both Gaussian and Uniform distributions, that can be mixed.
https://pomegranate.readthedocs.io/en/latest/GeneralMixtureModel.html
Latest version has multi-variate mixtures as default.
Has example of Dirac + Poisson
https://pomegranate.readthedocs.io/en/latest/tutorials/B_Model_Tutorial_2_General_Mixture_Models.html

JMP software has two options for their Normal Mixtures Model,
Robust Normal Mixtures, or outlier cluster option which assumes a uniform distribution.
https://stats.stackexchange.com/a/339095/201327

#### Strategies
 
- Clean data using univariate outlier detection.
For example percentiles. Can be done as pre-processing. Simple, computationally effective
- Clean data using the 
- Downsample the dataset randomly.
With different subsets. Hoping that distribution will be stable across subsets, effect of noise removed.
Poor mans probablistic sampling...
- Integrate a noise component directly in the E-M loop
- Use a probalistic model (that includes a noise/uniform component).

#### Papers

Unsupervised Learning of GMM with a Uniform Background Component
https://arxiv.org/abs/1804.02744
2018/2020
Proposes Gaussian Mixture Model with Uniform Background (GMMUB)
A new model that assumes that data comes from a mixture of a number of Gaussians
as well as a uniform “background” component assumed to contain outliers and other non-interesting observations.


Filling the gaps: Gaussian mixture models from noisy, truncated or incomplete sample
https://arxiv.org/abs/1611.05806

Entropy-Based Anomaly Detection for Gaussian Mixture Modeling
https://www.mdpi.com/1999-4893/16/4/195
2023

Model-Based Gaussian and Non-Gaussian Clustering
https://www.jstor.org/stable/2532201
1993. 
Introduced concept of including an uniform component to explain noise.

Unsupervised Learning of Mixture Models with a Uniform Background Component
https://arxiv.org/abs/1804.02744v2

Estimation and computations for Gaussian mixtures with uniform noise under separation constraints
https://link.springer.com/article/10.1007/s10260-021-00578-2
Coretto. 2021

Maximum likelihood estimation of heterogeneous mixtures of Gaussian and uniform distributions
https://www.sciencedirect.com/science/article/abs/pii/S0378375810003174#bib1
Coretto/Hennig. 2011.

Robust Factorization Methods Using a Gaussian/Uniform Mixture Model
https://arxiv.org/abs/2012.08243


Model-Based Learning Using a Mixture of Mixtures of Gaussian and Uniform Distributions
https://www.computer.org/csdl/journal/tp/2012/04/ttp2012040814/13rRUxASuHr
2012.



### Supervised HMM-GMM in Python

Supervised training of HMM-GMM models.

Several places are asking for such functionality:

- https://stackoverflow.com/questions/50725830/can-we-do-supervised-learning-through-hmm
- https://github.com/hmmlearn/hmmlearn/issues/109
- https://github.com/hmmlearn/hmmlearn/issues/123
- https://github.com/jmschrei/pomegranate/issues/423

pomegranate has an implementation of supervised learning,
and can use GMM as the distributions. 
TODO: make some example code

The usual approach is to model one HMM per class label.
During training, the data is filtered per label to fit the HMM.
During prediction, the data is passed through each of the HMMs.
The model that maximizes the probability.

It would be convenient with a scikit-learn compatible Classifier implementing this.
This approach of class-dependent model for classification could apply to other
probalistic or distance based methods?
Examples could be a GMM, or DBSCAN.

### Visualizing 

Typical for the GMM is to show the distribution of the Gaussians over dimensions.
Effective in 1D and 2D. Will be a stretch in 3D, and a no-go in higher dimensions.

But one can also color in the areas where each state falls.
Will also be effective in 1D and 2D.
Example in 1D: http://www.astroml.org/book_figures/chapter4/fig_GMM_1D.html

For a HMM-GMM, would have plot the GMM visualization for each state. 
And combine this with a visualization of HMM transitions.

### Constrained Hidden Markov Models

See https://github.com/jonnor/machinehearing/tree/master/handson/constrained-hmm

