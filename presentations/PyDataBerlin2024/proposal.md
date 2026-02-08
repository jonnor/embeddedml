
## Title
Machine Learning on microcontrollers using MicroPython and emlearn

## Session type
30 minutes
Optional 45 minutes (long)

## Category
PyData: Machine Learning & Deep Learning & Stats

## Keywords
Embedded devices, Internet of Things, physical computing

## Tweet abstract
Deploy ML models to microcontrollers - using just the Python you already know!
A practical presentation on how to use the emlearn Machine Learning package and MicroPython to build smart sensor systems.

## Abstract
200 to 1500 characters.
Shortened version of description.

This presentation will show you how to deploy machine learning models
to affordable microcontroller-based systems - using the Python that you already know.
Combined with sensors, such as microphone, accelerometer or camera,
this makes it possible to create devices that can automatically analyze and react to physical phenomena.
This enables a wide range of useful and fun applications, and is often referred to as "TinyML".

The presentation will cover key concepts and explain the different steps of the process.
We will train the machine learning models using standard scikit-learn and Keras,
and then execute them on device using the emlearn library.
To run Python code on the microcontroller, MicroPython will be used.
We will demonstrate some practical use-cases using different sensors, such as
Sound Event Detection (microphone), Image Classification (camera), and Human Activity Recognition (accelerometer).


## Description
400 and 50000 characters

Modern Machine Learning makes it possible to automatically extract valuable information from sensor data.
While Machine Learning is often associated with costly, compute-intensive systems,
it is becoming feasible to deploy ML systems to very small embedded devices and sensors.
These devices typically use low-power, microcontrollers that cost as little as 1 USD.
This niche is often referred to as "TinyML", and is enabling a range of new applications
in scientific applications, industry and consumer electronics.

While microcontrollers are getting more powerful year by year,
it is still important to fit within the limited RAM, program size and CPU time available.
emlearn is an open-source Python library that allows converting scikit-learn and Keras models to efficient C code.
This makes it easy to deploy models to any microcontroller with a C99 compiler,
while keeping Python-based workflow that is familiar to Machine Learning Engineers.
Via emlearn-micropython it also supports MicroPython, a Python implementation designed for microcontrollers.
MicroPython runs on practically all microcontrollers with 16kB+ RAM,
and this makes it possible to write an entire application for microcontrollers using Python.
The emlearn-micropython packages provided as a set of MicroPython modules
that can be installed onto a device, without having to recompile any C code.
This preserves the ease-of-use that Python developers are used to on a desktop system.
Compared to pure-Python approaches, the emlearn-micropython models are typically 10-100x faster and smaller.

The models in emlearn support the core Machine Learning tasks types: classification, regression and anomaly detection.
Additionally there are also tools for data preprocessing, feature engineering and estimation of compute requirements. 
Since the start in 2019, emlearn has been used in a wide range of applications,
from detection of vechicles in acoustic sensor nodes,
to hand gesture recognition based on sEMG data,
to real-time malware detection in Android devices.

While emlearn and MicroPython can target a very wide range of hardware,
we will focus on the Espressif ESP32 family of devices.
These are very powerful and affordable, with good WiFi+BLE connectivity support,
gpod open-source toolchains, very popular both among hobbyist and companies,
and have many good ready-to-use hardware development kits.

## Intended audience and expected background

The audience is expected to have a basic literacy in Python and proficiency in programming,
and familiarity with core Machine Learning concepts such as
supervised/unsupervised learning, classification/regression, et.c.
Familiarity with microcontrollers and embedded systems is of course an advantage,
but the talk should be approachable to those who are new to this area.

