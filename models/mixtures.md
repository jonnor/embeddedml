
## Gaussian Mixture Models

### For outlier detection
The regular GMM formulation is vunerable to outliers
that do not fit into Gaussian clusters.

Unsupervised Learning of GMM with a Uniform Background Component
https://arxiv.org/abs/1804.02744
2018/2020
Proposes Gaussian Mixture Model with Uniform Background (GMMUB)
A new model that assumes that data comes from a mixture of a number of Gaussians
as well as a uniform “background” component assumed to contain outliers and other non-interesting observations.

JMP software has two options for their Normal Mixtures Model,
Robust Normal Mixtures, or outlier cluster option which assumes a uniform distribution.
https://stats.stackexchange.com/a/339095/201327

pygmmis implements an uniform background component, in pure Python
https://github.com/pmelchior/pygmmis

