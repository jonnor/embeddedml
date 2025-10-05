
import time
import machine
import array
import asyncio
import math
import os.path

from aw9523 import AW9523
from as7343 import AS7343
from encoder import M5StackEncoder
import npyfile

from machine import Pin, SoftI2C


from color_setup import ssd  # Create a display instance
from gui.core.nanogui import refresh
from gui.core.writer import Writer
from gui.widgets.meter import Meter
from gui.widgets.label import Label
import gui.fonts.courier20 as fixed


def update_screen(n, state):

    ssd.fill(0)

    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = Writer(ssd, fixed, verbose=False)
    wri.set_clip(False, False, False)

    textfield = Label(wri, 0, 2, wri.stringlen('measure'))
    textfield.value(state)

    #countfield = Label(wri, 0, 90, wri.stringlen('1'))

    #numfield.value('{:5.2f}'.format(40400 /1000))
    #countfield.value('{:1d}'.format(n))

    refresh(ssd)

async def measure_one(as7343, data, offset=0, wait_time=1.0):

    order = AS7343.CHANNEL_MAP

    # wait for condition to settle
    await asyncio.sleep(wait_time)

    # XXX: make sure to flush out old readings from FIFO
    for i in range(10):
        readings = as7343.read()
        await asyncio.sleep(0.10)

    # Copy data
    for i, c in enumerate(order):
        data[offset+i] = readings[c]

    await asyncio.sleep(wait_time)

async def measure_sample(as7343, ext, data, wait_time=1.0):
    """
    Make one complete measurement, consisting of 3 sub-measurements:

    - no excitation / baseline
    - UV excitation / flouresence
    - white / reflectance

    The values are concatenated
    """
    
    n_channels = len(AS7343.CHANNEL_MAP)
    n_datapoints = n_channels * 3
    assert len(data) == n_datapoints

    start = time.ticks_ms()
    print('measure-sample-start', start)

    # measure without exitation
    ext[0:16] = 0
    await measure_one(as7343, data, offset=0, wait_time=wait_time)

    # Measure with UV exitation
    ext[0:16] = 100
    await measure_one(as7343, data, offset=n_channels, wait_time=wait_time)
    ext[0:16] = 0

    # Measure with white LED
    as7343.set_illumination_led(True)
    await measure_one(as7343, data, offset=2*n_channels, wait_time=wait_time)
    as7343.set_illumination_led(False)

    duration = time.ticks_diff(time.ticks_ms(), start)
    print('measure-sample-end', time.ticks_ms(), duration)


def print_measurement(data):

    max_value = 20
    width = 40
    char = '*'
    base = 2.0

    max_value_seen = 0

    for i in range(len(data)):
        v = data[i]
        l = max(0, math.log(v+1e-9, base))
        if l > max_value_seen:
            max_value_seen = l
        
        w = int((l / max_value) * width)
        #print(v, l, w)
        s = char * w
        print(s)

    print('mm', max_value_seen)

def main():

    i2c_int = machine.I2C("i2c0")

    i2c_ext = machine.I2C("i2c1")
    ext = AW9523(i2c_ext, address=0x5b)
    as7343 = AS7343(i2c_ext)

    as7343.set_measurement_time(200) # ms
    as7343.set_integration_time(100*1000, repeat=1) # us
    as7343.start_measurement()

    as7343.set_illumination_led(False)
    as7343.set_illumination_current(20)

    measurement_data = array.array('f', (0.0 for _ in range(3*len(AS7343.CHANNEL_MAP))))


    encoder = M5StackEncoder(i2c_ext)
    accumulated = 0.0
    iteration = 0

    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    measurement_state = 'ready'

    async def check_inputs():

        nonlocal measurement_state
        nonlocal accumulated
        nonlocal iteration

        while True:

            button = encoder.read_button()
            if button:
                if measurement_state == 'ready':
                    measurement_state = 'measure'
                    await measure_sample(as7343, ext, data=measurement_data, wait_time=0.2)

                    # TODO: support specifying part of filename
                    filename = 'channels-' + str(time.time()) + '.npy'
                    path = os.path.join(data_dir, filename)
                    shape = (len(measurement_data),)
                    npyfile.save(path, measurement_data, shape=shape)
                    print('measurement-saved', path)

                    measurement_state = 'ready'
                else:
                    print('button-ignored', measurement_state)

            rel = encoder.read_relative()
            accumulated += rel

            iteration += 1
            await asyncio.sleep(0.010)

    async def make_measurement():

        while True:
            # XXX: does nothing right now
            pass
            await asyncio.sleep(5.0)


    async def update_display_loop():

        while True:

            start = time.ticks_ms()
            update_screen(n=iteration, state=measurement_state)
            duration = time.ticks_diff(time.ticks_ms(), start)
            print('screen-update', duration)
            await asyncio.sleep(0.5)

    async def run():
        await asyncio.gather(update_display_loop(), check_inputs(), make_measurement())
    asyncio.run(run())


if __name__ == '__main__':
    main()

