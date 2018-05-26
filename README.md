# Machine learning on embedded devices

Focused primarily on running inference/prediction/feed-forward part on a microcontroller (or small embedded device).
Training phase can run on a standard computer/server, using existing tools as much as possible.

# Status
**Research in progress**

* Decision trees ensembles implemented in [emtrees](https://github.com/jonnor/emtrees)
* Naive Bayes implemented in [embayes](https://github.com/jonnor/embayes)

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
* Speech/command recognition as human input device, using microphone. Keyword detection
* Battery saving in wireless sensors. Normally sending day/week aggregates, on event detection send data immediately
* Health status of animals via activity detected using accelerometer
* Monitoring eating activity using accelerometer [1](https://www.sciencedirect.com/science/article/pii/S0010482515000086)
* Environmental monitoring, using microphone to detect unwanted activity like cutting down trees
* Adaptive signalling and routing for wireless transmission in Wireless Sensor networks

# Techniques

Roughly ordered by relevance. Should both be useful for typical tasks and efficiently implementable. 

* Decision trees, random forests
* Naive Bayes
* Binary Neural networks
* Support Vector Machines. SVM.
* Nearest Neighbours. kNN.
* k-means clustering.
* PCA
* Independent Component Analysis (IDA). 
Unsupervised, data-driven technique for blind source separation.

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

Random Forests, Extra trees.

Resources

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

### Support Vector Machines

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
* ST devices. At WDC2018 announced STM32CubeMX.A SDK for neural networks on STM32 micros, and intent to develop NN coprocessor.



# Applications

## Audio classification

Existing work on microcontrollers

* [ML-KWS-for-MCU](https://github.com/ARM-software/ML-KWS-for-MCU/tree/master/Deployment).
Speech recognition on microcontroller.
Neural network trained with TensorFlow, then deployed on Cortex-M7, with FPU.
Using CMSIS NN and DSP modules.
* [CASE2012](http://elaf1.fi.mdp.edu.ar/electronica/grupos/lac/pdf/lizondo_CASE2012.pdf).
Implemented speech recognition using MFCC on 16-bit dsPIC with 40 MIPS and 16kB RAM.
A Cortex-M3 at 80 MHz should have 100+MIPS.

MFCC Feature extration

* [KWS](https://github.com/ARM-software/ML-KWS-for-MCU/blob/8ea22926f743f53c7d17d9c73eb2f1b22257ebe2/Deployment/Source/MFCC/mfcc.cpp)
Runs on ARM Cortex M(4F). Uses CMSIS for FFT. Clear code struture. Some things, like filterbank, can be precomputed in Python? Apache 2.0
* [libmfcc](https://github.com/wirahayy/libmfcc/blob/master/libmfcc.c). Takes FFT spectrum as input. MIT.
* Fixed-point is challenging. A naive approach to fixed-point FFT causes noise to go up a lot, and classification ability is drastically reduced. Optimized implementation proposed in  [Accuracy of MFCC-Based Speaker Recognition in Series 60 Device](https://link.springer.com/content/pdf/10.1155/ASP.2005.2816.pdf)
* STM32F103 (Cortex M3 at 72MHz) can do 1024 point FFT in 3ms using CMSIS, Q15/Q31 fixed point. radix-4 FFT.
STM32F091 (Cortex M0 at 48Mhz) takes 20 ms.
[STM32 DSP](http://www.st.com/content/ccc/resource/technical/document/application_note/group0/c1/ee/18/7a/f9/45/45/3b/DM00273990/files/DM00273990.pdf/jcr:content/translations/en.DM00273990.pdf).
Using software-emulated floating point for FFT on Cortex M4 is 10x slower than the FPU unit.
M4F is 3-4 times as energy efficient as the M3 (when using floats?).
[EMF32 DSP](https://www.silabs.com/documents/public/application-notes/AN0051.pdf).
CMSIS FFT is about 3-4x faster than a generic KissFFT-based version.
Teensy 3.2 was able to do approx 400 ops/sec (3ms) on 512 point FFT with generic version, using int32.2
[OpenAudio Benchmarking FFT](http://openaudio.blogspot.no/2016/09/benchmarking-fft-speed.html).
[FFT on ARM-Based Low-Power Microcontrollers](https://pdfs.semanticscholar.org/9eca/f67d19b8df4a508ad5c3d198989b70f16aa6.pdf)
found that CMSIS FFT with Q31 had slightly less error than with F32.

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

### Tools

* [librosa](https://librosa.github.io/librosa/feature.html)
* [essentia](http://essentia.upf.edu/documentation/algorithms_overview.html)

### Datasets

* [Urbansound-8k](https://serv.cusp.nyu.edu/projects/urbansounddataset/urbansound8k.html).
8k samples, 10 classes. Compiled from freesound.org data
* [ESC-50: Dataset for Environmental Sound Classification](https://github.com/karoldvl/ESC-50).
2k samples, 40 classes in 5 major categories. Compiled from freesound.org data
* [NOIZEUS: A noisy speech corpus for evaluation of speech enhancement algorithms](http://ecs.utdallas.edu/loizou/speech/noizeus/)
30 sentences corrupted by 8 real-world noises. 
* [Speech Commands Data Set](https://www.kaggle.com/c/tensorflow-speech-recognition-challenge/data).
Kaggle competition required submissions to run in below 200ms on a Raspberry PI3.
* Mozilla [Common Voice](https://voice.mozilla.org), crowd sourcing. Compiled dataset [on Kaggle](https://www.kaggle.com/mozillaorg/common-voice), 
* [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/), 100k utterances for 1251 celebrities.
* [Speakers in the Wild](https://www.sri.com/work/publications/speakers-wild-sitw-speaker-recognition-database)
* [Google AudioSet](https://research.google.com/audioset/). 2,084,320 human-labeled 10-second sounds, 632 audio event classes. 
* [BirdCLEF 2016](http://www.imageclef.org/lifeclef/2016/bird). 24k audio clips of 999 birds species

## Activity detection

Terms used

* Activity Recognition / human activity recognition (AR) 
* Activities of Daily Living (ADL).
* Action recognition
* Fall detection. FD

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

## Image analysis

Tools

* [VLFeat](http://www.vlfeat.org/api/index.html).
Portable C library with lots of feature extractors for computer vision tasks.

## Vibration analysis
Often used for 'machine condition' analysis, especially for rotating machines.

* [Fundamentals of Vibration Measurement and Analysis Explained](http://www.lifetime-reliability.com/free-articles/maintenance-management/Fundamentals_of_Vibration_Measurement_and_Analysis_Explained.pdf), explains how to capture data, process it to commonly used features etc
* [Beginning Vibration Analysis](http://www.vibranalysis.co.za/ctc/pdf/pubTechPapers/01-Beginning%20Vibration%20Analysis.pdf),
page 82+ shows data for some problematic cases

## Noise removal

* Denoising autoencoders. sDSA, stacked... [Theano tutorial](http://deeplearning.net/tutorial/SdA.html)
* mSDA, fast denoising autoencoder. [Applied to robot arm](http://fastml.com/very-fast-denoising-autoencoder-with-a-robot-arm/)

## Change detection

Novelity detection.
Anomaly detection.
Change point detection (mostly in time series).

* [Change point detection in time series data with random forests](https://www.sciencedirect.com/science/article/pii/S0967066110001073)
* [Two approaches for novelty detection using random forest](https://www.sciencedirect.com/science/article/pii/S0957417414008070)


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
Or some ARM Cortex M, possibly with LORA/NBIOT. Or NRF24 ARM Cortex with integrated BLE.
LoRa -> Wifi bridge. [Wemos TTGO](https://www.banggood.com/2Pcs-Wemos-TTGO-433470MHz-SX1278-ESP32-LoRa-0_96-Inch-Blue-OLED-Display-Bluetooth-WIFI-Module-p-1271663.html?rmmds=search&cur_warehouse=CN)
LoRa module. [1](https://www.banggood.com/LoRa-SX1278-Long-Range-RF-Wireless-Power-Mental-Module-For-Arduino-p-1159089.html?rmmds=search&cur_warehouse=CN)
STM32F030. [devkit](https://www.banggood.com/5Pcs-STM32F030F4P6-Small-Systems-Development-Board-CORTEX-M0-Core-32bit-Mini-System-p-1221406.html?rmmds=search&cur_warehouse=CN)
* Microphone. [Analog](https://www.digikey.co.uk/products/en/audio-products/microphones/158?k=microphone&k=&pkeyword=microphone&FV=ffe0009e%2Ca40062&quantity=0&ColumnSort=1000011&page=1&stock=1&nstock=1&datasheet=1&pageSize=25)
[I2S](https://www.digikey.co.uk/products/en/audio-products/microphones/158?FV=ffe0009e%2Ca4027e&quantity=&ColumnSort=1000011&page=1&k=microphone&pageSize=25&pkeyword=microphone)
* IMU
* Piezo vibration sensor? Might be better to use high-frequency accelerometer
* SPI ADC, [MCP3002](https://www.digikey.no/product-detail/en/microchip-technology/MCP3002T-I-SN/MCP3002T-I-SN-ND/319415)
* Camera. OV7670 (VGA-QCIF).
[Making work with STM32](http://embeddedprogrammer.blogspot.no/2012/07/hacking-ov7670-camera-module-sccb-cheat.html)
QCIF 176x144 is approx 40kB color, 20kB grayscale.
Version with AL422 FIFO is maybe a bit easier to interface. 8bit parallel readout.
[ex](https://www.aliexpress.com/item/J34-Free-Shipping-AL422-640x480-CMOS-With-3M-Bits-OV7670-FIFO-Camera-STM32-Chip-Driver-Module/32579976662.html).
OV7725. Older chip, rare now. [Object tracking with STM32](http://blog.tkjelectronics.dk/2014/01/color-object-tracking-with-stm32-ov7725/)
OV5647 RPi camera module.. 5MPi. MIPI CSI-2, too fast for microcontroller. Need FPGA or dedicated pheripheral? Overkill 
[ArduCAM](https://github.com/ArduCAM/Arduino) support 10+ camera modules incl OV7670. ESP8266 also supported.
[OpenMV](https://openmv.io/), very nice machine vision devkit with STMF7 and MicroPython.

Testcases

* Detect machine start/stop/running. Dishwasher, CNC. Accelerometer/microphone
* Detect door open/close. Accelerometer/microphone
* Detect speech present/not. Microphone
* Detect a hand gesture. Accelerometer
* Detect a spoken command. Microphone
* Detect/Estimate room occupancy. Accelerometer,microphone,PIR

## Using microflo
Dataflow engine. Especially for feature retrieval and processing

* Register pointertype for a vector of features. int32_t?
* Component(s) for putting data into feature vector
* Should complex I/O components like 9DOF IMU send a vector, then unpack as needed?
* Example component wrapping a generated classifier
* Component(s) for feature scaling/standardization
* Component(s) for creating lag features
* Component(s) for aggregating/summarizing a value, as feature
* Component(s) for framing/windowing a (time)series of values

# Funding


## Industry partners

Key technologies

* Microcontroller
* Embedded Systems
* Sensors
* Machine learning

Potential companies

Microcontrollers

* Nordic Semiconductors. Leader in Bluetooth low-energy chips. Nothing around machine learning?
* Microchip (prev Atmel). [.](https://www.finn.no/job/fulltime/ad.html?finnkode=117675050)
* Silicon Labs (prev. Energy Micron)

Embedded Systems

* Data Respons.
* Cisco (prev Tandberg). Lysaker.

Sensors

* Tunable. Gas sensors startup. Oslo. [.](https://www.finn.no/job/fulltime/ad.html?finnkode=119094407)
* Sensonor. Experienced MEMS sensors company. Horten.

## Grants

* [IEEE Computational Intelligence Society Graduate Student Research Grants](https://cis.ieee.org/graduate-student-research-grants.html).
1-4k USD. Housing costs, travel costs for visiting external institution.
Deadline: April-March?. Need to be student member of IEEE CIS 


# TODO


June 2018

* Contact potential companies for partnerships
* Assemble 1-2 nodes with a general sensor package 
* Write firmware for collecting data
* Setup data persistence
* Deploy and start collecting some data

August 2018

* Start work on DAT390 term paper
* Create demo of an application of ML on microcontroller

December 2018

* Deliver DAT390 term paper
* Decide research goal for thesis
* Industry partner is in place (if any)

May 2019

* Deliver master thesis

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

