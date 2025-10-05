
import time
import machine
import array
import asyncio
import math
import os.path
import gc

from aw9523 import AW9523
from as7343 import AS7343
from encoder import M5StackEncoder
import npyfile

from machine import Pin, SoftI2C


from color_setup import ssd, display_height, display_width  # Create a display instance
from gui.core.nanogui import refresh
from gui.core.writer import Writer
from gui.widgets.meter import Meter
from gui.widgets.label import Label
import gui.fonts.courier20 as fixed

# Free memory used by imports
gc.collect()

def draw_hlines(ssd, x0, x1, y0, y1, lines=10, dash=5, gap=2, color=1):

    y_dist = int((y1-y0) / lines)
    for y in range(y0, y1, y_dist):
        
        # dashed
        for x in range(x0, x1, dash + gap):
            ssd.hline(x, y, min(dash, x1-x), color)

def draw_vlines(ssd, x0, x1, y0, y1, lines=10, dash=5, gap=2, color=1):

    x_dist = int((x1-x0) / lines)
    for x in range(x0, x1, x_dist):
        
        # dashed
        for y in range(y0, y1, dash + gap):
            ssd.vline(x, y, min(dash, y1-y), color)

class NeighborsClassifier():

    def __init__(self,
            columns : list[int],
            classes : list[str],
            max_items=100,
            n_neighbors=1,
        ):

        self.classes = classes
        self.columns = columns

        import emlearn_neighbors
        self.model = emlearn_neighbors.new(max_items, len(columns), n_neighbors)

    def load_data(self, data_dir : str):

        for filename in os.listdir(data_dir):
            p = os.path.join(data_dir, filename)
            shape, data = npyfile.load(p)
            assert len(shape) == 1, shape

            tok = filename.split('-')
            classname = tok[0]
            if classname == 'unknown':
                continue
            x = self.transform(data)
            y = self.classes.index(classname)
            print('load-item', classname, y, x)
            self.model.additem(x, y)

    def transform(self, data):
        # Extract the relevant columns
        # TODO: maybe also do a log transform?
        values = array.array('h', ( int(data[i]) for i in self.columns ))
        return values

    def predict(self, measurement):
        # TODO: also check how close the closest point is?
        x = self.transform(measurement)
        print('predict', x)
        out = self.model.predict(x)
        return out


def update_screen(n, state, data, x_column, y_column, prediction, x_max=10000, y_max=500):


    # Blank the screen
    ssd.fill(0)

    x_offset = 0
    y_offset = 5

    width = display_width
    height = display_height

    if state == 'done':

        # Draw grid
        draw_hlines(ssd, x0=x_offset, x1=width, y0=y_offset, y1=height, lines=5, gap=8, dash=1)
        #draw_vlines(ssd, x0=x_offset, x1=width, y0=y_offset, y1=height, lines=10, gap=8, dash=1)

        # Draw datapoints
        print('draw-datapoints', len(data), x_column, y_column)
        x_paper = data[x_column] / x_max
        y_paper = data[y_column] / y_max
        
        if x_paper < 0.0 or x_paper > 1.0 or y_paper < 0.0 or y_paper > 1.0:
            print('point-out-of-bounds', x_paper, y_paper)

        x = int(x_paper * width)
        y = int(y_paper * height)
        color = 1
        size = 7

        print('draw-point', data[x_column], data[y_column], x, y)
        # Draw a small point
        ssd.fill_rect(x + x_offset, y + y_offset, size, size, color)

    elif state == 'result':

        Writer.set_textpos(ssd, 0, 0)
        wri = Writer(ssd, fixed, verbose=False)
        wri.set_clip(False, False, False)

        # TODO: center this
        textfield = Label(wri, 0, 2, wri.stringlen('measure'))
        textfield.value(prediction)        

    else:

        Writer.set_textpos(ssd, 0, 0)
        wri = Writer(ssd, fixed, verbose=False)
        wri.set_clip(False, False, False)

        textfield = Label(wri, 0, 2, wri.stringlen('measure'))
        textfield.value(state)

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

async def measure_sample(i2c_ext, ext, data, wait_time=1.0):
    """
    Make one complete measurement, consisting of 3 sub-measurements:

    - no excitation / baseline
    - UV excitation / flouresence
    - white / reflectance

    The values are concatenated
    """
    
    as7343 = AS7343(i2c_ext)

    as7343.set_measurement_time(200) # ms
    as7343.set_integration_time(100*1000, repeat=1) # us
    as7343.set_illumination_led(False)
    as7343.set_illumination_current(4)

    n_channels = len(AS7343.CHANNEL_MAP)
    n_datapoints = n_channels * 3
    assert len(data) == n_datapoints

    start = time.ticks_ms()
    print('measure-sample-start', start)

    as7343.start_measurement()
    await asyncio.sleep(0.1)   

    # measure without exitation
    #print('measure-no-light')
    #ext[0:16] = 0
    #await measure_one(as7343, data, offset=0, wait_time=wait_time)

    # Measure with UV exitation
    print('measure-uv')
    ext[0:16] = 100
    await measure_one(as7343, data, offset=n_channels, wait_time=wait_time)
    ext[0:16] = 0

    # Measure with white LED
    #print('measure-white')
    #as7343.set_illumination_led(True)
    #await measure_one(as7343, data, offset=2*n_channels, wait_time=wait_time)
    #as7343.set_illumination_led(False)

    as7343.stop_measurement()

    duration = time.ticks_diff(time.ticks_ms(), start)
    print('measure-sample-end', time.ticks_ms(), duration)



def main():

    i2c_int = machine.I2C("i2c0")

    i2c_ext = machine.I2C("i2c1")
    ext = AW9523(i2c_ext, address=0x5b)


    measurement_data = array.array('f', (0.0 for _ in range(3*len(AS7343.CHANNEL_MAP))))

    shape, measurement_data = npyfile.load('data2/channels-13800.npy')
    print('loaded-data', shape, len(measurement_data))

    encoder = M5StackEncoder(i2c_ext)
    accumulated = 0.0
    iteration = 0

    data_dir = 'data3'
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    classes = [
        'none',
        'sunflower',
        'canola',
        'EVOO',
        'ROO',
    ]
    last_prediction = None

    uv_start = len(AS7343.CHANNEL_MAP)*1
    x_index = uv_start + AS7343.CHANNEL_MAP.index('F7')
    y_index = uv_start + AS7343.CHANNEL_MAP.index('FZ')
    classifier = NeighborsClassifier(classes=classes, columns=[x_index, y_index])
    classifier.load_data(data_dir)

    #classifier.predict(measurement_data)

    measurement_state = 'ready'
    #measurement_state = 'done'

    selected_class = 'unknown'

    async def check_inputs():

        nonlocal measurement_state
        nonlocal accumulated
        nonlocal iteration
        nonlocal last_prediction

        while True:

            button = encoder.read_button()
            if button:
                if measurement_state == 'ready':
                    measurement_state = 'measure'

                    gc.collect()
                    await measure_sample(i2c_ext, ext, data=measurement_data, wait_time=0.2)

                    filename = selected_class + '-channels-' + str(time.time()) + '.npy'
                    path = os.path.join(data_dir, filename)
                    shape = (len(measurement_data),)
                    npyfile.save(path, measurement_data, shape=shape)
                    print('measurement-saved', path)

                    measurement_state = 'done'
                    await asyncio.sleep(2.0)

                    class_idx = classifier.predict(measurement_data)
                    class_name = classifier.classes[class_idx]
                    last_prediction = class_name
                    print('predict-result', class_idx, class_name)
                    measurement_state = 'result'
                    await asyncio.sleep(2.0)

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
            if True:
                update_screen(n=iteration,
                    state=measurement_state,
                    data=measurement_data,
                    x_column=x_index,
                    y_column=y_index,
                    prediction=last_prediction,
                )
                duration = time.ticks_diff(time.ticks_ms(), start)
                print('screen-update', duration)
            await asyncio.sleep(0.5)

    async def run():
        await asyncio.gather(update_display_loop(), check_inputs(), make_measurement())
    asyncio.run(run())


if __name__ == '__main__':
    main()

