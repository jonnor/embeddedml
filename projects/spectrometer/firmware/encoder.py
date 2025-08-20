
"""
Rotary encoder driver

License: MIT
Copyright: Soundsensing AS, 2024
"""

import machine
import struct
import time

ENCODER_REG = 0x10
BUTTON_REG = 0x20
RGB_LED_REG = 0x30

# only in "new" firmware
MODE_REG = 0x00
RESET_REG = 0x40

class M5StackEncoder():
    """
    I2C rotary encoder by M5Stack "Unit Encoder"

    https://docs.m5stack.com/en/unit/encoder
    https://github.com/m5stack/M5UnitEncoder_Firmware
    """

    def __init__(self, i2c, addr=0x40):
        self.i2c = i2c
        self.addr = addr
        self._last_count = None

    def read_count(self) -> int:
        # XXX: doing a 2 byte read does not seem to work. So do two 1 bytes instead
        low = self.i2c.readfrom_mem(self.addr, ENCODER_REG, 1)
        high = self.i2c.readfrom_mem(self.addr, ENCODER_REG+1, 1)
        data = low + high

        count = low[0] | (high[0] << 8)
        self._last_count = count # keep track of deltas
        return count

    def read_relative(self) -> int:
        prev = self._last_count
        next = self.read_count()
        delta = find_delta(prev, next)
        return delta

    def read_button(self) -> bool:
        data = self.i2c.readfrom_mem(self.addr, BUTTON_REG, 1)
        pressed = data[0] == 0 # active low
        return pressed

    def set_led(self, led : int, rgb : bytearray):
        command = bytearray([led]) + rgb
        self.i2c.writeto_mem(self.addr, RGB_LED_REG, command)

    def set_mode(self, mode):
        """XXX: does not seem do anything"""
        if mode == 'pulse':
            val = 0
        elif mode == 'ab':
            val = 1
        else:
            raise ValueError("Mode must be 'pulse' or 'ab'")        
        self.i2c.writeto_mem(self.addr, MODE_REG, bytearray([val]))

    def set_encoder(self, count): 
        """XXX: does not seem to do anything"""
        data = struct.pack('<H', count)
        self.i2c.writeto_mem(self.addr, ENCODER_REG, data)

    def reset_counter(self):
        """XXX: does not seem do anything"""
        self.i2c.writeto_mem(self.addr, RESET_REG, bytearray([1]))



def find_delta(prev, next, max_value=2**16-1, margin=6000):
    """
    The rotary encoder wraps around from max_value <-> 0

    To be able to get increments/delta/relative changes from this, we need to account for it.
    This is done by a heuristic that transitions across the max_value/0 boundary
    are probably a move across it, as long as it is within a certain margin from the boundary.
    """

    low_limit = margin
    high_limit = max_value - margin

    if prev is None:
        # initialization
        delta = 0
    elif prev > high_limit and next < low_limit:
        # assume forward wraparound
        delta = (max_value - prev) + next + 1
    elif prev < low_limit and next > high_limit:
        # assume backward wraparound
        delta = (next - max_value) - prev - 1
    else:
        # assume regular change
        delta = next - prev

    assert delta <= max_value, delta
    assert delta >= -max_value, delta
    return delta

def test_encoder_relative():

    # current, next => delta
    cases = [
        (None, 3400, 0), # init small
        (None, 64000, 0), # init huge
        (3000, 3400, 400), # small forward
        (3400, 3000, -400), # small reverse
        (3000, 10000, 7000), # big forward
        (10000, 65000, 55000), # huge forward
        (10000, 65000, 55000), # huge backward
        (65000, 1000, 65536-65000+1000), # rollover forward
        (1000, 65000, -(65536-65000+1000)), # rollover backward
    ]
    
    failures = 0
    for current, next, expect in cases:
        delta = find_delta(current, next)
        fail = delta != expect
        print(current, next, 'delta:', delta, '==',expect, ':', 'FAIL' if fail else 'OK')
        if fail:
            failures += 1

    assert failures == 0, failures

def main():

    test_encoder_relative()

    from machine import Pin
    i2c = machine.I2C(0, sda=Pin(32), scl=Pin(33))
    encoder = M5StackEncoder(i2c)

    #encoder.set_mode('pulse')
    #encoder.reset_counter()

    color1 = bytearray([255, 0, 255])
    color2 = bytearray([0, 255, 0])

    accumulated = 0
    while True:

        encoder.set_led(0, color1)
        encoder.set_led(1, color1)

        button = encoder.read_button()
        if button:
            encoder.set_led(0, color2)
            encoder.set_led(1, color2)          

        rel = encoder.read_relative()
        rot = encoder.read_count()
        accumulated += rel

        print(button, rot, rel, accumulated)
        time.sleep_ms(100)

if __name__ == '__main__':
    main()
