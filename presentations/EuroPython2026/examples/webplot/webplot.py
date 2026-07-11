
import machine
import asyncio
import time
import os

# mpremote mip install https://raw.githubusercontent.com/miguelgrinberg/microdot/refs/heads/main/src/microdot/microdot.py
from microdot import Microdot
from microdot import send_file

app = Microdot()

WIFI_SSID='Wokwi-GUEST'
WIFI_PASSWORD='wokwiwokwi'

@app.route('/')
async def index(request):
    return send_file('index.html')

@app.get('/data.csv')
async def index(request):
    return send_file('data.csv')

async def do_connect(timeout=30.0):
    try:
        import network
    except ImportError:
        # assuming we are on Unix/PC
        return 'localhost'

    wlan = network.WLAN()
    wlan.active(True)
    start = time.ticks_ms()
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            duration = time.ticks_diff(time.ticks_ms(), start) / 1000
            if duration > timeout:
                raise Exception("Wifi timeout")
            await asyncio.sleep(0.1)
    host = wlan.ipconfig('addr4')[0]
    return host

async def sensor_task():

    with open('data.csv', 'w') as f:
        f.write('time,measurement\n')

    adc = machine.ADC(machine.Pin(26))

    while True:
        t = time.time()
        measurement = adc.read_u16()
        print('measure', t, measurement)

        with open('data.csv', 'a') as f:
            f.write(f'{t},{measurement}\n')

        await asyncio.sleep(2.0)

async def main():

    # check that we have neccesary html file
    os.stat('index.html')

    port = 5000
    host = await do_connect()
    print(f'Server: http://{host}:{port}')

    # runs forever
    task1 = asyncio.create_task(app.start_server(debug=True, port=port))
    task2 = asyncio.create_task(sensor_task())
    await asyncio.gather(task1, task2)

if __name__ == '__main__':
    asyncio.run(main())

