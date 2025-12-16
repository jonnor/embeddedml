
from mqtt_as import MQTTClient, config
import asyncio

import machine

# GPIO 19 is red LED on M5Stick PLUS 2
led = machine.Pin(19, machine.Pin.OUT)

# Local configuration
config['ssid'] = 'bitraf'  # Optional on ESP8266
config['wifi_pw'] = 'grimbadgerassault'
config['server'] = 'test.mosquitto.org'  # Change to suit e.g. 'iot.eclipse.org'
config['port'] = 0 # 0 is default

prefix = 'micropython-oslo/jon'

async def messages(client):
    # Respond to incoming messages
    async for topic, msg, retained in client.queue:
        data = bool(int(msg.decode()))
        print('Received', topic.decode(), msg.decode(), data)
        led.value(data)

async def up(client):  # Respond to connectivity being (re)established
    while True:
        await client.up.wait()  # Wait on an Event
        client.up.clear()
        # renew subscriptions
        await client.subscribe(prefix+'/led', 1) 

async def main(client):
    
    await client.connect()
    
    # setup tasks
    for coroutine in (up, messages):
        asyncio.create_task(coroutine(client))
        
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish', n)
        # NOTE: If WiFi is down the following will pause for the duration.
        await client.publish(prefix+'/count', '{}'.format(n), qos = 1)
        n += 1

config["queue_len"] = 1  # Use event interface with default queue size
MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
    