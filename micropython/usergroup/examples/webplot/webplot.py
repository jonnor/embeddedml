
import machine
import network
import esp32
import asyncio
import time

from microdot import Microdot
from microdot import send_file

app = Microdot()

SSID='bitraf'
PASSWORD='grimbadgerassault'

#temp_adc = machine.ADC(machine.Pin(4), atten=machine.ADC.ATTN_6DB)
#temp_adc.atten(machine.ADC.ATTN_11DB)

@app.route('/')
async def index(request):
    return send_file('index.html')

@app.get('/data.csv')
async def index(request):
    return send_file('data.csv')


def do_connect():
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))


def fahrenheit_to_celsius(fahrenheit):
    celsius = (fahrenheit - 32.0) * 5.0 / 9.0
    return celsius


async def other_task():

    with open('data.csv', 'w') as f:
        f.write('time,measurement\n')

    adc = machine.ADC(machine.Pin(36), atten=machine.ADC.ATTN_0DB)

    while True:

        t = time.time()
        #r = esp32.raw_temperature()
        m = adc.read()

        print('measure', t, t, m)
        with open('data.csv', 'a') as f:
            f.write(f'{t},{m}\n')

        await asyncio.sleep(2.0)

async def main():

    # runs forever
    task1 = asyncio.create_task(app.start_server(debug=True, port=5000))
    task2 = asyncio.create_task(other_task())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    do_connect()
    asyncio.run(main())

