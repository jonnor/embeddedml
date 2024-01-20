
# Connectivity

- 315Mhz/433 Mhz. Below `0.1 USD @ 1k`
- BLE. From `0.2 USD @ 1k`
- USB

## USB

CH340 US $0.2848


## Bluetooth 

#### Holtek BC7161
BLE beacon IC
`0.2 USD @ 1k`. 
SO8 package
https://www.holtek.com/productdetail/-/vg/BC7161
Communication over I2C

Holtek BC7262
SO10 package
Communication over I2C

### BLE advertisement

Non-connectable Undirected — This type is used to broadcast to all devices.
The result is one-way communication, where the information is transmitted from a device.


### Manufacturer ID

Need to get from the Bluetooth SIG.
Seems 

### Advertizement payload size

> If you are using legacy advertising packets,
> you can include up to 27 bytes of actual data
> (using the Manufacturer Specific Data type)

https://novelbits.io/maximum-data-bluetooth-advertising-packet-ble/

Two first octets shall contain a company identifier from the
company identifier assigned numbers (free to obtain for Bluetooth SIG members)

Examples

0x09A3 ARDUINO SA
0xFEBB adafruit industries
0x0059 Nordic semi
0x0030 ST Microelectronics

Nothing for Holtek Semiconductor?
What do they use in their example code?

### Advertisement

20 ms to 10.24 seconds, in steps of 0.625ms

Guidelines

    Less than 100ms - for very aggressive connections and usually for short periods of time
    100ms to 500ms - normal fast advertising for most devices
    1000ms to 2000ms for devices that connect to gateways and where latency is not critical

### Channel selection

Recommended is to advertise on all (3) channels


### Forwarding using Android

#### ThingsUp BLE scanner

https://play.google.com/store/apps/details?id=io.thingsup.blescanner&hl=en&gl=US
Free
Captures raw data in the logs
Can export to CSV/Excel
Can transmit data via MQTT
? can it run on startup

Custom application.
Can of course be written in Java
But Kivy also allows to write such in Python

BluetoothDispatcher
    def on_device(self, device, rssi, advertisement):
