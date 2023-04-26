
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



## Desc

Sensor systems take measurements using a set of sensing elements,
and use a combination of electro-mechanical systems, analog electronics, and digital processing
to extract the information of interest.
The more high-level the desired information, the more involved this processing chain needs to be.

Sensor nodes are self-contained physical units
that contain the sensig elements along with the neccesary electronics for power, signal conditioning and communication,
along with some limited data processing capabilities.

In a Wireless Sensor Network, the sensor nodes communicate wirelessly,
and use battery or energy harvesting as a power source.
--Not needing cables means a considerable lower installation costs,
--and provides a large increase in the flexibility and ability to position sensors.
However the amount of energy available is limited,
and this puts considerable constraints of what is possible to achieve. 

The majority of energy of the node is usually consumed by.
A) sampling input data
B) processing the input data and extracting relevant information
C) transmitting the information over the wireless link

In each of these areas there are potentials for Machine Learning to improve energy efficiency,
and we will look at some examples of this.


emlearn is a Python library for deploying Machine Learning models to
the kind of microcontrollers and microprocessors found in sensor nodes.
It enables converting models in Python with scikit-learn or Keras into computationally efficient C code for doing inference on the target device.
It also supports doing on-device learning of simple models for
It supports models for classification, regression and anomaly detection.

The sensor nodes


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


