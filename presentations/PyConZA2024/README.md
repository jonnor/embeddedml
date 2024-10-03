
# PyConZA 2024

## Sensor data processing on microcontrollers with MicroPython and emlearn

Slides
[PDF](PyConZA2024 - Sensor data processing on microcontrollers with MicroPython.pdf) | 
[PowerPoint](PyConZA2024 - Sensor data processing on microcontrollers with MicroPython.pptx).

Video recording. Will be published to Youtube later, by the organizers.

#### Abstract

Being able to measure physical phenomena is critical to many areas of science and engineering; from measuring pollution in public spaces to monitoring of critical infrastructure. Over the last decades, the capabilities and costs of sensor system has become much better, driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication. Thanks to this Wireless Sensor Networks and "Internet of Things" (IoT) sensor systems are becoming common.

Typical sensor nodes use microcontroller-based hardware, and the firmware developed primarily using C (or C++). However, it is now becoming feasible to write microcontroller firmware using Python. This is thanks to the MicroPython project, combined with affordable and powerful hardware from the last couple of years. Using the familiar and high-level Python programming language makes the process of creating sensor nodes more accessible to an engineer or scientist.

In this talk we will discuss developing microcontroller-based sensors using MicroPython. This includes a brief introduction to MicroPython, how to do efficient data processing, and share our experience applying this to process accelerometer and microphone data, using both Digital Signal Processing and Machine Learning techniques. We will apply some functionality, techniques, and lessons learned from the emlearn-micropython project - a Machine Learning and Digital Signal Processing library for MicroPython. Code available at: https://github.com/emlearn/emlearn-micropython

Intended audience: Any developer or data scientist curious about sensor data processing, IoT, and how Python scales down to the smallest of devices.

#### See also

emlearn-micropython: a Machine Learning and Digital Signal Processing library for MicroPython
https://github.com/emlearn/emlearn-micropython

