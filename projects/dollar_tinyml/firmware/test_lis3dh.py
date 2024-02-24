
import time
from machine import Pin, I2C

# https://github.com/jposada202020/MicroPython_LIS3DH/
from micropython_lis3dh import lis3dh

i2c = I2C(1, sda=Pin(17), scl=Pin(14), freq=100000)

def init():

    lis = lis3dh.LIS3DH(i2c, address=0x19)

    for _ in range(3):
        accx, accy, accz = lis.acceleration
        print(f"x: {accx}m/s^2, y: {accy}m/s^2, z: {accz}m/s^2")
        print()
        time.sleep(1)

while True:
    try:
        init()
    except Exception as e:
        print(e)
        pass
    time.sleep(1)
