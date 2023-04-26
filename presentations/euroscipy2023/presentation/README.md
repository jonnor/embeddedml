
# Proposal

## Title
Next-generation sensor systems using on-edge Machine Learning

## Format
15 minutes / 30 minutes

## Track
Machine and Deep Learning

## Abstract
between 200 and 1500 characters.

Being able to adequately sense physical phenomena is critical to many areas of science;
from detecting particles in physics, to measuring pollution in public health, to monitoring bio-diversiry in ecology.
Over the last decades the availability, capabilities and costs of sensor system has become much better,
driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication.
This has led to increased deployments of Wireless Sensor Networks, and "Internet of Things" (IoT) systems
with a central "cloud" for data storage and processing.

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
between 400 and 50000 characters.

FIXME: write based on outline. Include take-aways and audience expectations.

Who is it for

- Researchers/Engineers/developers working on embedded devices / IoT
- Researchers/engineers/developers in sensing and sensor-systems
- Tinkerers/makers who like to make physical things
- Those interested in computationally-efficient Machine Learning

Assumed knowledge

- Basic literacy in Python and proficiency in programming
- Familiarity with core Machine Learning concepts.
Supervised/unsupervised learning. Classification/regression.

Beneficial but not neccesary

- Familiarity with embedded devices
- Familiarity with time-series data

## Notes

A tutorial on will also be submitted.

What grew into the emlearn project was first presented at EuroScipy 2018,
in the talk Machine Learning for microcontrollers with Python and C (Jon Nordby). 
https://www.euroscipy.org/2018/descriptions/Machine%20Learning%20for%20microcontrollers%20with%20Python%20and%20C.html
Since then the tool has been used in a range of projects and cited in dozens of scientific papers.


## Meta

### Motivation

Get out there again

- Visibility as expert in embedded/sensor ML

Improve the project

- Improved documentation. Especially onboarding / introduction
- Improved marketing materials. Especially examples, demos, pictures/videos
- Maturing existing functionality. Adding new functionality, especially for for practical usecases

Grow the project community

- Attract potential users, contributors

### Goals

- At least 10 people can use emlearn for basic tasks. ! need tutorial
- A least 100 relevant people hear about emlearn.
And another 1000 during the following year. Via online follow ups. ! need video. ! need social media posts
- Get another talk on emlearn out there
- Demonstrate the good things people already did with emlearn
- Get to 10 citations per year for emlearn

### Audience

Who is it for

- Researchers/Engineers/developers working on embedded devices / IoT
- Researchers/engineers/developers in sensing and sensor-systems
- Tinkerers/makers who like to make physical things
- Those interested in computationally-efficient Machine Learning

Assumed knowledge

- Basic literacy in Python and proficiency in programming
- Familiarity with core Machine Learning concepts.
Supervised/unsupervised learning. Classification/regression.

Beneficial but not neccesary

- Familiarity with embedded devices
- Familiarity with time-series data

### Takeaways

- New possibilities for sensor systems due to on-sensor ML
More things can be done on battery power.
More things can be done while maintaining privacy
More things can be automated
Lower unit costs
(conclusions -> continued explosive growth in deployments of sensors/IoT)
- Practical systems are already being deployed for some years
- Getting started with TinyML is doable.
Tooling such as emlearn helps.
Can do almost everything in Python. MicroPython viable for hobby devices
- BUT. Make sure you need it.
on-edge, low-power, low-cost, ML always more difficult than in-cloud, fixed power



## Description

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
This can be the case for accelerometer, microphone and image based sensing
- and the processing may include a Machine Learning model.

In all cases, care must be taken that the additional energy used to process the models
is not higher than the energy savings they enable.
Combined energy improvements can make it possible to bring
the energy usage low enough to enable battery-powered use instead of requiring external power.

#### Improved privacy using on-device ML

FIXME: describe

#### Standalone operation using on-device ML

Running inference on-device instead of in the cloud means being able to operate stand-alone.
This enables solutions that work fully or partially without Internet connectivity,
and that have consistently low latency.
This enables sensors using ML that are integrated into electronics appliances.

Doing learning on device also enables specialized detection models.
This can be done few-shot learning methods of feature extractors pipeline.
The feature extraction pipeline may include a pre-trained neural network, to produce compact features vectors (embedding).
FIXME: focuse in on sensors again. Anomaly Detection.

#### Implementing on-device ML

emlearn is a Python library for deploying Machine Learning models to
the kind of microcontrollers and microprocessors found in sensor nodes.
It enables converting models in Python with scikit-learn into computationally efficient C code for doing inference on the target device.
It also supports doing on-device learning of simple models for

Tensorflow Lite for Microcontrollers (TFLite Micro) enables running neural networks built
with Tensorflow/Keras on constrained devices.
It supports common architectures such as Recurrent Neural Networks (RNN) and Convolutional Neural Networks (CNN).

We will discuss how these two libraries can be used to implement the kinds of Machine Learning models mentioned above.

### Outline

- Sensor systems

Continious sampling with Wireless Sensor Networks / IoT devices
Key considerations. Costs, power, battery, data communication
The sensing pipeline. Information out vs data in. What we want to know vs what we have to process to get it.
Trends. IoT connectivity. Software-defined. Falling hw costs. Subscription models.

- What on-edge ML makes possible 

Data reduction.
Power efficiency.
Working without network connectivity
Personalized models

On-edge preprocessing. Learned representations. Embeddings
On-edge inference
On-edge learning

- emlearn project

Training in Python, device code in C.
Doing everything in Python. Using MicroPython on device
On-edge learning. Personalized
Anomaly Detection.
? Novelty Detection

- Real-world application
Examples of usecases. Made with emlearn and other TinyML tools.

- How to get started

Call to action. Get started with emlearn on real hardware. Come join me in sprints session

### Scientific questions
that emlearn can help address

People use emlearn to research ...

Can task X be done on-edge?
What would the benefits be over a cloud-based solution?
Power, battery life, unit costs, installation costs, privacy, robustness

What could better hardware architectures for edge-ML (inference) be

What are ways to optimize ML models for inference on microcontrollers

What could be alternative ways to make sensors for XX using on-sensor ML inference

How can we do things better if we lift the constraint of having to have
human-understandable "input" data that is then processed by human-engineered data processing pipeline?


### Use-cases

TODO, check existing papers using emlearn for inspiration



## Adaptive sampling

### Energy management in wireless sensor networks with energy-hungry sensors
http://info.iet.unipi.it/~anastasi/papers/im09.pdf
300 citations
2009

Taxonomy of Adaptive Sensing Strategies

- Model-based Active Sensing
- Activity-based Adaptive Sampling
- Harvesting-aware Adaptive Sampling
- Triggered Hierarchical Sensing
- Multi-scale Hierarchical Sensing

Hierarchical Sensing.
Using multiple sensors with different accuracy and power consumption. 

Adaptive sampling
Techniques are aimed at dynamically adapting the sampling rate by exploiting correlations
among the sensed data and/or information related to the available energy.
For instance, if the quantity of interest evolves slowly with time – so that
subsequent samples do not differ very much– it is possible to take advantage of the
temporal correlation. On the other side, it is very likely that measurements taken by
sensor nodes that are spatially close each other do not differ significantly. Spatial
correlation can thus be exploited to further reduce the sensing energy consumption.
Obviously, both these approaches can be combined to further reduce the number of
samples to be acquired. Finally, the sampling rate can be adjusted dynamically depending
on the available energy.

Model-based active sampling consists in building a model of the sensed phenomenon on
top of an initial set of sampled data. Once the model is available, next data can be
predicted by the model instead of sampling the quantity of interest, hence saving the
energy consumed for data sensing. Whenever the requested accuracy is no more satisfied,
the model needs to be updated, or re-estimated, to adhere to the new dynamics of the
physical phenomenon under observation.

Harvesting-aware Adaptive Sampling exploits
knowledge about the residual and the forecasted energy coming from the harvester module
to optimize power consumption at the unit level.

Defining the concept of energy-neutral operating mode which guarantees that the harvested energy
is consumed at an appropriate rate to maximise the lifetime of the units.



