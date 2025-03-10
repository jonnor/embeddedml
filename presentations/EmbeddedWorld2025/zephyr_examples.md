
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

Pinetime has BMA421
T-Watch S3 has BMA423.
Might have breakout boards with adxl345, at the office?

Magic wand example also uses adxl345.


# Zephyr sensor readout example case

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

## Open questions:

- Can setup be done outside the thread?
- Can we provide a macro that does all the neccesary setup, like what thread etc

- Can we have a unified API for decoded and fetch cases?
Would have to be sensor_value based - fetch does not support raw values

- What would we pass on?
I guess it would be sensor_value for now...
- Raw data only feasible with new decode API
Could be a separate implementation?
Following same conventions?

- How does this relate to Digital Mic and Video cases?

- How does this relate to ADC cases?
ADC also seems to be quite low-level
Primarily single-sample oriented


```C

struct {
    int window_length;
    int hop_length;
    int samplerate;

    sensor_value *read_samples;
    int read_samples_index;

    sensor_value *output_buffer;
    int output_buffer_index;

    int n_channels;
    enum sensor_channel *channels;

    const struct device *dev;
    struct k_msgq *queue;
    struct k_thread *thread;

} sensor_chunk_reader;

struct sensor_chunk_msg {
    int sample_no;
    sensor_value *output_buffer; // n_channels * window_length
}


sensor_chunk_reader_start(sensor_chunk_reader *self) 
{
    // start new thread

    k_tid_t my_tid = k_thread_create(&my_thread_data, my_stack_area,
                                     K_THREAD_STACK_SIZEOF(my_stack_area),
                                     sensor_chunk_reader_task,
                                     self, NULL, NULL,
                                     MY_PRIORITY, 0, K_NO_WAIT);

}


#define SENSOR_CHUNK_READER_MAX_CHANNELS 9

// Designed to be called in a new thread
sensor_chunk_reader_task(sensor_chunk_reader *self)
{
    // verify that sensor is setup. Check ready?

    struct sensor_value values[SENSOR_CHUNK_READER_MAX_CHANNELS];

    // MAYBE: support a way of exiting loop gracefully?
    while (1) {

        // Read data
        // TODO: count failures intead of printing here
	    const int fetch_ret = sensor_sample_fetch(dev);
	    if (fetch_ret < 0) {
		    printk("%s: sensor_sample_fetch() failed: %d\n", dev->name, ret);
		    return ret;
	    }

	    for (size_t i = 0; i < self->n_channels; i++) {
		    const int get_ret = sensor_channel_get(dev, self->channels[i], &values[i]);
		    if (get_ret < 0) {
			    printk("%s: sensor_channel_get(%c) failed: %d\n", dev->name, 'X' + i, ret);
			    return ret;
		    }
	    }

        // Buffer received data
        const int read_offset = (self->read_samples_index*self->n_channels);
        memcpy(read_samples+read_offset)
        
        if (self->read_samples_index == ) {
            // Push onto output buffer

            // Check if output buffer is full
            if () {
                // Send as message
	            int put = k_msgq_put(struct k_msgq *msgq, self->output_buffer, K_NO_WAIT);

            }
        }

        // FIXME: calculate from sampling rate
        const int wait_timeout_us = 1000000/self->samplerate;
        k_usleep(wait_timeout_us);
    }
}
```


```


#define SAMPLERATE 100
#define WINDOW_LENGTH 100
#define HOP_LENGTH 25

// Configuration
#define N_CHANNELS = 3;
enum sensor_channel sensor_reader_channels[N_CHANNELS] = {
	SENSOR_CHAN_ACCEL_X,
	SENSOR_CHAN_ACCEL_Y,
	SENSOR_CHAN_ACCEL_Z,
};


// Reader internals
sensor_value sensor_reader_output_buffer[WINDOW_LENGTH*N_CHANNELS];
sensor_value sensor_reader_new_buffer[HOP_LENGTH*N_CHANNELS];

K_THREAD_STACK_DEFINE(sensor_reader_stack, MY_STACK_SIZE);
struct k_thread sensor_reader_thread;

K_MSGQ_DEFINE(sensor_reader_queue, sizeof(struct data_item_type), 1, 1);


struct sensor_chunk_reader {
    .samplerate=SAMPLERATE,
    .thread=&sensor_reader_thread,


    .read_samples=sensor_reader_new_buffer,
    .read_samples_index=0,

    .output_buffer=sensor_reader_output_buffer,
    .output_buffer_index=0,

    .n_channels=N_CHANNELS,
    .channels=sensor_reader_channels,

    .dev=sensor,
    .queue=&sensor_reader_queue,
    .thread=&sensor_reader_thread,
}


static int set_sampling_freq(const struct device *dev, int samplerate)
{
	int ret;
	struct sensor_value odr;
	odr.val1 = samplerate;
	odr.val2 = 0;
	ret = sensor_attr_set(dev, SENSOR_CHAN_ACCEL_XYZ, SENSOR_ATTR_SAMPLING_FREQUENCY, &odr);

	return 0;
}


int main(void)
{
	int ret;

    struct sensor_chunk_msg chunk;

	if (!device_is_ready(sensor) }
			printk("sensor: device %s not ready.\n", sensors[i]->name);
			return 0;
		}
		set_sampling_freq(sensor, SAMPLINGRATE);
	}

    sensor_chunk_reader_start(&sensor_reader);

	while (1) {

        // check for new data
        int get_status = k_msgq_get(reader->queue, &chunk, K_NO_WAIT);


		k_msleep(100);
	}
	return 0;
}

```
