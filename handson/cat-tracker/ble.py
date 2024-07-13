
import sys

from micropython import const

import asyncio
import aioble
import bluetooth

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


# Register GATT server.
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)



# This would be periodically polling a hardware sensor.
async def sensor_task():
    t = 24.5
    # NOTE: anything over 253 bytes gets silently truncated
    data = bytearray(250)
    sequence_no = 0
    while True:

        struct.pack_into("<h", data, 0, int(sequence_no))
        struct.pack_into("<h", data, len(data)-2, int(sequence_no))
        temp_characteristic.write(data, send_update=True)

        print('write new', sequence_no)
        await asyncio.sleep_ms(100)
        sequence_no += 1


# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        print('start advertise')
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="mpy-temp",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected(timeout_ms=None)


# Run both tasks.
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    await asyncio.gather(t1, t2)


asyncio.run(main())

