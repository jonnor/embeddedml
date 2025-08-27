
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
- Learn more about Zephyr, practical development
- Attract users to emlearn. Maybe also contributors
- Get emlearn promoted more via Zephyr

## Story arc

Learn How to use machine learning for solving a real-world (custom).
See what pieces we need - with a focus on the device-side and Zephyr.
Completely open-source pipeline.
Task oriented. But not a full step-by-step tutorial.

## Call to Action

- visit me in Speaker Working Hours
- come visit at the Zephyr booth
- Help out in improving the integration / making examples
https://github.com/emlearn/emlearn/issues/108

## Take aways

Running machine learning inference on microcontroller grade is useful in many applications

Zephyr is a good base for TinyML applications
Sensor API, filesystem, connectivity

emlearn makes deploying models simple
Converting scikit-learn or Keras to efficient C code
Easy to use via Zephyr module

Bonus: MicroPython can also be used with Zephyr and emlearn-micropython

#### What we need

A full pipeline that supports

- Inference on device.
- Data collection on device
- Training on PC
- Validation on-device
- Acting on the model outputs.

Steps

- Define task.
Time-series continous classification (HAR).
- Data collection.
Reading sensors. Sensor API
Storing data. CSV. To filesystem. TODO: .npy files
Tranferring data to PC. Serial/USB with mcumgr. Alt: BLE/Networking
- Label data
Point to Label Studio
- Preprocessing
Portable C code.
- Training model
Using scikit-learn. har_trees pipeline
- Deploying model
Converting with emlearn.
Device code to load and run model.
- Validating model
Using a validation set on-device. Read from file
- Doing something with the output
Ex: Transmit over BLE

Bonus

- Unknown/other handling. Classification, AD/outlier, model probabilities
- Regression. HAR extension could be, calorie estimation. Might also want heartbeat etc. Or maybe number of repetitions.
- Post-processing. Median filtering, low-pass. Morphological. Discretization into events. Min/max durations.

Out-of-scope:
- GMM-HMM post-processing.
- Anomaly detection. Temperature in relation to control


## Outline

Introduction
- Applications
- TinyML system diagram overall

- TinyML tasks. Clear definition for each, with example in TinyML setting
Classification, Regression, Anomaly Detection

Activity Reconition task

- Continious classification. HAR
Related like toothbrush, exercise detection, animal activity etc

- Software system diagram. **KEY**
Which components need to be in place. The differences how they are used. ML pipeline as a core.
Runnning inference. Collecting data. Preprocessing during training. Validation.

Sensor data input

- Overlapped windows.
Chunks. Sampling is time-sensitive, but processing not.
- Reading accelerometer in Zephyr with polling sensor thread
ADC. Would follow same thread-based example
- Reading IMU with new fetch and decode API
https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/subsys/rtio/sensor_batch_processing/src/main.c

(- Honorable mention. Zephyr dmic API)

Creating a dataset

- Saving using file system
CSV support in emlearn
- Tranferring to PC via cable. USB/serial
- Wireless options. BLE/Ethernet etc
- Labeling. mention of Label Studio

Training

- preprocessing as portable C, run on PC
- har_trees pipeline

Deploying model

- emlearn convert
- emlearn for C
- emlearn Zephyr module

Validating model

- Validating on PC.
- Load data from filesystem. CSV
Run though entire pipeline. Check outputs

Summarize. Putting it all together

- There are many pieces. But emlearn and Zephyr provides help in all areas
Important to follow best practices to ensure correctness
Reuse preprocessing code.
Use portable code
Test end2end

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

- Add Call to Action slide
- Add Summary slide
- Do a check over all slides, check nothing big missing

## Zephyr code samples

#### Stretch

- Fix overlap/hop handling in sensor readout
- Finish preprocessing script. Fix window/hop handling.
- Setup data collection. Save CSV to file-system. Transfer with USB MSC
- Setup validation using pipeline. CSV file(s) from filesystem. USB MSC
- Get file transfer over serial with mcumgr to work

- Finish toothbrush demo on Zephyr+MicroPython
Inference. Need better LSM6 support.
Fallback: Polling asyncio in MicroPython. 50 Hz is 20 ms.
Alt A: Queues in Zephyr, custom module
Alt B: FIFO in MicroPython

#### Later

- Implement LSM6 with FIFO support in MicroPython
- Add support for XIAO BLE Sense with Zephyr MicroPyhon port in har_trees example
- FFT support in C feature extraction
- .npy support in C

- Gyro sensor fusion. With zscilib? complimentary filter or Magdewick
- Sensor readout for read and decode with RTTI
https://docs.zephyrproject.org/latest/hardware/peripherals/sensor/read_and_decode.html
Can still use a queue, stays compatible
- Test the new video labeling in Label Studio

- soundlevel example for dmic
https://docs.zephyrproject.org/latest/samples/drivers/audio/dmic/README.html#dmic

#### DONE

- Add feature extraction to LSM6
- Add sensor readout with thread
- Improve API for CSV reader in emlearn
- Add API for CSV writer in emlearn


## Learning

? could or should one integrate an ML build step that has code generation into west?

#### How to store and transfer files with Zephyr

Seems mcumgr is a good option?
https://pypi.org/project/smpclient/
There is an SMP server sample. Was unable to get it to run, aborted due to Kconfig warnings
https://docs.zephyrproject.org/latest/samples/subsys/mgmt/mcumgr/smp_svr/README.html#smp-svr-sample-build

USB mass storage with FATFS worked on XIAO
https://docs.zephyrproject.org/latest/samples/subsys/usb/mass/README.html#fat-fs-example


## Dream design for emlearn + Zephyr

Zephyr used for the HAL.
Complete ML pipeline can run in C.
Examples, docs and tools exist for entire life-cycle of ML project,
supporting best practices.

emlearn has feature-extraction / pre-processing transformers,
with integrated support for C code.

emlearn supports for doing on-device model validation and data recording.
Ideally via .npy files. CSV is an OK stop-gap.

Zephyr enables to run entire sensor-applications on right architecture using simulation,
and also execution time estimates, and program/RAM size estimates.

emlearn-micropython also works with Zephyr (same as other MicroPython ports)

MAYBE. Example of how to expose a complete C pipeline to MicroPython application


## File transfer with Zephyr

MCUmgr with Simple Management Protocol (SMP)
https://docs.zephyrproject.org/latest/services/device_mgmt/mcumgr.html
https://docs.zephyrproject.org/latest/samples/subsys/mgmt/mcumgr/smp_svr/README.html#smp-svr

USB Mass storage
https://docs.zephyrproject.org/latest/samples/subsys/usb/mass/README.html



### Zephyr IMU readout

Zephyr has a unified API for sensor data access.
Two flavors of this

- Fetch and Get
- Read and Decode

With Zephyr 4.x+ Read and Decode has become the preferred API generally.
https://docs.zephyrproject.org/latest/hardware/peripherals/sensor/index.html

Fetch and Get API, but not so well suited for medium sample-rates.
Accelerometers/IMUs etc. Common in TinyML.
No support for getting many samples at a time, or sensor FIFOs, or async reading.
In TinyML setting we often need to get N samples before we will process again.
Rolling overlapped windows.

Theoretical strategy:
If you need to use a driver with Fetch and Get, write an adapter that gives async.


XIAO NRF52840 sense has a on-board LSM6DSL.
People have resported various problems, but also gotten it to work eventually.
https://devzone.nordicsemi.com/f/nordic-q-a/109732/running-the-lsm6dls-imu-zephyr-example-with-nrf52840-based-xiao-ble-sense


## Zephyr IMU read with Read and Decode

TODO: example code for using Read and Decode

FUTURE: full example for processing IMU/accelerometer data with emlearn

In Zephyr 4.2, around 18 drivers with read and decode

git grep '\.get_decoder' -- drivers/sensor/

```
drivers/sensor/adi/adxl345/adxl345.c:   .get_decoder = adxl345_get_decoder,
drivers/sensor/adi/adxl362/adxl362.c:   .get_decoder = adxl362_get_decoder,
drivers/sensor/adi/adxl367/adxl367.c:   .get_decoder = adxl367_get_decoder,
drivers/sensor/adi/adxl372/adxl372.c:   .get_decoder = adxl372_get_decoder,
drivers/sensor/asahi_kasei/akm09918c/akm09918c.c:       .get_decoder = akm09918c_get_decoder,
drivers/sensor/bosch/bma4xx/bma4xx.c:   .get_decoder = bma4xx_get_decoder,
drivers/sensor/bosch/bme280/bme280.c:   .get_decoder = bme280_get_decoder,
drivers/sensor/broadcom/afbr_s50/afbr_s50.c:    .get_decoder = afbr_s50_get_decoder,
drivers/sensor/maxim/ds3231/ds3231.c:   .get_decoder = sensor_ds3231_get_decoder,
drivers/sensor/melexis/mlx90394/mlx90394.c:     .get_decoder = mlx90394_get_decoder,
drivers/sensor/memsic/mmc56x3/mmc56x3.c:        .get_decoder = mmc56x3_get_decoder,
drivers/sensor/pixart/paa3905/paa3905.c:        .get_decoder = paa3905_get_decoder,
drivers/sensor/pixart/pat9136/pat9136.c:        .get_decoder = pat9136_get_decoder,
drivers/sensor/pni/rm3100/rm3100.c:     .get_decoder = rm3100_get_decoder,
drivers/sensor/st/lis2dux12/lis2dux12.c:        .get_decoder = lis2dux12_get_decoder,
drivers/sensor/st/lsm6dsv16x/lsm6dsv16x.c:      .get_decoder = lsm6dsv16x_get_decoder,
drivers/sensor/tdk/icm42688/icm42688.c: .get_decoder = icm42688_get_decoder,
drivers/sensor/tdk/icm45686/icm45686.c: .get_decoder = icm45686_get_decoder,
```

In git master per March 2025, around 12 drivers implement.
A few accelerometers, IMUs, magnetometers, humidity/pressure.

git grep '\.get_decoder' -- drivers/sensor/

```
drivers/sensor/adi/adxl345/adxl345.c:   .get_decoder = adxl345_get_decoder,
drivers/sensor/adi/adxl362/adxl362.c:   .get_decoder = adxl362_get_decoder,
drivers/sensor/adi/adxl367/adxl367.c:   .get_decoder = adxl367_get_decoder,
drivers/sensor/adi/adxl372/adxl372.c:   .get_decoder = adxl372_get_decoder,
drivers/sensor/asahi_kasei/akm09918c/akm09918c.c:       .get_decoder = akm09918c_get_decoder,
drivers/sensor/bosch/bma4xx/bma4xx.c:   .get_decoder = bma4xx_get_decoder,
drivers/sensor/bosch/bme280/bme280.c:   .get_decoder = bme280_get_decoder,
drivers/sensor/maxim/ds3231/ds3231.c:   .get_decoder = sensor_ds3231_get_decoder,
drivers/sensor/melexis/mlx90394/mlx90394.c:     .get_decoder = mlx90394_get_decoder,
drivers/sensor/memsic/mmc56x3/mmc56x3.c:        .get_decoder = mmc56x3_get_decoder,
drivers/sensor/st/lsm6dsv16x/lsm6dsv16x.c:      .get_decoder = lsm6dsv16x_get_decoder,
drivers/sensor/tdk/icm42688/icm42688.c: .get_decoder = icm42688_get_decoder,
```

Pinetime has BMA421. https://docs.zephyrproject.org/latest/boards/pine64/pinetime_devkit0/doc/index.html
T-Watch S3 has BMA423. https://docs.zephyrproject.org/latest/boards/lilygo/twatch_s3/doc/index.html
Might have breakout boards with adxl345, at the office?

mmc56x3 magnetometer is also interesting. Have one of those?

Magic wand example also uses adxl345.




# Gyro sensor fusion

zscilib implements complimentary filter and Magdewick, etc
There is some example code
https://github.com/zephyrproject-rtos/zscilib/blob/master/samples/orientation/apitest/src/main.c
But no real-world examples, and no mention in main Zephyr docs?

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

# Unrelated

Machine learning on Zephyr - users experience?
https://lists.zephyrproject.org/g/users/topic/machine_learning_on_zephyr/112897072


