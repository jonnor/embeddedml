"""
Get current weather from OpenMeteo
"""

import asyncio
import time
import json
import requests

from urllib_parse import urlencode

def openmeteo_current_weather(latitude, longitude):
    # NOTE: must respect rate limiting

    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
    }

    p = urlencode(params)
    print(p)
    url = url + '?' + p

    r = requests.get(url)

    print(r.status_code)

    print(r.content)

    data = r.json()
    temp = data["current"]["temperature_2m"]

    return temp

OSLO_LATLON = (59.91, 10.75)
latitude, longitude = OSLO_LATLON
temperature = openmeteo_current_weather(latitude, longitude)
print('Temperature', temperature)

