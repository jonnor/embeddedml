
# Instructions

Title Casing
- Abstract text. The number of characters is limited to 1,500
- CV: The number of characters is limited to 500


# Zephyr CFP

CFP: https://cloud.wekanet.de/s/8wqTgcNeiFdMG3t?dir=undefined&openfile=2051409

### Title

emlearn - a Machine Learning module for Zephyr

### Abstract

Modern Machine Learning makes it possible to automatically extract valuable information from sensor data,
and it has become feasible to deploy ML systems to low-cost embedded devices and sensors.
This niche is often referred to as "TinyML", and is enabling a range of new applications
in consumer electronics, science and industry.

emlearn is an open-source library for deploying Machine Learning models to any device with a C99 compiler.
It provides a Python library for converting standard models (made with scikit-learn and Keras) to efficient C code.
The library has been used in a wide range of applications, from detection of vechicles in acoustic sensor nodes,
to hand gesture recognition, to real-time malware detection in Android devices.

Zephyr RTOS is a comprehensive open-source operating system for embedded devices.
It provides hardware support for a wide range of microcontrollers,
including low-power operation and common wireless communication protocols.
It also provides standardized "sensors" API and wide range of built-in drivers.
These features combined makes the platform very attractive for TinyML applications.

In this presentation we introduce the emlearn project, and show how it can be used together with Zephyr.
We will cover the key features and development tools that the library provides,
and demonstrate how one can perform common Machine Learning tasks (classification, regression and anomaly detection).

### More information
https://github.com/emlearn/emlearn


## Bio

Jon is a Machine Learning Engineer specialized in IoT systems.
He has a Master in Data Science and a Bachelor in Electronics Engineering,
and has published several papers on applied Machine Learning,
including topics like TinyML, Wireless Sensor Systems and Audio Classification.

These days Jon is co-founder and Head of Data Science at Soundsensing,
a leading provider of condition monitoring solutions for commercial buildings and HVAC systems.
He is also the creator and maintainer of emlearn,
an open-source Machine Learning library for microcontrollers and embedded systems.


# TinyML

EmbeddedWorld. Send proposal to TinyML. MicroPython focus
https://cloud.wekanet.de/s/My44Rc588TM4c3w?dir=undefined&openfile=1775426
Lowering the barriers to entry, and improving time-to-market

## Title
Bridging the TinyML language gap with MicroPython and emlearn

## Abstract

To realize a TinyML system requires combining embedded systems with Machine Learning.
These are two specialization with their own established languages:
C on the embedded device (for the firmware), and Python on the PC (for Machine Learning / Data Science).
This split can cause challenges in a project in quality assurance, execution speed and staffing.
If code is not shared, incompabilities in data pipelines arise quickly, and there is a duplication of effort.
The lack of a common lingua franca can make it hard for team members to understand eachother.
One strategy to reduce this friction, is utilize Python also on the embedded device.

MicroPython is an implementation of Python that runs on microcontrollers with 16kB+ of RAM.
The interpreter can be embedded in a C program or run as the top-level entrypoint of an application,
and individual MicroPython modules can be implemented either in Python or in C.
This enables mixing C and Python as required by the particular use-case and system architecture.

emlearn is a Machine Learning engine for microcontrollers and embedded systems, implemented in C99.
Since 2023 the project also provides a set of ML and DSP modules for MicroPython.
This enables TinyML application developers to build firmware almost entirely in Python,
while still enjoying the space/compute/power efficiency of C.
In this presentation we will discuss what kind of use-cases this approach is suitable for,
along with the current limitations.


