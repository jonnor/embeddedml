
## Title

Sensor data processing on microcontrollers with MicroPython


## Abstract

Being able to sense physical phenomena is critical to many areas of science;
from detecting particles in physics, to measuring pollution in public health, to monitoring bio-diversity in ecology.
Over the last decades the capabilities and costs of sensor system has become much better,
driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication.
Thanks to this Wireless Sensor Networks and "Internet of Things" (IoT) sensor systems are becoming common.

Typically sensor nodes use microcontroller-based hardware, and the firmware developed primarily using C (or C++).
However, it is now becoming feasible to write microcontroller firmware using Python.
This is thanks to the MicroPython project, combined with affordable and powerful hardware from the last couple of years.
Using the familiar and high-level Python programming language makes the process of creating sensor nodes
more accessible to an engineer or scientist.

In this talk we will discuss developing microcontroller-based sensors using MicroPython.
This includes a brief introduction to MicroPython, how to do efficient data processing,
and share our experience applying this to process accelerometer and microphone data,
using both Digital Signal Processing and Machine Learning techniques.


## Description


Battery powered.
Sleep as much as possible. Wake up as seldom as possible.
And go back to. Compute time.


ESP32 hardware.


MicroPython is an implementation of

efficient

ulab
Sensor data processing

Report on our investigations using
The limitations we found


## Outline

- BRIEF. (Wireless) Sensor Network concept. 
Wireless communication. Battery power.
- BRIEF.Sensor node concept.
Readout. Processing. Storage/buffering. Transmission
- BRIEF. MicroPython introduction. 
Purpose. Compat. Libraries.
- MAIN. Efficient data processing in MicroPython.
Cases. DSP and ML techniques. FFT, RMS, CNN, RF.
Show benchmarks. Compute time. Memory usage. 
Plain Python perf dos and dont. Avoid/reduce allocations!
@micropython.native and @viper annotators
User C modules.
Dynamic native modules.
emlearn.
ulab.
- BRIEF. Reading data
Accelerometer, microphone. (camera?)
- BRIEF. Storing data
Internal FLASH. Memory card
- BRIEF. Sending data
MQTT, HTTP, BLE. LoRa ?

Maybe show a simple end-to-end example.
Putting all the pieces together.


## Notes

Change of talk format possible given a notice ahead of time.
At least into 15 minutes + QA.

Planning a separate submission for a poster.

## Formats
Maintainer track. 45 minutes
25 minutes + QA
15 minutes + QA



## Categories

Scientific Applications

    Healthcare and Biomedicine
    Earth and Ocean Sciences
    Geo Sciences
    Physics
    Robotics & IoT

Data Science and Visualization

    Data Analysis and Data Engineering
    Model Deployment

Machine and Deep Learning

    Supervised Learning
    ML Applications (e.g. NLP, CV)

Community, Education, and Outreach

    Learning and Teaching Scientific Python
