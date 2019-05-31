# Machine learning on embedded devices

Focused primarily on running inference/prediction/feed-forward part on a microcontroller (or small embedded device).
Training phase can run on a standard computer/server, using existing tools as much as possible.

# Status
**Research in progress**

* Decision trees ensembles implemented in [emtrees](https://github.com/jonnor/emtrees)
* Naive Bayes implemented in [embayes](https://github.com/jonnor/embayes)

# State of the Art
Of ML inference on general-purpose microcontrollers.

- Deep models have efficient implementations for ARM Cortex-M. Ex: CNN and RNN in CMSIS-NN, FC in uTensor
- Some implementations available for non-neural models that *can* be used. Ex: SVM,RF,AdaBoost in sklearn-porter
- A few special-designed ML algorithms made. Ex: ProtoNN, Bonsai
- Basic tools available for converting Tensorflow models
- Keyword-spotting/wake-word on audio well established. Used in commercial products (Alexa etc)
- Human activity detecton on accelerometers.
- Computer vision is
- Lots of research and announcements for low-power co-processors, but little on market yet

Limitations

- Neural models lacking for non-ARM micros. ESP8266/ESP32
- Non-neural models missing inference engines designed for microcontrollers
- "Small DNN" work mostly on computer vision for mobile phones (model size 1000x of uC)
- Few/no pretrained models available. Transfer learning little explored?
- Very little documentation of entire development process.
From planning, data aquisition, model design
- Best practices underdocumented (or underdeveloped?) 

Ways of advancing, make contributions

- Faster inference. Power saving, or bigger problems.
- Smaller models. Cheaper MCU, or bigger problems.
- Better accuracy on a problem. Better user experience, new usecases
- Solve a concrete usecase. Easier to deploy similar usecases
- Comparison between approaches. Microcontroller, ML model
- Libraries or tools. Lower time to market, enable more developers

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


# Background

## What and when to use machine learning

The defaults right now are to do conventional signal processing (no learning) in sensor,
and stream raw data to the cloud for storage and processing. Machine learning happens in the cloud.
If gateways are used, they mostly forward communication (no data processing). 

On-edge processing valueable when

* Local response needed. Autonomy
* Adaptable response needed. Over time, in context.
* Low/predictable latency needed
* Sending raw sensor data has privacy implications.
Audio, video
* Unreliable connection
* High bandwidth sensor input.
Audio, video, accelerometer/IMU, current sensor, radiowaves.
* Low bandwidth algorithm output
* Events of interest are rare
* Low energy usage needed
* Full/raw sensor data is not valuable to store
* Low cost sensor unit

Example usecases

* Predictive maintenance, using audio/vibration data
* Activitity detection for people, using audio/accelerometer data. Assistive tech, medical
* Appliance disaggregation, using aggregated power consumption data. "Non-Intrusive Load Monitoring" (NILM)
* Anomaly/change detection for predictive maintenance, using audio/vibration data, or electrical data
* Gesture recognition as human input device, using accelerometer/gyro data.
* Speech/command recognition as human input device, using microphone. Keyword/Wake-word detection
* Battery saving in wireless sensors. Normally sending day/week aggregates, on event/anomaly detection send data immediately
* Health status of animals via activity detected using accelerometer
* Monitoring eating activity using accelerometer [1](https://www.sciencedirect.com/science/article/pii/S0010482515000086)
* Environmental monitoring, using microphone to detect unwanted activity like cutting down trees
* Adaptive signalling and routing for wireless transmission in Wireless Sensor networks
* Electronic nose using arrays of MEMS detectors
* Material identification using reflecive spectrometer [1](https://hackaday.io/project/143014-compact-25-spectrometer/)

## Energy budgets

Scenarios

* Constantly on wired power
* Periodically used on battery, else plugged in
* Always/normally battery powered
* Energy harvesting. Never connected to charger, should run forever

### Energy harvesting

Energy harvesting rules of thumb:

    Outdoor light – 10mW/cm2
    Industrial temperature difference – 1-10 mW/cm2

    Industrial vibration – 100µW/cm2
    Human temperature difference – 25µW/cm2
    Indoor light – 10µW/cm2
    Human vibration – 4µW/cm2

    GSM RF – 0.1µW/cm2
    Wifi RF – 0.001µW/cm2

[AI and Unreliable Electronics (*batteries not included)](https://petewarden.com/2016/12/29/ai-and-unreliable-electronics-batteries-not-included/). 

### Wireless transmission

TODO: overview of typical energy requirements, for different wireless tech

TODO: overview of data transmission capacity, for different wireless tech
TODO: overview of sending range, for different wireless tech

TODO: cost (monetary) of data transmission, for different wireless techs


## Privacy

Doing more of the data processing locally, enables storing or transmitting privacy sensitive data more seldom.

Ref

* [Scalable Machine Learning with Fully Anonymized Data](https://adamdrake.com/scalable-machine-learning-with-fully-anonymized-data.html)
Using feature hashing on client/sensor-side, before sending to server that performs training.
_hashing trick_ is an established way of processing data as part of training a machine learning model.
The typical motivation for using the technique is a reduction in memory requirements or the ability to perform stateless feature extraction.
While feature hashing is ideally suited to categorical features, it also empirically works well on continuous features

Ideas

* In audio-processing, could we use a speech detection algorithm to avoid storing samples with speech in them?
Can then store/transmit the other data in order to do quality assurance and/or further data analysis. 


# Techniques

Roughly ordered by relevance. Should both be useful for typical tasks and efficiently implementable. 

* Decision trees, random forests
* Convolutional Neural networks (quantized)
* Binary Neural networks
* Support Vector Machines. SVM.
* Naive Bayes
* Nearest Neighbours. kNN. Reduced prototypes 

Ideas

* Metric learning. Specially HDML / Hamming Distance Metric Learning (Norouzi 2012),
since Hamming distance is very compact, and neighbours can be found fast.


Machine learning tasks

* Classification
* Regression
* Prediction
* Outlier/novelty/anomaly detection

## Tree-based methods
Implemented in [emtrees](https://github.com/jonnor/emtrees)

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

Optimization

* Evaluation strategies
http://tullo.ch/articles/decision-tree-evaluation/ discusses flattening vs compiled
https://github.com/ajtulloch/sklearn-compiledtrees implements compiled regression trees for sklearn
* The tree is done as soon as a leaf is reached.
Can we reorder the tree to make this faster for typical data?

QuickScorer (QS). Claims 2-6x speedups over state-of-the-art.
Evaluates the branching nodes of the trees in cache-aware feature-wise order, instead of each tree separately.
Uses a bitvector for the comparison operations.
[Exploiting CPU SIMD Extensions to Speed-up Document Scoring with Tree Ensembles]().
V-QuickScorer (vQS). Extends QuickScorer to use SIMD. Claims a 3.2x speedup with AVX-2, scoring 8 documents in parallel.

* Can we reduce number of nodes in a tree? Using pruning?
* Can we eliminate redundant decisions across trees in the forest?
* How can one make use of SIMD? Do N comparisons at a time
Challenge: Divergent branches
https://github.com/weliveindetail/DecisionTreeCompiler considers SIMD for 
"SIMD-parallelization outweighs its initial overhead only for 7 or more nodes in parallel"
* How to best make use of multithreading?
Split by sample. Only works for batch predictions.
Split by tree. Works also for single sample. 


Related methods

* Deep Neural Decision Forests. [Explained](https://topos-theory.github.io/deep-neural-decision-forests/)
* Deep Forest. https://arxiv.org/abs/1702.08835
* [Convolutional Decision Trees for Feature Learning and Segmentation](https://link.springer.com/chapter/10.1007/978-3-319-11752-2_8). Laptev, 2014.
* Multivariate (oblique) trees. 

Unsupervised

* [Fault Detection using Random Forest Similarity Distance](https://www.sciencedirect.com/science/article/pii/S2405896315017188)

Kernels

* Original Extremely randomized trees paper includes a kernel-based interpretation
* Random Partition Kernels.
[The Random Forest Kernel and creating other kernels for big data from random partitions](https://arxiv.org/abs/1402.4293). 2014. Alex Davies

Metric Learning / similarity / distance learning

* Similarity Forests
* Random forest distance (RFD)

## Naive Bayes
Implemented in [embayes](https://github.com/jonnor/embayes)

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

* Compensate for naiviety, covariance. Bagging, one-against-many

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

## Neural Networks

References

* [Neural-Networks-on-Silicon](https://github.com/fengbintu/Neural-Networks-on-Silicon).
Also has a large section on Model Compression papers for Neural Networks.
* [Embedded-Neural-Network](https://github.com/ZhishengWang/Embedded-Neural-Network).
Large collection of papers for model compression, and for targeting HW acceleration.

Convolutional Neural Networks.

Much more compact models than fully connected for spatial-patterns.


* [Convolutional Neural Networks for Visual Recognition](http://cs231n.github.io/convolutional-networks/).
Explains FC->CONV equivalence, Layer Sizing Patterns,
Generally early layers have few kernels, many pixels (generic features).
Late layers many kernels, few pixels (specific features).
A fully connected (FC) layer can be converted to a CONV layer.
This allows to reduce the number of passes needed over the input,
which is more computationally effective.
Several layers of small kernels (3x3) is more expressive than bigger kernel (7x7),
because they can combine in non-linear ways thanks to activation functions.
Also requires less parameters.

Optimizing CNNs

* [convolution-flavors](https://github.com/gplhegde/convolution-flavors).
Kernel to Row an Kernel to Column tricks save memory.
Also has Vectored Convolution, 1D Winograd Convolution are computationally faster.
* ResNet use stride instead of pooling layers to reduce size. Less computations?
* Grouped convolutions. Not convolving (output of) entire past layers, but just subsets.
Allows to eliminate redundant computations.
https://github.com/ShichenLiu/CondenseNet - approx twice as efficient as MobileNets

### Kernel dictionaries

Use a fixed set of kernels in a CNN or convolutional feature-map extractor.
Store their index instead of individual weights?
To reduce weight storage size for big networks.

Kernel weights 3x3 @ 8 bit = 72 bits.
Kernel map index: 32-256kernels: 5-8 bit.
Approx factor 10x reduction.

Can be done using vector quantization or clustering on the CNN weights.

References

* Clustering Convolutional Kernels to Compress Deep Neural Networks. Sanghyun Son. ECCV 2018.
From a pre-trained model, extract representative 2D kernel centroids using k-means clustering.
Each centroid replaces the corresponding kernels. Use indexed representations instead of saving whole kernels.
Applied to ResNet-18. Outperforms its uncompressed counterpart in ILSVRC2012 with over 10x compression ratio.
3.3 Accelerating convolution via shared kernel representations. Rewriting multiple shared convolutions to Add-then-conv.
3.4 Transform invariant clustering. Vertical,horizontal flip, 90 degree rotation.
Only 32 centroids required for VGG-16 to get reasonable accuracy.
Fig. 5: The 16 most(Top)/least(Bottom) frequent centroids.

### Stacking kernels


* Learning Separable Fixed-Point kernels for Deep Convolutional Neural Networks. Sajid Anwar.
Approximate the separable kernels from non-separable ones using SVD.
Separable. For a K x K filter, the count of weights is reduced from K*K to K+K and the speedup is (K**K)/2K.

### Transfer learning
* DeCAF: A deep convolutional activation feature for generic visual recognition.
DeCAF layers taken from a general task, plus SVM/LogisticRegression training outperform existing state-of-the-art.
* CNN features off the shelf: an astounding baseline for recognition. Pre-trained CNN plus SVM.
"SIFT and HOG descriptors produced big performance gains a decade ago
and now deep convolutional features are providing a similar breakthrough for recognition"
"In any case, if you develop any new algorithm for a recognition task,
it **must** be compared against the strong baseline of generic deep features + simple classifier"

Could one try well-known normalized kernels, instead of learning them?
Ex: Sobel edge detectors, median/gaussian averaging etc.


Could it give performance benefits to flatten a deep model?
Ie use a deep model, compute typical activations for the different layers,
mimick these flat convolutional kernels. Teacher-student type learning.

### Other kernel learning methods
Could one learn CNN kernels using greedy selection of sets of N kernels?

Layer-wise greedy learning can be done. Can be unsupervised or supervised.
Goes back to Y Bengio, 2007. Not so popular in 2015, after ReLu etc improved.
Can still be beneficial for datasets with small amount of labeled samples.
[1](https://stats.stackexchange.com/questions/232616/is-greedy-layer-wise-training-of-deep-networks-necessary-for-successfully-traini)
Especially unsupervised pre-training/initialization, with supervised fine-tuning using back-propagation.
Stacked Autoencoders is one approach. [1](http://ufldl.stanford.edu/wiki/index.php/Stacked_Autoencoders)

[A pre-training strategy for convolutional neural network applied to Chinese digital gesture recognition](https://ieeexplore.ieee.org/document/7586597).
Principal Component Analysis (PCA) is employed to learn convolution kernels as the pre-training strategy.
Called PCA-based Convolutional Neural Network (PCNN).

Gabor filters

* [GaborCNN](https://ieeexplore.ieee.org/document/7726188). 2016. GaborCNN.
Convolutional neural network combined with Gabor filters for strengthening the learning of texture information.
81.53% on ImageNet.
* "Informative Spectro-Temporal Bottleneck Features for Noise-Robust Speech Recognition". 2013.
Uses Gabor filters for feature extraction. On Power-normalized spectrogram.
Filters selected using sparse PCA. Multi-layer-perceptron used, pretrained with Restricted Boltzman Machine.
* "Robust CNN-based Speech Recognition With Gabor Filter Kernels". 2014.
Gabor Convolutional Neural Network (GCNN). Incorporates Gabor functions into convolutional filter kernels.
Gabor-DNN features. 
Power-normalized spectrum (PNS) instead of mel-spectrogram.
Gammatone auditory filters equally spaced on the equivalent rectangular bandwidth (ERB) scale.
Medium-duration power bias is subtracted, where the bias level calculation was based on the
ratio of arithmetic mean and geometric mean (AM/GM ratio) of the medium duration power.
A power nonlinearity with an exponent of 0.1 replaces the logarithm nonlinearity used for compression.
* "".
Gabor Convolutional Networks (GCNs).
Convolutional Gabor orientation Filters (GoFs). Learned convolution filters modulated by Gabor filter. 
Performs slightly better than ResNet with slightly fewers trainable parameters.

Q. When transfer learning on CNNs, can one transfer kernels from different models/architectures.
SubQ. Do kernels in different CNNs tend to be similar? Cluster...

### Model compression

* [Pruning Convolutional Neural Networks for Resource Efficient Inference](https://openreview.net/forum?id=SJGCiw5gl&noteId=SJGCiw5gl). ICLR 2017. Prunin criterion based on Taylor expansion that approximates the change in the cost function induced by pruning network parameters.
Focus on transfer learning. Pruning large CNNs after adaptation to fine-grained classification tasks.
Demonstrates superior performance compared to other criteria, e.g. the norm of kernel weights or feature map activation.
* [Structural Compression of Convolutional Neural Networks Based on Greedy Filter Pruning](https://arxiv.org/abs/1705.07356).
* "Compressing Convolutional Neural Networks in the Frequency Domain". Wenlin Chen.
Called FreshNets. Uses HashedNets for FC parts. Evaluated at 1/16 and 1/64 compression.
* [CNNpack: Packing Convolutional Neural Networks in the Frequency Domain](https://papers.nips.cc/paper/6390-cnnpack-packing-convolutional-neural-networks-in-the-frequency-domain.pdf). Yunhe Wang. NIPS 2016. 41 citations.
Treat convolutional kernels as images. Decompose each kernel into common parts (ie cluster centers),
and residual (unique to the kernel).
A large number of **low-energy frequency coefficients** in both parts can be discarded to
produce high compression without significantly compromising accuracy.
Relax the computational burden of convolution operations in CNNs by linearly
combining the convolution responses of discrete cosine transform (DCT) bases.
Method: kernel coefficients -> DCT -> k-means clustering -> l1 shrinkage -> quantization -> Huffman -> Compressed Sparse Row.
For similar performance, 30-40x compression on AlexNet/VGG16, 10-25x speedup. 13x compression on ResNet50. !!

### Neural Architecture Search
For embedded almost always interested in performance under constraints,
on RAM, FLASH and CPU time / energy usage.
Of interest is to find Pareto-optimal (family of) models,
which offers the best performance/constraint tradeoff.

Large amount of literature linked from
https://www.automl.org/automl/literature-on-neural-architecture-search/

SpArSe: Sparse Architecture Search for CNNs on Resource-Constrained Microcontrollers
https://arxiv.org/abs/1905.12107v1
CNNs for 2kB RAM.

EfficientNet: Rethinking Model Scaling for Convolutional Neural Networks
https://arxiv.org/abs/1905.11946

#### On Random Weights and Unsupervised Feature Learning
NIPS 2010.

In this paper we pose the question, why do random weights sometimes do so well?
Our answer is that certain convolutional pooling architectures can be inherently
frequency selective and translation invariant, even with random weights.
Demonstrate the viability of extremely fast architecture search by using random weights to evaluate candidate architectures,
thereby sidestepping the time-consuming learning process. Process is approximately 30x faster. 
`TODO: does this have modern citations?`

#### AutoML: Methods, Systems, Challenges
https://www.automl.org/book/
2018
Reviews state of the art


#### Efficient Multi-objective Neural Architecture Search via Lamarckian Evolution
Proposes LEMONADE
https://arxiv.org/abs/1804.09081
April 2018 - Feb 2019
Bosch / Uni Freiburg

Trained on CIFAR-10, evaluted on ImageNet64x64
Accuracy versus number of parameters
Pareto optimal over NASNet, MobileNet V1. Parity with MobileNet V2
24-56 GPU days used


### Small Convolutional Neural Nets

* [SqueezeNet: AlexNet-level accuracy with 50x fewer parameters and <0.5MB model size](http://arxiv.org/abs/1602.07360). 2015.
1x1 convolutions over 3x3. Percentage tunable as hyperparameters.
Pooling very late in the layers.
No fully-connected end, uses convolutional instead.
5MB model performs like AlexNet on ImageNet. 650KB when compressed to 8bit at 33% sparsity. 
* [MobileNets: Efficient Convolutional Neural Networks for Mobile Vision Applications](https://arxiv.org/abs/1704.04861). 2017.
Extensive use of 1×1 Conv layers. 95% of it’s computation time, 75% parameters. 25% parameters in final fully-connected.
Also depthwise-separable convolutions. Combination of a depthwise convolution and a pointwise convolution.
Has two hyperparameters: image size and a width multiplier `alpha` (0.0-1.0).
Figure 4 shows log linear dependence between accuracy and computation.
0.5 MobileNet-160 has 76M mul-adds, versus SqueezeNet 1700 mult-adds, both around 60% on ImageNet.
Smallest tested was 0.25 MobileNet-128, with 15M mult-adds and 200k parameters.
* [ShuffleNet](https://arxiv.org/abs/1707.01083). Zhang, 2017.
Introduces the three variants of the Shuffle unit. Group convolutions and channel shuffles.
Group convolution applies over data from multiple groups (RGB channels). Reduces computations.
Channel shuffle randomly mixes the output channels of the group convolution.
* [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://arxiv.org/abs/1801.04381). 2018
Inserting linear bottleneck layers into the convolutional blocks.
Ratio between the size of the input bottleneck and the inner size as the expansion ratio.
Shortcut connections between bottlenecks.
ReLU6 as the non-linearity. Designed for with low-precision computation (8 bit fixed-point). y = min(max(x, 0), 6).
Max activtions size 200K float16, versus 800K for MobileNetV1 and 600K for ShuffleNet.
Smallest network at 96x96 with 12M mult-adds, 0.35 width. Performance curve very similar to ShuffleNet.
Combined with SSDLite, gives similar object detection performance as YOLOv2 at 10% model size and 5% compute.
200ms on Pixel1 phone using TensorFlow Lite.
* [EffNet](https://arxiv.org/abs/1801.06434). Freeman, 2018.
Spatial separable convolutions.
Made of depthwise convolution with a line kernel (1x3),
followed by a separable pooling,
and finished by a depthwise convolution with a column kernel (3x1).
* [FD-MobileNet: Improved MobileNet with a Fast Downsampling Strategy](https://arxiv.org/abs/1802.03750). 2018.
[3 Small But Powerful Convolutional Networks](https://towardsdatascience.com/3-small-but-powerful-convolutional-networks-27ef86faa42d).
Explains MobileNet, ShuffleNet, EffNet. Visualizations of most important architecture differences, and the computational complexity benefits.
[Why MobileNet and Its Variants (e.g. ShuffleNet) Are Fast](https://medium.com/@yu4u/why-mobilenet-and-its-variants-e-g-shufflenet-are-fast-1c7048b9618d).
Covers MobileNet, ShuffleNet, FD-MobileNet.
Explains the convolution variants used visually. Pointwise convolution (conv1x1), grouped convolution, depthwise convolution.

Open source projects

* [nn_dataflow](https://github.com/stanford-mast/nn_dataflow). Energy-efficient dataflow scheduling for neural networks (NNs),
including array mapping, loop blocking and reordering, and parallel partitioning.
* [Sparse-Winograd-CNN](https://github.com/xingyul/Sparse-Winograd-CNN). Efficient Sparse-Winograd Convolutional Neural Networks paper. ICLR 2018.
* [wincnn](https://github.com/andravin/wincnn). Simple python module for computing minimal Winograd convolution algorithms for use with convolutional neural networks. "Fast Algorithms for Convolutional Neural Networks" Lavin and Gray, CVPR 2016.
* [Tencent/FeatherCNN](https://github.com/Tencent/FeatherCNN). High performance inference engine for convolutional neural networks.
For embedded Linux and mobile, especially ARM processors.
* [dll](https://github.com/wichtounet/dll). C++ implementation of Restricted Boltzmann Machine (RBM) and Deep Belief Network (DBN) and their convolution versions.
* [CNN-Inference-Engine-Comparison](https://github.com/HolmesShuan/CNN-Inference-Engine-Quick-View).
Overview of CCN inference engines, and performance.
Shows MobileNetV1 at 60ms on 2-core 1.8Ghz Cortex-A72, ResNet-18 in 200ms.
* [ESP-WHO](https://github.com/espressif/esp-who). Face recognition based on MobileNets, which custom CNN implementation?
* [tflite micro](https://github.com/tensorflow/tensorflow/tree/master/tensorflow/lite/experimental/micro).
TensorFlow Lite for microcontrollers. Since November 2018. Supports ARM Cortex M, RISC-V and Linux/MacOS host.

## Sequence modelling

[Temporal Convolutional Networks](https://arxiv.org/abs/1608.08242). Using convolutions instead of Recurrent Neural Networks.
[An Empirical Evaluation of Generic Convolutional and Recurrent Networks for Sequence Modeling](https://arxiv.org/abs/1803.01271).

## Quantized Neural Networks

Using integer quantization, typically down to 8-bit. Reduces size of weights, allows to use wider SIMD instructions.
Most interesting for low, when applied to already-efficient deep learning architectures. Examples are MobileNet, SqueezeNet.
In microcontrollers, ARM Cortex M4F and M7 can do SIMD operations with 4x 8-bit integers.

Papers

* [Quantization and Training of Neural Networks for Efficient Integer-Arithmetic-Only Inference](https://arxiv.org/pdf/1712.05877.pdf).
Paper on the quantization supported in TensorFlow Lite.
Evaluated on Accuracy versus Latency tradeoff. Tested on Qualcomm Snapdragon 835 LITTLE. Using ReLU6 non-linearity. Primarily 8-bit arithmetics, 32-bit for some parts.
* Papers are expected from CVPR 2018 On-Device Visual Intelligence Challenge (June 2018),
competition focused on improving accuracy/latency tradeoff.


Blogposts

* [Why are Eight Bits Enough for Deep Neural Networks?](https://petewarden.com/2015/05/23/why-are-eight-bits-enough-for-deep-neural-networks/)
* [What I’ve learned about neural network quantization](https://petewarden.com/2017/06/22/what-ive-learned-about-neural-network-quantization/)
* [How to Quantize Neural Networks with TensorFlow](https://petewarden.com/2016/05/03/how-to-quantize-neural-networks-with-tensorflow/)
Allows to quantize in feedforward, but keep backprop as full precision floats.

Software

* [gemmlowp](https://github.com/google/gemmlowp). Low-precision General Matrix Multiplication.
C++ library for optimized GEMM using 8-bit integers, with 32 bit accumulator.
Can utilize SSE4,NEON for SIMD. Seems to run on Cortex M.
Well-documented archiecture and implementation of the quantization.

## Binarized Neural Networks

Bitwise arithmetic packed into integer representations.
Decreases weights storage drastically.
Implementable efficiently on constrained hardware (only fixed-point units).
Also called BNN, Binary Neutral Network, and XNOR neural network. 

References

* [Introduction](https://software.intel.com/en-us/articles/accelerating-neural-networks-with-binary-arithmetic)
* Paper: [Binarized Neural Networks: raining Neural Networks with Weights and Activations Constrained to +1 or −1](https://ai.intel.com/wp-content/uploads/sites/53/2017/06/1602.02830v3.pdf)
* eBNN. Paper: [Embedded Binarized Neural Networks](http://www.eecs.harvard.edu/~htk/publication/2017-ewsn-mcdanel-teerapittayanon-kung.pdf).
Runs MINST with 95% accuracy in under 50ms on Intel Curie. 32bit, 16KB RAM, 32MHz.
Reorders computation compared to BNN to only need a single floating point intermediate value, instead of one per layer.
[Code](https://gitlab.com/kunglab/ddnn). Python module which generates a C header, plus C library.
* [Deep Learning Binary Neural Network on an FPG](https://web.wpi.edu/Pubs/ETD/Available/etd-042717-145953/unrestricted/sredkar.pdf).
332,164 images per second with 85% accuracy on CIFAR-10.
* [Accelerating Binarized Neural Networks: Comparison of FPGA, CPU, GPU, and ASIC](http://jaewoong.org/pubs/fpt16-accelerating-bnn.pdf)
* [YodaNN: An Architecture for Ultra-Low Power Binary-Weight CNN Acceleration](https://arxiv.org/abs/1606.05487).
61.2TOps/sec/Watt at 900uW and 1TOps/sec/watt at 1.2v. 

Another alternative is binary shift networks, which replaces multiplications with bitshifts.

## Support Vector Machines

Strong linear classifier/regressor, also strong non-linear method when using a kernel (polynomial,RBF).

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
* Sampling to speep up training. Usually only on linear SVM.
Stocastic Gradient Descent (SGD), Sequential minimal optimization (SMO)
* Transductive, for semi-supervised learning
* Support vector clustering
* One-class SVM, for anomaly detection
* 

References

* [A basic soft-margin kernel SVM implementation in Python](http://tullo.ch/articles/svm-py/), incl RBF/polynomial/quadratic.
* [Effects of Reduced Precision on Floating-Point SVM Classification Accuracy](https://ac.els-cdn.com/S1877050911001116/1-s2.0-S1877050911001116-main.pdf?_tid=247ac167-834b-4e66-b538-b47bf7bec302&acdnat=1521981076_c65b50281adc8adfd4be4d1d782dd5cc). No dataset required a precision higher than 15 bit.
* [A Hardware-friendly Support Vector Machine for Embedded Automotive Applications](https://www.researchgate.net/publication/224292644_A_Hardware-friendly_Support_Vector_Machine_for_Embedded_Automotive_Applications). Used down to 12 bit without significant reduction in performance.
* [Approximate RBF Kernel SVM and Its Applications in Pedestrian Classification](https://hal.inria.fr/inria-00325810/file/mlvma08_submission_5.pdf).
Paper presents an O(d*(d+3)/2) implementation to the nonlinear RBF-kernel SVM by employing the second-order polynomial approximation.
"Due to their dot-product form, linear kernel SVMs are able to be transformed into a compact form by exchanging summation in classification formula, leading to extremely low O(d) complexity in terms of both time and memory."
* [approxsvm](https://github.com/claesenm/approxsvm): Approximating nonlinear SVM models with RBF kernel.
C++ implementation of a second-order Maclaurin series approximation of LIBSVM models using an RBF kernel.
* [An approximation of the Gaussian RBF kernel for efficient classification with SVMs](https://www.sciencedirect.com/science/article/pii/S016786551630215X). About 18-fold speedup on average, mostly without losing classification accuracy
* [Classification Using Intersection Kernel Support Vector Machines is efficient](https://web.stanford.edu/group/mmds/slides2008/malik.pdf). Intersection Kernel SVM (IKSVM). Constant runtime and space requirements by precomputing auxiliary tables. Uses linear-piecewise approximation.
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

### Nearest Neighbours

Canonical example is kNN.
However conventional kNN requires all training points to be stored, which is typically way too much for a microcontroller.

Variants

* Condensed kNN. Data reduction technique.
Selects prototypes for each class and eliminates points that are not needed.
[sklearn](http://contrib.scikit-learn.org/imbalanced-learn/stable/auto_examples/under-sampling/plot_condensed_nearest_neighbour.html?highlight=condensed)
* Fast condensed nearest neighbor rule. 2005. [Paper](https://dl.acm.org/citation.cfm?id=1102355)
* Approximate nearest neighbours.

References

* [Survey of Nearest Neighbor Condensing Techniques](https://www.thesai.org/Downloads/Volume2No11/Paper%2010-%20Survey%20of%20Nearest%20Neighbor%20Condensing%20Techniques.pdf)
* [Fast Classification with Binary Prototypes](http://users.ices.utexas.edu/~zhongkai/bnc.pdf)

## Existing work

Software libraries

* [Resource-efficient Machine Learning in 2 KB RAM for the Internet of Things](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/kumar17.pdf). Describes Bonsai, a part of Microsoft Research Indias open-source [EdgeML](https://github.com/Microsoft/EdgeML).
Bonsay is tree-based algorithm. Relatively powerful nodes to enable short trees (reduce RAM usage).
Uses sparse trees, and the final prediction is a sum of all the nodes (path-based).
Optimization: `tanh(x) ≈ x if x < 1 and signum(x) otherwise`. Can run on Atmel AVR8
* [ProtoNN: Compressed and Accurate kNN for Resource-scarce Devices](http://manikvarma.org/pubs/gupta17.pdf).
k-Nearest Neighbor implementation. Can run on Atmel AVR8
* [Embedded Learning Library](https://github.com/Microsoft/ELL) by Microsoft.
Set of C++ libraries for machine learning on embedded platforms. Includes code for kNN, RandomForest etc.
Also has some node-based dataflow system in place it seems. JavaScript and Python bindings.
* [Embedded Classification Software Toolbox](https://github.com/ma2th/ecst)
* [uTensor](https://github.com/uTensor/uTensor). Export Tensorflow model to mbed/ARM microcontrollers.
128+ kB RAM and 512kB+ flash recommended.
"3-layer MLP is less than 32kB". Does not support CNNs yet. https://github.com/uTensor/uTensor/issues/99
Not supported on ESP8266/ESP32. https://github.com/uTensor/uTensor/issues/137

Papers

* [Machine Learning for Embedded Systems: A Case Study](http://www.cs.cmu.edu/~khaigh/papers/2015-HaighTechReport-Embedded.pdf)
Support Vector Machines. Target system used for auto-tunic a mobile ad-hoc network (MANET) by
earns the relationships among configuration parameters. Running on ARMv7 and PPC, 128MB+ RAM.
Lots of detail about how they optimized an existing SVM implementation, in the end running 20x faster.

Books

* [Learning in Embedded Systems](https://mitpress.mit.edu/books/learning-embedded-systems), May 1993.

Research groups

* NTNU [Autonomous Adaptive Sensing](https://www.ntnu.edu/iik/aas)
* NTNU Telenor [AI lab](https://www.ntnu.edu/ailab)
* Simula [Relient Networks and Applications](https://www.simula.no/research/projects/center-resilient-networks-and-applications)
* [SINTEF Digital](https://www.sintef.no/digital/om-sintef-ikt/#Vreavdelinger)

Companies

* [SensiML](https://sensiml.com).
ISV providing the SensiML Analytics Toolkit, on-microcontroller ML algorithms and supporting tools.
* ST devices. At WDC2018 announced STM32CubeMX AI. A SDK for neural networks on STM32 micros, and intent to develop NN coprocessor.
Available since December 2018. https://www.st.com/content/st_com/en/stm32-ann.html
Integrated with STM32 device selectors: Analyzes provided model file, and filters possible devices that can fit it.
Supports Keras,Lasagne,Caffee.
Has integrated model compression. 4/8x settings. Templates for validation, system performance check and applications.
Validation compares on-device compressed model against full model, either with random input or custom data files.
Shows ROM,RAM used, time per inference, and time per layer.
Function packs available for audio and motion.
Motion performs Human Activity Detection. HAR.
Uses a 4order high pass at 1Hz to separate gravity component.
Dynamic portion is rotated such that it is always in the same direction, using Rodrigues' rotation formula.
3 different models.
HAR_GMP: ST proprietary design trained on an ST proprietary data set
HAR_IGN: ST simplified design taken from Andrey Ignatov, “Real-time human activity recognition from
accelerometer data using convolutional neural networks”, Applied Soft Computing 62 (2018), pp 915-922
trained on an ST proprietary data set.
HAR_IGN_WSDM: same network topology as HAR_IGN but trained on the public Wireless Sensor Data
Mining (WSDM) dataset in Jennifer R. Kwapisz, Gary M. Weiss and Samuel A. Moore. “Activity Recognition
using Cell Phone Accelerometers” in ACM SIGKDD Exploration Newsletter, volume 12 issue 2, December
2010, pp 74-82.
Audio computes log-mel representation. Acoustic Scene Classification as example, with 3 classes.
ASC. using simplified version of "Virtanen, DCASE 2016 acoustic scene classification using convolutional neural networks"
16kHz. 30 mels, 32 frames, inference every 1024ms.
Android application allows to push labels to the device and store on SDcard. SensorTile hardware used.
Looks like 1mA @ 1.8V average power consumption.
STM32CubeMX AI works OK on Linux when combined with the free.
Tested on an AI project setup from scratch, and STM32L476-Nucleo AI example.
The `Makefile` generation did however not work out-of-the-box.
* [XNOR.ai](https://www.xnor.ai/). 
* [Reality AI](https://reality.ai).
* Lattice Semicondutors. Announced CNN acceleration IP blocks,tools and devkits for their ICE40 FPGAs October 2018.
[eejournal](https://www.eejournal.com/article/lattice-raises-the-bar-on-low-power-ai/).
[Himax HM01B0 UPduino Shield](http://www.latticesemi.com/en/Products/DevelopmentBoardsAndKits/HimaxHM01B0),
with ultra-low-power imaging module and support for 2 microphones.
* STMicrocontrollers. STM32 X-CUBE-AI.
* [Sensory](https://www.sensory.com).
Wakeword/keyword spotting, speech reconginition, biometric authentication.

Blogposts

* [Why the Future of Machine Learning is Tiny (devices)](https://petewarden.com/2018/06/11/why-the-future-of-machine-learning-is-tiny)
Tiny Computers are Already Cheap and Everywhere. Energy is the Limiting Factor.We Capture Much More Sensor Data Than We Use.
* [embedded.com: Bringing machine learning to the edge](https://www.embedded.com/electronics-blogs/say-what-/4460873/Bringing-machine-learning-to-the-edge--A-Q-A-with-Neurala-s-Anatoli-Gorshechnikov-)
Predictions are much lower bandwidth than the raw sensor data (e.g. video)
It allows for local adaptation in the AI logic (L-DNN)
It achieves lower latency between observed event and action resulting from AI logic
"the most important question is what is the least amount accuracy and computation complexity we can do
while still delivering the business value?"
Top mistake: "Continuing with the top down approach ‘let’s make it perform the task first and then squeeze it on device`
instead of switching to bottom up ‘let’s make it run on device and fulfill all hardware constraints first,
and then tune it for the task at hand’."
* [How to run deep learning model on microcontroller with CMSIS-NN](https://www.dlology.com/blog/how-to-run-deep-learning-model-on-microcontroller-with-cmsis-nn/). Why run deep learning model on a microcontroller?
    Sensitive data gets to the cloud, photos, and audio recordings.
    The company who sells this may charge a service fee to use its service and even worse sell your private data.
    It won't work without the network connection to the server.
    Data traveling back and forth between the device and server introduces lag.
    Require network and wireless hardware components on the circuit design which increase the cost.
    It might waste bandwidth sending useless data.



Open hardware platforms

* [OpenMV](https://openmv.io/), very nice machine vision devkit with STMF7 and MicroPython.
Not low-power, 200mA cited. 75 USD.
* [AudioMoth](https://www.openacousticdevices.info/audiomoth).
Field audio recording device designed for battery power.
16 mAh with 10sec rec/10 sec sleep on 96kHz samplerate.
3xAA batteries. Over 100 days runtime.
Silicon Labs Cortex M4F. External 256kB SRAM.
Records and processes up to 384kHz.
50 USD.
[AudioMoth: Evaluation of a smart open acoustic device for monitoring biodiversity and the environment](https://besjournals.onlinelibrary.wiley.com/doi/full/10.1111/2041-210X.12955)
"AudioMoth can be programmed to filter relevant sounds such that only those of interest are saved,
thus reducing post‐processing time, power usage and data storage requirements."
"AudioMoth creates a unique opportunity for users to design specific classification algorithms for individual projects."
uses the Goertzel filter for real‐time classification algorithms.
This filter evaluates specific terms of a fast Fourier transform on temporarily buffered audio samples
without the computational expense of a complete transform. Samples are split into N windows
Precomputed filter coefficients. Hamming window, precomputed.
from 10 to 25 mW consumption when processing samples.
Many of the natural environments most prone to poaching have no Wi‐Fi or mobile coverage,
ruling out the use of cloud‐based acoustic systems.
5‐month total period of field deployment of 87 AudioMoths resulted in 129 hr of audio triggered by positive algorithm responses.
These were identified as false positives from a number of sources, including dog whistles, leaf noise during strong winds, and bird songs.
In comparison, recording continuously for 12 hr per day over the same period would have created 156,600 hr of audio data.
The most energy intensive task on AudioMoth was writing data to the microSD card, which consumed 17–70 mW.
80 μW when sleeping between sample, approx 6 years standby.
Further developments are exploring the potential for networking AudioMoth by LoRa radio,
to link them to a base station for real‐time signalling of acoustic events triggered by the detection algorithm.
record alternative types of data to memory, instead of memory inefficient uncompressed WAV files.
For example, summarise the important characteristics of sounds with measurements known as acoustic indices

## Sparsity

[Sparsity Lesson of Fundamentals of Digital Image and Video Processing](https://www.coursera.org/lecture/digital/applications-MNbjB)
Applications. Noise smoothing, inpainting, superresolution. Foreground/background separation. Compressive sensing.
Images are sparse in DCT decomposition. Can throw away many of the with minimal quality loss.
Noise is not correlated and will not compress well. This fact used in image denoising.
Compute a sparse representation, then reconstruct. Can be done with standard basis like DCT, or a learned dictionary.
Basis pursuit. Matching Pursuit. Orthonogonal Matching Pursuit. 
Foreground/background separation in video. Singular Value Decomposition. 
Can one do foreground separation of audio in a similar manner?

Compressive Data Aquisition. Replace sampling at Nyquist followed by compression with.
Sampling matrices. Suprising result: Random matrices work.


# Applications

## Machine Hearing

General info

* Blog: http://www.machinehearing.org/
Book: Human and Machine Hearing: Extracting Meaning from Sound
[Paper in IEEE, 2010](https://static.googleusercontent.com/media/research.google.com/en//pubs/archive/36608.pdf)
Key ideas. Modelling human hearing. Reusing machine vision learnings by representing sound as (moving) images.
Combined audiovisual models.
* [What’s wrong with CNNs and spectrograms for audio processing?](https://towardsdatascience.com/whats-wrong-with-spectrograms-and-cnns-for-audio-processing-311377d7ccd). Challenges:
Sounds intermix/blend into eachother, ie are "transparent".
Can also have complex relationships like phase cancellation.
Directions in spectogram have different meansings. Frequency,time. Features not invariant wrt to frequency, but generally wrt time.
Activations in the spectrogram are non-local, eg formants.
Sound information is serial 'events', observed only in one instance of time. Not visual stationary 'objects'.
If freezing time, cannot understand much of the information present (compared with video).
Temporal patterns are critical.


## Keyword spotting
Aka "wake word detection"

Existing work on microcontrollers

* [ML-KWS-for-MCU](https://github.com/ARM-software/ML-KWS-for-MCU/tree/master/Deployment).
Speech recognition on microcontroller.
Neural network trained with TensorFlow, then deployed on Cortex-M7, with FPU.
Using CMSIS NN and DSP modules.
* [CASE2012](http://elaf1.fi.mdp.edu.ar/electronica/grupos/lac/pdf/lizondo_CASE2012.pdf).
Implemented speech recognition using MFCC on 16-bit dsPIC with 40 MIPS and 16kB RAM.
A Cortex-M3 at 80 MHz should have 100+MIPS.
* [An Optimized Recurrent Unit for Ultra-Low-Power Keyword Spotting](https://arxiv.org/abs/1902.05026). February 2019.
Introduces `eGRU`, claimed to be 60x faster and 10x smaller than standard GRU cell.
Omits the `reset` gate (and assosicaed weights W_r).
Uses `softsign` instead of sigmoid and tanh. Faster, less prone to saturation.
Uses fixed-point integer operations only. Q15, bitshifts for divide/mul.
3-bit exponential weight quantization. -1,-0.5,-0.25,0,0.25,0.5,1.0. Bitwise operations, no lookup table.
Uses a quantization-aware training. Quantized in forward pass, full precision in backward (for gradient).
Evaluated on Keyword Spotting, Cough Detection and Environmental Sound Classification.
Sampling rate 8kHz. 128 samples STFT window, no overlap. 64 bands. No mel filtering!
250 timesteps for Urbansound8k.
eGRU_opt Urbansound8k scores 61.2%. 3kB model size.
eGRU_arc Urbansound8k score of 72%. Indicates 8kHz enough!

* [How to Achieve High-Accuracy Keyword Spotting on Cortex-M Processors](https://community.arm.com/processors/b/blog/posts/high-accuracy-keyword-spotting-on-cortex-m-processors).
Reviews many deep learning approaches. DNN, CNN, RNN, CRNN, DS-CNN.
Considering 3 different sizes of networks, bound by NN memory limit and ops/second limits. Small= 80KB, 6M ops/inference.
Depthwise Separable Convolutional Neural Network (DS-CNN) provides the best accuracy while requiring significantly lower memory and compute resources.
94.5% accuracy for small network. ARM Cortex M7 (STM32F746G-DISCO).
8-bit weights and 8-bit activations, with KWS running at 10 inferences per second.
Each inference – including memory copying, MFCC feature extraction and DNN execution – takes about 12 ms.
10x inferences/second. Rest sleeping = 12% duty cycle.
* [QuickLogic partners with Nordic Semiconductor for its Amazon Alexa-compatible wearables reference design using Voice-over-Bluetooth Low Energy](https://www.nordicsemi.com/News/News-releases/Product-Related-News/QuickLogic-partners-with-Nordic-Semiconductor-for-its-Amazon-Alexa-compatible-wearables-reference-design-using-Voice-over-Bluetooth-Low-Energy). 2017/11
Always-on wake word detection at 640uWatt typical.
nRF51822 with **external MCU**. EOS S3 SoC’s (Cortex M4F) hardware integrated Low Power Sound Detector.
* [Convolutional Recurrent Neural Networks for Small-Footprint Keyword Spotting](https://arxiv.org/abs/1703.05390).
Uses Per-Channel Energy Normalization on mel spectograms. CRNN with ~230k parameters, acceptably low latency on mobile devices.
Achieves 97.71% accuracy at 0.5 FA/hour for 5 dB signal-to-noise ratio. Down to 45k parameters tested.




General

* [Audio classification overview](http://www.nyu.edu/classes/bello/ACA_files/8-classification.pdf)
Criterias for good features,
PCA/LDA for dimensionality reduction. Sequential forward/backward selection
* [Environmental sound recognition: a survey](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/S2048770314000122) (2014).
Mentiones MPEG-7 based features, efficient and perceptual.
* [Dolph-Chebyshev Window](http://practicalcryptography.com/miscellaneous/machine-learning/implementing-dolph-chebyshev-window/),
good window function for audio. C reference implementation.
* [Voice Activity Detection, tutorial](http://practicalcryptography.com/miscellaneous/machine-learning/voice-activity-detection-vad-tutorial/)
Using 5 simple features.
* [Machine Learning for Audio, Image and Video Analysis](http://www.dcs.gla.ac.uk/~vincia/textbook.pdf).
* [Notes on Music Information Retrieval](https://musicinformationretrieval.com/index.html), series of Jupyter notebooks.
Lots of goodies, from feature extraction to high-level algorithms.
* [Detection and Classification of Acoustic Scenes and Events](https://hal.archives-ouvertes.fr/hal-01123760/document). 2014
Review of state of the art in machine listening.
Problem 1: Acoustic scene classification,
Characterize acoustic environment of an audio stream by selecting a semantic label for it.
Single-label classification. Similar to: Music genre recognition. Speaker recognition.
Also similar to other time-based classification, ie in video.
Approach 1. Bag of frames. Long-term statistical distribution of local spectral features. Ex MFCC.
Compare feature distributions using GMM.
Approach 2. Intermediate representation using higher level vocabulary/dictionary of "acoustic atoms".
Problem 2. Acoustic event detection. Label temporal regions within an audio recording; start time, end time and label for each event instance.
Related to. Automatic music transcription. Speaker diarisation.
Typically treated as monophonic problem, but polyphonic is desirable.
More challening that scene classification.
One strategy to handle polyphonic signals is to perform audio source separation, and then to analyse the resulting signals individually.

Efficiency

* [A multi-layered energy consumption model for smart wireless acoustic sensor networks](https://arxiv.org/abs/1812.06672). Gert Dekkers, 2018.
MATLAB code: https://github.com/gertdekkers/WASN_EM



## Acoustic event detection (AED)

* Aka Automatic Environmental Sound Recognition (AESR)
* Competitions: CLEAR "Classification of Events, Activities and Relation-
ships". DCASE Detection and Classification of Acoustic Scenes and Events (2016,2013)
[website](http://www.cs.tut.fi/~heittolt/research-sound-event-detection) shown progress on same dataset up to modern methods with f1-score=69.3%
using Convolutional Recurrent Neural Networks. Dataset TUT-SED2009 TUT-CASA2009
* [https://ieeexplore.ieee.org/document/7933055/](Bag-of-Features Methods for Acoustic Event Detection and Classification). Grzeszick, 2014/2017.
Features are calculated for all frames in a given time window.
Then, applying the bag-of-features concept, these features are quantized with respect to a learned codebook and a histogram representation is computed.
Bag-of-features approaches are particularly interesting for online processing as they have a low computational cost.
Using GCFF Gammatone frequency cepstral coefficients, in addition to MFCC.
Codebook quantizations used: soft quantization, supervised codebook learning, and temporal modeling.
Using DCASE 2013 office live dataset and the ITC-IRST multichannel.
BoF principle: Learn intermediate representation of features in unsupervised manner. Clustering like k-means
Hard-quantization: All N*K feature vectors are clustered. Only cluster centroids are of interest. Assign based on minimum distance.
Soft-quantization: GMM with expectation maximation. Codebook has mean,variance.
Supervized-quantization. GMM per class, concatenated.
Re-introducing temporality. Pyramid scheme, feature augumentation by adding quantizied time coordinate.
SVM classification. Multiclass. Linear, RBF. *Histogram-intersection kernel* works well.
Random Forests. Works well for AED. Frame size = 1024samples@44.1kZ=22.3 ms
The current python implementation uses a single core on a standard desktop machine and requires less than 20% of the real time for computation.

* [Bird Audio Detection using probability sequence kernels](http://machine-listening.eecs.qmul.ac.uk/wp-content/uploads/sites/26/2017/02/badChallenge_iitMandi.pdf)
Judges award DCASE2016 for most computationally efficient.
MFCC features (voicebox), GMM, SVM classifier from libsvm with probability sequence kernel (PSK).
AUC of 73% without short-term Gaussianization to adapt to dataset differences.

* LEARNING FILTER BANKS USING DEEP LEARNING FOR ACOUSTIC SIGNALS. Shuhui Qu.
Based on the procedure of log Mel-filter banks, we design a filter bank learning layer.
Urbansound8K dataset, the experience guided learning leads to a 2% accuracy improvement.

* [Automatic Environmental Sound Recognition: Performance Versus Computational Cost](https://ieeexplore.ieee.org/abstract/document/7515194/). 2016. Sigtia,...,Mark D. Plumbley
Results suggest that Deep Neural Networks yield the best ratio of sound classification accuracy across a range of computational costs,
while Gaussian Mixture Models offer a reasonable accuracy at a consistently small cost,
and Support Vector Machines stand between both in terms of compromise between accuracy and computational cost.
! No Convolutional Neural networks. ! used MFCC instead of mel-spectrogram

* [EFFICIENT CONVOLUTIONAL NEURAL NETWORK FOR AUDIO EVENT DETECTION](https://www.researchgate.net/publication/320098222_Efficient_Convolutional_Neural_Network_For_Audio_Event_Detection). Meyer, 2017.
structural optimizations. reduce the memory requirement by a factor 500,
and the computational effort by a factor of 2.1 while performing 9.2 % better.
Final weights are 904 kB. Which fits in progmem, but not in RAM on a ARM Cortex M7.
Needs 75% of theoritical performance wrt MACs, which is likely not relalizable.
They suggest use of a dedicated accelerator chip.

* [Robust Audio Event Recognition with 1-Max Pooling Convolutional Neural Networks](https://arxiv.org/pdf/1604.06338.pdf).
! Very shallow network performs similar to state-of-the art in event detection on very noisy datasets.
Convolution (3..25 wide x 52 tall) -> MaxPool per frame -> Softmax across frames.
Claims to also outperform with a single filter width setting.
Also uses window averaging to downsample spectrogram bins to 52 bins instead of typical triangular mel.
This arcitecture should be suitable also for Acoustic Scene Classification?

* [Baby Cry Sound Detection: A Comparison of Hand Crafted Features and Deep Learning Approach](https://link.springer.com/chapter/10.1007/978-3-319-65172-9_15). 2017
Shows that hand-crafted features can give same performance as state-of-art CNN at 20x the computational cost.
Features: Voiced unvoiced counter (VUVC), Consecutive F_0 (CF0), Harmonic ratio accumulation (HRA).
Classifier: Support Vector Data Description (SVDD).
"Further research should investigate ways of reducing complexity of CNN, by decreasing the number of filters and their size"
Dataset was constructed from http://www.audiomicro.com and https://www.freesound.org
Approx 1 hour cry, 1 hour non-cry for training.
! Testing set has only 26 baby cry events (15 min) as base. Upsampled by mixing in noise at 18dB.
Makes 4h of sound with sparse amounts of target event, and 2 hours without.

* [SwishNet: A Fast Convolutional Neural Network for Speech, Music and Noise Classification and Segmentation]()
1D Convolutional Neural Network (CNN). Operates on MFCC, 20 band.
Uses combinations of 1x3 and 1x6 convolutions. Only convolutions across temporal bands.
? Gated activations between each step.
? skip connections with Add.
Architecture inspired by Inception and WaveNet architecture.
Optionally use distilled knowledge from MobileNet trained on ImageNet.
Tested on MUSAN, GTZAN.
! used background noise removal
5k and 18k parameters. Versus 220k for MobileNet.
1ms prediction time for 1 second window on desktop CPU.
! simple problems, GMM baseline performed 96-99% and 90%,
MobileNet Random initialized 98-00% and 94-96%

* Kaggle: The Marinexplore and Cornell University Whale Detection Challenge
[Features & classification approaches](https://www.kaggle.com/c/whale-detection-challenge/discussion/4156).
Many approached used with good results.
Large range in feature sets. Mostly deep learning and tree ensembles, some SVM.
Winner used image template on spectograms with a GradientBoostingClassifier.



## Environmental sound monitoring
Aka

- Environmental Noise Monitoring
- Noise source identification

Datasets

* [Urbansound-8k](https://serv.cusp.nyu.edu/projects/urbansounddataset/urbansound8k.html).
8k samples, 10 classes. Compiled from freesound.org data
* [ESC-50: Dataset for Environmental Sound Classification](https://github.com/karoldvl/ESC-50).
2k samples, 40 classes in 5 major categories. Compiled from freesound.org data
* DCASE 2013. Audio Event Detection. Indoor office sounds. 16 classes. Segmented. 19 minutes total.
* [Google AudioSet](https://research.google.com/audioset/). 2,084,320 human-labeled 10-second sounds, 632 audio event classes. 

Papers

* [Acoustic Event Detection Using Machine Learning: Identifying Train Events](http://cs229.stanford.edu/proj2012/McKennaMcLaren-AcousticEventDetectionUsingMachineLearningIdentifyingTrainEvents.pdf). Shannon Mckenna,David Mclare.
Using RMS over 0.125 seconds and 1/3 octave frequency bands. Classify individual time instances as train-event,
then require a cluster of 3 train events successive. 
"Performance of our classifier was significantly increased when we normalized the noise levels by
subtracting out the mean noise level of each 1/3 octave band and dividing by the standard deviation"
Used Logistic Regression and SVM. From 0.6 to 0.9 true positive rate (depending on site), with `<0.05` false positive rate.
Tested across 10 sites.

Detection of Anomalous Noise Events on Low-Capacity Acoustic Nodes
for Dynamic Road Traffic Noise Mapping within an Hybrid WASN
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5948866/

## Speech commands

Datasets

* [Speech Commands Data Set](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/data).
Kaggle competition required submissions to run in below 200ms on a Raspberry PI3.
* [NOIZEUS: A noisy speech corpus for evaluation of speech enhancement algorithms](http://ecs.utdallas.edu/loizou/speech/noizeus/)
30 sentences corrupted by 8 real-world noises. 
* Mozilla [Common Voice](https://voice.mozilla.org), crowd sourcing. Compiled dataset [on Kaggle](https://www.kaggle.com/mozillaorg/common-voice), 


## Speaker detection

* [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/), 100k utterances for 1251 celebrities.
* [Speakers in the Wild](https://www.sri.com/work/publications/speakers-wild-sitw-speaker-recognition-database)

## Bird audio detection


* DCASE 2018. Audio Event Detection, single-class: bird-present. 6 datasets of some k samples each.
* [BirdCLEF 2016](http://www.imageclef.org/lifeclef/2016/bird). 24k audio clips of 999 birds species



## Human Activity Recognition

Terms used

* Activity Recognition / human activity recognition (AR) 
* Activities of Daily Living (ADL).
* Action recognition
* Fall detection. (FD)

Datasets

* [UniMiB SHAR](http://www.sal.disco.unimib.it/technologies/unimib-shar/)
11,771 samples of human activities and falls. 30 subjects, aged 18 to 60 years. 
17 fine grained classes grouped in two coarse grained classes. 9 types of activities of daily living (ADL), 8 types of falls.
* [UCI: ADL Recognition with Wrist-worn Accelerometer](https://archive.ics.uci.edu/ml/datasets/Dataset+for+ADL+Recognition+with+Wrist-worn+Accelerometer). 16 volunteers performing 14 Activities of Daily Living
* [UCI: Activity Recognition from Single Chest-Mounted Accelerometer](https://archive.ics.uci.edu/ml/datasets/Activity+Recognition+from+Single+Chest-Mounted+Accelerometer). 15 participantes performing 7 activities. 52Hz. 7 classes.
* [PAMAP2 Physical Activity Monitoring Data Set](https://archive.ics.uci.edu/ml/datasets/PAMAP2+Physical+Activity+Monitoring).
100 Hz, 3 IMUs: wrist,chest,ankle. Heartrate 9Hz. 18 physical activities, performed by 9 subjects 
* [LingAcceleration](http://www.ccs.neu.edu/home/intille/data/BaoIntilleData04.html). 20 activities, 20 subjects
* [UCI: Smartphone-Based Recognition of Human Activities and Postural Transitions Data Set](http://archive.ics.uci.edu/ml/datasets/Smartphone-Based+Recognition+of+Human+Activities+and+Postural+Transitions). 30 volunteers age 19-48 years. Six basic activities.
Preprocessed into 2.56 sec sliding windows with 50% overlap (128 readings/window), time+frequency based features.
Total 561 features, 10k instances.
* [UCI: OPPORTUNITY Activity Recognition Data Set](https://archive.ics.uci.edu/ml/datasets/OPPORTUNITY+Activity+Recognition)
Scripted execution with 4 users, 6 runs per user.
7 IMUs plus bunch of other sensors on body and around. 5 tracks of labels. 242 features, 2551 instances.
* [WISDM: Activity prediction](http://www.cis.fordham.edu/wisdm/dataset.php) in lab conditions.
Raw set 6 features, 1M instances, 6 classes.
Preprocessed set 46 fetures, 5k instances.
* [WISDM: Actitracer](www.cis.fordham.edu/wisdm/dataset.php#actitracker), real world data. 0.5% labeled data, rest unlabeled.
500 users. Available both as raw motion and preprocessed. Preprocessed data has 5k labeled classes. 6 basic classes.

Existing work

* [Efficient Activity Recognition and Fall Detection](https://dis.ijs.si/ami-repository/datasets/14/Kozina-Efficient_Activity_Recognition_and_Fall_Detection_Using_Accelerometers.pdf)
* [Limitations with Activity Recognition Methodology & Data Set](http://www.cis.fordham.edu/wisdm/Lockhart_Weiss_HASCA.pdf).
Focuses on model type, how AR training and test data are partitioned, and how AR models are evaluated.
personal, hybrid, and impersonal/universal models yield dramatically different performance.
* [Transfer Learning for Activity Recognition: A Survey](http://eecs.wsu.edu/~cook/pubs/kais12.pdf).
Summarizes 30+ papers using transfer learning.

## Gesture recognition

Using IMUs.

Datasets

* [martWatch Gestures Dataset](https://tev.fbk.eu/technologies/smartwatch-gestures-dataset)
8 users, 20 repetitions of 20 different gestures. 3-axis accelerometer
* [Australian Sign Language signs Data Set](https://archive.ics.uci.edu/ml/datasets/Australian+Sign+Language+signs).
95 signs were collected from five signers. Noisy. XYZ, roll, plus finger bend.
* [A Survey of Datasets for Human Gesture Recognition](https://diuf.unifr.ch/people/lalanned/Articles/RuffieuxHCII2014.pdf)
lists some 15 datasets, but only for image-based gesture recognition, mostly collected with Kinect.

Existing work

* [Xie & Pan 2014 - Accelerometer Gesture Recognition](http://cs229.stanford.edu/proj2014/Michael%20Xie,%20David%20Pan,%20Accelerometer%20Gesture%20Recognition.pdf). Dynamic-Threshold Truncation feature preprocessing increased.
With 5 classes and only 1 training example per-class was able to reach 96% accuracy.
Using multiple examples, both SVM and Naive Bayes performed well.
* [uWave: Accelerometer-based Personalized Gesture Recognition and Its Applications](http://www.ruf.rice.edu/~mobile/publications/liu09percom.pdf). Using template gestures and Dynamic Time Warping
* [](http://journals.sagepub.com/doi/full/10.5772/60077). Reviews existing methods of HMM and DTW.
Proposes an improved a distance-based model with kNN classification with low computational overhead.
Large margin nearest neighbour (LMNN).
* [](http://ieeexplore.ieee.org/document/7382120/). Uses accelerometer data directly as features. Using FastDTW.
* [Transfer Learning Decision Forests for Gesture Recognition](http://jmlr.csail.mit.edu/papers/volume15/goussies14a/goussies14a.pdf). 2014
* [PERSONALIZING A SMARTWATCH-BASED GESTURE INTERFACE WITH TRANSFER LEARNING](http://www.eurasip.org/Proceedings/Eusipco/Eusipco2014/HTML/papers/1569922319.pdf). Haar Wavelet Transform. Supervised Local Distance Learning. 5% increase in accuracy with transfer compared to without.
* [High Five: Improving Gesture Recognition by Embracing Uncertainty](https://arxiv.org/pdf/1710.09441.pdf).
Builds a model of the errors of gestures, and uses it to improve HMM-based classifier.

Feature processing

* Vector quantization
* Acceleration statistics
* Motion histogram
* Zero velocity compensation (ZVC)
* DWT. [FastDWT](https://cs.fit.edu/~pkc/papers/tdm04.pdf), approximation of DTW in linear time and linear space.


## Vibration analysis
Often used for 'machine condition' analysis, especially for rotating machines.

* [Fundamentals of Vibration Measurement and Analysis Explained](http://www.lifetime-reliability.com/free-articles/maintenance-management/Fundamentals_of_Vibration_Measurement_and_Analysis_Explained.pdf), explains how to capture data, process it to commonly used features etc
* [Beginning Vibration Analysis](http://www.vibranalysis.co.za/ctc/pdf/pubTechPapers/01-Beginning%20Vibration%20Analysis.pdf),
page 82+ shows data for some problematic cases

## Predictive maintenance

[NASA Prognostics Data Repository](https://ti.arc.nasa.gov/tech/dash/groups/pcoe/prognostic-data-repository).
Collection of datasets for operational and failed systems. Thermal, vibration, electronical


## Computer vision

"Recent studies show that the latencies to upload
a JPEG-compressed input image (i.e. 152KB) for a single inference
of a popular CNN–“AlexNet” via stable wireless connections with
3G (870ms), LTE (180ms) and Wi-Fi (95ms), can exceed that of DNN
computation (6∼82ms) by a mobile or cloud-GPU."
Moreover,the communication energy is comparable with the associated DNN computation energy.

Y. Kang, J. Hauswald, C. Gao, A. Rovinski, T. Mudge, J. Mars, and L. Tang,
“Neurosurgeon: Collaborative intelligence between the cloud and mobile edge,”
in Proceedings of the Twenty-Second International Conference on Architectural Support
for Programming Languages and Operating Systems. ACM, 2017, pp. 615–629.

Question.

* Can one do classification and object detection on compressed JPEG straight from the camera?
Operating on the blocks with DCT coefficients.

[Faster Neural Networks Straight from JPEG](https://openreview.net/forum?id=S1ry6Y1vG).
ICL2018. Modified libjpeg to return DCT coefficients. Blocks of 8x8. On ResNet50, 1.77x faster, same accuracy.
[On using CNN with DCT based Image Data](https://www.scss.tcd.ie/Rozenn.Dahyot/pdf/IMVIP2017_MatejUlicny.pdf). IMVIP 2017.

Can it be also done in a streaming fashion?

References

* [JPEG DCT, Discrete Cosine Transform (JPEG Pt2)- Computerphile](https://www.youtube.com/watch?v=Q2aEzeMDHMA).
Excellent visual walkthrough of JPEG compression and decompression. CbCrY,DCT,quantization,Huffman encoding. 


Tools

* [VLFeat](http://www.vlfeat.org/api/index.html).
Portable C library with lots of feature extractors for computer vision tasks.

### Segmentation

[ENet: A Deep Neural Network Architecture for Real-Time Semantic Segmentation](https://towardsdatascience.com/enet-a-deep-neural-architecture-for-real-time-semantic-segmentation-2baa59cf97e9)
0.7 MB weights (16 bit floats). 3.83 GFLOPS on 3x640x260 images.




## New sensor types

[How ML/DL is Disrupting Sensor Design](https://drive.google.com/file/d/0BzrlDxVZWSUpbkZrRnlMbmE2c2s/view).
Compressed sensing. Random projections.

[Rise of the super sensor](https://www.computerworld.com/article/3197685/internet-of-things/google-a-i-and-the-rise-of-the-super-sensor.html).
CMU has developed a generic 'synthetic sensor', using audio/vibration etc.
"the revolution is to install a super sensor once, then all future sensing (and the actions based on that sensing)
is a software solution that does not involve new devices"

Soft Robotics
[Youtube video about easy-to-construct soft gripper with integrated resistive sensors](https://www.youtube.com/watch?v=BLE5yhS3k3I).
Could train algorithms to detect objects gripped.

## Time series

Deep learning for time series classification: a review. https://arxiv.org/abs/1809.04356
Compares many different model types across 97 time-series datasets.
Finds that CNNs and ResNet performs the best.

# Application ideas

## Anomaly detection in 3d-printing

Consumer grade machines should just work, be safe in operation and guide user to do the right thing.
Also very price sensitive and mostly sold as a standalone appliance, makes microcontrollers attractive.

Sensors:

* Accelerometer on toolhead.
* High-speed current sensing of motors.
* Microphone
* Should one have tachometer on fan(s), so one can eliminate them more easily?

### Function

that can be implemented with sensors and machine learning

Detect malfuctions

* Print loose from bed, printing into thin air
* Warping, print lifts up on one side and starts pushing more on part
* Bottom layer too close to bed, usually leaves.
* Oozing or other source has left blob in model.
* Other unexpected obstruction of the toolhead, like a human hand
* Skipped steps

Detect wear/maintenance need

* Insufficient lubrication of linear bearings
* Timing belt slop/backlash. Might need to know the gcode/pathplanning
* Fan bearings worn out. Usually vibrates more and makes noise

Cost saving

* Sensors can maybe replace need for physical endstops for XY
* Sensors can maybe be used for probing Z level/bed


# Online learning

It is also desirable to learn on-the-fly.
First level is hybrid systems where new samples is used to tune/improve a pre-trained model.
More advanced is on-line training which can automatically detect new classes.
Get closer to typical Artificial Intelligence field, since now have an intelligent agent able to learn on its own.

Hybrid learning, adaptive machine learning, progressive learning, semi-supervised learning.
Q-learning (reinforcement learning).

# Transfer learning

Kinds of transfer learning

* Inductive transfer. Few labeled target data is available. Source data is used as auxillary.
* Transductive transfer. Lots of labeled source data. Lots of unlabeled data in target.
* Unsupervised transfer. Both source and target data is unlabeled.

Note: in transfer learning, performance on source dataset is generally ignored.
Goal is good performance on target.

How to transfer

* Instance based. Reuse instances in source domains that are similar to target domain.
Ex: Instance reweigthing, importance sampling
* Feature based. Find an alternate feature space for learning target domain, while projecting source into this space.
Feature subset selection, feature space transformation. 
* Model/parameter based. Use model parameters/hyper-parameters to influence learning target.
Parameter-space partitioning, superimposing shape constraints.

Boosting based transfers

* TrAdaBoost
* TransferBoost. Based on AdaBoost

References

* [Boosting based transfer learning](https://www.slideshare.net/ashok124/thesis-presentation-51445891)
* [Learn on Source, Refine on Target: A Model Transfer Learning Framework with Random Forests]().
Shows two methods of adapting a Random Forest. Structure Expansion Reduction (SER) and Structure Transfer (STRUT).
* [Transfer Learning Decision Forests for Gesture Recognition](). 2014.
Mixed information gain, which is a data-based regularizer. 
Label propagation, which infers the manifold structure of the feature space.
* [Transferring Knowledge by Prior Feature Sampling](). 2008.
Tested on Time series classification (TSC).
Simple modification to the Gradient Boosting Trees learning algorithm using information about the importance of features.

# Change detection

Novelity detection.
Anomaly detection.

Change point detection.
In Time series, at which point something changes.
Often growth rate. Can also be amplitude.
Changes in distribution.

Breakout detection.
In time series, when the mean shifts relatively suddenly.
Mean divergence/shift. Or transition too/from (rampup).

Usecases

* Network Intrusion Detection (IDS)
* Condition Monitoring of machines

Resources

* [Change point detection in time series data with random forests](https://www.sciencedirect.com/science/article/pii/S0967066110001073)
* [Two approaches for novelty detection using random forest](https://www.sciencedirect.com/science/article/pii/S0957417414008070)
* [Introduction to Anomaly Detection: Concepts and Techniques](https://iwringer.wordpress.com/2015/11/17/anomaly-detection-concepts-and-techniques/). Very good overview, with recommendations for different cases
* [Awesome Time Seeries Anomaly Detection](https://github.com/rob-med/awesome-TS-anomaly-detection).
Lists software packages and a few labling tools and benchmark datasets.
* [Twitter: Introducing practical and robust anomaly detection in a time series](https://blog.twitter.com/engineering/en_us/a/2015/introducing-practical-and-robust-anomaly-detection-in-a-time-series.html).
* [](https://anomaly.io/anomaly-detection-using-twitter-breakout/).
Based on Mean Shift Clustering.
Based on algorithm called E-Divisive.
E-Divisive with Medians (EDM) faster version, estimates median using interval trees. 
Mentions Moving Median as a statistic which is robust to anomalies.
* [Anomaly detection and condition monitoring](https://towardsdatascience.com/how-to-use-machine-learning-for-anomaly-detection-and-condition-monitoring-6742f82900d7).
PCA for dimensionalty reduction, and using Mahalanobis distance (MD) threshold for anomaly detection.
AutoEncoder as alternative. Learned dimensionality reduction, using probability distribution of recontruction error for anomaly detect.
Demonstrated on NASA Gear Bearing failure example.
By Axibit AS.
* [Anomaly detection strategies for IoT sensors](https://medium.com/analytics-vidhya/anomaly-detection-strategies-for-iot-sensors-6281e84263df)
Point-wise anomalies: individual devices.
Collective anomalies: multiple devices together.
Contextual anomalies: takes into account context, such as day-of-week etc.

Software

* [tslearn](https://github.com/rtavenar/tslearn).
Time-series machine learning tools. scikit-learn inspired
* [seglearn](https://github.com/dmbee/seglearn)
Time-series. scikit-learn inspired.
* [banpei](https://github.com/tsurubee/banpei).
Change-point detection using Singular Spectrum Transform (SST),
Outlier detection using Hotelling's theory.


Datasets

* [Outlier Detection DataSets (ODDS)](http://odds.cs.stonybrook.edu/).
Huge number of datasets.
In multiple groups:
Multi-dimensional point,
time-series point (uni/multivariate),
time-series graph data,
adverserial/attack data,
* Numenta Anomaly Benchmark [NAB](https://github.com/numenta/NAB).
50+ different time-series, benchmarked on many methods.
* [UCSD Anomaly Detection Dataset](http://svcl.ucsd.edu/projects/anomaly/dataset.htm).
Video of pedestrian walkway. Anomalies are non-pedestrians.
A subset has pixel-level masks. 

Methods

* [DeepADoTS](https://github.com/KDD-OpenSource/DeepADoTS).
From paper "A Systematic Evaluation of Deep Anomaly Detection Methods for Time Series". 
Implements 7 deep neural models for anomaly detection.
* [telemanom](https://github.com/khundman/telemanom).
STMs to detect anomalies in multivariate time series data.
Includes anomaly dataset from NASA Mars Rover.

# Research questions

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

# Prototyping

Hardware platform

* Microcontroller with connectivity. Ex: ESP8266/ESP32 with WiFi/BLE.
Or some ARM Cortex M, possibly with LORA/NBIOT. Or NRF51/NRF52 ARM Cortex with integrated BLE.
LoRa -> Wifi bridge. [Wemos TTGO](https://www.banggood.com/2Pcs-Wemos-TTGO-433470MHz-SX1278-ESP32-LoRa-0_96-Inch-Blue-OLED-Display-Bluetooth-WIFI-Module-p-1271663.html?rmmds=search&cur_warehouse=CN)
LoRa module. [1](https://www.banggood.com/LoRa-SX1278-Long-Range-RF-Wireless-Power-Mental-Module-For-Arduino-p-1159089.html?rmmds=search&cur_warehouse=CN)
STM32F030. [devkit](https://www.banggood.com/5Pcs-STM32F030F4P6-Small-Systems-Development-Board-CORTEX-M0-Core-32bit-Mini-System-p-1221406.html?rmmds=search&cur_warehouse=CN)
[NRF52: ADC capturing at 4uA using RTC](https://github.com/NordicPlayground/nRF52-ADC-examples/tree/master/saadc_low_power)
NRF52. Bluetooth 5.0, up to 100 meters. ADC. 15us=66kHz, good for 2-4 channel lowfi audio.
NRF51. Bluetooth 4.2, 30 meters typ max. ADC. 68us=17kHz for 10bit, OK for 1-channel lowfi audio.
[100-250uA analog, 700-1000uA digital microphone consumption](https://devzone.nordicsemi.com/f/nordic-q-a/19208/nrf52-microphone-saadc-pdm-or-i2s)
* Microphone. [Analog](https://www.digikey.co.uk/products/en/audio-products/microphones/158?k=microphone&k=&pkeyword=microphone&FV=ffe0009e%2Ca40062&quantity=0&ColumnSort=1000011&page=1&stock=1&nstock=1&datasheet=1&pageSize=25)
[I2S](https://www.digikey.co.uk/products/en/audio-products/microphones/158?FV=ffe0009e%2Ca4027e&quantity=&ColumnSort=1000011&page=1&k=microphone&pageSize=25&pkeyword=microphone)
SPV0840LR5H-B, Microphone MEMS 60 uA.
MCP6231 20uA. 300kHz gain*bw.
TL062. 200uA

* IMU
* Piezo vibration sensor? Cheaper than high-frequency accelerometer? Useful when wanting many sensors.
* SPI ADC, [MCP3002](https://www.digikey.no/product-detail/en/microchip-technology/MCP3002T-I-SN/MCP3002T-I-SN-ND/319415)
* Camera. OV7670 (VGA-QCIF).
[Making work with STM32](http://embeddedprogrammer.blogspot.no/2012/07/hacking-ov7670-camera-module-sccb-cheat.html)
QCIF 176x144 is approx 40kB color, 20kB grayscale.
Version with AL422 FIFO is maybe a bit easier to interface. 8bit parallel readout.
[ex](https://www.aliexpress.com/item/J34-Free-Shipping-AL422-640x480-CMOS-With-3M-Bits-OV7670-FIFO-Camera-STM32-Chip-Driver-Module/32579976662.html).
OV7725. Older chip, rare now. [Object tracking with STM32](http://blog.tkjelectronics.dk/2014/01/color-object-tracking-with-stm32-ov7725/)
OV5647 RPi camera module.. 5MPi. MIPI CSI-2, too fast for microcontroller. Need FPGA or dedicated pheripheral? Overkill 
[ArduCAM](https://github.com/ArduCAM/Arduino) support 10+ camera modules incl OV7670. ESP8266 also supported.


Testcases

* Detect machine start/stop/running. Dishwasher, CNC. Accelerometer/microphone
* Detect door open/close. Accelerometer/microphone
* Detect speech present/not. Microphone
* Detect a hand gesture. Accelerometer
* Detect a spoken command. Microphone
* Detect/Estimate room occupancy. Accelerometer,microphone,PIR

### Hackerspace indoor monitor
Build and deploy in IoT hackathons

Sensor node

Temperature, Humidity. DHT22
PM2.5, PM10. SDS011
Sound level. ?
CO2: ?

Status display/sign

Air mufflers: Lit if sound too high
Dust mask: Lit if finedust too high 



# Funding


## Industry partners

Key technologies

* Microcontroller
* Embedded Systems
* Sensors
* Machine learning

## Grants

* [IEEE Computational Intelligence Society Graduate Student Research Grants](https://cis.ieee.org/graduate-student-research-grants.html).
1-4k USD. Housing costs, travel costs for visiting external institution.
Deadline: April-March?. Need to be student member of IEEE CIS 

Travel support

* [NUUG](https://www.nuugfoundation.no/no/reisestipend/utlysning-2018.shtml).
1 page report, up to 10k NOK.
* [UMB forskningsfond](https://www.nmbu.no/forskning/forskere/forskningsfinansiering/intern/node/27932).
3 page report, up to 30k NOK.
Challenge: most money tied to agriculture.

# Writing

http://approximatelycorrect.com/2018/07/10/troubling-trends-in-machine-learning-scholarship/

Avoid anthropomorphic language

Ask “what worked?” and “why?”, rather than just “how well?”
Strongest empirical papers include:
* error analysis
* ablation studies
* robustness checks

"Would I rely on this explanation for making predictions or for getting a system to work?"

ML Paper Checklist
https://github.com/N-McA/ml-paper-checklist/blob/master/README.md



# Dissemination

## Paper publishing

* WikiCFP
[embedded system](http://www.wikicfp.com/cfp/servlet/tool.search?q=embedded+system&year=f)
[machine learning](http://www.wikicfp.com/cfp/servlet/tool.search?q=machine+learning&year=f)
[sensor](http://www.wikicfp.com/cfp/servlet/tool.search?q=sensor&year=f)

CFPs

* SENSORS Special Issue: Algorithm and Distributed Computing for the Internet of Things. Nov 30.
[CFP](http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=74395&copyownerid=54155)
"original, unpublished high-quality articles, not currently under review by another conference or journal, clearly focused on theoretical and implementation solutions for IoT, including intelligent approaches"

Journals

* IJASUC: International Journal of Ad hoc, Sensor & Ubiquitous Computing. Open-access, bi-monthly.
[CFP example](http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=66923&copyownerid=33993)
* SDAP: Smart Devices, Applications, and Protocols for the IoT. (bi)Yearly.

Conferences

* iWOAR 2018. International Workshop on Sensor-based Activity Recognition and Interaction. Berlin, September.
[CFP 2018](http://www.wikicfp.com/cfp/servlet/event.showcfp?eventid=73357&copyownerid=76599). June 15. 

## Blogposts

Topics

* Demo/announce of embayes
* Demo/announce of emtrees
* Supervised machine learning on microcontroller: Data collection and labeling (ex using ESP8266)
* Feature engineering/processing with MicroFlo

Ideas

* Machine learning for microcontroller/DSP engineers.
Using ML tools/workflows to tune/tweak paramters of DSP chain and evaluate results 


# emlearn
    
## Compared to sklearn-porter

    Only support C language
    Uses float instead of doubles
    Support for integer-math only
    No dynamic allocations


## Wishlist
Demos:
    Audio Event Detection. MicroPopcorn popping detector->turn off & notify.
    Gesture recognition capacitive sensor arrays. Sign language? Humidity sensor? Detect fluid type? Water vs saltwater vs coke vs juice?
    Human activity recognition accerelometer.
    Gesture recognition accelerometer.
    Wakeword/keyword spotting audio.
    Voice command/control audio.
    Object recognition image.
    Anomaly detection. Isolation Forest.
    Gaussian Mixture Model+Hidden Markov Model. Viterbi algorithm. Especially for sequences.

Feed-Forward Support Vector Machine Without Multipliers
https://ieeexplore.ieee.org/abstract/document/1687940
Fixed-point arithmetic, using only shift and add operations.
Maintains good classification performance respect to the conventional Gaussian kernel.

### Capacity modelling tools

Purpose: Check if a proposed model fits within contraints.
Model storage, memory usage, inference time, CPU "utilization"
Allow to declare budgets, function for checking if over?

Device benchmark:

eml_bench_device
    multiply_adds/second,
    convolutions_3x3/second
    node_evaluations/second (trees)
    ffts/second (melspec)

    Average, standard deviation, 75%, 95%

Ran for each supported hardware. Publish numbers

Perf modelling.
 
    takes perf constants from benchmark
    + ML model 
    => estimate model size, mem use, inference time 

Model benchmark

    Test the real model.
    Verify against Perf model.
    Do this for a set of example models, publish numbers


Models:

    Generic linear model. SVC,LogisticRegression
    Kernel. SVM

On-line DSP tools:

    Streaming summarizers/estimators. min/max, mean/std, median
    Reservoir sampling.
    Voice Activity Detection
    Sound level. Incl IEC A-weighting

Transformers:

    Scalers: Standard,MinMax
    Dimensionality: PCA,NMF

Perf:

    8/16bit weights. NNs
    Integer-math only for compiled trees. 32bit/8bit
    Support sparse models. Autoreduce during conversion?
    Sparse dictionary representations

Advanced stuffs

    Audio beamforming.


# Microcontroller implementation

## Audio processing

MFCC Feature extration

* [KWS](https://github.com/ARM-software/ML-KWS-for-MCU/blob/8ea22926f743f53c7d17d9c73eb2f1b22257ebe2/Deployment/Source/MFCC/mfcc.cpp)
Runs on ARM Cortex M(4F). Uses CMSIS for FFT. Clear code struture. Some things, like filterbank, can be precomputed in Python? Apache 2.0
* [libmfcc](https://github.com/wirahayy/libmfcc/blob/master/libmfcc.c). Takes FFT spectrum as input. MIT.
* Fixed-point is challenging. A naive approach to fixed-point FFT causes noise to go up a lot, and classification ability is drastically reduced.
Optimized implementation proposed in  [Accuracy of MFCC-Based Speaker Recognition in Series 60 Device](https://link.springer.com/content/pdf/10.1155/ASP.2005.2816.pdf)

FFT on microcontroller

* STM32F103 (Cortex M3 at 72MHz) can do 1024 point FFT in 3ms using CMSIS, Q15/Q31 fixed point. radix-4 FFT.
STM32F091 (Cortex M0 at 48Mhz) takes 20 ms.
[STM32 DSP](http://www.st.com/content/ccc/resource/technical/document/application_note/group0/c1/ee/18/7a/f9/45/45/3b/DM00273990/files/DM00273990.pdf/jcr:content/translations/en.DM00273990.pdf).
Using software-emulated floating point for FFT on Cortex M4 is 10x slower than the FPU unit.
M4F is 3-4 times as energy efficient as the M3 (when using floats?).
* [EMF32 DSP](https://www.silabs.com/documents/public/application-notes/AN0051.pdf).
CMSIS FFT is about 3-4x faster than a generic KissFFT-based version.
* Teensy 3.2 was able to do approx 400 ops/sec (3ms) on 512 point FFT with generic version, using int32.2
[OpenAudio Benchmarking FFT](http://openaudio.blogspot.no/2016/09/benchmarking-fft-speed.html).
* [FFT on ARM-Based Low-Power Microcontrollers](https://pdfs.semanticscholar.org/9eca/f67d19b8df4a508ad5c3d198989b70f16aa6.pdf)
found that CMSIS FFT with Q31 had slightly less error than with F32.
* [esp32-fft](https://github.com/fakufaku/esp32-fft). 1024 lenght float32 FFT in 1ms on ESP32.


Goertzel filter

* [embedded.com The Goertzel Algorithm](https://www.embedded.com/design/configurable-systems/4024443/The-Goertzel-Algorithm),
example code in C++.
* [embedded.com Single tone detection with Goertzel](https://www.embedded.com/design/real-world-applications/4401754/Single-tone-detection-with-the-Goertzel-algorithm). Example code in C++
* [Efficiently detecting a frequency using a Goertzel filter](https://netwerkt.wordpress.com/2011/08/25/goertzel-filter/),
several implementation variants in C.
* Matched Filter Design
The Goertzel algorithm is advantageous compared to the FFT when
`M < 5/6 log_2(N)`, with DFT length N and number of desired pins M.
N=1024, M=8.
* [Overlap Add STFT implementation of linear filters](https://www.dsprelated.com/freebooks/sasp/Overlap_Add_OLA_STFT_Processing.html)
Faster than convolution in time domain for FIR
 filters with n>64 taps, which can happen in audio without noticable delay 
* https://stackoverflow.com/questions/11579367/implementation-of-goertzel-algorithm-in-c

