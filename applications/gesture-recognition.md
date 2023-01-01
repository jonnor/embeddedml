
# Gesture Recognition

Using IMUs (triaxial accelerometer plus gyro).

## Datasets

* [martWatch Gestures Dataset](https://tev.fbk.eu/technologies/smartwatch-gestures-dataset)
8 users, 20 repetitions of 20 different gestures. 3-axis accelerometer
* [Australian Sign Language signs Data Set](https://archive.ics.uci.edu/ml/datasets/Australian+Sign+Language+signs).
95 signs were collected from five signers. Noisy. XYZ, roll, plus finger bend.
* [A Survey of Datasets for Human Gesture Recognition](https://diuf.unifr.ch/people/lalanned/Articles/RuffieuxHCII2014.pdf)
lists some 15 datasets, but only for image-based gesture recognition, mostly collected with Kinect.

## Existing work

* [Xie & Pan 2014 - Accelerometer Gesture Recognition](http://cs229.stanford.edu/proj2014/Michael%20Xie,%20David%20Pan,%20Accelerometer%20Gesture%20Recognition.pdf). Dynamic-Threshold Truncation feature preprocessing increased.
With 5 classes and only 1 training example per-class was able to reach 96% accuracy.
Using multiple examples, both SVM and Naive Bayes performed well.
* [uWave: Accelerometer-based Personalized Gesture Recognition and Its Applications](http://www.ruf.rice.edu/~mobile/publications/liu09percom.pdf). Using template gestures and Dynamic Time Warping
* [Paper1](http://journals.sagepub.com/doi/full/10.5772/60077). Reviews existing methods of HMM and DTW.
Proposes an improved a distance-based model with kNN classification with low computational overhead.
Large margin nearest neighbour (LMNN).
* [Paper2](http://ieeexplore.ieee.org/document/7382120/). Uses accelerometer data directly as features. Using FastDTW.
* [Transfer Learning Decision Forests for Gesture Recognition](http://jmlr.csail.mit.edu/papers/volume15/goussies14a/goussies14a.pdf). 2014
* [PERSONALIZING A SMARTWATCH-BASED GESTURE INTERFACE WITH TRANSFER LEARNING](http://www.eurasip.org/Proceedings/Eusipco/Eusipco2014/HTML/papers/1569922319.pdf).
Haar Wavelet Transform. Supervised Local Distance Learning.
5% increase in accuracy with transfer compared to without.
* [High Five: Improving Gesture Recognition by Embracing Uncertainty](https://arxiv.org/pdf/1710.09441.pdf).
Builds a model of the errors of gestures, and uses it to improve HMM-based classifier.

## Feature processing

* Vector quantization
* Acceleration statistics
* Motion histogram
* Zero velocity compensation (ZVC)
* DWT. [FastDWT](https://cs.fit.edu/~pkc/papers/tdm04.pdf), approximation of DTW in linear time and linear space.
