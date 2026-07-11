"""
Send a notification to phone/PC via ntfy.sh
"""

from machine import Pin, ADC, I2C, PWM
import machine
import asyncio
import network
import time
import json
import requests

WIFI_SSID='Wokwi-GUEST'
WIFI_PASSWORD='wokwiwokwi'

# NOTE: you should edit topic and subscribe to it on PC/phone
NOTIFICATION_TOPIC = 'europython2026-jonnor'

def connect_wifi(timeout=20.0):

    try:
        import network
    except ImportError:
        # assuming we are on Unix/PC
        return

    print("Connecting to WiFi")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    start = time.ticks_ms()
    while not sta_if.isconnected():
        print(".", end="")
        elapsed = time.ticks_diff(time.ticks_ms(), start) / 1000.0
        if elapsed >= timeout:
            raise Exception("WiFi connection timed out")
        time.sleep(0.2)

    print(' success')


def send_notification(topic, text):
    """
    Ref https://docs.ntfy.sh/publish/#send-http-request
    """

    data = text.encode('utf-8')
    r = requests.post("https://ntfy.sh/"+topic, data=data)
    if r.status_code != 200:
        raise Exception(f"Response error status={r.status_code}")

def main():

    # wait for WiFi
    connect_wifi()

    topic = NOTIFICATION_TOPIC
    send_notification(topic, "hello")
    print("Notification sent on topic", "https://ntfy.sh/"+topic)

if __name__ == '__main__':
    main()
