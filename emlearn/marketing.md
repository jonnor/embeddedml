
## Audience

Primary

- TinyML researchers
- Embedded software developers
- DSP developers
- Hackers and makers


### Marketing

Identify the major open forums that are relevant.

- Medium publications
- Reddit subs
- Discord channels
- Blogs
- Conferences


## Existing venues

### TowardsDataScience
TowardsDataScience TinyML. Posts get 100-1000 claps
https://towardsdatascience.com/tagged/tinyml
Probably means 10k readers?

## Content producers

Giri wrote about Roest. Maybe he would be interested in writing about emlearn?
https://towardsdatascience.com/roasting-coffee-to-perfection-using-ai-33ff249377e4 

Sanjay wrote about KNN on rp2040 pico with MicroPython 
https://www.analyticsvidhya.com/blog/2021/07/how-to-use-machine-learning-on-microcontroller-devices/



## Long form content ideas

For TowardsDataScience or similar.

#### Introduction to open-source TinyML

Write article about open-source TinyML frameworks.
An introduction to what exists
MicroMLGen, m2gen, skompiler, emlearn
NNoM, TensorFlow lite
Publish on Medium?
Scope: Benchmarks are out. Coming later

#### Benchmarking X on TinyML devices 
Performance comparison of TinyML frameworks
MicroMLGen, m2gen, skompiler, emlearn

FLASH, RAM, inference time. Predictive accuracy
- AVR8. 8 bit, no FPU.
- Cortex M0. 32 bit, no FPU. RP2040 ?
- Cortex M4F. 32 bit, FPU. NRF52 ?
- Xtensa. 32 bit, FPU. ESP32. 

Models. Focus on a single one? Ex. RandomForest / DecisionTree.
At a couple of different sizes / problems?
Trained in the same way. Just conversion different

Arduino sketch/environment as the base?
But write everything in C99, for portability.
Put into emlearn project - maybe as a separate repo

## Medium posts

The demos are decent starting point?
Just need to make sure they are informative enough.
As there is a policy against posts that just reiterate project documentation.

Write a bit more around the core.
For example detection principles. Physics of it, DSP principles 
References to other works.
Put it into a usage context


# TODO

## Minor

Make post in Sound of AI about microvad
Maybe once there is a video

LinkedIn post about MicroPython support

LinkedIn post about getting started documentation

Write intro in Seed Studio discord
Maybe blurb in edge ai discord?

Make a little post in Arduino project-sharing discord.
Color Detector demo?
Sequence detector

