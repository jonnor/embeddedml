

## Format

30 minute slot.
20 minutes, 5 minutes QA

## Abstract

- emlearn
key features and development tools that the library provides
demonstrate how one can perform common Machine Learning tasks - classification, regression and anomaly detection
- Use emlearn with Zephyr

## TODO

- Double check disposition
- Set up all existing slides
- Create placeholders for missing slides
- Fill in missing slides

## Disposition

2 min
- intro/TinyML

8 min
- emlearn (C lib)
- emlearn with Zephyr (new)

8 min
- The TinyML language gap (new)
- emlearn-micropython

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
Using a queue etc.



TODO: example code for using Fetch and Get

Accel polling example in Zephyr supports either
https://docs.zephyrproject.org/latest/samples/sensor/accel_polling/README.html
https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/sensor/accel_polling/src/main.c


XIAO NRF52840 sense has a on-board LSM6DSL.
People have resported various problems, but also gotten it to work eventually.
https://devzone.nordicsemi.com/f/nordic-q-a/109732/running-the-lsm6dls-imu-zephyr-example-with-nrf52840-based-xiao-ble-sense

https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/modules/tflite-micro/magic_wand
example of polling combined with a machine learning model


## Zephyr IMU read with Read and Decode

TODO: example code for using Read and Decode

FUTURE: full example for processing IMU/accelerometer data with emlearn

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

Pinetime has BMA421
T-Watch S3 has BMA423.
Might have breakout boards with adxl345, at the office?

Magic wand example also uses adxl345.


