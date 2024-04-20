
# TODO

- Do a test in timing
- Make the slides. Incl image and code samples

## Guidelines

https://embeddedonlineconference.com/blog/Best_Practices_for_Speaking_at_the_Embedded_Online_Conference

- Use their template
- Use the slides with webcam placeholder to designe space for that
- Record your presentation in 1920x1080 resolution.  H.264/MP4 format.
- Use webcam video overlay. For example with OBS
- Also deliver a PDF file for all slides
- Share via Google Drive (or similar)

## Format
5-10 minute

## Audience

Embedded Software Engineers
Maybe some DSP background

## Communication goals

- ML is useful in embedded systems for analyzing sensor data
- emlearn is project that implements classical ML algorithms
- Can deploy models to microcontroller by generating C code
- Supports classification, regression, anomaly detection

Basically 2 minutes on each point. = 8 minutes
2-3 slides per point?

## Outline

ML is useful

- Sensor data analysis
- TinyML concept. Inference on device
- Real-world examples
- Classification, regression, anomaly detection

emlearn project

- Open source. MIT licensed
- Implemented in C99. No dynamic allocations
- Works on any platform. make, cmake, etc.
- Models can be loaded at runtime, OR
- generate "inline" C code for a specific model
- Takes under 2 KB FLASH under 1 kB RAM. Supports the smallest systems. 8 bit micros!
- Implemented with fixed-point mostly. FPU optional

Deploy

EXAMPLE CODE

- Simple classification. Core concepts
- Bit more involved / realistic.
Involving feature pre-processing, and maybe post-processing ?


# Content



## Example C code

```
// Include the generated model code
#include "mynet_model"
// index for the class we are detecting
#define MYNET_SPEECH 1

// Array to hold input data
#define N_FEATURES 6
float features[N_FEATURES];

#define SENSOR_DATA_LENGTH 128
int16_t sensor_data[SENSOR_DATA_LENGTH];

// Inside a continious loop
// main

    // Get data and pre-process it
    read_microphone(sensor_data, SENSOR_DATA_LENGTH);
    preprocess_data(sensor_data, features);

    // Run the model
    const int32_t out = mynet_predict(features, N_FEATURES);

    if (out == MYNET_SPEECH) {
        set_display("speech detected");
    } else {
        set_display("");
    }


```

## Slides

Image explaining TinyML. ML runs on the sensor itself.
NOT sending raw data off to another machine for ML

Image. System block diagram. Sensor data sources in. Communication protocols out. Bitrates in + out.
Maybe also battery at the top or bottom (secondary in importance).

Real-world example.

? explain what classification, regression and anomaly detection are. 1-2 sentences each

More info.
Optimization. Evaluation tools.
Regression. Anomaly Detection.



Probably not

- image showing the kind of models that are in emlearn. KNN, trees, MLP


## Data rates in TinyML

#### Accelerometer / IMU.
16 bit, 3 channels, 100 Hz
0.6 kbit / second

#### Sound
16 bits, 16000 Hz
256 kbit / second

#### Images
640x480, 1 fps
7372 kbit / second

#### LoraWAN
0.3 kbit/s to 50 kbit/s per channel.
51 bytes maximum.
Fair Access Policy Practice. 
payload under 12 bytes
Several minutes between each message

0.0016 kbit/second

#### BLE beacon
27 bytes Manufacturer Specific Data

N x 0.625 msec advertisement interval
Plus 0-10msec advertising delay to avoid collisions
Typical rate every 100ms to 1sec.
27 bytes / second

0.300 kbits/second

#### Modbus RTU (RS485)
250 bytes max application data. 125 x 16 bit registers
Some devices only support 16 words / 32 bytes
Polling rate from master limited by number of devices on bus
100 ms to 1 second could be in practice

32*10*8

2.5 kbit/second


#### I2C
400 kbit/s


## Train scikit-learn

## Train Keras

import keras

model = Sequential([
    Dense(16, input_dim=n_features, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid'),
])
model.compile(....)

model.fit(X_train, Y_train, epochs=1, batch_size=10)

## Train scikit-learn

from sklearn.ensemble import RandomForestClassifier
estimator = RandomForestClassifier(n_estimators=10, max_depth=10)

from sklearn.neural_network import MLPClassifier
estimator = MLPClassifier(hidden_layer_sizes=(100,50,25))

estimator.fit(X_train, Y_train)


## Convert to C code




## Random

### Cattle behavior

Data from neck acceleration tags for training cow's feeding behavior classifier
https://zenodo.org/records/6784671

Japanese Black Beef Cow Behavior Classification Dataset
https://zenodo.org/records/5399259

Precision Beef - Animal Behaviour Classification
https://zenodo.org/records/4064802

## Examples

Low rate signals. Audio. Image. Radar.

Battery condition monitoring

Novelty detection. Send more frequently when anomalies or change happens.

Motor control?

Gesture recognition. Human Interfaces

New sensors. More a research topic.

## Abstract promises

- TinyML enabling new applications
- Examples relevant to embedded systems
- Python-based workflow
- Demonstrate classification, regression, AD

## Scope

Keep to the "deploy to microcontroller" phase
Assume that dataset has been collected.
Have some setup for model development in Python.

Focus on classical ML.
Feature Engineering / preprocessing + model.

Out-of-scope

- Data collection / design of experiments
- Monitoring while deployed
- Neural networks


