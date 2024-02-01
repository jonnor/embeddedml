

# TinyML EMEA Innovation Forum 2024

June 24-26, 2024
Milano, Italy

## Call
https://www.tinyml.org/news/emea-2024-call-for-presentations-and-posters

Theme of “Amplifying Impact – Unleashing the Potential of TinyML for Positive Change.”

Impactful Technical Advancements:

    Submissions are encouraged in the area of
    Hardware, algorithms, models, software, sensors, and deployment / MLOPS,
    highlighting practical aspects
    and demonstrating how these advancements contribute to increased impact.

Innovation Showcase:

    Showcase latest innovations in TinyML technology: Demos, prototypes, PoC…
    Demonstrations of cutting-edge TinyML projects that not only highlight technical prowess
    but also emphasize their impact on various themes.

Impact Across Industries

    Explore and articulate how TinyML is making a tangible impact across diverse industries.

## Bio

Jon is a Machine Learning Engineer specialized in IoT systems.
He has a Master in Data Science and a Bachelor in Electronics Engineering,
and has published several papers on applied Machine Learning,
including topics like TinyML, Wireless Sensor Systems and Audio Classification.

These days Jon is co-founder and Head of Data Science at Soundsensing,
a leading provider for condition monitoring solutions for commercial buildings and HVAC systems.
He is also the creator and maintainer of emlearn,
an open-source inference engine for microcontrollers and embedded systems.


## Ideas

### 1 Dollar TinyML
Section: Innovation Showcase
Format: Demo

Those familiar with TinyML know that there is a lot one can do with a low-cost microcontroller,
and that what is achievable within a certain budget is increasing year-by-year.
For example, for 1 dollar one can now get the RP2040 microcontroller (including FLASH),
providing a hefty 256 kB RAM and 4 MB program memory, running at 133 Mhz.
But a microcontroller alone is not sufficient to realize a TinyML system -
we also need sensors to get input data, some power solution to keep it running,
and to do something useful with the outputs of our Machine Learning models.
Inspired by the ever growing possibilities of low-cost hardware, we asked the question:
Can we build an entire TinyML system for under 1 dollar? What can it do, and what is not possible?

To our suprise we have been able to find solutions for both
microphone, accelerometer, microcontroller, wireless connectivity and power
- all within a 1 dollar Bill of Material (BOM).
In this budget we could only get an 24 MHz microcontroller with 4 kB RAM and 32 kB FLASH.
This has to fit the entire firmware, including sensor data buffers and TinyML models.
But it looks to be possible to perform popular tasks such
as Human Activity Recognition and Audio Classification within these resources.

The "Dollar TinyML" project, is a usecase study for the emlearn TinyML software library.



For 1 

 is a lot one can do with a

Extreme low end.
Ultra low cost hardware.

Our findings show that it is indeed possible to get a full system with a Bill of Material below 1 USD.
32-bit microcontroller

To our suprise we have been able to find solutions for both
microphone, accelerometer, microcontroller, wireless connectivity and power.

Of course it means that the entire firmware, with sensor data buffers and TinyML models,
must fit in 4 kB RAM and 32 kB FLASH.

This project serves as a torture test for emlearn, an open-source library of TinyML.


1 dollar gets you

STM32F072 with 16 kB RAM and 64 kB FLASH. USB
STM32F030 with 32 kB RAM and 256 kB FLASH
RP2040 with 256 kB RAM and 4 MB FLASH. 133 Mhz

https://www.lcsc.com/product-detail/Microcontroller-Units-MCUs-MPUs-SOCs_Raspberry-Pi-RP2040_C2040.html
W25Q32JVSSIQ
https://www.lcsc.com/product-detail/Microcontroller-Units-MCUs-MPUs-SOCs_STMicroelectronics-STM32F030RCT6_C81046.html

But what if the entire system should cost under 1 dollar?
Is it possible to make a useful system? What are the limitations?
What implications does this have over the coming years?
What will the impact become?

Motivation
Findings/Status
Demonstrate

Working within such strict constraints requires creative solutions.


### emlearn 5 years
Section: Impact Across Industries / 

#### Abstract

emlearn is an open-source Python library that allows converting scikit-learn and Keras models to efficient C code.
The goal of the project is to make it easy to deploy efficient models to any microcontroller with a C99 compiler,
while keeping Python-based workflow that is familiar to Machine Learning Engineers.
The project was first released in 2018, predating many other TinyML libraries.
Over the years the library has been used in a wide range of applications,
from detection of vechicles in acoustic sensor nodes,
to tracking welbeing of grazing cows using accelerometers,
to hand gesture recognition based on sEMG data,
to real-time malware detection in Android devices.
In this presentation we will showcase a selection usecases and discuss their impact.
We will also cover some of the latest improvements,
such as optimized decision tree ensembles, and native support for MicroPython.


- emlearn impact over.
Portable classical methods for microcontrollers
A scikit-learn for microcontrollers
Impact via papers written about it

IDEA: invite authors to provide more details.
Stories. Images. Videos. Funny,anecdotal
Basically anything that goes.


# Notes

## Misc

emlearn 0.1.0 was tagged 2018
Available on PyPi as emtrees since March
https://pypi.org/project/emtrees/0.2.0/
Renamed to emlearn in October, 2018
https://pypi.org/project/emlearn/0.3.1/

Before TinyML was an established term

X-CUBE-AI, 17-Dec-2018
https://petewarden.com/2019/03/07/launching-tensorflow-lite-for-microcontrollers/
