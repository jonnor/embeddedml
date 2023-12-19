
A) "Explainable Features for Acoustic Condition Monitoring of Machinery"
B) "Dominant Sound Event method for automatic classification of noise events"

Candidates

- Machine Learning on microcontrollers using MicroPython and emlearn
- Learning to detect sound events - without labling every single event


## Title
Machine Learning on microcontrollers using MicroPython and emlearn

## Session type
30 minutes
Optional 45 minutes (long)

## Category
PyData: Machine Learning & Deep Learning & Stats

## Keywords


## Abstract
200 to 1500 characters.
Shortened version of description.


## Description
400 and 50000 characters


### Audience

Level: Intermediate

Assumed knowledge

- Basic literacy in Python and proficiency in programming
- Familiarity with core Machine Learning concepts.
Supervised/unsupervised learning. Classification/regression.

Beneficial but not neccesary

- Familiarity with embedded devices
- Familiarity with time-series data

Who is it for

- Researchers/Engineers/developers working on embedded devices / IoT
- Tinkerers/makers who like to make physical things
- Those interested in computationally-efficient Machine Learning


## Goal

You as a Python developer
with some experience with standard Python ML libraries (scikit-learn/Keras)
can deploy ML models to a microcontroller device

## Key elements

Minimum

- What can and cannot be done (in terms of ML) on a microcontroller. Conceptual,guidelines,tooling
- What are usecases where microcontrollers shine. Autonomous. Battery power. Placement.
- Motivating usecases. Examples
- Choosing/buying hardware. Very brief
- Installing MicroPython. Very brief
- Installing emlearn-micropython. Thorough
- Training a model. Brief
- Converting model to emlearn. Thorough
- Deploying to device. 
- Loading model on device, running on data
- Verifying conversion
- Checking size constraints
- Using model outputs. Transmitting
- Demo to show that it is real

Bonus

- Collecting data. Transmit to host or record to FLASH.

## Take aways

Primary

- Runs everywhere that MicroPython runs
- Super easy to get started. 
- Installable as a module
- Do not have do deal with any C code
- Very good performance. Inference time, size, RAM
- Compatible with standard PyData stack. scikit-learn, Keras, etc
- Supports common tasks. Classification, regression, anomaly/outlier detection
- Supports common usecases. Image classification, Sound Event Detection, Human Activity Recognition

If you know how to make a scikit-learn/Keras model,
you know how to deploy it to a microcontroller


## Notes

Microcontrollers are getting more powerful
Raspberry PI Pico, ESP32

It used to be that everything had to be writte in C or C++.
Now you can get a 10 USD development board.

M5Stack AtomS3U. 15 USD
LilyGo T-Watch S3. 50 USD
Arduino Nano 33 BLE Sense. 

MicroPython

Program everything in Python

Practical examples of
Image classification, Sound Event Detection, Human Activation Recognition

emlearn is a tiny machine learning for embedded devices and microcontrollers.
It focuses on inference, but also supports a few on-device learning methods.


scikit-learn for microcontrollers.

emlearn-micropython are MicroPython bindings

Models can be loaded from CSV files.

Install as a module
Without any recompilation.


## Questions

How much under-the-hood to show?
Implementation details on the bindings.
Maybe the choice of array.array is relevant
Minimize allocations
Dynamic user module versus existing module
Separate modules instead of big

Comparison with ulab

MicroPython contributions
- linker fixes
- ? HTTP support in mpremote cp 

What is the FOTA story with MicroPython?

