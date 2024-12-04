from mqtt_as import MQTTClient, config
import asyncio
from mpu6886 import MPU6886
from machine import I2C

# Local configuration
config['ssid'] = 'FIXME'  # Optional on ESP8266
config['wifi_pw'] = 'FIXME'
config['server'] = 'test.mosquitto.org'

mpu = MPU6886(I2C(0, sda=21, scl=22, freq=100000))

async def main(client):
    print('main-start')
    await client.connect()
    print('connected')
    
    while True:
        t = mpu.temperature
        print('publish-data', t)
        await client.publish('pydataglobal2024/send', f'{t:.2f}', qos = 0)
        await asyncio.sleep(30)

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()
