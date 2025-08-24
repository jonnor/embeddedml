
# Speaker office hours

Machine Learning for sensor-data analysis.
Especially on microcontroller-grade systems, but also on larger embedded systems (Linux),
or on desktop/server.

technical guidance, best practices

# Talk

## Format

40 minute slot.
30 minutes + QA.

30-45 slides total

## Goals

- Make emlearn for Zephyr and C better
- Learn more about Zephyr
- Attract users of emlearn. Maybe also contributors

## Call to Action

- visit me in Speaker Working Hours
- come visit at the Zephyr booth
- ? try out the samples
- ? check out the MR

## Take aways

- Running machine learning inference on microcontroller grade is useful in many applications
- Zephyr is a good base for TinyML applications. Sensor API, connectivity
- emlearn for scikit-learn or Keras to efficient C code
- emlearn can be used together with Zephyr via the C library/module


## Outline

- Applications
- TinyML system diagram overall

- ML tasks. Clear definition for each, with example in TinyML setting
Classification, Regression, Anomaly Detection

- emlearn overview
- emlearn for C

- Worked example. Anomaly Detection, low-dimensionality. Sensor API. GMM ?
Ex two temperature sensors, or control signal and power or temperature

- Software system diagram


- Worked example, continious classification
- Zephyr API audio. dmic?

- Zephyr APIs for sensor data
New fetch and decode API

- Recording data ?

- Labeling of data ?

MicroPython+Zephyr+emlearn
Quite short, say 3-4 slides
- MicroPython for Zephyr
- emlearn with MicroPython


## Audience considerations 

Assuming most will be firmware engineers / embedded software engineers.
Not ML engineers / data scientists. Probably have less exposure to machine learning.
Might have some digital signal processing exposure.

Expect that people have familiarity with Zephyr, C programming.

Expect them to be more interested in C development compared to (Micro)Python
! keep focus on C + Zephyr
MicroPython mentioned only briefly

! need to define relevant ML terms simply and clearly
? focus on Classification
Supervised learning


## TODO

- Create outline
- Import all reference slides from existing presentations
- Add placeholders for planned slides
- Fill inn all missing slides

- Complete Zephyr C code samples

#### Maybe

- Sample code for sensor data readout with Zephyr, on XIAO BLE Sense
Accelerometer/dyro readout
https://docs.zephyrproject.org/latest/samples/sensor/lsm6dsl/README.html
Alternatively dmic soundlevel example
https://docs.zephyrproject.org/latest/samples/drivers/audio/dmic/README.html#dmic

- ? feature extraction pipeline for accelerometer in C
Foremost toothbrush grade
Stretch: FFT etc
Take raw sensor data buffers, returns features
Wrap as MicroPython module? Integrate into har_trees that way?

- ? demo of toothbrush application on Zephyr+MicroPython
Inference foremost
Need LSM6 support. Queues in Zephyr would be preferred.
Fallback: FIFO in MicroPython

- ? test the new video labeling in Label Studio?

#### Later

- ? add XIAO BLE with Zephyr support to har_trees
Need LSM6 with FIFO support

## Learning

? could or should one integrate an ML build step that has code generation into west?

## Dream design for emlearn + Zephyr

Zephyr used for the HAL
Complete ML pipeline can run in C
Nice tools to make this clear and supporting best practices

emlearn has feature-extraction / pre-processing transformers,
with integrated support for C code

emlearn supports for doing on-device model validation and data recording,
via .npy files

Zephyr enables to run entire sensor-applications on right architecture using simulation,
and also compute/size estimates

emlearn-micropython also works with Zephyr (same as other MicroPython ports)

MAYBE. Example of how to expose a complete C pipeline to MicroPython application


## File transfer with Zephyr

MCUmgr with Simple Management Protocol (SMP)
https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html
https://docs.zephyrproject.org/latest/samples/subsys/mgmt/mcumgr/smp_svr/README.html#smp-svr

USB Mass storage
https://docs.zephyrproject.org/latest/samples/subsys/usb/mass/README.html



# Color detection of candy

## Sensors

APDS-9960.
RGB and Gesture Sensor
https://docs.zephyrproject.org/latest/samples/sensor/apds9960/README.html
https://www.sparkfun.com/sparkfun-rgb-and-gesture-sensor-apds-9960.html

## Datasets
Images of packs of skittles, sorted by color
https://github.com/possibly-wrong/skittles
468 packs
Images are 1024×768 pixels.
Quite realistic data.
Seems to be taken with phone/camera, semi-poor conditions.
Seems quite consistent between each shot.
Can probably use horizontal location in image as class label base.

Also has whitespace / non-sample data.
Relevant for a conveyer/sorting application.
Could emulate a single color sensor,
by taking random samples of a


https://universe.roboflow.com/marek-wawrzyniak-taqvz/skittles_recognition/browse?queryText=&pageSize=50&startingIndex=0&browseQuery=true
Seems to have ground truth bounding boxes
40 images, random distribution of skittles


## Sorting devices

https://github.com/majd-kontar/M-M-and-Coin-Sorting-Machine
RPi camera, two belts.

## IVC Sorting Machine - Skittles and M&M's
https://www.youtube.com/watch?v=H7HTQai7Wwg
https://beta.ivc.no/wiki/index.php/Skittles_M%26M%27s_Sorting_Machine


Will sort an entire 1.5kg/56oz bag in approx. 5 minutes.
It is made of an AVR microcontroller (Arduino Uno), color sensor, distance sensor, servo actuators, plastic frame tubes and a few custom 3D printed parts.

## Arduino-MM-Color-Sorter
https://www.instructables.com/Arduino-MM-Color-Sorter/
https://hackaday.com/2021/06/20/compact-mm-sorter-goes-anywhere/

Very compact


## Pennings

https://willempennings.nl/mms-and-skittles-sorting-machine/
Similar to IVC. Uses stepper instead of servo.
Added lights to show the color, and which is being dispensed.

## High speed sorting machine

https://www.reviewmylife.co.uk/blog/2014/12/22/high-speed-mandm-sorting-machine/
Lets the MMs fall by gravity, and have multiple servos that shift them


