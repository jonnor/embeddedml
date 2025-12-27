
import struct
import bluetooth
import asyncio

def manufacturer_specific_advertisement(data : bytearray,
    manufacturer=[0xca, 0xab],
    limited_disc=False,
    br_edr=False):
    """Format BLE advertisement for Manufacturer specific data"""
    _ADV_TYPE_FLAGS = const(0x01)
    _ADV_TYPE_CUSTOMDATA = const(0xff)
    _ADV_MAX_PAYLOAD = const(31)

    payload = bytearray()

    # Advertising payloads are repeated packets of the following form:
    #   1 byte data length (N + 1)
    #   1 byte type (see constants below)
    #   N bytes type-specific data
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

async def send_bluetooth_le(sequence,
        advertisements=4,
        advertise_interval_ms=50,
        format=0xAA,
        version=0x01):
    """
    Send data as BLE advertisements
    Delivery of advertisements are not guaranteed. So we repeat N times to have a decent chance
    """

    # Start BLE
    ble = bluetooth.BLE()   
    ble.active(True)
    mac = ble.config('mac')

    # Encode data as BLE advertisement. Max 29 bytes
    data = bytearray()
    data += struct.pack('B', format)
    data += struct.pack('B', version)
    data += struct.pack('>H', sequence)

    # FIXME: encocde the payload

    payload = manufacturer_specific_advertisement(data)

    print('ble-advertise', 'mac='+mac[1].hex(), 'data='+data.hex())

    # send and wait until N advertisements are sent
    advertise_us = int(1000*advertise_interval_ms)
    ble.gap_advertise(advertise_us, adv_data=payload, connectable=False)
    await asyncio.sleep(advertisements*advertise_interval_ms/1000.0)

    # Turn of BLE
    ble.active(False)


async def send_ble_loop():

    counter = 0
    while True:
        print('send-ble-iter', counter)
        await send_bluetooth_le(sequence=counter)
        await asyncio.sleep(10)
        counter += 1

async def start():

    # TODO: also have sensor read task
    send_ble_task = asyncio.create_task(send_ble_loop())
    await asyncio.gather(send_ble_task)

    await asyncio.sleep(1)

try:
    asyncio.run(start())
finally:
    asyncio.new_event_loop()  # Clear retained state


