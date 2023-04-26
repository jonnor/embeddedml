
# EuroScipy2023

## CFP
https://pretalx.com/euroscipy-2023/cfp

## Track matching

Scientific Applications
- Robotics & IoT
- Earth and Ocean Sciences

Machine and Deep Learning
- Supervised Learning
- Unsupervised Learning
- ML Applications (e.g. NLP, CV)

Community, Education and Outreach
- Reports on the Use of Python in Scientific achievements or ongoing projects



## Title
Between 10 and 200 characters.

Next-generation sensor systems using on-edge Machine Learning

    Improving cost and power of wireless sensor networks using Machine Learning



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


# Tutorial
90 minutes.

#### Title
Machine Learning on sensors using MicroPython and emlearn


### Planning 

### !needs

- MicroPython support in emlearn
- Working examples.
Tested on real hardware.
Basic classification project? Then time-series? Gesture recognition?
Or jump straight to time-series. Consider other a special case of that
- Working getting-started process
Tested with real people.
?? do some trial runs? 2-3 times. At Bitraf. With some friends? Jensa? Trygvis? Elias H.? At local meetup in Oslo.
- Hardware for running code on.
Keep low by sharing in groups? 2-5 persons per group
Potential income by allowing people to buy kit. Sell half of the kits, at 100% markup = pay for kits in 1 round 
8 kits a 250 NOK = 2000 NOK.

### Hardware platform

Needs

* Basic on-device outputs. 2 LEDs+
* Basic on-device inputs. 1 button+
* At least one sensor. Accelerometer.
* No need for external programmer/debugger

Want

* Good MicroPython support
* Microphone and accelerometer
* Hard to mess up. Maybe enclosed board
* Multiple LED(s), RGB

Nice-to-have

- LCD screen

HW platforms

- ESP32
- NRF52
- RP2
- STM32

Candidate boards

- M5Stick-C
- pyboard
- MicroBit
- RPi Pico
- Arduno Nano33 Sense


https://micropython.org/download/arduino_nano_33_ble_sense/

M5Stick-C Pico Min
https://www.adafruit.com/product/4290 - 25 USD.
Has casing.
Has a watch strap option. 30 USD

https://shop.m5stack.com/products/stick-c
15 USD from offical store
Has onboard accel and mic. Onboard button. Onboard LCD. WiFi and BLE. Captouch. Grove connector.


https://shop.m5stack.com/products/m5stickc-plus-with-watch-accessories

Kit also available on Digikey, 250 NOK
https://www.digikey.no/no/products/detail/m5stack-technology-co-ltd/K016-H/15771301


!! M5StickC and M5StickCplus don't have SPIRAM. Only 520K RAM

Thread says esp32/GENERIC firmware works
https://forum.micropython.org/viewtopic.php?f=18&t=10117#p69640

https://micropython.org/download/esp32/


### micropython support

Audio via I2S for since 2021 https://github.com/miketeachman/micropython-i2s-examples
on ESP32, NRF and STM32
PDM mic not so good?

touch on ESP32. Via machine.TouchPad

esp32-s2. No Bluetooth, WiFi only. ESP32-C3 and ESP32-S3 do have BLE

https://docs.espressif.com/projects/esp-idf/en/v4.3/esp32s2/hw-reference/chip-series-comparison.html


## Existing TinyML on micropython


https://dev.to/tkeyo/tinyml-machine-learning-on-esp32-with-micropython-38a6
Jul 1, 2021
https://github.com/tkeyo/tinyml-esp

was able to read 100 Hz from accelerometer
used m2gen to generate Python code
separate X, Y and Circle gestures
Using RandomForest
Inference time with 10 estimators is approximately 4ms which is viable even at 10 ms sampling period
! no feature engineerng, using samples directly ?
used 660 ms window
! detection performance not so good

https://eloquentarduino.com/micropython-machine-learning/
using everywhereml to generate Python
shows usage on some MNIST data

https://medium.com/@subirmaity/a-simple-neural-network-implementation-approach-in-micropython-for-deep-learning-application-760ab35cb538
pure MicroPython implementation of a simple MLP


