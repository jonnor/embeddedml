
import bluetooth
import asyncio
import aioble
import struct

def manufacturer_specific_advertisement(data : bytearray, manufacturer=[0xca, 0xab], limited_disc=False, br_edr=False):
    _ADV_TYPE_FLAGS = const(0x01)
    _ADV_TYPE_CUSTOMDATA = const(0xff)
    _ADV_MAX_PAYLOAD = const(31)

    payload = bytearray()

    def _append(adv_type, value):
        nonlocal payload
        payload += struct.pack("BB", len(value) + 1, adv_type) + value

    # Flags
    _append(
        _ADV_TYPE_FLAGS,
        struct.pack("B", (0x01 if limited_disc else 0x02) + (0x18 if br_edr else 0x04)),
    )

    # Specify manufacturer-specific data
    manufacturer_id = bytearray(manufacturer)
    _append(_ADV_TYPE_CUSTOMDATA, (manufacturer_id + data))

    if len(payload) > _ADV_MAX_PAYLOAD:
        raise ValueError("advertising payload too large")

    return payload

async def ble_advertise(data : bytearray, duration_ms=1000, interval_ms=250):

    #adv_data = manufacturer_specific_advertisement(data)
    
    interval_us = int(interval_ms*1000)

    try:
        print('ble-advertise-start')
        async with await aioble.advertise(
            interval_us,
            connectable=False,
            name=None,
            #adv_data=adv_data,
            timeout_ms=duration_ms,
            manufacturer=(0xabcd, data)
        ) as connection:
            print('ble-connect')
            pass

    except asyncio.TimeoutError:
        # expected, we want to stop nicely in this case
        print('ble-advertise-stop')
        pass


async def ble_task():

    sequence_no = 0

    while True:
        await ble_advertise(bytearray([0xAA, sequence_no]))
        print('sleep-start')
        await asyncio.sleep(10.0)
        print('sleep-done')

        sequence_no += 1

# Run both tasks.

async def main():
    t1 = asyncio.create_task(ble_task())
    #t2 = asyncio.create_task(ble_task())
    await asyncio.gather(t1)

asyncio.run(main())
