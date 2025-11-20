
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


## Youtube ideas

So far on Youtube, seems like:

- MicroPython content is doing better than TinyML.
- Shorts getting as many or more views as long-form.

Shorts:

- Speeding up MicroPython compute using code emitters. RMS
- Dynamic native C module in MicroPython. RMS
- Use FIFO for IMU with MicroPython, power saving
- Extra virgin olive oil detection with UV and AS7343
- Linear regression on device, with emlearn-micropython, npyfile
- Toothbrush NRF52 with Zephyr and MicroPython 


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

## People in the TinyML space

Benjamin Cabe,  Zephyr

Kevin YouTube
Shawn Hymel
Ibrahim at OpenMV

https://github.com/Mjrovai ? https://www.hackster.io/mjrobot/projects 
He is in the TinyML research community

https://medium.com/@subirmaity/a-simple-neural-network-implementation-approach-in-micropython-for-deep-learning-application-760ab35cb538 
When MLP is supported

https://www.hackster.io/dmitrywat 
https://www.hackster.io/timothy_malche/ 
https://www.hackster.io/roni-bandini/projects 
https://www.hackster.io/alankrantas/ 

https://www.linkedin.com/in/vijay-janapa-reddi-63a6a173/ ?

https://ashishware.com/index.html 

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

Zephyr is a good base for portability.
But write everything in C99.
Put into emlearn project - maybe as a separate repo

## Medium posts

The demos are decent starting point?
Just need to make sure they are informative enough.
As there is a policy against posts that just reiterate project documentation.

Write a bit more around the core.
For example detection principles. Physics of it, DSP principles 
References to other works.
Put it into a usage context


## Marketing channels for emlearn 

- Towards Data Science
- Hackster.io
- HackAday.io
- LinkedIn groups. Which?
- Reddit communities. Which?
- Instructables
- Embedded.com 
- EmbeddedRelated.com / DSPRelated / MLRelated.com
- DataCamp
- Vendor communities. M5Stack/Seeed Studio/
- Maker platforms. Elecrow
- 

## Keyword marketing for emlearn?

End goal: Citations in scientific publications

Note, there are big lags. Probably 1-3 years between exposure and publication out.

#### Does it make sense without a webpage?
Need to have somewhere to drive people.
Is the Github repo or ReadTheDocs good enough?
Or do need to setup a https://emlearn.org - potentially built from the docs.

#### What would be good keywords?
Keyword Planner

Who are the target audience?

Researchers
Engineers
Makers

What are the most popular search terms related to TinyML?

Can one get any meaningful traffic with a small budget?
- What is the cost per click?

Can one get to self sustaining?
Enough income that it pays for the ads?
GitHub sponsorship.
Patreon
BuyMeACoffe ?
Affiliate links to products?


# TODO

## Minor

Make post in Sound of AI about microvad
Maybe once there is a video

Make a little post in Arduino project-sharing discord.
Color Detector demo?
Sequence detector

