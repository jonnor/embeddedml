
## Human Activity Detection using accelerometer and tree-based ML models 

It seems that our project will have a 32-bit microcontroller
with around 4 kB RAM and 32 kB FLASH (such as the Puya PY32F003x6).
This sets the contraints that our entire firmware needs to fit inside.
The firmware needs to collect data from the sensors, process the sensor data, run the Machine Learning model, and then transmit (or store) the output data.

The input buffers, intermediate buffers, tends to take up a considerable amount of RAM.
Therefore we must consider them carefully to establish an appropriate tradeoff between sampling rate, precision (bit width) and length (in time).


TABLE: RAM utilization versus samplerate,bitwidth,duration

Accelerometer data used in this manner tends to be sampled at relatively low sample rates,
for example 100 Hz.
However there needs to be.
Furthermore the input data from a tri-axial accelerometer has 3 channels, and often comes in 16-bit resolution. 



Constraints
Under 50% of RAM and FLASH for ML model
2 kB of RAM and 16 kB FLASH
Preferably would like to be closer to 25%, ie 1 kB RAM and 8 kB FLASH

Task
Human Activity Detection

Have a wide range of applications.
Medical, health, exercise, elderly care etc
Not just human activities, also animals
Wrist mounted device. Smart watch. Fitness bracelet etc.

Sample rates of around 100 Hz

How to realize
Feature computations

IMAGE: feature extraction illustrated


Decision tree ensemble
TODO: Estimate model size for Cortex M0+ with emlearn using integers



IMAGE: decision tree forest



## References

### Are Microcontrollers Ready for Deep Learning-Based Human Activity Recognition?
https://www.mdpi.com/2079-9292/10/21/2640

Just 9 features
max_depth 9.
Used 10-100 trees. After 50 trees, marginal improvements in F1 score
! did not try different depth limits based on trees.
Possible that smaller amount of trees could have performed better with more regularization
! used floating point, not integers

At 10 trees, used 10kB FLASH for model.
At 100 trees, used nearly 100 kB FLASH
50 trees appear to be around 50 kB FLAH
! Not clear if feature compute code size is counted.

According to benchmarks in emlearn,
when using integers the code size for model is approximately halved.
Would be 25 kB instead of 50 kB.
A forest with average tree depth of 7.78 and 50 trees took under 11 kB with uint8_t on Cortex-M0

Tested 128 and 256 samples window size
1.5kB or 3.0 kB for triaxial int16 data
!! a bit high for our RAM
Can we go down to 8 bit? Potentially applying some non-linear compression, like pow

Running on NRF5340
Inference time of approx 1ms
9 features selected

Experiemental setup is well described, and sensible.
Subject-based cross evaluation. Wrist accelerometer only

Their feature selection code is at
https://github.com/atiselsts/feature-group-selection

The experimental code _might_ be at
https://github.com/atiselsts/feature-on-board-activities/blob/main/rf/ml_state.py

Some odd remapping of classes, into 12 classes total?
https://github.com/atiselsts/feature-on-board-activities/blob/main/cnn/datasets.py#L54





