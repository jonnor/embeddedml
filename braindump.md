
# emlearn
    
## Compared to sklearn-porter

    Only support C language
    Uses float instead of doubles
    Support for integer-math only
    No dynamic allocations


## Wishlist
Demos:
    Audio Event Detection. MicroPopcorn popping detector->turn off & notify.
    Gesture recognition capacitive sensor arrays. Sign language? Humidity sensor? Detect fluid type? Water vs saltwater vs coke vs juice?
    Human activity recognition accerelometer.
    Gesture recognition accelerometer.
    Wakeword/keyword spotting audio.
    Voice command/control audio.
    Object recognition image.
    Anomaly detection. Isolation Forest.
    Gaussian Mixture Model+Hidden Markov Model. Viterbi algorithm. Especially for sequences.

Feed-Forward Support Vector Machine Without Multipliers
https://ieeexplore.ieee.org/abstract/document/1687940
Fixed-point arithmetic, using only shift and add operations.
Maintains good classification performance respect to the conventional Gaussian kernel.

### Capacity modelling tools

Purpose: Check if a proposed model fits within contraints.
Model storage, memory usage, inference time, CPU "utilization"
Allow to declare budgets, function for checking if over?

Device benchmark:

eml_bench_device
    multiply_adds/second,
    convolutions_3x3/second
    node_evaluations/second (trees)
    ffts/second (melspec)

    Average, standard deviation, 75%, 95%

Ran for each supported hardware. Publish numbers

Perf modelling.
 
    takes perf constants from benchmark
    + ML model 
    => estimate model size, mem use, inference time 

Model benchmark

    Test the real model.
    Verify against Perf model.
    Do this for a set of example models, publish numbers


Models:

    Generic linear model. SVC,LogisticRegression
    Kernel. SVM

On-line DSP tools:

    Streaming summarizers/estimators. min/max, mean/std, median
    Reservoir sampling.
    Voice Activity Detection
    Sound level. Incl IEC A-weighting

Transformers:

    Scalers: Standard,MinMax
    Dimensionality: PCA,NMF

Perf:

    8/16bit weights. NNs
    Integer-math only for compiled trees. 32bit/8bit
    Support sparse models. Autoreduce during conversion?
    Sparse dictionary representations

Advanced stuffs

    Audio beamforming.


# Application ideas

## Anomaly detection in 3d-printing

Consumer grade machines should just work, be safe in operation and guide user to do the right thing.
Also very price sensitive and mostly sold as a standalone appliance, makes microcontrollers attractive.

Sensors:

* Accelerometer on toolhead.
* High-speed current sensing of motors.
* Microphone
* Should one have tachometer on fan(s), so one can eliminate them more easily?

### Function

that can be implemented with sensors and machine learning

Detect malfuctions

* Print loose from bed, printing into thin air
* Warping, print lifts up on one side and starts pushing more on part
* Bottom layer too close to bed, usually leaves.
* Oozing or other source has left blob in model.
* Other unexpected obstruction of the toolhead, like a human hand
* Skipped steps

Detect wear/maintenance need

* Insufficient lubrication of linear bearings
* Timing belt slop/backlash. Might need to know the gcode/pathplanning
* Fan bearings worn out. Usually vibrates more and makes noise

Cost saving

* Sensors can maybe replace need for physical endstops for XY
* Sensors can maybe be used for probing Z level/bed

## Misc

* Detect machine start/stop/running. Dishwasher, CNC. Accelerometer/microphone
* Detect door open/close. Accelerometer/microphone
* Detect speech present/not. Microphone
* Detect a hand gesture. Accelerometer
* Detect a spoken command. Microphone
* Detect/Estimate room occupancy. Accelerometer,microphone,PIR

## Hackerspace indoor monitor
Build and deploy in IoT hackathons

Sensor node

* Temperature, Humidity. DHT22
* PM2.5, PM10. SDS011
* Sound level. ?

Status display/sign

* Air mufflers: Lit if sound too high
/ Dust mask: Lit if finedust too high 
