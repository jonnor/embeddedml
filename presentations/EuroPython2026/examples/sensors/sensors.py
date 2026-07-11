
import time
from machine import Pin, ADC, PWM
import machine

from mpu6050 import MPU6050


adc = ADC(Pin(26))
led = PWM(Pin(13))
led.freq(1000)

i2c = machine.I2C(sda=Pin(0), scl=Pin(1), freq=100_000)
mpu = MPU6050(i2c)


while True:
    value = adc.read_u16()
    duty = int(value/10)
    led.duty_u16(duty)

    v = mpu.get_values()

    print(duty, v)
    time.sleep(0.1)


