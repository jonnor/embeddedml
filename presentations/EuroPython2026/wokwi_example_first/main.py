"""
MicroPython mip install example
"""

from machine import Pin, ADC, I2C, PWM
import time
import sys

# rotary encoder
from rotary_irq_rp2 import RotaryIRQ


class DemoBoard:
    def __init__(self):
        # LEDS
        self.led_red = Pin(11, Pin.OUT)
        self.led_green = Pin(12, Pin.OUT)
        self.led_blue = Pin(13, Pin.OUT)

        # Buttons
        self.button_red = Pin(18, Pin.IN, Pin.PULL_UP)
        self.button_green = Pin(19, Pin.IN, Pin.PULL_UP)
        self.button_blue = Pin(20, Pin.IN, Pin.PULL_UP)

        # Potentiometers
        self.pot_red = ADC(Pin(26))
        self.pot_green = ADC(Pin(27))
        self.pot_blue = ADC(Pin(28))

        # Buzzer
        self.buzzer = PWM(Pin(2,Pin.OUT))

        # Rotary encoder
        self.encoder = RotaryIRQ(pin_num_clk=7,
              pin_num_dt=8,
              min_val=0,
              reverse=True,
              range_mode=RotaryIRQ.RANGE_UNBOUNDED)
        self.encoder_button = Pin(6, Pin.IN, Pin.PULL_UP)  


        # I2C. Screen SSD1306 and IMU MPU6050
        self.i2c = I2C(0, scl=Pin(1), sda=Pin(0), freq=400_000)



board = DemoBoard()

devices = board.i2c.scan()
print('I2C devices', devices)

val_old = board.encoder.value()

while True:

    b_r = not board.button_red()
    b_g = not board.button_green()
    b_b = not board.button_blue()

    board.led_red.value(b_r)
    board.led_green.value(b_g)
    board.led_blue.value(b_b)

    a_r = board.pot_red.read_u16() / 65535
    a_g = board.pot_green.read_u16() / 65535
    a_b = board.pot_blue.read_u16() / 65535

    # check encoder value
    val_new = board.encoder.value()
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)

    if board.encoder_button.value() == 0:
        print("Encoder button pressed")
        # Sound buzzer when pressed
        board.buzzer.freq(400)
        board.buzzer.duty_u16(int(0.5*65535))

        while board.encoder_button.value() == 0:
            continue
    board.buzzer.duty_u16(0)

    print("buttons", b_r, b_g, b_b)
    print("pots", a_r, a_g, a_b)
    time.sleep(0.2)
