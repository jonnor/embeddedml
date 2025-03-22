
## Context

## TinyML phases

- Task definition
- Hardware bringup
- Data collection
- Exploratory Data Analysis
- Data annotation/curation
- Model pipeline setup
- Iterating. Model and dataset
- Lab/field testing
- Monitoring in production

emlearn is a model deployment tool.
Convert Python model to efficient C code.
Associated tools for validating the optimized.

## Pipeline

- Data reading/loading
- Pre-processing
- ML model
- Post-processing
- Acting

Convert ML model to optimized version.

## Evaluation

- Train/validation/test
- With/without post-processing.
Instance versus event
- With original model, with 
- On PC versus on-device

## Learning goals

Overall

- Convert a model. From scikit-learn
- Validate a converted model on PC
- Selecting hyper-parameters for performance/costs
- Use model on device
- Validate on-device model

Assumed

- Have data/dataset
- Have scikit-learn pipeline
- Have feature extraction
- Have evaluation setup

Later

- Continious classification
- Post-processing
- Test-time augmentation using time-shift and prediction aggregation


## Brainstorming

### Morten ideas

Cover a bit on

- typical usecases
- why TinyML makes sense
- maybe a bit on how traditional ML differs from / makes sense vs. DeepLearning models, like edgeimpulse tooling (will also be introduced),
- maybe some thoughts on quantization / required dataformats 8/16/32

Anything that makes sense, leading up to some of the hands on labs you have described

### Hardware they have

- Particle Photon 2. 2 MB FLASH, BLE 5.3
- ADXL343 accelerometer (3 axis)
- PDM microphone breakout
- Battery?

## Classroom applications

Any good ideas for classroom suited applications, where data can be collected by students?
Maybe combined with existing datasets ?

For classroom applications, useful if data be collected in controlled experiments
(as opposed to from some natural phenomena of process which one cannot influence).

- Can use their own body. Motion, voice, etc
- Can use objects typically found in or around a building
- Using easily available materials, say from a grocery store. Food etc

Human Activity Recognition is a good starting point.
Fun related application are Gesture Recognition (to maybe trigger some action) and classifying exercises.
Stretch could be to detect and count repetitions.

Electronic nose for food etc could be interesting.
But do not have the sensors for that.

## TinyML use-cases

What makes TinyML interesting / a good fit

- Sensing can be done with little no / without human intervention
- Known to be doable on a large device
- Beneficial to do on a more low-cost device/sensor
Either one-off, or as regular/continious process

- Beneficial to have autonomous system, OR non-expert usage.
Click-a-button

- Sensors are relatively affordable.
Such that processing part is not trivially cheap in comparison.
- Low-power and/or battery operation is beneficial
- Sensors relatively low-power.
Such that their use does not dominate the power budget
- Where power can be saved by transmitting less data (or more seldom)

- Can use cheaper sensors + ML to replace more expensive sensors

IoT sensor.
Transmit immediately if thing detected. Otherwise slow batch, or archival on device
Transmit primarily cases with thing detected. And some non-target for QA. Otherwise archive on device.

## Usecases

Quality control
Non destructive testing
End of line testing
Envuronmental monitorint
Safety
Medical monitoring
Wearables

Fruits,vegetables,food,chocholate
Wine,beer,cider,coffee


## Semi-related

Photon 2 has a file system. POSIX style API. Uses LittleFS under the hood.
https://docs.particle.io/reference/device-os/file-system/
https://docs.particle.io/reference/device-os/api/file-system/file-system-open/

Zephyr scientific library
No support for numpy files?
https://github.com/zephyrproject-rtos/zscilib


.npy file support in C

https://github.com/onai/npio
MIT licensed
Has proper Python dict parser, and dtype parser
Uses file descriptor ints as interface
Allocates internally

https://github.com/oysteijo/npy_array
Seems to work without seek
Quite simple header parsing
Uses FILE API
Supports npz via libzip
Supports mmap for read
Simple usage examples
Provides variadic macros for constructing shape and array info
No support for streaming write?

https://github.com/elgw/npio
MIT
Allocates internally
Uses FILE interface
No support for streaming?


C++
https://github.com/fengwang/cnpypp
https://github.com/cdcseacave/TinyNPY
https://github.com/rogersce/cnpy
https://github.com/llohse/libnpy

## Demo dataset, tabular-ish

Smoke detection
1 Hz
https://www.kaggle.com/datasets/deepcontractor/smoke-detection-dataset
https://www.hackster.io/stefanblattmann/real-time-smoke-detection-with-ai-based-sensor-fusion-1086e6


Alcohols with different structures are used frequently in hygiene products and cosmetics.
It is desirable to classify these alcohols to evaluate their potential harmful effects using less costly methods.
https://www.kaggle.com/datasets/chaozhuang/alcohol-qcm-sensor-dataset

5 types of sensors. QCM3, QCM6, QCM7, QCM10, QCM12
In each sensor, There is alcohol classification of five types
1-octanol, 1-propanol, 2-butanol, 2-propanol, 1-isobutanol


Suitable for on-device learning. KNN may be relevant?

Graphical methods.
bar charts, profiles polar and offset polar plots are

Nearest Neighbor Based Feature Selection for Regression and its Application to Neural Activity
> Our algorithm involves a feature-weighted version of the k-nearest-neighbor algorithm.
leave-one-out mean squared error of the kNN estimator and minimize it using a gradient ascent on an “almost” smooth function.

Regression
https://archive.ics.uci.edu/dataset/186/wine+quality
Ordinal target. quality
Alt: type red/white

pure groundnut oil and various levels of adulteration with palm oil. The data was collected at 128 wavelengths
https://www.kaggle.com/datasets/kishore24/groundnut-oil-adulteration
High dimensionality, otherwise interesting
Ordinal target.
Need to set a threshold for acceptable adulteration

Process quality prediction. time-series. Ideal goal, forecasting
https://www.kaggle.com/datasets/edumagalhaes/quality-prediction-in-a-mining-process


determines the quality of products produced on a roasting machine
https://www.kaggle.com/code/alexkaggle95/production-quality-prediction-mae-6-954

## Electronic nose

Moved to own notes/page under applications.

## Gesture recognition

Mucle activity gesture recognition
https://www.kaggle.com/datasets/kyr7plus/emg-4

## Activity recognition

https://www.kaggle.com/datasets/sezginfurkan/geophone-sensor-dataset

https://www.kaggle.com/datasets/benjamingray44/inertial-data-for-dog-behaviour-classification

## Regression

Water level (regression) from ultrasonic sensor
https://www.kaggle.com/datasets/caetanoranieri/water-level-identification-with-lidar

concrete strength (regression)
https://www.kaggle.com/datasets/arshmankhalid/concrete-strength-dataset

## Discarded

orange vs grapefruit. Color, weight, diameter
!! The dataset is mostly fictional.
https://www.kaggle.com/datasets/joshmcadams/oranges-vs-grapefruit

!! completely random data
https://www.kaggle.com/datasets/adityakadiwal/water-potability/discussion/248871

Real data. But no target
https://www.kaggle.com/datasets/natanaelferran/river-water-parameters

! no targets
https://www.kaggle.com/datasets/syedfahadfazal/industrial-dataset-air-quality-reading


### food quality / preference

Adulteration

Cereals quality
https://www.kaggle.com/datasets/crawford/80-cereals

Apple quality
https://www.kaggle.com/datasets/nelgiriyewithana/apple-quality

Banana quality
https://www.kaggle.com/datasets/l3llff/banana

https://www.kaggle.com/datasets/mrmars1010/banana-quality-dataset

Milk quality
https://www.kaggle.com/datasets/cpluzshrijayan/milkquality

ripeness
https://www.kaggle.com/datasets/juanfelipeheredia/cocoa-ripeness-dataset-tcs-01

## Spectroscopy

spectroscopy
Raman
spectrometer
Chromatography
spectrometry


pure groundnut oil and various levels of adulteration with palm oil. The data was collected at 128 wavelengths
https://www.kaggle.com/datasets/kishore24/groundnut-oil-adulteration

https://www.kaggle.com/datasets/edumisvieramartin/multi-wavelength-for-metal-classification

https://www.kaggle.com/datasets/codina/raman-spectroscopy-of-diabetes

https://www.kaggle.com/datasets/aswatik/choclate-quality-analysis-dataset
! missing target


https://www.kaggle.com/datasets/adolfocobo/libs-potatoes

miniaturized NIR spectrometer to identify cultivars of barley, chickpea and sorghum
https://www.kaggle.com/datasets/fkosmowski/crop-varietal-identification-with-scio

Manuka vs regular honey. Hyperspectral camera
https://www.kaggle.com/datasets/peyushgedela/adulterated-honey-dataset

the classes are strawberry (authentic samples) and non-strawberry (adulterated strawberries and other fruits)
Fourier transform infrared (FTIR) spectroscopy with attenuated total reflectance (ATR) sampling
https://www.kaggle.com/datasets/priyamvada2000/strawberry


## Condition Monitoring

### Keywords

Machine
Predictive mainteinance
Maintenance
HVAC
Bearing
Chiller
Air condition
Motor
Electric motor
industrial
rotating equipment
Pump
Failure
Compressor
Engine


Prognostics
Remaining Useful Life
RUL


## Datasets

https://www.kaggle.com/datasets/aadharshviswanath/aircraft-sensor-and-engine-performance
https://www.kaggle.com/datasets/wkirgsn/electric-motor-temperature
https://www.kaggle.com/datasets/umerrtx/machine-failure-prediction-using-sensor-data
https://www.kaggle.com/datasets/mayank1897/condition-monitoring-of-hydraulic-systems
https://www.kaggle.com/datasets/chillerenergy/chiller-energy-data
https://www.kaggle.com/datasets/uciml/aps-failure-at-scania-trucks-data-set
https://www.kaggle.com/datasets/mayank1897/condition-monitoring-of-hydraulic-systems
https://archive.ics.uci.edu/dataset/791/metropt+3+dataset
Compressor's Air Production Unit (APU)
https://www.kaggle.com/datasets/vinayak123tyagi/milling-data-set-prognostic-data


