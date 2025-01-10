

import time

# mpremote mip install https://github.com/robert-hh/hx711/raw/refs/heads/master/hx711_gpio.py
from hx711_gpio import HX711
from machine import Pin

pin_OUT = Pin(14, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(17, Pin.OUT)

hx711 = HX711(pin_SCK, pin_OUT)

hx711.tare()

while True:
    value = hx711.read()
    value = hx711.get_value()
    print(value)
    time.sleep(0.1)

