

## PDF approximations
How rough/fast approximation can be used for the Normal PDF in Gaussian methods?

* Naive Bayes classification
* Gaussian Mixture model (GMM)
* Hidden Markov Model (HMM)
* Kalman filtering
* RBF/Gaussian kernel in kernel SVM/logits

It looks like the *logarithm of normpdf()* can be easily simplified to the quadratic function,
see [embayes: Quadratic function in Gaussian Naive Bayes](https://github.com/jonnor/embayes/blob/master/doc/Probability%20Density%20Function.ipynb).

Can this be applied for SVM with RBF kernel also? RBF: k(xi, xj) = exp(-y * ||xi - xj||^2)
Does not seem like it, at least not with the kernel trick. No way to split: sum( z_i*y_i*k(x_i, x))

References

* [A Unifying Review of Linear Gaussian Models](https://cs.nyu.edu/~roweis/papers/NC110201.pdf)


# Research questions

* How to take inference cost into account in model/feature evaluation/selection? (time,energy)

Especially with computationally heavy features, that one can generate lots of. Ie dictionary of convolutional kernels.
Perhaps set desired score as a hyperparameter, and then optimize for inference cost?
Alternatively set a inference cost budget, and find best model that fits.
Using standard FS wrapper methods (and uniform feature costs):
Do SBS/SFB to obtain score/feature mapping, apply a inference cost function, chose according to budget.
Or (with methods robust to irrelevant/redundant features), estimate feature number within budget
Could one implement model/feature searchs that take this into account?
Could be first feature then model. Or joint optimization?
Does it perform better than other model/feature selection methods? Or is more practical. Ease of use.
Non-uniform feature-calculation costs. Ie different sized convolution kernels. Convolutions in different layers.
Classifier hyper-parameters influencing prediction time. Ie RandomForest `min_samples_split`/`min_samples_leaf`/`max_depth`.
Need to specify a cost function. Number of features. Typical/average depth in tree based methods. Number of layers in CNN-like architecture.

* How to optimize/adapt existing machine learning methods for use on small CPUs.

Memory usage, CPU, prediction time.
RandomForest on-demand memoized computation of non-trivial features?
Approximation of RBF kernel in SVM?
PDF simplification in Naive Bayes.
(Recurrent) Convolutional Neural Network.
How to compress models efficiently?
How to conserve memory (and compute) by minimize the receptive field of the network?
Feature selection techniques. Sparsity contraints.
Can something like feature permutation be used to find/eliminate irrelevant features?
In frequency domains. In time domain.
How to select the right resolution, to minimize compute.
Frequency domain (filterbands).
Time domain (window size, overlap).
Network architecture search. Constrained by compute resources.
Tool(s) for reasoning about computational efficienty of CNN. Constraint/solver based.
Give base architecture and constraints like Nparameters,FLOPs => produce model variations that match.
Could also just do random mutations (within ranges), check the flops/parameter count, and filter those not maching?
