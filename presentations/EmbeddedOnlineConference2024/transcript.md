
## Intro
Hi everyone,
and welcome to this microtalk about Machine Learning for microcontrollers,
and quick introduction to the emlearn open-source software package.

My name is Jon Nordby, and I am the Head of Data Science at Soundsensing.
We are a leading provider of Predictive Maintenance solutions for buildings and ventilation systems.

## Sensor

Machine Learning is applied in more and more fields,
covering a very diverse set of applications. 

When it comes to Machine Learning on microcontrollers,
we are obviously not going to be running any Large Language Models or generative image models.
But one usecase where ML is incredibly useful is in analysing sensor data.

Sensors such as accelerometers, microphonones, radars, and cameras have gotten incredibly cheap and powerful.
But in order to get useful information out of these, the raw data must be processed.
Using Machine Learning, in combination with Digital Signal Processing, allows analyzing complex phenomena.

If this is done on the microcontroller, we get a range of benefits:
...

The component in blue is the Machine Learning model,
and is typically trained ahead of time on a PC.

## Example

Here is an example of a practival project:
Analysing cattle activity using an accelerometer.

A decision tree model is used to analyze the accelerometer data,
and classify into lying/walking/standing/grazing/ruminating.
These categories are very compact and are transmitted over LoRaWAN.

And the data over time can be used to detect abnormal behavior,
which can indicate health issues, external threats or stressors.

They found that running the Machine Learning on-sensor
uses 50 times less power than transmitting raw data.
Giving a huge increase in battery life.

## emlearn

emlearn is an open-source software library that can be used to implement such projects.
It provides embedded friendly implementations of Machine Learning models.

It supports converting models trained in Python, the most popular programming languge
for ML / Data Science projects.
Can either use scikit-learn or Keras, two very established frameworks.

The code is portable and clean C99.
It can be used on even the smallest MCUs,
as it does not need FPU, and the code size is very small.

## Supported models and tasks

emlearn supports the three most common ML tasks:

classification, regression, anomaly detection.

Supports a selection of embedded friendly models:

Tree-based ensembles, K Nearest Neighbors and Neural Networks


## How to use
Now we will quickly show how to use emlearn.

The library can be installed either as a Python package,
or be included as a git submodule.

## Training a model

Training a model is done using a standard framework like scikit-learn or keras.
You will need to already have a dataset collected and labeled for your task.

There is nothing emlearn specific at this point
- although you should use a model small enough to fit on your target device.
We also provide some tools for checking this.

Once you have a trained model, you are ready to deploy it to the device.

## Convert model to C

emlearn provides a function to convert your trained Python model
into an optimize C model,
and a function to save this as C code.

There are a few model-specific options for convert,
but for most cases, nothing needs to be specified.

The are also tools verification of the optimized C model again the original Python.


## Run the C code

To use the code, include the generated header file.

Pass the data to the predict() call of the model.

The output can the be used to trigger relevant actions,
such as controlling motors, logging event that occur,
or sent an external system.

In this example, we just show the model output on a display.

## Summary

...

You will find more information on emlearn.org

## Thank you

Thank you for listening.
I hope you found it interesting and useful.

