

## Practical examples for emlearn on Zephyr

Issue: https://github.com/emlearn/emlearn/issues/108

Some rough notes below.

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

Magic wand example also uses adxl345.


# Zephyr sensor readout example case

Moved to
https://github.com/emlearn/emlearn/issues/108

### Existing practice

Accel polling example in Zephyr
https://docs.zephyrproject.org/latest/samples/sensor/accel_polling/README.html
https://github.com/zephyrproject-rtos/zephyr/blob/main/samples/sensor/accel_polling/src/main.c
Supports both API styles
Does polling in the main function

Nordic NCS sensor manager
Support LIS2DH
https://docs.nordicsemi.com/bundle/ncs-2.9.0/page/nrf/libraries/caf/sensor_manager.html#caf-sensor-manager
? how does application get the data
focused on sensor sleeping on triggers

https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/modules/tflite-micro/magic_wand
example of polling combined with a machine learning model.
! seems to not read continiously. But instead reads a burst, then processes it, then continues reading.

### Design criteria

- Consumer can get data from a message queue. Using a low-priority queue
- Dedicated thread (higher priority) used internally to sample the data
- Parameters fixed at compile time (not runtime changable): samplerate/hop/window/channels etc
- Rather easy to set up. By default hide internal aspects
- Allow static allocated memory
- Support multiple instances. With different parameters.
Means the output buffer sizes can differ. So messages have to pass pointers/copies?
Might imply limiting queue length to 1 initially?
- Work with fetch & get sensors
- (later) Support decode API sensors
- Work with 3-axis accelerometer
- (later) Support 3-axis magnetometer, 6-axis, 9 axis IMU

## Considerations

- Can sensor setup be done outside the thread?
Yes.

- Can we provide a macro that does all the neccesary setup, like what thread etc

- Can we have a unified API for decoded and fetch cases?
fetch does not support raw values.
Would have to be sensor_value based, or something derived from it.
The primary interaction point would be a queue with data.
If messages are the same/similar, that would maybe be sufficient?
Most important that rest of the code - preprocessing etc, is independent.

- What would we pass on?
float * is an option.
I guess it would be sensor_value for now...
Or back-tranlate to int16

- Raw data only feasible with new decode API
Could be a separate implementation?
Following same conventions?

- How does this relate to Digital Mic and Video cases?
dmic API is already a chunk based.
Is smilar in that regard. But not using thread/queue.

- How does this relate to ADC cases?
ADC also seems to be quite low-level
Primarily single-sample oriented.
Would use fetch approach with thread.



