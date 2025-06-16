
# TinyML Days 2025 Aarhus

https://events.au.dk/tinymldays/conference

10.00 - 12.30: Workshop 1:  EM Learn - Jon Nordby, SoundSensing

## Format

## Exercises

- Train on existing dataset
- Deploy and run this model on device. Check that it behaves as expected in basic cases
- Can you trick this model? What weaknesses have you identified?
- Collecting data to make a better model. Train, deploy, test.
- Make a model for your own usecase
- Bonus. Do something different with the model predictions?

### Post-mortem

Everyone had programmed some Python before.
Few had experience with Machine Learning.

Took over 2 hours to get everyone up and running.
Limited the amount of time to teach/learn.

Good that little time was spent on talking.
Had around 4-5 minor bugs in setup. 3 fixed in the workshop.
Had around 3-4 minor issues in exercise documentation. Fixed in workshop.
Critical to be able to live update slides.
Several had trouble, due to not following instructions correctly. Missing commands. Not copying correctly.

Had 2 people have issue without workarounds, locked down Windows machines. Firewall blocked USB forwarding for WSL.
Had around 2 devices with seemingly hardware issues.
Have 2 persons have USB connection issues / semi unreliable.

Learnings

- ARM Macs. Must use a newer Python than system/default. Otherwise fail to install wheels
- Windows. How to activate virtualenv on Powershell / cmd.exe
- Windows. Must tick "add to PATH" when installing new Python

Positive findings

- USB serial drivers were not needed, it seems


## Follow-ups

Fixes

- HAR. Fix sampling of testdata. Must handle under n=10 samples for a class. Warn instead
- HAR. Gives an obscure exception if only 1 class. Fail with nicer
- Exercises. Add virtualenv activation for cmd.exe/Powershell
- Exercises. Show mpflash command on flashing page

Maybe

- HAR. Add a record time counter to har_record.py
- HAR. Add free/used filesystem counter? If fast enough
- ??HAR. Fix program not starting when not plugged into USB

Bonus

- Links to MicroPython examples for own exercise

Future

- HAR. Add some visualizations for the classes, from train
- HAR. Lock dependencies ?
- HAR. Add automated test on Github
- HAR. Automatic download of npyfile.py instead of checking into repo
- HAR. Add frequency/FFT features
- HAR. Allow switching Python version used for precompute
- HAR. Add automatic download of PC micropython
- MicroPython (Unix) installable via pip, using manylinux wheels. Maybe RFC


#### Slides

- Organization / structure
Work together in pairs
Who here has which OS?

- ! how to reset / power on/off device
- ! how to exit in mpremote. c X c C

## Done

- HAR. Support dataset definitions as a YAML file
- HAR. Maybe load dataset info from .json file ?
- Make emlearn install not require a C/C++ compiler.
- Test flashing with mpflash
FAILED https://github.com/Josverl/mpflash/issues/28


## Wierd after power

(venv) [jon@jon-thinkpad har_trees]$ mpremote reset && mpremote run har_live.py 
b"s Ju<\x80\x00\x00\x00R\xd5\xb1\x812\x01:\x00\xa6\x12\x19\x16\xc4{\x82>\x18\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00Y\xd7dt\xf3`ts\xe0`ts \xca@ts Ju\xfc\x00\xd7\x81Jul 29 20\x00'\x93SH\xa8HH\xcd\xd1\xe90x\xaa\xca\xea%UM\x15Q\xa5,bo\x0fB\x9aA%}\x19\x05MQ}\x191\x05\r\xa5\r\nconfigsip: \x02\xa2\x92b\x02\x9aA%]A\xe90xe\x05drv:0x00,q_drv:}\x91\xc9\xd9\xe90x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00\r\nmode:DIO, clock div:2\r\nload:0x3fff0030,len:4892\r\nho 0 tail 12 room 4\r\nload:0x40078000,len:14896\r\nload:0x40080400,len:4\r\nload:0x40080404,len:3372\r\nentry 0x400805b0\r\nM5Stack StickC Plus2 Shake Detector\r\nShake the device to flash the LED!\r\nIMU initialized successfully\r\nTesting LED...\r\nReady! Shake the device...\r\nShake detected! Flashing LED...\r\nShake detected! Flashing LED...\r\n"
Traceback (most recent call last):

### Installing deps

mpremote mip install \
    https://emlearn.github.io/emlearn-micropython/builds/master/xtensawin_6.3/emlearn_trees.mpy \
    github:jonnor/micropython-npyfile \
	github:jonnor/micropython-zipfile \
    github:jonnor/micropython-mpu6886 \
    github:peterhinch/micropython-nano-gui/drivers/st7789 \
	github:peterhinch/micropython-nano-gui \
	github:peterhinch/micropython-async/v3/primitives


## Toothbrush timer

https://www.youtube.com/shorts/U8TeewQ9t-k


https://www.youtube.com/watch?v=KkrfKPlnoZQ


## Custom data exercise

(venv) [jon@jon-thinkpad har_trees]$ mpremote cp cgestures.trees.csv cgestures.meta.json :


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
- Understand key elements of data collection and curation.
Factors, out-of-distribution, labeling, cleaning

Bonus

- Understand model optimization and tradeoffs

Out-of-scope

- Other sensor modalities. Audio/image.
Participants can follow examples on their own.
Link to emlearn-micropython code examples
- Have an overview of the parts and process to making a production-grade model?

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

Anguita et al (2013)

> The gravitational force is assumed to have only low frequency components,
> found from the experiments that 0.3 Hz was an optimal corner frequency for a constant gravity signal.

? also 3rd order 

https://www.nature.com/articles/s41597-024-03951-4
Uses 3rd order

## Sampling rate

Anguita et al (2013)

> These signals were pre-processed for noise reduction
> with a median filter and a 3rd order low-pass Butterworth
> with 20 Hz cutoff frequency
> sufficient for body motion since 99% of its energy is contained below 15Hz


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


## Follow-up content/presentations

- Human Activity Recoginition
- Explainable features for HAR
- Feature selection for tiny HAR
- Building ML datasets (for HAR)
- Error analysis / dataset vs model diagnostics
- Annotating HAR data using video groundthruth (Label Studio)
- Handling unseen sensor data in ML classification

Tooling

- Annotation helpers for HAR
Segmentation using Matrix Profile


## Features

These should have examples in emlearn

- Gravity separation using IIR filter
- Spectral data, using FFT
- Signal Magnitude Area (SMA).
- Spectral entropy
- Spectrogram using FFT, for deep learning models

Time-domain features for distinguishing static vs. dynamic activities

Explainable features for activity recognition

- Is motion primarily in 1, 2 or 3 dimensions?
- Which direction is motion, relative to orientation? Relative to gravity?


Fig. 2. Power spectral density (PSD) and median frequency for the Z-axis data for walking and running
median frequency was calculated from power spectral density (PSD) of Z-axis

Elliptical IIR High Pass filter (HPF) of seventh order with 0.5 Hz cutoff frequency
was used to separate the bodily accelerations from the gravity accelerations.


#### A benchmark for domain adaptation and generalization in smartphone-based human activity recognition
https://www.nature.com/articles/s41597-024-03951-4
November 2024

> AGHAR benchmark, a curated collection of datasets for domain adaptation and generalization studies in smartphone-based HAR

> We standardized six datasets in terms of accelerometer units, sampling rate, gravity component, activity labels, user partitioning, and time window size, removing trivial biases while preserving intrinsic differences

Dataset: https://zenodo.org/records/11992126
Ku-HAR, MotionSense, RealWorld, UCI-HAR, WISDM
https://github.com/H-IAAC/DAGHAR

Table 5 Performance of models using baseline view.
!! no feature extraction is done

Random Forest using frequency data just a few percentage points behind deep learning models

! KNN in frequency domains did very good (but bad in time)

60 time-steps at 20 hz, 3 second windows (non-overlapping)


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

Human Activity Recognition https://github.com/jonnor/embeddedml/blob/master/applications/human-activity-recognition.md
Fall Detection https://github.com/jonnor/embeddedml/blob/master/applications/fall-detection.md

Animal Activity Recognition. Pets, livestock, wild animals https://github.com/jonnor/embeddedml/blob/master/applications/animal-activity-recognition.md

Other TinyML tasks related to motion / IMUs

- Gesture Recognition https://github.com/jonnor/embeddedml/blob/master/applications/gesture-recognition.md
- Condition Monitoring of Machinery https://github.com/jonnor/condition-monitoring

Other applications of accelerometers, TinyML potential

- Equipment Usage Monitoring – Track heavy machinery operation for maintenance prediction.
- Structural Health Monitoring – Detect vibrations in buildings or bridges for early signs of damage.
- Vibration-Based Fault Detection – Identify faults in motors or rotating machinery.

- Machine Health Monitoring. Predict failures or maintenance needs in CNC machines, conveyors, or robots based on vibration trends.
- Tool Wear Detection. Monitor cutting or drilling tools by detecting subtle changes in vibration that indicate wear or breakage.
- Process Consistency Validation. Ensure processes like stamping, welding, or packaging are running consistently by detecting irregular motion profiles.
- Package Handling Monitoring – Detect drops, shocks, or mishandling during shipping.
- Appliance Usage Recognition – Classify usage patterns of household devices (e.g., washing machine, refrigerator).



## Flashing

https://micropython.org/download/ESP32_GENERIC/

esptool.py --chip esp32 --port /dev/ttyACM0 erase_flash

esptool.py --chip esp32 --port /dev/ttyACM0 --baud 460800 write_flash -z 0x1000 /home/jon/Downloads/ESP32_GENERIC-SPIRAM-20250415-v1.25.0.bin


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


# Make it go wrooom

Higher prediction accuracy.

## CNN

FFT spectrogram -> 2D CNN
Can be implemented with emlearn_cnn

Convolutional Neural Networks for human activity recognition using mobile sensors (2014)

1D CNN can also work OK
https://machinelearningmastery.com/cnn-models-for-human-activity-recognition-time-series-classification/
Got 90.x% - though SVM got 89%


## RNN/LSTM/GRU

Can work OK
https://machinelearningmastery.com/how-to-develop-rnn-models-for-human-activity-recognition-time-series-classification/
Got 90.x% - though SVM got 89%

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

