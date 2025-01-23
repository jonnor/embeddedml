

## Embedded devroom
https://lists.fosdem.org/pipermail/fosdem/2024q4/003575.html

## Title
MicroPython - Python for microcontrollers and Embedded Linux

### Abstract

MicroPython is a tiny implementation of Python,
designed for very contrained environments such as microcontrollers and embedded devices.
It can run on devices with as little as 64 kB of RAM and 256 kB of FLASH.
Over the last 10 years, MicroPython has become a productive development environment and mature platform for firmware development.
It has been used in many applications - and has been deployed on everything from smartwatches to medical devices and satelites.

There are many features of MicroPython that make it an attractive way of developing firmware,
such as: the built-in file systems, first-class package management, built-in communication over WiFi/Ethernet/BLE/USB/etc,
interactive programming via REPL, automated testing on PC and device.
We will introduce these features briefly, and then discuss our favorite feature: the support for C modules,
and how it enables building sensor systems that are both computationally efficient and fast to develop.


### Outline

- MicroPython on Embedded Linux.
Especially for devices with < 512 MB RAM and FLASH, where regular Python.
For example OpenWRT.
Gateway type devices, etc.
For example, GL.iNet Puli (GL-XE300).
CPU: QCA9531. Memory / Storage: DDR2 128MB / NOR Flash 16MB + NAND Flash 128MB.
GL.inet Mango (GL-MT300N-V2). 128 MB RAM / 16 MB FLASH.


### Key takeaways

- Python can run on microcontrollers and embedded devices
- Acts like a full computer system.
REPL, file system, networking, package management, base drivers included
- Python has a good testing story
- Automated testing on host PC using Unix port
- Automated testing on-device using mpremote
- Combine C with Python. Not one or the other!
- Faster development compared to (modern) C
- Especially beneficial for teams who use Python for other things

=> fun and productive environment for wide range of usecases

Great for

- Devices with 1+ MB RAM/FLASH
- Microcontrollers with 
- Fast time-to-market
- Ease of customization
- End-user customization/scripting

Not good for

- Devices with under 100 kB RAM
- Very low power devices
- ?


Benefits

- Excellent testing support
- High-level facilities. File system etc
- Good connectivity. WiFi, BLE



### Notes

Faster development
Ref Matt Trentini
Medical devices

Especially relevant for teams that already know Python.
Or where improving Python skills are useful
Python becoming a more common tooling and testing language
Also a data processing, data analysis tooling, engineering
And of course the predominant for Machine Learning


## Call to Action
Try out MicroPython today.
Getting started.
For example on Unix. do
Recommend testing on ESP32 or RPi Pico W as first hardware.

## MicroPython on Alpine

FROM alpine:edge
RUN apk add --no-cache micropython
ENTRYPOINT ["micropython"]

docker run -it $(docker build -q .)

MicroPython v1.24.0 on 2024-10-30; linux [GCC 14.2.0] version
Use Ctrl-D to exit, Ctrl-E for paste mode
>>> import requests
>>> requests.get('https://google.com')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "requests/__init__.py", line 201, in get
  File "requests/__init__.py", line 69, in request
ImportError: no module named 'tls'

... not so useful

## MicroPython on OpenWRT

Available as official OpenWRT package for several years.

https://github.com/openwrt/packages/tree/master/lang/python/micropython

Ships 1.23 right now.

!! OpenWrt is transitioning from opkg to apk

rootfs image currently outdated.
Here is how to build https://github.com/openwrt/openwrt/issues/16935#issuecomment-2515575187

FROM openwrt/rootfs:latest
RUN mkdir /var/lock/ && opkg update && opkg install micropython
ENTRYPOINT ["micropython"]

Can make HTTPS requests.
Seems more useful.

## MicroPython on Buildroot

Ships MicroPython 1.22

https://github.com/open-power/buildroot/blob/master/package/micropython/micropython.mk



## MicroPython on own ASIC 

Mike Bell ported MicroPython to a RISC-V CPU deployed as an ASIC using the TinyTapeout project.

Twice! On TTO4 and TTO6
https://rebel-lion.uk/@mike/113778218386475967
https://github.com/MichaelBell/tinyQV/

https://rebel-lion.uk/@mike/112864886097489771

https://github.com/MichaelBell/tt04-nanoV
