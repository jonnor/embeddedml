
import machine
import network

from microdot import Microdot

app = Microdot()

@app.route('/')
async def index(request):
    return send_file('index.html')

from microdot import send_file

@app.get('/data.csv')
async def index(request):
    return send_file('data.csv')

SSID='bitraf'
PASSWORD='grimbadgerassault'

def do_connect():
    wlan = network.WLAN()
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            machine.idle()
    print('network config:', wlan.ipconfig('addr4'))

if __name__ == '__main__':
    do_connect()
    app.run(port=5000)
