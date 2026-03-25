
# Questions for them

- What kind of data or tasks are the students working with?

# Context

- Use Particle Photon 2. ARM Cortex M33 CPU, memory 3MB RAM / 2MB Flash
- Doing data collection project now
- Previous week they had feature engineering


## Usage on Particle

Particle libraries are heavily inspired by Arduino library system
https://docs.particle.io/getting-started/device-os/firmware-libraries/

But they note some caveats. 
? is emlearn Arduino library actually compatible

Would be nice to have example with filesystem
! want .npy file support

# Adjustments?

## Examples of wireless buses
And their data constraints

## Complexity of tasks

- Low complexity.
Low amount of features. 2-10 dimensions.
Relevant values more-of-less direct from sensors.
No need for feature-extraction / transformation
Metal Oxide sensors. Color.

- Medium complexity.
Known feature extraction methods exists

## Validating model
- Slide is not so nice. Benefit from visuals
Compare 

## Compute constraint slide
Could be split into multiple slides.
Slide 1. Overview
Slide 2. FLASH/RAM. Highlight being a step-wise
Slide 3. CPU/energy. Highlight being continious,
link between energy usage and active time.

## Continious classification
Good example for why overlapped windows: Double clap.

But there is no visuals that illustrate this. Could be nice to add

## Trees performance plots
Would be nice to have also the COST plots.
For model size, and inference time estimate.

## Create a data collection plans
For physical/sensor machine learning task.
For example in a TinyML setting

What are the axes of variabilty?
What kind of scenarios 
What is the environment like for your usecase?
Control as many of them as possible.
Create a set of experiments that execise what is relevant.
"Pre-labeling"
Decide on the desired behavior or undesired

What are the potential confusor?

## Data labeling
Add a slide about it?

Label Studio.
Can take video and sensor-data.
Handles up to a few minutes.

Was requested in the previous lesson.


# Notes

? Have a nicer hyperparameter tuning example
5,10,20,40

Decision-trees/forests are incredibly RAM efficient.
! benefit for ASIC


