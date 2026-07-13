
# Abstract

Python is the standard solution for many machine learning and data science applications, from large cloud systems, to workstations, and even on larger embedded or robotics systems.
But as we move down into more constrained environments regular (C)Python starts to be a less good fit.
The MicroPython project provides a Python implementation that is tailored for such environments,
and this makes it possible scale down to microcontrollers with just a few megabytes of RAM (or less!).
As a bonus, MicroPython with WebAssembly also makes lightweight browser applications possible.
In this talk, we will discuss how to combine IoT devices, MicroPython and browser to build stand-alone sensor systems and laboratory gear for physical data science.

## Description

In this talk, we will discuss how to combine IoT devices, MicroPython and browser to build stand-alone sensor systems and laboratory gear for physical data science.

Typical Internet of Things devices send off most of the data to an external cloud service for analysis.
This causes challenges both in terms of privacy, poor reliability under poor connectivity, and loss-of-availability when the service is discontinued.

We would like to show that it is possible to achieve the majority of functionality using a local-first approach,
including machine-learning based sensor-data analysis.
And that this can done on low-cost microcontrollers such as ESP32.

This talk will cover how to build stand-alone devices for measuring and analying physical sensor data, using MicroPython. This includes these aspects:

    Measuring the surroundings using sensors
    Connectivity using WiFi
    Data storage using on-board filesystem
    Serving a webui for configuration/control, using Microdot
    Automated data processing/analysis using DSP and ML, with emlearn-micropython
    Enabling interactive data analysis via webui
    Managing concurrency on microcontroller, using asyncio
    Optional integration. Pull using HTTP, and/or push using Webhooks/MQTT

The sensor data will either be accelerometer, sound or images/video (To be Decided).
