

## Title
emlearn - run Machine Learning models on microcontrollers

## Abstract

Advances in Machine Learning has made it possible to automatically extract valuable information from sensor data.
While most associate Machine Learning with costly and compute-intensive systems,
it is becoming feasible to deploy ML systems directly to very small embedded devices and sensors.
These devices typically use small, low-power, microcontrollers that cost as little as 1 USD.
This niche is often referred to as "TinyML", and is enabling a range of new applications
in scientific applications, industry and consumer electronics.

emlearn is an open-source Python library that allows converting scikit-learn and Keras models to efficient C code.
This makes it easy to use a Python-based workflow while deploying to any microcontroller with a C99 compiler. 
The library has been used in a wide range of applications, from detection of vechicles in acoustic sensor nodes,
to hand gesture recognition based on sEMG data, to real-time malware detection in Android devices.
In the poster session we will highlight some of the use-cases for emlearn,
and the tools and features that the library provides to make development efficient and accessible.

## Description

emlearn supports both supervised learning (classification, regression),
and unsupervised learning (outlier/anomaly/novelty detection).
The library supports a range of popular Machine Learning models, including:

- tree-based models (RandomForest/ExtraTrees/DecisionTree et.c.),
- simple neural networks (MultiLayerPerceptron),
- mixture-models (Gaussian Mixture Models).

emlearn aims to take a "batteries-included" approach,
that also includes microcontroller-friendly tools for preprocessing, post-processing and evaluation.
Evaluation tools includes estimating and measuring model size (memory/storage).
Preprocessing tools include common feature extraction for audio data (soundlevel, mel-spectrogram, MFCC),
and for accelerometer/IMU data (RMS, p2p, FFT).
Examples of post-processing is event decisionmaking (discretization, median filtering).

The combination of models and tools makes it easy to implement common TinyML usecases,
such as time-series classification, Event Detection, Gesture Recognition, Voice Activity Detection, et.c.
This can be used to build applications for smart-watches, wireless sensor networks, mobile devices,
wearable devices et.c.

Come chat to us about the intersection of physical computing, sensors, electronics and Data Science!

## Notes

We have also submitted a presentation and tutorial on related topics.


## Take aways

- Machine Learning inference can be done on low-cost microcontrollers

- emlearn is a tool that makes this possible


- emlearn is an open-source Python library
allows converting scikit-learn and Keras models to efficient C code

## Notes

Aims to be a batteries-included approach.
Similar to scikit-learn.
Including tools for preprocessing, post-processing, evaluation.

Make it very easy to

- Get an initial model running on device
- Get decent performance by following relevant recipies/examples
- Evaluate whether it is possible to achieve target performance within given device contraints
- Perform common tasks.
Classification
Event Detection
Regression
Anomaly Detection in time-series

