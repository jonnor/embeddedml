
### About Soundsensing

I work for a company called Soundsensing.
We provide predictive maintenance solutions for HVAC systems in buildings.
Using vibration and sound-based monitoring.

For us, Edge AI // TinyML is a way to do extract relevant information directly on sensors.
Which can then be further processed using time-series machine learning in the cloud.

## Outline


Here we are mostly concerned with the smallest systems.
Aka TinyML.
Typically on a low-cost microcontroller.
Often running battery-powered.
But several of the points discussed here are relevant also for larger "Edge AI" systems.


## Sensor data analysis with ML

A simplified system architecture for a TinyML system.
Have sensors, a microcontrolller, some actuators //or outgoing connectivity.

The microcontroller will run a trained Machine Learning model.
So we will do *inference* on device.
The training/learning has happened offline on a regular PC.

In addition to the ML model, there is usually some pre-processing and post-processing.

Pre-processing can include

- Format conversions
- Data normalization
- Feature extraction

Post-processing

- Aggregation of predictions
- Filtering
- Decision logic

Pre-processing can be quite computationally intensive.
Post-processing is usually computationally easy - but may have a lot of business logic.


## TinyML challenge

Two worlds:
Training on PC.
Inference on device.

By default, these two worlds are often quite distinct.

Differences between these versions of the pipeline will cause trouble!
Often data pipeline failures will fail silently.
There will be no errors, but the results will be worse than expected.
Can be subtly wrong across a range of inputs,
or give complete failure on smaller subsets of inputs. 

For model conversion, there exist standard tools, that can transform in a compatible way.
But pre- and post- processing often not.

## Strategy for TinyML challenge

Multi-step validation, using a small validation dataset.
Run the entire pipeline.
A type of and end2end or integration test.

1b) Run in your Continious Integration pipeline 
1c) Run with Hardware-In-the-Loop

=> the output must be portable between PC and device.

If the tools are not compatible, then you should probably use simulation.

## emlearn overview

Python library used on PC.
C library used on device.
MicroPython library used on device.

All device code is portable, and runs also in PC.
To facilitate the kind of quality assurance I mentioned earlier.


## emlearn on Zephyr

The emlearn C library can be used on any platform.
By downloading the code, and adding the header files to include path.

But to make it easy and clean, we provide some dedicated support for popular platforms.

Zephyr has a standardized build tool called West,
and a configuration system based on KConfig.

emlearn provides a module that can be used directly with this.

## Zephyr sensor APIs


## Continious classification

When doing ML on sensor data, we often have a time-series of data.
Like audio, accelerometer, or other sensors that are sampled regularly.

Usually we need to collect a set of samples, and then pass that into the ML model.
And we do this continiously.


## Bridging the TinyML language gap

Data Scientists know Python.
Firmware people know C.

So often these pipelines are quite disjoint, both technically and socially.

There are multiple ways of achieving code re-use and improved collaboration.

Here I will discuss one of the options - using MicroPython as a common "platform",
which allows running the same code both on device and on PC.
Enable the Data Scientists to work directly on the pipeline that runs on device.


## About MicroPython

Good platform support.
Via Zephyr can run on a very wide range of devices.

MicroPython has excellent support for C modules

Can also be used in "embedding" mode.
I have not tested it.
Should potentially allow running a data pipeline on any device.


## MicroPython C modules

Just a few lines of code to expose C code as a Python function.


## MicroPython Data Science ecosystem

In CPython one has arguably the best data science ecosystem out there.
For MicroPython there are now re-implementation of several of core libraries.
For example we have.

* ulab - implements numpy arrays and operators. Also a subset of scipy.
* OpenMV. Computer vision. Also has Tensorflow Lite for microcontrollers
* emlearn-micropython. Implements a selection of ML models from scikit-learn and Keras/Tensorflow

Data formats. Not covered here.
There is support for common multi-media formats, though it could be improved.
Awesome MicroPython has an overview.

## emlearn-micropython overview

Implements ML models from scikit-learn and Keras

Also implements common Digital Signal Processing algorithms that are often used in feature extraction.

Infinite Impulse Response Filters
Fast Fourier Transform


## emlearn-micropython. More examples

Found in the Github repository

These run both on PC (Unix port) and on device (ESP32).
To demonstrate the ability to develop and verify across PC and device.


