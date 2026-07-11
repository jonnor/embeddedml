"""
Get current weather from OpenMeteo
"""

import asyncio
import time
import json
import requests

WIFI_SSID='Wokwi-GUEST'
WIFI_PASSWORD='wokwiwokwi'

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

def openmeteo_current_weather(latitude, longitude):
    # NOTE: must respect rate limiting

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "",
    }
    metrics = ",".join(['temperature_2m','wind_speed_10m'])
    url = url + '?' + f'latitude={latitude:4f}&longitude={longitude:.4f}&current={metrics}'
    r = requests.get(url)

    if not r.status_code == 200:
        raise Exception(f'Error: {r.content}')

    data = r.json()
    temp = data["current"]["temperature_2m"]

    return temp

def main():

    # wait for WiFi
    connect_wifi()

    OSLO_LATLON = (59.91, 10.75)
    latitude, longitude = OSLO_LATLON
    temperature = openmeteo_current_weather(latitude, longitude)
    print('Temperature', temperature)

if __name__ == '__main__':
    main()

