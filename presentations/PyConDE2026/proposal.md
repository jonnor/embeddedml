
# Proposal


## Title
Embedding Data Science in the Internet of Things with MicroPython and emlearn

## Length

20 minutes. Alternatively: 40 minutes 

## Abstract

Python is the standard solution for many machine learning and data science applications,
from large cloud systems, to workstations, and even on larger embedded or robotics systems.
But as we move down into more constrained environments regular (C)Python starts to be a less good fit.
The MicroPython project provides a Python implementation that is tailored for such environments,
and this makes it possible scale down to microcontrollers with just a few megabytes of RAM (or less!).
As a bonus, MicroPython with WebAssembly also makes lightweight browser applications possible.
In this talk, we will discuss how to combine IoT devices, MicroPython and browser to build
stand-alone sensor systems and laboratory gear for physical data science.


## Description

Typical Internet of Things devices send off most of the data to an external cloud service for analysis.
This causes challenges both in terms privacy, poor reliability under poor connectivity, and loss-of-availability when the service is discontinued.

We would like to show that it is possible to achieve the majority of functionality using a local-first approach, including machine-learning based sensor-data analysis.
And that this can done on low-cost microcontrollers such as ESP32.

This talk will cover how to build stand-alone devices for measuring and analying physical sensor data, using MicroPython. This includes these aspects:

- Measuring the surroundings using sensors
- Connectivity using WiFi
- Data storage using on-board filesystem
- Serving a webui for configuration/control, using Microdot
- Automated data processing/analysis using DSP and ML, with emlearn-micropython
- Enabling interactive data analysis via webui
- Managing concurrency on microcontroller, using asyncio
- Optional integration. Pull using HTTP, and/or push using Webhooks/MQTT

The sensor data will either be accelerometer, sound or images/video (To be Decided).

### About MicroPython

MicroPython is an implementation of Python that runs on practically all microcontrollers with 128kB+ RAM.
It provides access to the microcontroller hardware, functions for interacting with sensors and external pheripherals,
as well as connectivity options such as WiFi, Ethernet, Bluetooth Low Energy, etc.

While MicroPython can target a very wide range of hardware,
we will focus on the Espressif ESP32 family of devices.
These are very powerful and affordable, with good WiFi+BLE connectivity support,
good open-source toolchains, are very popular both among hobbyist and companies,
and have many good ready-to-use hardware development kits.

### About emlearn-micropython

emlearn-micropython is Machine Learning and Digital Signal Processing package for MicroPython, built on top of the emlearn C library. It provides convenient and efficient MicroPython modules, and enables application developers to run efficient Machine Learning models on microcontroller, without having to touch any C code.
Compared to pure-Python approaches, the emlearn-micropython models are typically 10-100x faster and smaller.

### Intended audience and expected background

Intended audience: Any developer or data scientist curious about sensor data processing, IoT, and how Python scales down to the smallest of devices.

The audience is expected to have a basic literacy in Python and proficiency in programming. 
Familiarity with microcontrollers and embedded systems is of course an advantage,
but the talk should be approachable to those who are new to this area.
Familiarity with basic networking and web/browser concepts in an advantage.


