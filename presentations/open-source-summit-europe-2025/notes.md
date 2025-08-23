
# Speaker office hours

Machine Learning for sensor-data analysis.
Especially on microcontroller-grade systems, but also on larger embedded systems (Linux),
or on desktop/server.

technical guidance, best practices

# Talk

## Format

40 minute slot.
30 minutes + QA.

30-45 slides total

## Goals

- Make emlearn for Zephyr and C better
- Learn more about Zephyr
- Attract users of emlearn. Maybe also contributors

## Call to Action

- visit me in Speaker Working Hours
- come visit at the Zephyr booth
- ? try out the samples
- ? check out the MR

## Take aways

- Running machine learning inference on microcontroller grade is useful in many applications
- Zephyr is a good base for TinyML applications. Sensor API, connectivity
- emlearn for scikit-learn or Keras to efficient C code
- emlearn can be used together with Zephyr via the C library/module


## Outline

- Applications
- TinyML system diagram

- ML tasks. Clear definition for each, with example in TinyML setting
Classification, Regression, Anomaly Detection

- Zephyr APIs for sensor data
Sensor API. accel/gyro, dmic

- emlearn overview
- emlearn for C
- emlearn C + Zephyr

- Recording data ?
- Labeling of data ?

MicroPython+Zephyr+emlearn
Quite short, say 3-4 slides
- MicroPython for Zephyr
- emlearn with MicroPython


## Audience considerations 

Assuming most will be firmware engineers / embedded software engineers.
Not ML engineers / data scientists. Probably have less exposure to machine learning.
Might have some digital signal processing exposure.

Expect that people have familiarity with Zephyr, C programming.

Expect them to be more interested in C development compared to (Micro)Python
! keep focus on C + Zephyr
MicroPython mentioned only briefly

! need to define relevant ML terms simply and clearly
? focus on Classification
Supervised learning


## TODO

- Create outline
- Import all reference slides from existing presentations
- Add placeholders for planned slides
- Fill inn all missing slides

- Complete Zephyr C code samples

#### Maybe

- Sample code for sensor data readout with Zephyr, on XIAO BLE Sense
Accelerometer/dyro readout
https://docs.zephyrproject.org/latest/samples/sensor/lsm6dsl/README.html
Alternatively dmic soundlevel example
https://docs.zephyrproject.org/latest/samples/drivers/audio/dmic/README.html#dmic

- ? feature extraction pipeline for accelerometer in C
Foremost toothbrush grade
Stretch: FFT etc
Take raw sensor data buffers, returns features
Wrap as MicroPython module? Integrate into har_trees that way?

- ? demo of toothbrush application on Zephyr+MicroPython
Inference foremost
Need LSM6 support. Queues in Zephyr would be preferred.
Fallback: FIFO in MicroPython

- ? test the new video labeling in Label Studio?

#### Later

- ? add XIAO BLE with Zephyr support to har_trees
Need LSM6 with FIFO support

## Dream design for emlearn + Zephyr

Zephyr used for the HAL
Complete ML pipeline can run in C
Nice tools to make this clear and supporting best practices

emlearn has feature-extraction / pre-processing transformers,
with integrated support for C code

emlearn supports for doing on-device model validation and data recording,
via .npy files

emlearn-micropython also works with Zephyr (same as other MicroPython ports)

MAYBE. Example of how to expose a complete C pipeline to MicroPython application


