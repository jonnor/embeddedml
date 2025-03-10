

## Format

30 minute slot.
Full 25-30 minutes can be used.
QA will be done together at end of session, 15 minutes.


## Abstract

- emlearn
key features and development tools that the library provides
demonstrate how one can perform common Machine Learning tasks - classification, regression and anomaly detection
- Use emlearn with Zephyr

## TODO

- Create placeholders for missing slides
- Fill in missing slides
- Add some recommended talks at Zephyr conf?

## Disposition

Maximum. 30 slides 

2 min
- intro/TinyML

10 min
- emlearn (C lib)
- emlearn use-cases
- emlearn with Zephyr (new)

10 min

- The TinyML language gap (new)
- emlearn-micropython
- Examples with MicroPython

2 min
- outro


## Call to Action

- Check out the emlearn C library
- Try out MicroPython!
- Try out emlearn-micropython

## Cross-linking

- Zephyr
- Continious Integration for fw/embedded.
Host-based testing
- Other Edge AI

## Take aways

- Re
- It is feasible to run (MicroPython) on device
- MicroPython with C modules enables a portable and efficient ML pipeline
- Running the same pipeline on host

- Is possible to build TinyML applications using just Python. By leaning on existing bindings

## Talking points

- emlearn project, C library
- Runs anywhere C does. Zephyr, Arduino etc
- OpenMV
- ulab
- emlearn-micropython
- MicroPython, runs on microcontrollers. Also Zephyr support
- Excellent support for C modules. Allows combining C with Python, as needed

## Slides outline

- Cover
- 


### Bridging the TinyML language gap

Overall story-arc

- TinyML system requires combining embedded systems with Machine Learning.
- Two specialization with their own established languages:
C on the embedded device (for the firmware), and Python on the PC (for Machine Learning / Data Science).
- Cause challenges in a project in quality assurance, execution speed and staffing.
- One strategy to reduce this friction, is utilize Python also on the embedded device.


## The TinyML gap - device versus host, train versus predict time

Key chalenge: Maintaining compatibility across

Approaches

- Have two separate implementations of pipeline steps
- Implement everything in (portable / embedded-friendly) C
- Implement everything in (portable / embedded-friendly) Python
- Mix C and MicroPython. C for computationally intensive, Python
- (Reuse standard components where possible)

Simplified pipeline

- Pre-processing
- ML model
- Post-processing.

Pre-processing can include

- Format conversions
- Data normalization
- Feature extraction

Post-processing

- Aggregation of predictions
- Filtering
- Decision logic


## MicroPython Data Science ecosystem

Need 

- Filesystem - super useful. Data transfer etc
- File format support. Depends
- Numeric computing.
- Machine Learning
- Feature pre-processing

For practical sensors,

- Sensor drivers
- Connectivity
- Low power support



Are we Data Science yet?
Have some notes on this in emlearn-micropython.


## emlearn module for Zephyr

TODO: describe how to use emlearn

https://emlearn.readthedocs.io/en/latest/getting_started_zephyr.html

## Zephyr sensor readout.

- Audio input. Digital mic (dmic), or I2S codec
- Camera. Video API
- IMU/accelerometer/gyro. Sensor API
- Other. Sensor API, or custom


