

import machine
from machine import Pin, I2C

import gc
import time
import math
import struct
import array
import asyncio
import sys

sys.path.insert(0, 'lib/') # XXX: why not on path?

from recorder import Recorder

HW_M5STICK_PLUS2 = 'm5stick-plus2'
HW_XIAO_BLE_SENSE = 'xiao-ble-sense'

is_m5stick = 'ESP32' in sys.implementation._machine
hardware = HW_M5STICK_PLUS2 if is_m5stick else HW_XIAO_BLE_SENSE

# Free memory used by imports
gc.collect()


def empty_array(typecode, length, value=0):
    return array.array(typecode, (value for _ in range(length)))


def deinterleave_samples_xiao(buf : bytearray,
        xs, ys, zs, rowstride=6, offset=0, format='>hhh'):
    """
    Convert raw bytes into X,Y,Z int16 arrays
    """
    assert (len(buf) % rowstride) == 0
    samples = len(buf) // rowstride
    assert len(xs) == samples
    assert len(ys) == samples
    assert len(zs) == samples

    for i in range(samples):
        idx = offset + (i*rowstride)
        x, y, z = struct.unpack_from(format, buf, idx)
        xs[i] = y
        ys[i] = x
        zs[i] = -z

def deinterleave_samples_m5stick(buf : bytearray,
        xs, ys, zs, rowstride=6, offset=0, format='>hhh'):
    """
    Convert raw bytes into X,Y,Z int16 arrays
    """
    assert (len(buf) % rowstride) == 0
    samples = len(buf) // rowstride
    assert len(xs) == samples
    assert len(ys) == samples
    assert len(zs) == samples

    for i in range(samples):
        idx = offset + (i*rowstride)
        x, y, z = struct.unpack_from(format, buf, idx)
        xs[i] = x
        ys[i] = y
        zs[i] = z

def decode_samples(
        buf : bytearray,
        samples : array.array,
        rowstride,
        offset=0,
        format='<hhhhhh',
    ):
    """
    Convert raw bytes for gyro+accelerometer into int16 array
    """

    in_stride = rowstride
    assert (len(buf) % in_stride) == 0
    n_samples = len(buf) // in_stride

    out_stride = len(format)-1
    assert len(samples) == out_stride*n_samples, (len(samples), out_stride*n_samples)

    #view = memoryview(buf)
    for i in range(n_samples):
        idx = offset + (i*in_stride)
        values = struct.unpack_from(format, buf, idx)
        for j, v in enumerate(values):
            samples[(i*out_stride)+j] = v



def main():

    print('init-start')

    # Settings
    hop_length = 52
    window_length = hop_length
    record_enable = True
    record_duration = 20.0
    record_dir = 'record'
    record_class = 'rowing'

    # FIXME: standardize configuration between hardwares
    if hardware == HW_M5STICK_PLUS2:
        samplerate = 50
        accel_offset = 0 # data is AxAyAzTc
        accel_format = '>hhh'
        # FIXME: make MPU also support gyro
        bytes_per_sample = 8 
        record_format = '>hhh'
    else:
        samplerate = 52
        bytes_per_sample = 12
        accel_offset = 6 # data is GxGyGzAxAyAz
        record_format = '<hhhhhh'
        accel_format = '<hhh'

    if record_enable:
        record_samples = len(record_format) - 1
        record_buffer = array.array('h', (0 for _ in range(record_samples*hop_length))) # decoded int16
    else:
        record_buffer = None

    # working buffers
    x_values = empty_array('h', hop_length)
    y_values = empty_array('h', hop_length)
    z_values = empty_array('h', hop_length)
    chunk = bytearray(bytes_per_sample*hop_length)

    print('setup-hardware-start')

    time.sleep(1)

    # Setup hardware-specific things
    if hardware == HW_XIAO_BLE_SENSE:
        print('hardware-init-xiao-ble-sense')
        time.sleep(1)

        import lsm6ds
        # On XIAO BLE, pin 6, 26, 30 has RGB LED. Active low
        record_pin = machine.Pin(("gpio0", 6), machine.Pin.OUT) # 6=blue
        error_pin = machine.Pin(("gpio0", 26), machine.Pin.OUT) # 26=red
        detect_pin = machine.Pin(("gpio0", 30), machine.Pin.OUT) # 30=green
        record_pin.value(1)
        detect_pin.value(1)

        # Indicate start
        error_pin.value(0)
        time.sleep(0.1)
        error_pin.value(1)

        # FIXME: use 52 Hz, and FIFO
        i2c = I2C("i2c0")
        assert samplerate == 52
        imu = lsm6ds.LSM6DS3(i2c, mode=lsm6ds.MODE_52HZ | 0b0000_1000)

        imu.fifo_enable(True)
        deinterleave_samples = deinterleave_samples_xiao

    else:
        raise ValueError("Unknown hardware: " + hardware)

    print('setup-hardware-end')


    print('init-done')

    def main_task():
        print('main-start')

        count = 0

        with Recorder(samplerate, record_duration, directory=record_dir, items_per_sample=6) as recorder:

            if record_enable:
                #recorder.delete()
                recorder.set_class(record_class)
                recorder.start()

            while True:

                count = imu.get_fifo_count()
                #print('fifo check', count)
                if count >= hop_length:
                    start = time.ticks_ms()

                    # read data
                    read_start = time.ticks_ms()

                    imu.read_samples_into(chunk)

                    deinterleave_samples(chunk, x_values, y_values, z_values,
                        rowstride=bytes_per_sample, offset=accel_offset, format=accel_format)

                    if record_enable:
                        record_pin.value(0)
                        decode_samples(chunk, record_buffer,
                            format=record_format, rowstride=bytes_per_sample)
                        recorder.process(record_buffer)
                        record_pin.value(1)

                    read_duration = time.ticks_ms() - read_start

                    process_start = time.ticks_ms()
                    # TODO: add in analyzer
                    #motion, brushing = processor.process(x_values, y_values, z_values)
                    process_duration = time.ticks_ms() - process_start

                    t = time.time()

                    # Update outputs
                    d = time.ticks_diff(time.ticks_ms(), start)
                    print('main-iter-times', d, read_duration, process_duration)

                gc.collect()
                await asyncio.sleep_ms(10)
                #machine.lightsleep(100)

    asyncio.run(main_task())

if __name__ == '__main__':

    #test_outputs()

    main()

    #try:
    #    main()
    #except KeyboardInterrupt:
    #    raise
    #except Exception as e:
    #    print('unhandled-exception', e)
    #    time.sleep(1)
    #    raise e
    #    machine.reset()


