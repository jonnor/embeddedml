
# Support Vector Machines

Strong linear classifier/regressor, also strong non-linear method when using a kernel (polynomial,RBF).
Very popular in early 2000s.

Benefits

* O(nd) classification for *n* support vectors and *d* features.

Challenges

* Kernel function can be expensive
* Can sometime output a lot of cofefficients (support vectors)
* Training slow on large datasets, O(n^3)

Variations

* Soft-margin, to reduce effects of noise/outliers near margin
* Sparse methods. Reducing number of support vectors 
* Approximations. For instance using Nyström method.
[sklearn Nystroem/RBFSampler](https://github.com/scikit-learn/scikit-learn/blob/a24c8b46/sklearn/kernel_approximation.py#L24)
* Sampling to speed up training. Usually only on linear SVM.
Stocastic Gradient Descent (SGD), Sequential minimal optimization (SMO)
* Transductive, for semi-supervised learning
* Support vector clustering
* One-class SVM, for anomaly detection

### Optimizing SVM inference

References

* [A basic soft-margin kernel SVM implementation in Python](http://tullo.ch/articles/svm-py/), incl RBF/polynomial/quadratic.
* [Effects of Reduced Precision on Floating-Point SVM Classification Accuracy](https://ac.els-cdn.com/S1877050911001116/1-s2.0-S1877050911001116-main.pdf?_tid=247ac167-834b-4e66-b538-b47bf7bec302&acdnat=1521981076_c65b50281adc8adfd4be4d1d782dd5cc). No dataset required a precision higher than 15 bit.
* [A Hardware-friendly Support Vector Machine for Embedded Automotive Applications](https://www.researchgate.net/publication/224292644_A_Hardware-friendly_Support_Vector_Machine_for_Embedded_Automotive_Applications). Used down to 12 bit without significant reduction in performance.
* [Approximate RBF Kernel SVM and Its Applications in Pedestrian Classification](https://hal.inria.fr/inria-00325810/file/mlvma08_submission_5.pdf).
Paper presents an O(d*(d+3)/2) implementation to the nonlinear RBF-kernel SVM by employing the second-order polynomial approximation.
"Due to their dot-product form, linear kernel SVMs are able to be transformed into a compact form by exchanging summation in classification formula, leading to extremely low O(d) complexity in terms of both time and memory."
* [approxsvm](https://github.com/claesenm/approxsvm): Approximating nonlinear SVM models with RBF kernel.
C++ implementation of a second-order Maclaurin series approximation of LIBSVM models using an RBF kernel.
* [An approximation of the Gaussian RBF kernel for efficient classification with SVMs](https://www.sciencedirect.com/science/article/pii/S016786551630215X).
About 18-fold speedup on average, mostly without losing classification accuracy
* [Classification Using Intersection Kernel Support Vector Machines is efficient](https://web.stanford.edu/group/mmds/slides2008/malik.pdf).
Intersection Kernel SVM (IKSVM).
Constant runtime and space requirements by precomputing auxiliary tables.
Uses linear-piecewise approximation.
* [Locally Linear Support Vector Machines](https://www.inf.ethz.ch/personal/ladickyl/llsvm_icml11.pdf). LL-SVM.
Using manifold learning / local codings, with Stocastic Gradient Decent.
Approaches classification perfomance of RBF SVM, at 1/10 to 1/100 the execution time. Still 10-50xslower than linear SVM.
* [Support vector machines with piecewise linear feature mapping](https://www.sciencedirect.com/science/article/pii/S0925231213001963). 2013. PWL-SVM.
Mapping the feature space into M piecewise linear sections, where M is a hyperparameter. Typical M values are 10-50.
Learns the anchor points and parameters of the linear sections. Can then pass the data to regular SVM or Least Squares LS-SWM.
Reaches performance similar to RBF SVM.
More compact coefficient representation when number of support vectors > number of features.
Prediction only requires adding, multiplication, and maximum operations.
10-100x faster to train than other non-linear methods. ! No prediction times given >(
* [Feed-Forward Support Vector Machine Without Multipliers](https://ieeexplore.ieee.org/abstract/document/1687940)
Fixed-point arithmetic, using only shift and add operations.
Maintains good classification performance respect to the conventional Gaussian kernel.
