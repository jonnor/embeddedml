
# Naive Bayes
Implemented in [emlearn](https://github.com/emlearn/emlearn)

Simple generative model. Very effective at some classification problems.
Quick and easy to train, just basic descriptive statistics.
Making predictions also quick, amounts to calculating probabilities for each class.

Variations

* Gaussian,Multinomial,Bernouilli
* Adaptive Naive Bayes (ANBC)
* Fuzzy Naive Bayes
* Rough Gaussian Naive Bayes
* Non-naive Bayes. Actually takes covariance into account

Naive Bayes classifier implementations
 
* Python. Discrete Naive Bayes. [AppliedMachineLearning](https://appliedmachinelearning.wordpress.com/2017/05/23/understanding-naive-bayes-classifier-from-scratch-python-code/)
* Gaussian Naive Bayes in Python. 
[MachineLearningMastery](https://machinelearningmastery.com/naive-bayes-classifier-scratch-python/)
* Discrete Naive Bayes in C++ [codeforge](http://www.codeforge.com/read/387365/BayesianClassifier.cpp__html)
* Discrete,Gaussian,Multinomial,etc in Python [scikit-learn](https://github.com/scikit-learn/scikit-learn/blob/master/sklearn/naive_bayes.py)
* Gaussian Naive Bayes from scratch, in Python. [chrisalbon](https://chrisalbon.com/machine_learning/naive_bayes/naive_bayes_classifier_from_scratch/). Good walkthrough
* Multinomial, Bernoulli and Gaussian. In Python, with sklearn APIs.
[kenzotakahashi](https://kenzotakahashi.github.io/naive-bayes-from-scratch-in-python.html)

Techniques for improvement

* Compensate for naive assumption of indepenence. Introduce covariance.
* Bagging, one-against-many

References

* [Binary LNS-based Naive Bayes Hardware Classifier for Spam Control](https://pdfs.semanticscholar.org/61eb/34423db29a7f634bcf4742049ef22084336e.pdf). Naive Bayes on FGPA. Not using a gaussian.

Gaussian Naive Bayes

* [Naive Bayes Models for Probability Estimation](https://icml.cc/Conferences/2005/proceedings/papers/067_NaiveBayes_LowdDomingos.pdf)
Proposes naive Bayes models as an alternative to Bayesian networks for general probability estimation tasks.
Compared on 50 UCI repo datasets.
The two take similar time to learn and are similarly accurate,
but naive Bayes inference is orders of magnitude faster.
[Code](http://aiweb.cs.washington.edu/ai/nbe/)
* [Comparing fuzzy naive bayes and gaussian naive bayes for decision making in robocup 3d](https://www.researchgate.net/publication/220887471_Comparing_Fuzzy_Naive_Bayes_and_Gaussian_Naive_Bayes_for_Decision_Making_in_RoboCup_3D)
Fuzzy Naive Bayes classiﬁer just a little better than the Gaussian Naive Bayes. Beat Decision Trees.

Prior art for embayes optimization

* [Fast Gaussian Naïve Bayes for searchlight classification analysis](https://www.sciencedirect.com/science/article/pii/S1053811917307371)
Called M-GNB / Massive-GNB. Equation (2) has the simplfied quadratic equation also found in embayes.
Also uses a sparse computation. Was 34 times faster than libSVM.
[Code](https://github.com/mlsttin/massive_gaussian_naive_bayes) in MATLAB/C++.
* [Learning with Mixtures of Trees](http://jmlr.csail.mit.edu/papers/volume1/meila00a/meila00a.pdf).
* [The Likelihood, the prior and Bayes Theorem](https://www.image.ucar.edu/pub/TOY07.4/nychka2a.pdf).
Derives equation close to embayes via minus log likelyhood of Gaussian distribution.
* [GENERATIVE AND DISCRIMINATIVE CLASSIFIERS: NAIVE BAYES AND LOGISTIC REGRESSION](https://www.cc.gatech.edu/~lsong/teaching/CSE6740/NBayesLogReg.pdf), chapter 2.4, 3.1.
maximum likelihood estimator (MLE) and minimum variance unbiased estimator (MVUE) which is very similar.
Explains relationship between Gaussian Naive Bayes and Logistic Regression.
"if the GNB assumptions hold, then asymptotically (with training examples)
the GNB and Logistic Regression converge toward identical classifiers"

Baysian Networks

* [Learning of Bayesian Network Classifiers Under Computational Constraints](https://pdfs.semanticscholar.org/97cb/096d0998b9eebded56154f2cdca551a8b965.pdf).
Online learning of Bayesian network classifiers (BNCs).
Using low bit-width fixed-point numbers.
