
## Format
30 minutes talk
Online.

## Title
Microcontrollers + Machine Learning in 1-2-3


## Abstract

Learn to build powerful sensors running on low-cost microcontrollers, all in Python!

Did you known that (Micro)Python can scale all the way down to microcontrollers
that have less than 1 MB of RAM and program memory? Such devices can cost just a few collars, and are widely used to measure, log, analyze and react to physical phenomena. This enables a wide range of useful and fun applications - be it for a smart home, wearables, scientific measurements, consumer products or industrial solutions.

In this talk, we will demonstrate how to get started with MicroPython on a ESP32 microcontroller.
We will first show how to create a basic Internet-connected sensor node using simple analog/digital sensors. And then we will show how to create advanced sensors that use Digital Signal Processing and Machine Learning to analyze microphone, accelerometer or camera data.


## Outline

- This is a microcontroller, these are its features
- Let us install Python on it! pip install esptool, download MicroPython, Flash
- OK - how do I program it? Using ViperIDE
- Lets make a sensor! Measure temperature, send to the cloud
- Lets level up. Doing compute intensive tasks in MicroPython. Sound level meter example.
- Lets go TinyML. Running a pre-trained ML model.

Bonus

- Building a custom ML model. Capturing data, labeling, running training, deploying to device

## Notes

I have recently given two talks on the same overall topic:
PyData Berlin 2024 (https://github.com/jonnor/embeddedml/tree/master/presentations/PyDataBerlin2024)
PyCon ZA 2024 (https://github.com/jonnor/embeddedml/tree/master/presentations/PyConZA2024).

This presentation will be new, in that it will have a much more application/demo centric flow.

## Description

Here is a brief introdution of the various technologies we will touch upon in this talk.

#### Sensor systems

Being able to measure physical phenomena is critical to many areas of science and engineering;
anything from measuring pollution in public spaces to monitoring of critical machinery.
Over the last decades the capabilities and costs of sensor system has become much better,
driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication.
Thanks to this Wireless Sensor Networks and "Internet of Things" (IoT) sensor systems are becoming common.

#### MicroPython

MicroPython is an implementation of Python for microcontrollers.
It runs on with a wide range of microcontrollers, provided they have at least 16kB+ RAM and 256 kB program memory.
Using the familiar and high-level Python programming language makes the process of creating sensor nodes
more accessible to an engineer or scientist.
MicroPython has excellent tools for optimizing code for embedded,
supporting Numba/Cython-style decorators for JIT/AOT compilation (native/Viper code emitters),
inline Assembly on ARM, and installable Python modules implemented in compiled languages.
This makes it possible to create very efficient and advanced systems, previously done mostly in C/C++.

Webpage: https://micropython.org/

#### TinyML

Modern Machine Learning makes it possible to automatically extract valuable information from sensor data.
While Machine Learning is often associated with costly, compute-intensive systems,
it is becoming feasible to deploy ML systems to very small embedded devices and sensors.
These devices typically use low-power, microcontrollers that cost as little as 1 USD.
This niche is often referred to as "TinyML", and is enabling a range of new applications
in scientific applications, industry and consumer electronics.

#### emlearn-micropython

emlearn-micropython is a Machine Learning and Digital Signal Processing library for MicroPython.
The package is provided as a set of MicroPython .mpy modules (written in C),
which can be installed at runtime, without having to recompile any C code.
This preserves the ease-of-use that Python developers are used to on a desktop system.
Compared to pure-Python approaches, the emlearn-micropython models are typically 10-100x faster and smaller.

The models in emlearn support the core Machine Learning tasks types: classification, regression and anomaly detection.
Additionally there are also tools and examples for data preprocessing and feature engineering.
Since the start in 2019, emlearn has been used in a wide range of applications,
from detection of vechicles in acoustic sensor nodes, to hand gesture recognition based on sEMG data,
to real-time malware detection in Android devices.

Github: https://github.com/emlearn/emlearn-micropython

#### Viper IDE

Viper IDE is an innovative MicroPython / CircuitPython IDE for Web and Mobile.
It supports directly connecting to a MicroPython device, over USB/serial, BLE or WiFi.
Makes it very easy to get started developing on a microcontroller.

Run it: https://viper-ide.org/


#### ESP32 microcontroller hardware

While MicroPython and emlearn can target a very wide range of hardware,
we will focus on the Espressif ESP32 family of devices.
These are very powerful and affordable, with good WiFi+BLE connectivity support,
excellent open-source toolchains, very popular both among hobbyist and companies,
and have many good ready-to-use hardware development kits.

#### Audience

Intended audience: Any developer or data scientist curious about sensor data processing, IoT,
and how Python scales down to the smallest of devices.

The audience is expected to have a basic literacy in Python and proficiency in programming.
Some familiarity with Machine Learning, and/or with microcontrollers/embedded systems is of course an advantage - but the talk should be approachable to those who are new to these areas.

