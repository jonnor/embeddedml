
# Proposal

* [CFP](https://pretalx.com/euroscipy18/cfp)
* Status: Submitted May 01

## Title
Machine Learning for microcontrollers with Python and C

## Abstract
How to deploy efficient machine learning classifiers on tiny microcontrollers,
using standard Python and scikit-learn workflows.

## Description
Machine learning is making its way into many industries and applications,
and for many usecases the Python ecosystem has excellent solutions available, for example scikit-learn.
However applications based on embedded systems and microcontrollers have severe
memory, CPU and energy constraints which make established Python-based solutions unsuitable.

This talk shows how existing scikit-learn estimators can be combined with classifier implementations
in portable C code tailored for running on embedded hardware platforms.
This approach allows to train and validate models using existing Python workflows,
and then run efficiently on low-end microcontrollers.
Currently the project covers classifiers using Decision Tree ensembles (Random Forest and extratrees),
and Gaussian Naive Bayes. This is provided by two Python packages,
[emtrees](https://github.com/jonnor/emtrees) and [embayes](https://github.com/jonnor/embayes).

Some aspects might also be of interest when hitting performance bottlenecks in larger computing systems.

## Topics

* Algorithms implemented or exposed in Python
* Deep Learning & AI
* Robotics & IoT
* Statistics

# Contents

## Goals

At the end of talk

* Audience understands microcontroller constraints for ML
Memory/RAM. Energy usage
* Know what can currently be done with Python+emtrees
Tree-based classifiers.
* Have a starting point for using or further developing these methods.
PyPI. Github repository.

## Scope

* On microcontroller: Inference only. Training happens the standard way.
* Offline learning. No continious learning.
* Not much about deep learning. Focus on tree-based methods
* Focused on microcontrollers, but same techniques and libraries can be applied to bigger systems.
Embedded Linux, high perf server.
* ? Supervised learning primarily. Unsupervised: anomaly detect, compressive sensing.

## Audience background

Assumed
* Machine Learning fundamentals
Beneficial
* Microcontrollers

## Key aspects

* Why ML on microcontrollers.
Motivation, possible applications.
Energy-constrained device
Cost-constrained
Wireless Sensor Network
Rich/complex input data
* Microcontroller-specific considerations for ML.
Memory constraints, CPU constraints, Energy constraints.
* Covered methods.
Decision tree ensembles. Random Forest / extratrees.
* How to train
Python. sklearn APIs.
* How to deploy
Serialized model vs code generation.
Supported platforms.
* Performance
Examples. MNIST,DCASE
Classification scores, runtime, memory usage. Energy usage


## Slides

### About me

Electronics Engineer.
10 years experience as software developer
around Embedded Linux, audio,image processing
Independent consultant last 5 years
Currently doing a Master in Data Science
at Norwegian University of Life Sciences.
Focusing on Machine Learning, especially researching ML on microcontrollers


### This presentation

Background.
What is machine learning on microcontrollers and why is it interesting
Constraints, considerations unique to microcontrollers.
Limitations of scope

Current state
What is out there
Existing libraries

Getting practical
Using emtrees

What is it,why interesting


Early preview of master thesis topic

### Microcontroller, what does it mean
Constrast with typical laptop,server cases

Memory
Compute
Energy
Costs.
GPU. FPU. without FPU

10 USD, 100 USD, 1000 USD
microwatt, watt, 100 watt

Embedded Linux. 128 - 1GB
Mobile machine-learning. 


Range of microcontrollers

8-bit. 20 bytes RAM.
Arduino Uno. Atmega 328. 2kB RAM, no FPU.

32bit. 72Mhz
STM32F0. ARM Cortex M0. 8kB RAM. No FPU!
NRF52. ARM Cortex M4F. BLE 5.0

ESP32. 512kB RAM. WiFi,BLE.
ARM Cortex M7. 200MHhz+

### Example usecases

Fitness bracelet
Activity detection
Gesture recognition

Wireless Sensor Network node
Contious acoustic monitoring
Birdsong
Outdoor

Industrial machine monitoring
Vibration, accelerometer
Anomaly detection


New sensor technology
Arrays, semiconductors. MEMS
Combine/compensate in software


Commonalities:

* Generic input data with high bitrate
* Low power desired
* Minimize power usage by minimizing time spent transmitting data

### Power consumption

Sleep
1.9uA

Running@32MHz
1856 uA. 1.9mA

Transmitting GPRS
450 mA

Connection GPRS time
1 second

https://serverfault.com/questions/387627/why-do-mobile-networks-have-high-latencies-how-can-they-be-reduced


### Maybe

#### emtrees How does it work
Decision tree nodes
Extracted from skicit-learn
Two modes: 1) walking datastructure 2) generate code

Python module

#### ML architectures in Wireless Sensor Networks
Image(s)
Cloud: Sensor -> gateway -> cloud (ML)
Edge: Sensor -> gateway (ML) -> cloud
Micro: Sensor (ML) -> gateway -> cloud

N sensors per gateway, N gateways per cloud service
Sensor is battery/energy-harvesting.
Gateway is per site. Embedded Linux. Normally powered.


### Wireless transmission technologies
Chart/table
Bandwith,distance,energy
LoRa,SigFox,BTLE,GSM,WiFi.

### ML pipeline
Sensor -> Feature extraction -> Aggregation -> Classification
N samples, N per second => data rate.

Ex: Acoustic Event detection

Microphone | windowing | FFT | melspectrogram | max | randomforest
  samples            frames                  features    prediction

fft_hop=1024
n_mels=64
decision_period=10 second

Visualize as chart, size=bytes per second for each step?

1 [int16] @ 44100 Hz   88200 bytes per second
513 [float32] @ 43 Hz
64 [float32] @ 43 Hz
64 [float32] @ 0.1 Hz    26 bytes/second
int8 @ 0.1 Hz           0.1 bytes/second

Sampling or

Aggregation. Binary classification, count number of positive
1 int8 per minute
1 int16 per hour

Sampling. If OK with less


LoRa. 400 bytes per hour. 6 bytes per minute
https://www.thethingsnetwork.org/docs/lorawan/limitations.html

BTLE packet size. 33 bytes total, 20 bytes payload

### Optional/bonus

* Tools
Driving predictions over serialport for testing



# CATBoost
https://github.com/catboost/

Build and used by Yandex in many many places

CatBoost builds symmetric trees. Low depth
LightGBM on other hand builds very deep

Supports categorical features
not just one-hot-encoding
automatically calculates statistics
and random permutations
greedy construction of feature combinations,
including estimated priors

Ordered boosting. Reduces bias in leaf value estimations

Tasks: Classification,Regression,Ranking

Decicated support for (grouped) ranking.
Pairwise does not need absolute values.
Can give better results, but slower
Top-N and top-1

Supports GPU based training
Very fast for many features
40-50 times speedup versus CPU
GTX1080i

30-60 times faster during prediction

Feature interaction
Per-object feature importance

Nodes values availabe using a 'JSON model'
https://github.com/catboost/catboost/issues/202

CoreML exporter exists
CoreML supports tree-based ensembles
https://developer.apple.com/documentation/coreml/converting_trained_models_to_core_ml

C++ evaluator for ARM architecture desired
https://github.com/catboost/catboost/issues/408


# JupyterHub for teaching
Auth plugins
Spawner plugins

Launch different kernels
When using Lab can have all the files on right hand side
Using a script to deploy new study materials progressively

# nbgrader
Creating and Grading assignments in Jupyter notebook

Automatically graded using unit-tests

