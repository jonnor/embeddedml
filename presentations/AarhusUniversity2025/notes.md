
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
- Acting on outputs

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

Pre-requisite knowledge

- Know about microcontrollers
- Know basic C coding
- Know Photon development, hardware/software

Assumed

- Have data/dataset
- Have scikit-learn pipeline
- Have feature extraction
- Have evaluation setup


Later

- Continious classification
- Post-processing
- Test-time augmentation using time-shift and prediction aggregation
- Accelerometer feature preprocessing
- Audio feature preprocessing

Out-of-scope

- How accelerometer FIFO enables power saving
- 

## Disposition presentation 1

Talk intro. 2-5 minutes

- Talk outline
- A TinyML system
- TinyML context - where in the phases and pipeline
- Questions?

emlearn - overview. 2-5 min

- emlearn project introduction
- Model show-down. What/how too choose?
- Relevance "classic" methods in a deep learning world
- emlearn vs other frameworks.
tflite micro. Edge Impulse
- (aside) emlearn-micropython. For ESP32 etc
- Questions?

emlearn - deploy first classification model. 10 min

- scikit-learn pipeline
- Converting the model
- Validate converted model on PC
- Use model on device. C code
- (MAYBE) Validate model on device? Preferably include pre- and post- processing.
- Questions?

emlearn - tuning model performance. 10 min

- Model requirements.
Predictive performance.
Cost (RAM, progmem/FLASH, inference time)
- Practical strategies for. Hard constraints vs optimization target.
- Tradeoffs. Pareto frontier and Pareto optimality
- Random Forest. Model structure, cost-vs-performance, parameters
- Hyperparameter tuning.
- Questions?

emlearn - more/related. 5 min

- Regression
- Anomaly detection
- Pre-processing. FFT, IIR.
But also in CMSIS-DSP et.c.
- Upcoming. File formats. Accelerometer pre-processing. Audio pre-processing
- Questions?

Outro. 2-5 min

- Summary
- emlearn on the Photon. Lab by Morten?
- Documentation, official resources
- Documentation, additional talks
- Questions?


## Slides

## Model performance and constraints

- RAM and FLASH are hard step-wise limits
- Usually need to switch microcontroller/part to upgrade
- But as long as not exeeding limit, no direct cost/downside

- CPU usage also has hard limit if pushing really hard
- If within limits, then there is an energy cost. Matters on battery
- Energy is (all else equal) ~proportional to total prediction time

System costs

- Sensor-readout
- Pre-processing
- Model inference
- Post-processing
- Communication

Entire ML pipeline only a part of total system.
Might need considerable resource for other parts.

Pre-processing / feature extraction may be a large part of model pipeline costs.
Output buffers might be considerable if transmitting in batch for power,
or or intermittent connectivity.

Visuals

- CPU inference.
Timeline, horizontal. Wakeup. Active time. Waiting time.
- FLASH/RAM.
Memory map. Upwards. Like a stacked barchart.
RAM. Data buffers.
FLASH. Code. Constant data.


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



