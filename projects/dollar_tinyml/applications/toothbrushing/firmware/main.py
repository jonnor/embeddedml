

import machine
from machine import Pin, I2C
from mpu6886 import MPU6886

import gc
import time
import math
import struct
import array

from sketch import StateMachine

import timebased
import emlearn_trees    

# Free memory used by imports
gc.collect()


def empty_array(typecode, length, value=0):
    return array.array(typecode, (value for _ in range(length)))

def mean(arr):
    m = sum(arr) / float(len(arr))
    return m

def magnitude_3d(x, y, z):
    r2 = x**2 + y**2 + z**2
    r = math.sqrt(r2)
    return r

def euclidean(a, b):
    s = 0.0
    assert len(a) == len(b)
    for av, bv in zip(a, b):
        s += (av-bv)**2

    return math.sqrt(s)

def clamp(value, lower, upper) -> float:
    v = value
    v = min(v, upper)
    v = max(v, lower)
    return v

def energy_xyz(xs, ys, zs, orientation):
    assert len(xs) == len(ys)
    assert len(ys) == len(zs)

    xo, yo, zo = orientation
    
    # compute RMS of magnitude, after having removed orientation
    s = 0.0
    for i in range(len(xs)):
        m = magnitude_3d(xs[i]-xo, ys[i]-yo, zs[i]-zo)
        s += m**2

    rms = math.sqrt(s)
    return rms

class DataProcessor():

    def __init__(self):
        model_path = 'models/brushing_trees.csv'
        self.brushing_model = self.load_model(model_path)

        features_typecode = timebased.DATA_TYPECODE
        n_features = timebased.N_FEATURES
        self.features = array.array(features_typecode, (0 for _ in range(n_features)))
    
        self.brushing_outputs = array.array('f', (0 for _ in range(2)))

    def load_model(self, model_path):

        # Load a CSV file with the model
        model = emlearn_trees.new(10, 1000, 10)
        with open(model_path, 'r') as f:
            emlearn_trees.load_model(model, f)

        return model

    def process(self, xs, ys, zs):
        """
        Analyze the accelerometers sensor data, to determine what is happening
        """

        up_direction = [ 0, 1.0, 0.0 ] # the expected gravity vector, when toothbrush is upright (not in use)
        max_distance_from_up = 0.80
        max_motion_energy = 3000
        brushing_energy = 20000

        # find orientation
        orientation_start = time.ticks_ms()
        orientation_xyz = mean(xs), mean(ys), mean(zs)
        mag = magnitude_3d(*orientation_xyz)
        norm_orientation = [ c/mag for c in orientation_xyz ]

        distance_from_up = euclidean(norm_orientation, up_direction)
        energy = energy_xyz(xs, ys, zs, orientation_xyz)    

        # dummy motion classifier
        motion = clamp(energy / max_motion_energy, 0.0, 1.0)

        # dummy brushing classifier
        # assume brushing if
        # a) not perfectly upright (stationary in holder)
        # AND b) relatively high energy
        # TODO: replace with trained ML classifier
        not_upright = clamp(distance_from_up / max_distance_from_up, 0.0, 1.0)
        high_energy = clamp(energy / brushing_energy, 0.0, 1.0)

        dummy_brushing = clamp((not_upright*2) * (high_energy*1.5), 0.0, 1.0)
    
        orientation_duration = time.ticks_ms() - orientation_start

        #norm_orientation, distance_from_up

        # compute features
        features_start = time.ticks_ms()
        ff = timebased.calculate_features_xyz((xs, ys, zs))
        for i, f in enumerate(ff):
            self.features[i] = int(f)
        features_duration = time.ticks_ms() - features_start

        # run model
        predict_start = time.ticks_ms()
        self.brushing_model.predict(self.features, self.brushing_outputs)
        brushing = self.brushing_outputs[1]
        predict_duration = time.ticks_ms() - predict_start

        print('comp', features_duration, predict_duration)

        return motion, brushing



from buzzer_music import music

# Copy/paste from 
progress_1 = """0 C5 1 43;2 D#5 1 43;1 D5 1 43"""
progress_2 = """0 F5 1 43;1 F#5 1 43;2 G5 1 43"""
progress_3 = """0 A5 1 43;1 B5 1 43;2 C6 1 43"""
progress_4 = """0 D6 1 43;1 D#6 1 43;2 F6 1 43"""
success_song = """0 C6 1 43;1 G5 1 43;2 E5 1 43;4 C5 4 43"""
fail_song = """3 D4 4 43;0 C5 2 43"""

class OutputManager():

    def __init__(self, led_pin, buzzer_pin):

        self.buzzer_pin = buzzer_pin
        self.led_pin = led_pin

        self.last_state = None
        self.last_progress = None

    def _play_song(self, notes):
        song = music(notes, pins=[self.buzzer_pin], looping=False)
        while True:
            running = song.tick()
            if not running:
                break
            time.sleep_ms(30)    

    def run(self, state : str, progress_state : int):

        if state == self.last_state and progress_state == self.last_progress:
            return

        led_on = state == 'brushing'
        self.led_pin.value(led_on)

        if state == 'sleep':
            pass
        elif state == 'idle':
            pass
        elif state == 'brushing':
            songs = [
                progress_1,
                progress_2,
                progress_3,
                progress_4,
            ]
            s = songs[progress_state]
            self._play_song(s)

        elif state == 'done':
            # XXX: blocking
            self._play_song(success_song)

        elif state == 'failed':
            self._play_song(fail_song)

        else:
            raise ValueError(f"Unsupported state {state}")
    
        self.last_state = state
        self.last_progress = progress_state

def test_outputs():

    buzzer_pin = machine.Pin(2, machine.Pin.OUT)
    led_pin = machine.Pin(19, machine.Pin.OUT)


    sm = StateMachine()
    states = sm._state_functions.keys()
    out = OutputManager(buzzer_pin=buzzer_pin, led_pin=led_pin)

    for state in states:
        print('test-output-state', state)
        out.run(state)
        time.sleep(1.0)


def main():

    mpu = MPU6886(I2C(0, sda=21, scl=22, freq=100000))

    # Enable FIFO at a fixed samplerate
    mpu.fifo_enable(True)
    samplerate = 50
    mpu.set_odr(samplerate)

    hop_length = 25
    window_length = hop_length
    chunk = bytearray(mpu.bytes_per_sample*hop_length)

    x_values = empty_array('h', hop_length)
    y_values = empty_array('h', hop_length)
    z_values = empty_array('h', hop_length)

    # On M5StickC we need to set HOLD pin to stay alive when on battery
    hold_pin = machine.Pin(4, machine.Pin.OUT)
    hold_pin.value(1)

    # Internal LED on M5StickC PLUS2
    led_pin = machine.Pin(19, machine.Pin.OUT)

    # Buzzer
    buzzer_pin = machine.Pin(2)

    out = OutputManager(buzzer_pin=buzzer_pin, led_pin=led_pin)

    print('main-start')

    processor = DataProcessor()
    sm = StateMachine(time=time.time())

    # TEST config
    sm.brushing_target_time = 60.0

    while True:

        count = mpu.get_fifo_count()
        if count >= hop_length:
            start = time.ticks_ms()

            # read data
            read_start = time.ticks_ms()
            mpu.read_samples_into(chunk)
            mpu.deinterleave_samples(chunk, x_values, y_values, z_values)
            read_duration = time.ticks_ms() - read_start

            process_start = time.ticks_ms()
            motion, brushing = processor.process(x_values, y_values, z_values)
            process_duration = time.ticks_ms() - process_start
    
            t = time.time()
            sm.next(t, motion, brushing)

            print('inputs', t, brushing, motion, sm.state)

            # TODO: put this into state machine
            brushing_progress_states = 4
            brushing_progress = clamp(sm.brushing_time / sm.brushing_target_time, 0.0, 0.99)
            brushing_progress_state = int(brushing_progress * brushing_progress_states)

            print('progress state', brushing_progress_state)

            # Update outputs
            out.run(sm.state, brushing_progress_state)

            d = time.ticks_diff(time.ticks_ms(), start)
            print('process', d, read_duration, process_duration)

        time.sleep_ms(100)
        #machine.lightsleep(100)


if __name__ == '__main__':

    #test_outputs()

    main()
