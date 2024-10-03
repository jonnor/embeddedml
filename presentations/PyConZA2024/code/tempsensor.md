
# XXX: pseudo-code, not fully ran

import machine

N_SAMPLES = 10
SAMPLE_INTERVAL = 1.0
SLEEP_INTERVAL = 60.0

analog_input = machine.ADC(machine.Pin(22))
samples = array.array('H', range(N_SAMPLES)) # raw values from ADC, as uint16
measurement_no = 0

while True:

    # collect data for measurement
    for i in range(N_SAMPLES):
        samples[i] = adc.read_u16()
        time.sleep(SAMPLE_INTERVAL)

    # aggregate samples, convert to temperature
    raw = median(samples)
    temperature = (raw * 0.323) - 50.0 # calculation depends on type of analog sensor

    # Do something with the measurement
    send_bluetooth_le(measurement_no, temperature)

    # sleep until next time to collect new measurement
    machine.lightsleep(int(SLEEP_INTERVAL*1000))
    measurement_no += 1

def median(data):
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2

def send_bluetooth_le(sequence, temperature, advertisements=4, advertise_interval_ms=250, format=0xAA, version=0x01):
    # ref https://github.com/jonnor/embeddedml/blob/master/handson/micropython-ble/ble_advertise_custom.py

    # Start BLE
    import bluetooth
    ble = bluetooth.BLE()   
    ble.active(True)

    # Encode data as BLE advertisement. Max 29 bytes
    data = bytearray()
    data += struct.pack('B', format)
    data += struct.pack('B', version)
    data += struct.pack('>H', sequence)
    data += struct.pack('>H', (temperature*100)) # centigrade signed integer

    payload = manufacturer_specific_advertisement(data)
    advertise_us = int(1000*advertise_interval_ms)
    ble.gap_advertise(advertise_us, adv_data=payload, connectable=False)

    time.sleep_ms(advertisements*advertise_interval_ms)

    # Turn of BLE
    ble.active(False)

