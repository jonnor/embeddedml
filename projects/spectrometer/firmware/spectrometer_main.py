
import time
import machine
import array
import asyncio

from aw9523 import AW9523
from as7343 import AS7343
from encoder import M5StackEncoder

from machine import Pin, SoftI2C


from color_setup import ssd  # Create a display instance
from gui.core.nanogui import refresh
from gui.core.writer import Writer
from gui.widgets.meter import Meter
from gui.widgets.label import Label
import gui.fonts.courier20 as fixed


def update_screen(n):
    ssd.fill(0)
    #refresh(ssd)
    Writer.set_textpos(ssd, 0, 0)  # In case previous tests have altered it
    wri = Writer(ssd, fixed, verbose=False)
    wri.set_clip(False, False, False)
    textfield = Label(wri, 0, 2, wri.stringlen('longer'))
    numfield = Label(wri, 25, 2, wri.stringlen('99.99'), bdcolor=None)
    countfield = Label(wri, 0, 90, wri.stringlen('1'))

    textfield.value("longer")
    numfield.value('{:5.2f}'.format(40400 /1000))
    countfield.value('{:1d}'.format(n))

    refresh(ssd)


async def measure_sample(as7343, ext):
    # TODO: take the array as an input, and fill it
    print('ss')

    order = AS7343.CHANNEL_MAP
    print(order)

    # measure without exitation
    ext[0:16] = 0
    await asyncio.sleep(1.0)
    # XXX: make sure to flush out old readings from FIFO
    for i in range(10):
        readings = as7343.read()
        await asyncio.sleep(0.10)

    #as7343.stop_measurement()
    values = array.array('f', (readings[c] for c in order))
    print('off     ', readings['F7'], values)

    await asyncio.sleep(1.00)

    # Turn on exitation
    ext[0:16] = 100
    await asyncio.sleep(1.00)

    # XXX: make sure to flush out old readings from FIFO
    for i in range(10):
        readings = as7343.read()
        await asyncio.sleep(0.10)

    #as7343.stop_measurement()
    values = array.array('f', (readings[c] for c in order))
    print('excited!', readings['F7'], values)

    # TODO: turn on white LED, measure reflectance spectra


def main():

    i2c_int = machine.I2C("i2c0")

    i2c_ext = machine.I2C("i2c1")
    ext = AW9523(i2c_ext, address=0x5b)
    as7343 = AS7343(i2c_ext)

    as7343.set_measurement_time(200) # ms
    as7343.set_integration_time(100*1000, repeat=1) # us
    as7343.start_measurement()

    #test_encoder()

    encoder = M5StackEncoder(i2c_ext)

    #encoder.set_mode('pulse')
    #encoder.reset_counter()

    color1 = bytearray([255, 0, 255])
    color2 = bytearray([0, 255, 0])

    accumulated = 0.0

    encoder = M5StackEncoder(i2c_ext)

    iteration = 0

    async def check_inputs():

        nonlocal accumulated
        nonlocal iteration

        while True:
            intensity = (accumulated/20000)
            c = bytearray([0, int(255*intensity), 0])

            encoder.set_led(1, c)
            button = encoder.read_button()
            if button:
                encoder.set_led(1, color2)          

            rel = encoder.read_relative()
            accumulated += rel

            iteration += 1
            await asyncio.sleep(0.005)

    async def make_measurement():

        while True:
            print('mm')
            await measure_sample(as7343, ext)
            print('xx')
            await asyncio.sleep(5.0)


    async def update_display_loop():

        while True:

            start = time.ticks_ms()
            update_screen(n=iteration)
            duration = time.ticks_diff(time.ticks_ms(), start)
            print('screen-update', duration)
            await asyncio.sleep(0.5)

    async def run():
        await asyncio.gather(update_display_loop(), check_inputs(), make_measurement())
    asyncio.run(run())


if __name__ == '__main__':
    main()

