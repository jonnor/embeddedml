

import machine
from machine import Pin, I2C
from mpu6886 import MPU6886

import gc
import time
import math
import struct
import array

from core import StateMachine
from process import DataProcessor, empty_array, clamp
from buzzer_music import music  

# Free memory used by imports
gc.collect()


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

    hop_length = 50
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
