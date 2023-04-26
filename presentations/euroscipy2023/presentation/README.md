
# Proposal

## Title
Next-generation sensor systems using on-edge Machine Learning

## Format
15 minutes / 30 minutes

## Track
Machine and Deep Learning

## Abstract
between 200 and 1500 characters.

Being able to accurately and adequately sense physical phenomena is critical to many areas of science,
TODO: add examples
Over the last decades the cost and capabilities of microprocessors has improved a lot.
This combined with low-cost wireless communication, has led to the widespread deployment of Wireless Sensor Networks.
When combined with near-ubiquitious Internet access, this can be seen as part of the "Internet of Things".
Now another wave of technological improvements is impacting sensor systems: Machine Learning.

What can be achieved when on-edge Machine Learning inference and learning is performance directly on sensor nodes?
And what are the consequences for practical science and engineering applications?

In this talk we will present some of the challenges, recent progress, and development trends in using
on-edge machine learning to improve sensor nodes and sensor networks.
We will cover how Python is a key part of the worflow in researching, developing and deploying such improvements.
This includes the Python library "emlearn",
which can be used to deploy Machine Learning models to small microcontroller-based embedded devices.

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


