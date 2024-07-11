
# Meta

## Presentation TODO


- Styling. Add emlearn logo on all slides

## Example application TODOs

- Test emltrees on RP2040
- Fix emltrees on ESP32.
Enable debug prints in the module
Try to reduce the example further
Check allocations any writes - potentially out-of-bounds
- Classify basic gestures w/o feature preprocessing
- Record a demo video / take demo images
- Implement spectral gesture detection preprocessing


## Format
30 minutes. 25 minutes, 5 minutes Q+A

## Goals

- Establish emlearn-micropython project for TinyML for Python developers
- Get contributors make TinyML + MicroPython great.
Application examples, demos.
Documentation of best practices.
- Introduce people to MicroPython,
building a Python experience for microcontrollers.
mpip install ...

## Purpose
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
- Installing emlearn-micropython. Thorough, concise
- Training a model. Brief
- Preprocessing code. Continious classification. Overlapped windows
- ? data recording and labeling. Skip
- ? sensor reading. Skip
- Converting model with emlearn. Thorough
- Deploying to device. 
- Loading model on device, running on data
- Verifying performance after conversion
- Checking size constraints
- Using model outputs. Transmitting
- Demo to show that it is real

Bonus

- Collecting data. Transmit to host or record to FLASH.

Ecosystem challenges

- Packaging of native modules.
mpip install https://
mpip install nativemodule
- No standard/interoperable multi-dimensional array type
- Lack of best-practices for performant numerical compute
- Lack of best-practices for performant sensor-readout.
Use the FIFO!

Other

- Audio classification. CNN/RNN, spectrogram preprocessing
- Image classification. CNN
- Comparison with other tools in MicroPython
m2cgen, everywhereml
OpenMV (TensorFlow Lite for Microcontrollers / tflite_micro)
https://docs.openmv.io/library/omv.tf.html
ulab. https://github.com/v923z/micropython-ulab

Install method. Supported models. Performance

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


# Outline

- Motivation - why ML on microcontrollers. 3-5 minutes
- MicroPython - a Python for microcontrollers. 3-5 minutes

- emlearn - TinyML project. 5 minutes
- How to use emlearn with MicroPython. 10 minutes

## Assumed knowledge

Machine Learning core concepts.
Familiarity with scikit-learn.
Classic ML models.

If you do not yet have this, the talk might be a little bit confusing.
But there are plenty of resources online to help fill these gaps.


# Code examples


### Convert

import emlearn

converted = emlearn.convert(estimator)

converted.save(name='gesture', format=’csv’, file='gesture_model.csv')


### Recording data

def write_buffer_csv(buffer, file, rowstride = 3):
    rows = int(len(buffer) / rowstride)

    file.write('x,y,z\n')
    for row in range(0, rows):
        x = buffer[(row*rowstride)+0]
        y = buffer[(row*rowstride)+1]
        z = buffer[(row*rowstride)+2]
        file.write('%.4f,%.4f,%.4f\n' % (x, y, z))

t = isoformat(rtc.datetime())
with open(data_dir + '/acceleration-'+t+'.csv', 'w') as f:
    write_buffer(accel_buffer, f)

### Reading sensor

    # Setup accelerometer
    i2c = SoftI2C(sda=10,scl=11)
    sensor = bma423.BMA423(i2c, addr=0x19)
    sensor.set_accelerometer_freq(50)
    sensor.fifo_enable()
    sensor.fifo_clear()

    # Overlapped window handling
    window_samples = 60
    hop_samples = 20
    assert (window_samples % hop_samples) == 0, 'window must be divisible by hop'
    accel_buffer = bytearray(hop_samples*3*2) # Raw bytes from sensor. 3 axes, 2 bytes per value
    window = array.array('f', list(range(0, window_samples*3))) # Sensor data in g
    window_offset = 0

    while True:


# Check if sufficient new data is available
if sensor.fifo_level() >= len(accel_buffer):

    # Read raw data
    sensor.fifo_read(accel_buffer)
    
    # check if window buffer is full. Shift old data over to make room for more
    if window_offset == window_samples:
        window[0:(window_samples-hop_samples)*3] = window[hop_samples*3:]
        window_offset -= hop_samples

    # Decode sensor data
    decode_acceleration(sensor, accel_buffer, window, window_offset)
    window_offset += hop_samples

    # Preprocess features
    preprocessor.run(window, features)

    # Run model
    out = model.predict(features)


## Loading model

# Instantiate model
# Specifying capacity for trees, decision nodes, classes
model = emltrees.new(20, 200, 10)

# Load model "weights"
with open('gesture_model.csv') as f:
    emltrees.load_model(model, f)


## Training model


# preprocess data
windows = train.groupby(['class', 'sample']).apply(create_windows, length=int(2000/15), hop=int(260/16))
features = windows.groupby(['class', 'sample', 'window']).apply(spectral_features, include_groups=False)

# train model
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

X_train = features
Y_train = features.reset_index()['class']
estimator = RandomForestClassifier(n_estimators=10, max_depth=5)
out = cross_validate(estimator, X_train, Y_train)



# Ideas

### When are C modules needed?
And when can Viper do a good enough job?

Especially on pre-processing, which tends to be custom.
Examples.
- Computing the RMS of vibration/audio signal (chunk)?
- Multiplying by scaler and/or converting data-type
- Copying/slicing an array
Probably depends on length. Maybe also on data-type?
Ideal: As much as possible is doable in Python
Would like to have some benchmarks on this.
Gives performance numbers.
Also a reference to copy from.
And use as starting-point for new calculations.

This is also an open questions for the ML classifiers themselves.
MicroPython general recommendations:
Write it first in Python, then optimize the slow parts.
Although datastructures, overall algorithmic approach may not follow from this approach.
Avoiding frequent allocations.
Also, no reference what is the ballpark of maximal achievable speed.

Depends a bit on how efficient the data shuffling is,
the size of work, and the call overheads for FFI.


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

## Preprocessing strategies

FFT. Energy in bands
IIR filterbank. Energy in bands (per axis).
Statistical time-based summaries. catch22

Projection to 2d. As used in Magic Wand example.

? TODO: provide references to the various types

## Magic wand preprocessing
Project strokes to 2d image

Convert the strokes into rastered images 
https://colab.research.google.com/github/tinyMLx/colabs/blob/master/4-8-11-CustomMagicWand.ipynb#scrollTo=Ml1UYg-oMpQo
Uses fixed point mult/add - interesting

Here is the C++ code
https://github.com/petewarden/magic_wand/blob/main/rasterize_stroke.cpp
Uses a linear array.
Still uses R,G,B ??? Why?


? is this fast enough to run directly as MicroPython
Uses numpy array. But otherwise might be portable

? can RandomForestClassifier to a resonable job at this data

Seems to only record the X and Y coordinates!
Use must make sure to hold it horizontal
Rasterized into 32x32
Training pipeline also has some data augmentation


## Continious gestures example

https://edge-impulse.gitbook.io/docs/tutorials/end-to-end-tutorials/continuous-motion-recognition

Window size. 2000 ms
Window hop. 240 ms

Low pass. Cutoff 8 Hz, 6th order

FFT 64 bin

uses spectral features pre-processing block
https://edge-impulse.gitbook.io/docs/edge-impulse-studio/processing-blocks/spectral-features
- a low or high filter with optional decimation. Butterworth
- statistical features (RMS, skewness, kurtosis)
- automatically removes FFT bins based on the low/high freq settings
- does filter first, then mean subtraction, then statistical features and FFT
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



