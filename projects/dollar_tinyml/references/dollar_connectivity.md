
# Connectivity

- 315Mhz/433 Mhz. Below `0.1 USD @ 1k`
- BLE. From `0.2 USD @ 1k`
- USB. 

## Usecases

Transmitting regularly.
For at 1 second to 10 minute intervals, and up to 29 bytes.
Can use BLE.
Receive with smartphone or PC.

Dumping a batch of data.
For example 1 MB, collected over some hours or days.
Use USB? Tricky, most solutions too expensive.
Use SDcard? Unknown

## Audio

http://web.eecs.umich.edu/~prabal/projects/hijack/

## Visible light / LEDs

### WebJack
https://webjack.io/

SoftModem Arduino library
to create two-way communication between a browser windo
Bell 202 modem-like
FSK 1225 bit/s


#### HiJack
300 baud data transfer using Bell 202 FSK signaling, or
8.82 kbaud using a Manchester-encoded, direct-digital communication using hardware accelerators on the HiJack microcontroller.

https://github.com/ggerganov/ggwave
8-16 bytes/sec depending on the protocol parameter
Provides libraries for many platforms, including Arduino and WebAssembly

https://github.com/weckbach/AstroMech


https://github.com/cstroie/Arabell300
Frequency modulated (FM) protocol
Old school Arduino modem, Bell 103 compatible, at 300 baud

#### Audio jack hardware

Needs to be 4 pin for 2 way communication.
Several options at LCSC at decent prices.

Shenzhen Kinghelm Elec KH-PJ-313B-6P
1000+ 	US$0.0518 	US$ 51.80
HC-PJ-3134-6P-D
HC-PJ-313E8-B-SMT
PJ-313B6-B


## USB

Having ability to do USB Mass Storage would enable sensor
to be a "USB stick" that one can dump data from.
This is useful for "data logger" type deployments,
where sensor is running autonomously for some hours/days (possibly on battery),
but it is OK to get the results as one batch afterwards.
As opposed to a 24/7 autonomous system that transmits data continious all the time.

CH552G. 16 kB FLASH, 1.25 kB RAM. USB. 8 bit
1000+ US$0.3103 
https://www.wch-ic.com/products/CH552.html

CH32V003 bitbang USB
https://github.com/cnlohr/rv003usb/tree/master

CH32V103 USB 2.0. 1000+ US$0.7207 
Has USB, but too expensive

CH32X035 has built-in USB and PD PHY
https://www.wch-ic.com/products/CH32X035.html
Scale pricing not available?
AliExpress has 20 pcs for 13 USD, so should be sub 1 dollar.
50 cent maybe?

Puya PY32.
Open issue for software/bitbanging based USB
https://github.com/IOsetting/py32f0-template/issues/12


Cortex M0+ software bitbanged
Has been demonstrated to work on 48 Mhz units, since 2015
But never really deployed widely?
https://github.com/lemcu/LemcUSB
https://github.com/xobs/grainuum


USB to serial chips. CH340 US $0.2848. Nothing cheaper?
Can only act as serial device.
Not very useful. And the same cost as the entire microcontroller.

For Atmel AVR8 there are multiple software-only USB projects, notably V-USB and USBTiny.
https://www.obdev.at/products/vusb/index.html
https://dicks.home.xs4all.nl/avr/usbtiny/

TinyUSB is a popular microcontroller USB stack,
but I am pretty sure it requires USB pheripherals in hardware.
https://github.com/hathach/tinyusb
https://github.com/dmitrystu/libusb_stm32

TinyUSB mass storage example
https://github.com/hathach/tinyusb/blob/master/examples/device/cdc_msc/src/msc_disk.c
16 blocks a 512 bytes = 8kB. Said to be smallest that Windows will mount
FAT32 file system is exposed.


## SDCard
Many (most?) people have an (micro) SDcard reader.
Could one provide that interface, in order to be able to drop files?
Need to emulate both the communication protocol, the electrical levels, and the physical/mechanical interface.

Protocol
Can the SPI pheripheral be used?
Are there software implementations available?

Mechanical, SD


Mechanical, microSD
Is thinner than 1.6 mm PCB? Only around 10 mm wide.


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
