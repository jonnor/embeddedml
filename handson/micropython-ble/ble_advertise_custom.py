
from micropython import const
import struct
import bluetooth
import machine
import time

def manufacturer_specific_advertisement(data : bytearray, manufacturer=[0xca, 0xab], limited_disc=False, br_edr=False):
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

def serialize_data(sequence : int, format=0xAA, version=0x01):
    data = bytearray()
    
    data += struct.pack('B', format)
    data += struct.pack('B', version)
    data += struct.pack('>H', sequence)

    return data
    

def main():

    advertise_interval_ms = 250
    sleep_ms = 5*1000

    sequence_no = 0


    while True:

        print('start', sequence_no)

        ble = bluetooth.BLE()
        ble.active(False)
        time.sleep_ms(100)
        # XXX: this sometimes times out if device has been reconnected
        ble.active(True)

        mac = ble.config('mac')
        print('mac', mac)

        d = serialize_data(sequence_no)
        payload = manufacturer_specific_advertisement(d)

        print(payload)

        ble.gap_advertise(int(1000*advertise_interval_ms), adv_data=payload, connectable=False)
        time.sleep_ms(1000)

        print('sleep', sequence_no)
        sequence_no += 1
        time.sleep_ms(sleep_ms)
        #machine.lightsleep(sleep_ms)

if __name__ == "__main__":
    main()
