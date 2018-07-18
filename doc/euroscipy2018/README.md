
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

* Audience understands microcontroller constraints/limitations for ML
* Know what can currently be done with Python+emtrees
Have a starting point for using or further developing these methods.

## Scope

* On microcontroller: Inference only. Training happens the standard way.
* Offline learning. No continious learning
* Not much about deep learning.
* Focused on microcontrollers, but same techniques and libraries can be applied to bigger systems.
Embedded Linux, high perf server.

## Outline


### Key aspects

* Why ML on microcontrollers.
Motivation, possible applications.
* Microcontroller-specific considerations for ML.
Memory constraints, CPU constraints, Energy constraints.
* Covered methods.
Decision tree ensembles. Random Forest / extratrees.
? Naive Bayes.
* How to train
Python. sklearn APIs.
* How to deploy
Serialized model vs code generation.
Supported platforms.
* Performance
Examples. MNIST,DCASE
Classification scores, runtime, memory usage. Energy usage

### Maybe

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



