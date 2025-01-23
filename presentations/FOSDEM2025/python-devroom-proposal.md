
# Python devroom proposal
https://lists.fosdem.org/pipermail/fosdem/2024q4/003564.html

## Topics
* Data science, AI and Machine Learning
* MicroPython, CircuitPython, embedded software

## Format
25 minutes presentation, including Q&A, if any.

## Title
Sensing the world with MicroPython and microcontrollers

## Abstract

Being able to measure physical phenomena is critical to many areas of science and engineering; from measuring pollution in public spaces to monitoring of critical infrastructure. Over the last decades, the capabilities and costs of sensor system has become much better, driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication. Thanks to this Wireless Sensor Networks and "Internet of Things" (IoT) sensor systems are becoming common.

Typical sensor nodes use microcontroller-based hardware, and the firmware developed primarily using C (or C++). However, it is now becoming feasible to write microcontroller firmware using Python. This is thanks to the MicroPython project, combined with affordable and powerful hardware from the last couple of years. Using the familiar and high-level Python programming language makes the process of creating sensor nodes more accessible to an engineer or scientist.

In this talk we will discuss developing microcontroller-based sensors using MicroPython. This includes a brief introduction to MicroPython, best practices for high-rate data processing in limited RAM/FLASH/CPU, and energy efficiency wrt to wireless protocols.
We will share our experience applying this to process accelerometer, image, and microphone data; using both Digital Signal Processing and Machine Learning techniques. We will apply some functionality, techniques, and lessons learned from the emlearn-micropython project - a Machine Learning and Digital Signal Processing library for MicroPython. Code available at: https://github.com/emlearn/emlearn-micropython

Intended audience: Any developer or data scientist curious about sensor data processing, IoT, and how Python scales down to the smallest of devices.

## Notes
Improved version of a talk given at PyConZA 2024.

## Call to Action
Try building sensors. It is fun and practical!
You can use the Python that you already know!

## Outline

Start from PyData Global 2024, or PyCon ZA 2024.
Add in a practical bit? Demo/walkthrough. With ViperIDE.

