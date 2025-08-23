
import time
from machine import PWM, Pin

# On XIAO BLE, pin 6, 26, 30 has RGB LED
led = Pin(("gpio0", 26), Pin.OUT)

while True:
   led.value(1)
   time.sleep(1)
   led.value(0)
   time.sleep(1)
