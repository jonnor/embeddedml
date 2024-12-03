from mqtt_as import MQTTClient, config
import asyncio

# Local configuration
config['ssid'] = 'FIXME'  # Optional on ESP8266
config['wifi_pw'] = 'FIXME'
config['server'] = 'test.mosquitto.org'

async def main(client):
    print('main-start')
    await client.connect()
    print('connected')
    
    n = 0
    while True:
        await asyncio.sleep(5)
        print('publish-data', n)
        await client.publish('pydataglobal2024/send', '{}'.format(n), qos = 0)
        n += 1

MQTTClient.DEBUG = True  # Optional: print diagnostic messages
client = MQTTClient(config)
try:
    asyncio.run(main(client))
finally:
    client.close()  # Prevent LmacRxBlk:1 errors
