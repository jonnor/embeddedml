
import sys

from micropython import const

import machine
import asyncio
import aioble
import bluetooth

import time
import random
import struct

# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000


async def send_data(data):

    # Register GATT server.
    temp_service = aioble.Service(_ENV_SENSE_UUID)
    temp_characteristic = aioble.Characteristic(
        temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
    )
    aioble.register_services(temp_service)

    temp_characteristic.write(data, send_update=False)

    print('start advertise')
    try:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="mpy-temp",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
            timeout_ms=5000,
        ) as connection:
            print("Connection from", connection.device)

            #await connection.disconnected(timeout_ms=None)

            #await asyncio.sleep_ms(1000) # so data can be transmitted

            print('wrote data')
            await asyncio.sleep_ms(1000) # so data can be transmitted

    except asyncio.TimeoutError as e:
        print('connection-timeout', e)


# Run both tasks.
async def main():

    # NOTE: anything over 253 bytes gets silently truncated
    data = bytearray(250)
    sequence_no = 0

    while True:
        print('iter', sequence_no)

        struct.pack_into("<h", data, 0, int(sequence_no))
        struct.pack_into("<h", data, len(data)-2, int(sequence_no))

        t = asyncio.create_task(send_data(data))
        await asyncio.gather(t)
        sequence_no += 1

        aioble.stop()
        machine.lightsleep(1000)
        #time.sleep_ms(1000)


machine.freq(80000000)

asyncio.run(main())


