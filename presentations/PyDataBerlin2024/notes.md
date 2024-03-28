
# Meta

## TODO

- Implement accelerometer data capture on watch
- Reproduce simple gesture detection example
- Capture some data

## Format
30 minutes. 25 minutes, 5 minutes Q+A

## Goal
Purpose of this presentation

> You as a Python developer
> with some experience with standard Python ML libraries (scikit-learn/Keras)
> can deploy ML models to a microcontroller device
> using emlearn

## Audience

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
- Verifying performance after conversion
- Checking size constraints
- Using model outputs. Transmitting
- Demo to show that it is real

Bonus

- Collecting data. Transmit to host or record to FLASH.

## Take aways

Primary

- Runs everywhere that MicroPython runs.
Which is most microcontrollers with 16 kB+ RAM plus
- Super easy to get started. 
Installable as a module
- Do not have do deal with any C code
- Very good performance. Inference time, size, RAM
- Compatible with standard PyData stack. scikit-learn, Keras, etc
- Supports common tasks. Classification, regression, anomaly/outlier detection
- Supports common usecases. Image classification, Sound Event Detection, Human Activity Recognition

If you know how to make a scikit-learn/Keras model,
you know how to deploy it to a microcontroller


# Content planning

## Choosing hardware

ESP32 is probably the best general bet.
Huge community
Lots of hardware options
From very cheap bare-bones, to more plug & play solutions

If not familiar with hardware, start with something that has interesting sensors built-in.
Sensors available on I2C breakout boards generally easy to add later.

M5Stack AtomS3U. 15 USD
LilyGo T-Watch S3. 50 USD
T-Camera S3. 20 USD
M5Stack CoreS3. 60 USD
ESP32-S3-BOX. 50 USD

Adafruit's MEMENTO
SparkFun MicroMod

M5Stack Core2. 50 USD
Arduino Nano 33 BLE Sense. 
Raspberry PI Pico also strong community

## Worked example

Would be nice to have a worked example.
Something that we are going to show how to make.

Ideally there will be overlap with what is needed for TinyML EMEA / 1 dollar ML project.

### Constraints
Might be best for now to go with accelerometer!

Accelerometer

- Low data rate.
- Can do feature-enginering in Python.
- Can do drivers in Python (I2C/SPI)
- Easy to store and transfer recorded data. Can probably use MicroPython file-system. CSV files
- Bunch of drivers already out there
- Should be able to get far with RandomForest ?
- Have a paper with reference for the HAR pre-processing

Sound Event detection

- Driver needs to be in C
- PDM support is WIP for ESP32, not yet mainline
https://github.com/micropython/micropython/pull/14176
- Feature pre-processing has to happen in C
- emlearn missing strong classifiers. RNN/CNN
- emlearn-micropython missing bindings for audio pre-processing
- Might get into performance issues

### Ideas

Should be fun and/or useful. But relatively simple.

Accelerometer/IMU

- Human Activity Detection
- Gesture detection

Specifics

- Excercise repetitions
- Shake to turn on
- Continious motion classification
- Magic wand
- Air writing.
- Air drummer.
- Washing machine cycle tracker. Is it done yet?


Could use a smart-watch type hardware as the base?
https://www.lilygo.cc/products/t-watch-s3
Has same MCU as T-watch 2020 V3. BMA423

Could display on screen.
Could communicate results to a phone or central. Using BLE of WiFi.
Left as exercise for the reader

## Activity recognition examples

https://blog.tensorflow.org/2021/05/building-tinyml-application-with-tf-micro-and-sensiml.html
jab vs hook

https://www.hackster.io/leonardocavagnis/gesture-recognition-tinyml-for-8-bit-microcontroller-1cb0a8
punch vs flex

https://github.com/tkeyo/tinyml-esp
x move vs Y move vs circle

## Continious gestures example

https://edge-impulse.gitbook.io/docs/tutorials/end-to-end-tutorials/continuous-motion-recognition

uses spectral features pre-processing block
https://edge-impulse.gitbook.io/docs/edge-impulse-studio/processing-blocks/spectral-features
- a low or high filter with optional decimation
- automatically removes FFT bins based on the low/high freq settings
- does mean subtraction before FFT
- overlapped 50% windows by default
- optional log transform
- FFT bins in window are summarized using max()


uses Anomaly Detection (with k means) to handle out-of-distribution data

provides a dataset
https://edge-impulse.gitbook.io/docs/pre-built-datasets/continuous-gestures
15 minutes of data sampled from a MEMS accelerometer at 62.5Hz
idle - board sits idly on your desk. There might be some movement detected, e.g. from typing while the board is present.
Snake - board moves over the desk as a snake.
Updown - board moves up and down in a continuous motion.
Wave - board moves left and right like you're waving to someone.

## Activity Tracking

https://gadgetbridge.org/basics/features/sports/

## Physical Activity Monitor Service - BLE standard

https://www.bluetooth.com/specifications/pams-1-0/

Have a concept of a "session".
Physical activity session/sub-session is started when the user triggers the start of a session/sub-session via the server User Interface (UI),
when the server starts a session/sub-session on its own (for example,
every 24 hours or based on automatic activity detection and segmentation in user activity-defined sessions/sub-sessions).

## MicroPython on smart watch

https://github.com/jeffmer/TTGO-T-watch-2020-Micropython-OS
Updated to MicroPython 1.22 recently
Does not include LVGL

https://github.com/wasp-os/wasp-os
PineTime64, nRF52 devices

https://github.com/antirez/t-watch-s3-micropython
Uses "generic" ESP32 S3 image


https://unexpectedmaker.com/shop.html#!/TinyWATCH-S3/p/597047015/category=0
Has a board definition in mainline MicroPython
https://micropython.org/download/UM_TINYWATCHS3/



## MicroPython BLE communication


https://github.com/micropython/micropython/blob/master/examples/bluetooth/ble_advertising.py
gap_advertise

https://github.com/Wave1art/ESP32-Web-Bluetooth


## MicroPython WiFi HTTP communication

WLAN. HTTP. requests + json
https://docs.micropython.org/en/latest/esp32/quickref.html#wlan

WiFi managers
https://github.com/brainelectronics/Micropython-ESP-WiFi-Manager
https://github.com/george-hawkins/micropython-wifi-setup
https://github.com/ferreira-igor/micropython-wifi_manager

# Planning

## Misc

Microcontrollers are getting more powerful
Raspberry PI Pico, ESP32

It used to be that everything had to be writte in C or C++.
Now you can get a 10 USD development board.

This has a wide range of usecases across industries, from medical, to sports, acriculture, robotics.

Traditionally microcontroller development required programming in a low-level language such as C or C++.
However in the recent years it has become increasingly feasible to use a high-level language such as Python,
thanks to continued progress in hardware and open-source projects such as MicroPython.

MicroPython
Program everything in Python

emlearn is a tiny machine learning for embedded devices and microcontrollers.
It focuses on inference, but also supports a few on-device learning methods.

"scikit-learn for microcontrollers"
emlearn-micropython are MicroPython bindings

Models can be loaded from CSV files.

Install as a module. Without any recompilation.


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


# Misc unrelated

### GRU
Would enable SED. With small RAM usage

RNNs explained (covering RNN and LSTM, but not GRU explicitly)
https://cs231n.github.io/rnn/

Pytorch implementation. See class GRU
https://github.com/pytorch/pytorch/blob/main/torch/nn/modules/rnn.py 

Keras implementation. See class GRUCell, and standard_gru and its step() function
https://github.com/keras-team/keras/blob/v2.14.0/keras/layers/rnn/gru.py#L45-L391

numpy implementation
https://stackoverflow.com/questions/49755826/implementing-a-stateful-gru-in-pure-numpy-based-on-a-trained-keras-model

C embedded fixed point implementation, mostly using q15
https://github.com/majianjia/nnom/blob/master/src/layers/nnom_gru_cell.c

Open issue about Tensorflow lite micro
https://github.com/tensorflow/tensorflow/issues/43380

### DTW KNN

Would enable on-device learning

https://github.com/wannesm/dtaidistance/blob/master/dtaidistance/lib/DTAIDistanceC/DTAIDistanceC/dd_dtw.c
Wearable Real-time Air-writing System Employing KNN and Constrained Dynamic Time Warping
https://ieeexplore.ieee.org/document/10118944
Constrained dynamic time warping (cDTW) algorithm for the distance measure and K-nearest neighbors (KNN) as the classifier


