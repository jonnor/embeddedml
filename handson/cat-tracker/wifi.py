
import machine
import ntptime
import network
import time

import requests

from secrets import WIFI_SSID, WIFI_PASSWORD

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


hold_pin = machine.Pin(4, machine.Pin.OUT)
buzzer_pin = machine.Pin(2, machine.Pin.OUT)
led_pin = machine.Pin(19, machine.Pin.OUT)

def main():

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

    host = '192.168.87.93:5000'
    url = 'http://'+host+'/data'
    data = 'fofo'
    while True:

        led_pin.value(1)
        time.sleep_ms(1)
        led_pin.value(0)

        start_time = time.ticks_ms()
        response = requests.request("POST", url, data=data)
        duration = time.ticks_diff(time.ticks_ms(), start_time)
        print('response', response.status_code, duration)
        time.sleep(5.0)

if __name__ == '__main__':
    main()
