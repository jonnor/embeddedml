
# Meta

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

