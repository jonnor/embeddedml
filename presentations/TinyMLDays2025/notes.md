
# TinyML Days 2025 Aarhus

https://events.au.dk/tinymldays/conference

10.30 - 12.30: Workshop 1:  EM Learn - Jon Nordby, SoundSensing

## Format

## TODO

Now

- Advertise the event on Discord. EDGE AI, 
- Advertise the event on LinkedIn
- Test the various tooling options.
Local-first with Thonny
- Test micropython binary on Windows with WSL. Incl emlearn-micropython modules
- Test micropython binary on common Linux, like Ubuntu 22.04 / 24.04 / 25.04
- Test micropython binary on common Mac OS
- Finalize workshop design


Prep before event

- HAR. Fix bugs found by mastensg
- HAR. Support dataset definitions as a file
- HAR. Add frequency/FFT features
- HAR. Add mpremote to dependencies
- HAR. Lock dependencies ?
- HAR. Add automated test on Github
- HAR. Maybe load dataset info from .json file ?
- HAR. Add automatic download of PC micropython
- Send out instructions for setup
- Do a trial run of workshop at Bitraf
- Test instructions on Windows/Mac/Linux
- Create slides for things to be explained

Maybe

- Make emlearn install not require a C/C++ compiler.
Drop the C++ modules at package time.
So that we do not need it for emlearn-micropython.
Enable IIR and melspec via subprocess communication, npy files

Future

- MicroPython (Unix) installable via pip, using manylinux wheels
- Use MTP or similar to get USB drive type functions for sharing code without special tools

Key

- emlearn-micropython not built for, or tested, on Windows or Mac
Linux binary should work on WSL 2.
Try building micropython extmod for Mac OS
? Do not support Mac OS in the workshop ?

## Goals

At the end of the workshop, each of the participants shall:

Must

- Have setup a functioning emlearn and MicroPython development environment on computer
- Have deployed a model onto device. M5StickC
- Understand the "Activity Recognition" usecase(s)
- Understand how continious classification works.
Pipeline (pre, model, post).
Prediction form. Window splitting. Relation/Difference to event detection, sequence modelling.
Data/labeling requirements/setup
- Understand what TinyML is, what it is used for, benefits/drawbacks
- Understand what emlearn project is, what it can do/not
- Understand basics of what MicroPython is, what it can do/not

Maybe

- Adapted the example code to do something different with prediction outputs
- Have collected their own data, trained and deploying a model
- Understand key elements of data collection and curation. Factors, out-of-distribution, labeling, cleaning
- Have an overview of the parts and process to making a production-grade model?

Bonus

- Understand model optimization and tradeoffs

Out-of-scope

- Other sensor modalities. Audio/image.
Participants can follow examples on their own.
Link to emlearn-micropython code examples


Possibly confusing things

- There are 3 Python versions at play
CPython on host
MicroPython on PC
MicroPython on device

## Learning goals wrt real-world-models
Wrt activity detection as the example task.

System maturity ladder

- A PoC shows how a model could work
- Prototype 1 works in the happy path. Anything outside ignored.
- Prototype 2 works in typical cases. Edge cases ignored.
- Production 1. Common edge cases also work well.
- Production 2. Vast majority of edge cases work well. Also handles intentional misuse/abuse

In workshop mostly talking about the first levels.

## Challenges of real-world sensor data

- Multi-modal. Often many ways of doing "the same thing"
- Person-dependent.
Different people do things slightly (or completely) different.
Same action may have different data.
Same data might come from different action. Ie what constitutes "running" vs "jogging", for someone young vs old
- Context-dependent. Showing for demonstration vs doing it for real
- Ambigious. Might be hard to deliminate



## Learning areas

- Evaluation
- Data collection
- Data labeling
- Data curation/cleaning

- Tune RF model size
- Identify potentially useful features. Explainable
- Select suitable time-resolution
- Select effective features
- Identifying/handling out-of-distribution data
- Pre label data
- Label activity data from video using Label Studio
- Post-processing techniques

What are sources of variation?

- Diff orientation
- Diff frequency
- Diff intensity

Which aspects of the are characteristic of the action?
Which are fundamental? Which are informative but not fundamental?
Which are irrelevant? 


Explainable features for activity recognition

- Is motion primarily in 1, 2 or 3 dimensions?
- Which direction is motion, relative to orientation? Relative to gravity?


## Accelerometers / Inertial Motion Units

- Low cost. 0.30 USD @ 1k
- Low power. 1-100 uA typical
- Data rates. 1 Hz - 1000 Hz

Wearable devices. Fitness watch, smartwatch, smartphone,
Battery operated.

- 100+ millions units shipped anually

* 3-Axis MEMS Accelerometer
* 6-Axis MEMS IMU (3-Axis Gyro + 3-Axis Accelerometer)
* 9-Axis MEMS IMU (3-Axis Gyro + 3-Axis Accelerometer + 3-Axis Compass):
* 10-axis MEMS IMU, includes barometer


## Data considerations

- Time-series. Multi-variate, 3d
- Sampling rate needs to be selected wrt phenomena of interest
- 

## Challenges with accelerometer-only

- Gravity and motion are coupled - accelerometer values are a mix
- Orientation of device changes gravity vector - dominates the accelerometer values
- Would need gyro (or magnetometer) to separate properly

- Assuming only 3-axis accelerometer.
Making assumption that gravitation is constant, orientation changes slowly or not-so-much, motion changes (relatively) quickly


Orientation assumptions. Might be violated, for example wrist-mounted when running


## Separating gravity

Low-pass filter to estimate gravity vector
? parameters - order and 

## Orientation-independent

Can rotate by the (estimated) gravity vector, to get earth-referenced acceleration

- Vertical
- Horizontal

Note: accelerometer cannot give orientation of the horizontal plane



Smartphone-based activity recognition independent of device orientation and placement (2015)
https://dl.acm.org/doi/10.1002/dac.3010

> The technique is validated using activity recognition experiments with four different orientations of a single tri-axial accelerometer
> placed on the waist of 13 subjects performing a sub-class of activities of daily living.
> A high subject-independent accuracy of 90.42% has been achieved,
> reflecting a significant improvement of 11.74% and 16.58%,
> compared with classification without input transformation and classification with orientation-specific models


Device Orientation Independent Human Activity Recognition Model for Patient Monitoring Based on Triaxial Acceleration (2023)

> highlight the impact of changes in device orientation on a HAR algorithm and the potential of simple wearable sensor data augmentation for tackling this challenge.
> When applying small rotations (<20 degrees), the error of the baseline non-augmented model steeply increased.
> On the contrary, even when considering rotations ranging from 0 to 180 along the frontal axis, our model reached a f1-score of 0.85±0.11 against a baseline model f1-score equal to 0.49±0.12.

## Window stacking

- Concatenate features from consequtive windows 
- Delta and delta-delta (acceleration) features


2021
> Low computational complexity and calculation simplicity make hand-crafted features still a good practice for activity recognition.

## TCN

Temporal Approaches for Human Activity Recognition using Inertial Sensors (2019)
https://ieeexplore.ieee.org/document/9018465

PAMAP2 and OPPORTUNITY.
! not clear if subject independent evaluation
deepConvTCN roughly matched LSTM-FCN and deepConvLSTM


Human Activity Recognition Using Temporal Convolutional Network
On UCI HAR.
Dilated TCN, 93.80 and Encoder-Decoder TCN, 94.60


An Architecture for Human Activity Recognition Using TCN-Bi-LSTM HAR based on Wearable Sensor (2025)
> Propose a Temporal Convolutional Network (TCN) combined with a Bidirectional Long Short-Term Memory (Bi-LSTM) architecture to address the issues of insufficient time-varying feature extraction and gradient explosion caused by too many network layers.
> ..
> UCI-HAR, PAMAP2, and WISDM, achieving significant accuracies of 99.1%, 94.8%, and 98.3%, respectively, outperforming other state-of-the-art architectures.


MSTCN: A multiscale temporal convolutional network for user independent human activity recognition

> Results: The performance of MSTCN is evaluated on UCI and WISDM datasets using a subject independent protocol with no overlapping subjects between the training and testing sets. MSTCN achieves accuracies of 97.42 on UCI and 96.09 on WISDM.

!! Has very large amount of results for UCI-HAR, in Table 6.
Statistical features plus CNN generally did very well


## Features

#### Significant Features for Human Activity Recognition Using Tri-Axial Accelerometers
2022
https://www.mdpi.com/1424-8220/22/19/7482?utm_source=chatgpt.com
References some 

Used 4 datasets

- Wireless Sensor Data Mining Dataset (WISDM)
- Heterogeneity Activity Recognition Dataset (HARDS)
- Smartphone-Based Recognition of Human Activities and Postural Transitions Dataset
- Physical Activity Monitoring for Aging People (PAMAP2)

FFT, Root Mean Square (RMS), mean, autocorrelation and wavelet were among the most significant features for human activity recognition for these two datasets.

On the other hand, when the sampling frequency is raised, features related to signal repeatability, regularity and level of chaos (RQA, Permutation Entropy, Lyapunov exponent), and WPD were shown among the most significant.
This has been shown in the results from the PAMAP2 and HARDS datasets. 


#### Separating Movement and Gravity Components in an Acceleration Signal and Implications for the Assessment of Human Daily Physical Activity
https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0061691

Compared

- Euclidian norm (EN)
- Euclidian norm minus one (ENMO)
- Euclidian norm of the high-pass filtered signals (HFEN)
- HFEN plus Euclidean norm of low-pass filtered signals minus 1 g (HFEN+)

In the human experiments, metrics HFEN and ENMO on hip were most discrepant.
Within- and between-individual explained variance of 0.90 and 0.46, respectively.
ENMO, HFEN and HFEN+ explained 34%, 30% and 36% of the variance in daily PAEE, respectively, compared to 26% for a metric which did not attempt to remove the gravitational component (metric EN).

Gravity Components

If one has a gyro (and/or a compass), sensor fusion is better.

MEMS based IMU for tilting measurement: Comparison of complementary and kalman filter based data fusion
https://www.researchgate.net/profile/Pengfei_Gui/publication/308850497_MEMS_based_IMU_for_tilting_measurement_Comparison_of_complementary_and_kalman_filter_based_data_fusion/links/5a7832450f7e9b41dbd26dfe/MEMS-based-IMU-for-tilting-measurement-Comparison-of-complementary-and-kalman-filter-based-data-fusion.pdf
Gyro+accelerometer

## Activity Recognition using Inertial Motion Units


Many applications.

A large amount of them are relevant for TinyML cases.


- Human Activity Recognition
https://github.com/jonnor/embeddedml/blob/master/applications/human-activity-recognition.md
- Fall Detection
https://github.com/jonnor/embeddedml/blob/master/applications/fall-detection.md

- Animal Activity Recognition.
Pets, livestock, wild animals
https://github.com/jonnor/embeddedml/blob/master/applications/animal-activity-recognition.md

Other IMU TinyML tasks

- Gesture Recognition
https://github.com/jonnor/embeddedml/blob/master/applications/gesture-recognition.md
- Condition Monitoring of Machinery
https://github.com/jonnor/condition-monitoring

Other applications of accelerometers, TinyML potential

- Equipment Usage Monitoring – Track heavy machinery operation for maintenance prediction.
- Structural Health Monitoring – Detect vibrations in buildings or bridges for early signs of damage.
- Vibration-Based Fault Detection – Identify faults in motors or rotating machinery.

- Machine Health Monitoring. Predict failures or maintenance needs in CNC machines, conveyors, or robots based on vibration trends.
- Tool Wear Detection. Monitor cutting or drilling tools by detecting subtle changes in vibration that indicate wear or breakage.
- Process Consistency Validation. Ensure processes like stamping, welding, or packaging are running consistently by detecting irregular motion profiles.


- Package Handling Monitoring – Detect drops, shocks, or mishandling during shipping.
- Appliance Usage Recognition – Classify usage patterns of household devices (e.g., washing machine, refrigerator).



# Ideas

Preparations

- ? Install Thonny. With Python 3.10. Check that it runs
- Download materials for workshop. emlearn-micropython with har_trees
- Open har_trees in Thonny
- Create virtualenv. Create directory in browser, then use Thonny
- Install har_trees requirements. Using Thonny
Alt: Use pip install -r requirements.txt inside
?? which shell


## Things to do with model outputs predictions 

- Send data to computer, do something on the computer.
WiFi MQTT, via broker on Internet
https://test.mosquitto.org/
Receive in Python ?
Receive in Javascript / WebSocket
- Log the data on device.
File system, CSV file etc
- Send data to mobile phone, do something there
MQTT? BLE?
- Indicate to user via LEDs
- Indicate to user via screen

## Fun things to do

- Exercise tracker. Put everyones output on a webpage?

## Dataset building

- Mapping out possible factors
- Generalized performance - dataset splitting
- Estimating required amounts of data
- Error analysis -> identify gaps in data
- Pre-labeling vs post-labeling




