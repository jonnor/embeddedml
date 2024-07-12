
import machine
from machine import Pin, I2C
import ntptime
import network
import time

import requests

from secrets import WIFI_SSID, WIFI_PASSWORD

# https://github.com/tuupola/micropython-mpu6886/blob/master/mpu6886.py
from mpu6886 import MPU6886, SF_G, SF_DEG_S

def wifi_connect(timeout=5.0):

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        print('wifi-already-connected')
        return

    print('wifi-connect')    
    start_time = time.ticks_ms()
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        t = time.ticks_ms()
        if t > start_time + (timeout*1000):
            raise Exception("WiFi connection failed")

    duration = time.ticks_ms() - start_time
    print('wifi-connected', duration)

    print('ntp-start')
    ntptime.settime()
    print('ntp-done')


def main():

    hold_pin = machine.Pin(4, machine.Pin.OUT)
    buzzer_pin = machine.Pin(2, machine.Pin.OUT)
    led_pin = machine.Pin(19, machine.Pin.OUT)

    i2c = I2C(scl=Pin(22), sda=Pin(21))
    accelerometer = MPU6886(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)

    # indicate that we have woken up
    buzzer_pin.value(1)
    led_pin.value(1)
    time.sleep_ms(50)    
    buzzer_pin.value(0)
    led_pin.value(0)

    # M5StickC we need to set HOLD pin to stay alive when on battery
    hold_pin.value(1)

    wifi_connect(timeout=30.0)

    print('start-time', time.localtime())

    def data_chunks():
        for i in range(10):
            n_bytes = 2*3*50
            data = bytearray(n_bytes)
            yield data
            #time.sleep_ms(1000)

    host = '192.168.87.93:5000'
    url = 'http://'+host+'/data'
    while True:

        acc = accelerometer.acceleration
        print('orientation', acc)

        # Tiny blink to show we are alive
        led_pin.value(1)
        time.sleep_ms(1)
        led_pin.value(0)

        start_time = time.ticks_ms()
        for i in range(6):
            response = requests.request("POST", url, data=data_chunks())
            print('response', response.status_code)
        duration = time.ticks_diff(time.ticks_ms(), start_time)
        print('batch-send-done', duration)

        time.sleep(5.0)

if __name__ == '__main__':
    main()
