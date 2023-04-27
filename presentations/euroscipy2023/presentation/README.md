
# Proposal

## Title
Next-generation sensor systems using on-edge Machine Learning

## Format
15 minutes / 30 minutes

## Track
Machine and Deep Learning

## Abstract

Being able to adequately sense physical phenomena is critical to many areas of science;
from detecting particles in physics, to measuring pollution in public health, to monitoring bio-diversiry in ecology.
Over the last decades the capabilities and costs of sensor system has become much better,
driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication.
This has led to increased deployments of Wireless Sensor Networks, and "Internet of Things" (IoT) systems
using a central "cloud" for data processing.

Now another wave of technological improvements is impacting sensor systems: Machine Learning.
This is frequently used in the cloud side of an IoT sensor system, to analyze the vast amount of collected data.
Recently it has become more feasible to implement Machine Learning on-edge, on the sensor nodes themselves.
Which possibilities arise when we can performing inference and learning inside the sensor nodes?
And what are the consequences for practical science and engineering applications?

In this talk we will present some of the challenges, recent progress, and development trends in using
on-edge machine learning (sometimes called TinyML) to improve sensor nodes and sensor networks.
We will describe how Python used to research, develop and deploy such improvements,
including the the Python library "emlearn", which allows to deploy Machine Learning models to small microcontroller-based embedded devices.

## Description

This presentation will explain some of the benefits on-edge
Machine Learning provides for sensor systems.
In particular we will cover 3 major areas:
Energy optimizations, improved privacy and standalone operation.
We will mention practical use-cases that are deployed today,
explain in high-level how these may be solved,
and highlight some open-source Python libraries that may be used.

The different aspect of the presentation is further described below.

### Who is it for

- Researchers/Engineers/developers working on embedded devices / IoT
- Researchers/engineers/developers in sensing and sensor-systems
- Tinkerers/makers who like to make physical things
- Those interested in computationally-efficient Machine Learning

Assumed knowledge

- Basic literacy in Python and proficiency in programming
- Familiarity with core Machine Learning concepts:
Supervised/unsupervised learning. Classification/regression.

Beneficial but not neccesary

- Familiarity with embedded devices
- Familiarity with time-series data

### Detailed contents

#### Sensor systems background

Sensor systems take measurements using a set of sensing elements,
and use a combination of electro-mechanical systems, analog electronics, and digital processing
to extract the information of interest.
The more high-level the desired information, the more involved this processing chain needs to be.

Sensor nodes are self-contained physical units
that contain the sensig elements along with the neccesary electronics for power, signal conditioning and communication,
along with some limited data processing capabilities.

In a Wireless Sensor Network, the sensor nodes communicate wirelessly,
and use battery or energy harvesting as a power source.
Not needing cables means a considerable lower installation costs,
and provides a large increase in the flexibility and ability to position sensors.
However the amount of energy available is limited,
and this puts considerable constraints of what is possible to achieve. 

#### Energy optimizations using Machine Learning

The majority of energy of the node is usually consumed by:
A) sampling input data from sensing elements
B) processing the input data and extracting relevant information
C) transmitting the information over the wireless link

In each of these areas there are potentials for Machine Learning to improve energy efficiency.
We we will illustrate some of approaches that have been proposed:

Adaptive-sampling methods can reduce sampling energy (A).
For slow-moving temporal phenomena an adaptive sampling method can be implemented using a forecasting model.
The forecasted value is compared to a sampled value, and the sampling rate is adjusted based on the errors. 
Values in between are interpolated using the forecasting model.

Event-based or novelty-based triggers can reduce processing energy (B).
Event-based trigger can be implemented using an Event Detection model.
It operates on short windows of data and uses a low-complexity classifier to determine if the window should be processed further.

Novelty-based sampling can be a Novelty Detection model.
This is similar to Outlier Detection / Anomaly Detection, but using a rolling buffer as the normal data.
An learning algorithm continiously models this data and computes the novelty score of the latest samples.
For novelty scores above a certain, further processing is triggered.

Reducing the amount of data to be transmitted is the primary way to reduce transmission energy (C).
For sensing applications that have a high rate of input data
but a low rate of high-level information, implementing the processing on-device
allows to send only the high-level information, instead of the much higher rate input data.
This can be the case for accelerometer, microphone and image based sensing - and the processing may include a Machine Learning model.

In all cases, care must be taken that the additional energy used to process the models
is not higher than the energy savings they enable.
Combined energy improvements can make it possible to bring
the energy usage low enough to enable battery-powered use instead of requiring external power.

#### Improved privacy using on-device ML

Several sensing modalities, such as audio and image
may carry personally identifiable or other sensitive information.
When the information of interest can be derived using
An example coud be an bio-diversity monitoring device that process sounds
in order to detect presence of bird and only outputs infomation about detected birdssong.
It may be more secure and trustworthy if the audio data never leaves
the processing device, compared to sending it over Internet to a hard-to-verify cloud service.

#### Standalone operation using on-device ML

Running inference on-device instead of in the cloud means being able to operate stand-alone.
This enables solutions that work fully or partially without Internet connectivity,
and that have consistently low latency.
This enables sensors using ML that are integrated into electronics appliances.

Doing learning on device also enables specialized detection models.
This can be done few-shot learning methods of feature extractors pipeline.
The feature extraction pipeline may include a pre-trained neural network,
to produce compact features vectors (embedding).
This enables the on-device learning to use simple models on top of the simplified feature space.
This can be used for personalized, task, location or device-specific classification or Anomaly Detection models.

#### Implementing on-device ML

emlearn is a Python library for deploying Machine Learning models to
the kind of microcontrollers and microprocessors found in sensor nodes.
It enables converting models in Python with scikit-learn into computationally efficient C code for doing inference on the target device.
It also supports doing on-device learning of simple models for

Tensorflow Lite for Microcontrollers (TFLite Micro) enables running neural networks built
with Tensorflow/Keras on constrained devices.
It supports common architectures such as Recurrent Neural Networks (RNN) and Convolutional Neural Networks (CNN).

We will discuss how these two libraries can be used to implement the kinds of Machine Learning models mentioned above.

## Notes

The presentation may be compressed down to a 15 minute talk, if given advance notice.

A tutorial for introduction to practical on-edge Machine Learning will also be submitted.

What grew into the emlearn project was first presented at EuroScipy 2018,
in the talk Machine Learning for microcontrollers with Python and C (Jon Nordby). 
https://www.euroscipy.org/2018/descriptions/Machine%20Learning%20for%20microcontrollers%20with%20Python%20and%20C.html
Since then the tool has been used in a range of projects and cited in dozens of scientific papers.


