
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

- At least 10 people can use emlearn for basic tasks.
! need tutorial
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



