

# Tutorial

## Format
90 minutes

## Title
Machine Learning on hardware devices using emlearn

## Abstract

Physical computing involves interactive systems that can sense and respond to the world around them.
By using a hardware unit with sensors and combining it with Machine Learning,
it becomes possible detect objects, events or other phenomena of interest.
The sensor data can be motion, vibration, sound, images, proximity, et.c.
However standard low-cost and power-efficient hardware devices use
microcontrollers with severely limited storage, memory and compute,
which must be taken into account when developing such systems.

In this tutorial you will learn how to deploy Machine Learning models to a microcontroller,
to make a practical and customizable sensor that detects physical motion events.

We will use the emlearn Python library, which converts ML models made with
scikit-learn and Keras to efficient C code designed to run on microcontrollers. 
We will also have a look at MicroPython,
which makes it possible program a microcontroller application in Python instead of C code.

## Description

This is intended to be a practical, hands-on and fun tutorial.
Prior exposure to hardware device is not needed!

#### Who is it for

The following should find this especially interesting

- Tinkerers/makers who like to create physical things
- Researchers/engineers/developers working on embedded devices / IoT
- Researchers/engineers/developers in sensing and sensor-systems
- Those curious about computationally-efficient Machine Learning

We assume that you are

- comfortable with programming in Python
- comfortable with installing OS packages/drivers and using a shell
- familiar with basic machine learning, such as supervised learning and classification

It it is beneficial, but not neccesary, if you

- have programmed an embedded device. Arduino et.c. before
- have some familiarity with time-series data

#### What to bring 
Participants must bring their own laptop and have Python 3.8+ installed.
If you need an adapter for USB Type-C, please bring it with you! 

The neccesary hardware kits will be provided for the tutorial.
Participants will work in groups of 2-5 persons per kit.
If anyone is interested, kits can also be purchased to bring home.

#### Course structure

0: Introduction.

- Learning goals for tutorial
- Structure of the tutorial
- Basics on developing against external hardware device
- Introduction to example project

1: First setup, using stock model.

- Installing emlearn and other Python dependencies
- Install device communication tools
- Run training pipeline on existing data 
- Upload initial firmware, already provided

2: Collecting new data.

- Define a few classes of behavior
- Record data for each class
- Check and clean the data

3: Train and run custom model.

- Re-run training pipeline with new data
- Upload firmware with new model

4: Individual work.

- With assistance from teacher

#### Details to be decided

The hardware platform used will probably be a ESP32-based board with integrated sensors,
compatible with common open-source frameworks such as MicroPython and Arduino.

The example project will potentially be gesture recognition with accelerometer,
or a similar fun, personal and physical project.

We may used a combination of MicroPython and C/C++ device code,
depending on what is realistic for the project.

### Notes

The tutorial will be tested with a group before the conference.

I might also run this tutorial during the sprint day / weekend.

A presentation will also be proposed on a related topic.



