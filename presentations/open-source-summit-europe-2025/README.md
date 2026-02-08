
# Machine Learning for Microcontrollers With Zephyr and emlearn

https://osseu2025.sched.com/event/25Voe/machine-learning-on-microcontrollers-with-zephyr-and-emlearn-jon-nordby-soundsensing

Monday August 25, 2025 15:35 - 16:15 CEST

#### Video recording

[Linux Foundation YouTube](https://www.youtube.com/watch?v=FZ0q6RLCYPM)

[Jon Nordby YouTube](https://www.youtube.com/watch?v=rbRCk2DCEWY)


#### Slides
[.PPTX](<Machine Learning for Microcontrollers With Zephyr and emlearn.pptx>)
| [.PDF](<Machine Learning for Microcontrollers With Zephyr and emlearn.pdf>)

#### Notes
[Notes](./notes.md) | [Proposal](./proposal.md)


## Abstract

Modern Machine Learning makes it possible to automatically extract valuable information from sensor data,
and it has become feasible to deploy ML systems to low-cost embedded devices and sensors.
This niche is often referred to as "TinyML", and is enabling a range of new applications in consumer electronics, science and industry.

emlearn is an open-source project for deploying Machine Learning models to any device with a C99 compiler.
It provides a Python library for converting models made with scikit-learn or Keras to efficient C code.
The library has been used for many applications across a range of sensor modes,
such as audio, vibration, power-line, radar, et.c.

Zephyr RTOS is a comprehensive open-source operating system that runs on a wide range of microcontrollers.
The support for low-power operation, communication protocols,
and standardized "sensors" API makes it a very attractive platform for TinyML applications.

In this presentation we introduce the emlearn project, and show how it can be used together with Zephyr.
We will cover the key features and tools that the library provides,
and demonstrate how to perform practical Machine Learning tasks.
