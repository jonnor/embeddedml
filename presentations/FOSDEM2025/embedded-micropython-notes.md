

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


# Talk planning

### Format

25 minutes, including Q&A ?

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

### Goal

Audience target.
Embedded software developer.
Professional or hobbyist



### Scope

- Focusing on relevance to sensor-systems
Sensor communication.
Data processing (incl potentially DSP and ML).
Sending data. Connectivity
- Not covering other use-cases
Graphics/screens, user interfaces
Low-latency or real-time. Where low is under 10 milliseconds
- Dynamic native C modules, how they enable efficient & convenient
- Embedded Linux. Brief


### Outline

Introduction

- About Soundsensing
- MicroPython related at FOSDEM. Stand, presentation tomorrow
- Goal / Scope of talk
- Outline

Introduction to MicroPython

- About the project
- Where does it fit/not
- Trying it out

What MicroPython provides

- It is Python. Supported/not
- Basic HAL. GPIO, I2C, SPI
- Connectivity. WiFi, BLE
- File system
- Package manager
- C modules
- ? Testing
- ? Caveats. GC, latency, interrupts
- Reading sensors. I2C/SPI
- Reading audio. I2S. No PDM :((
- Reading camera. Library on ESP32. OpenMV

Sensors with MicroPython and emlearn

- DSP with emlearn-micropython. FFT, IIR. Audio. scipy.signal
- Classic ML with emlearn-micropython. RF, HAR. scikit-learn
- Deep learning with emlearn-micropython. CNN, image. Keras/Tensorflow

MicroPython on Embedded Linux

- Motivation. Low memory systems
- Unix port limitations
- ? State of embedded distros

Dropped / bonus

- Embedding
- Inline assemblers. ARM. PIO


#### Where does MicroPython fit in the embedded toolbox

Great for

- Devices with 1+ MB RAM/FLASH
- Fast time-to-market
- Ease of customization
- End-user customization/scripting
- Explorative/iterative uses. Hardware bringup

Not good for

- Devices with under 100 kB RAM
- Very low power devices.
Sleep modes are not that well supported. NRF5x, the best low-power BLE
- ?

Usecases that need extra care

- Low-latency and real-time
Interrupts on some ports are soft interrupts, meaning scheduled by OS.
ESP32=soft only. STM32=hard capable.
Garbage collector can easily introduce variable latency
Consider doing low-latency sensitive things in C module, or dedicated microcontroller peripherals (PIO on RP2xxx).
Or dedicated core running C.

#### Pros and cons

Benefits

- Easy programming language
- Portable. To different microcontroller
- High-level facilities. File system etc
- Good connectivity. WiFi, BLE
- C modules. Native
- Convenient automated testing. Python language
- Support for embedding the interpreter

Disadvantages

- Garbage collector. Mark and sweep.
Will give delays. Typically 1-10 millisecond order. Can be higher. Slow/external RAM especially.
- Startup time. Can suffer with large modules/programs
- Library ecosystem is not so mature
A lot of MicroPython modules found on Github are one-off hobby projects
micropython-lib

#### Sensor reading I2C/SPI accel


jonnor/micropython-mpu6886
https://github.com/jonnor/micropython-mpu6886/

Implementing an IMU/accelerometer/gyro driver? Use the FIFO!
https://github.com/orgs/micropython/discussions/15512 


#### Getting started super easy

#### REPL in browser

https://pyscript.net/
has MicroPython on the frontpage

#### Simulator in browser

https://wokwi.com/projects/305569065545499202

#### ViperIDE



## Call to Action

Try out MicroPython today.

Either on PC using Unix port.
Or recommend ESP32 or RPi Pico W as first hardware.

Interested in sensor data processing, Digital Signal Processing and Machine Learning
- try out the emlearn-micropython library



## MicroPython on Embedded Linux

### MicroPython much more space efficient

RAM and FLASH

/usr/bin/time -v python -c "print('hello world')" 2>&1 | grep 'Maximum resident'
	Maximum resident set size (kbytes): 12264

/usr/bin/time -v micropython -c "print('hello world')" 
	Maximum resident set size (kbytes): 4144


/usr/bin/time -v python -c "import array; arr = array.array('f', range(100))"
	Maximum resident set size (kbytes): 13156

/usr/bin/time -v python -c "import numpy; a = numpy.zeroes(100)"
	Maximum resident set size (kbytes): 29860

/usr/bin/time -v micropython -c "import array; arr = array.array('f', range(100))"
	Maximum resident set size (kbytes): 4316


/usr/bin/time -v python -c "from sklearn.ensemble import RandomForestClassifier; est=RandomForestClassifier()"
	Maximum resident set size (kbytes): 128224


/usr/bin/time -v micropython -X heapsize=10M test_trees.py 
1000000

100 trees, 4k nodes per tree (max_depth=12)

	Maximum resident set size (kbytes): 6552

### Good fit for devices with limited RAM

Especially for devices with < 512 MB RAM and FLASH
For example OpenWRT.
Gateway type devices, etc.

For example,
- GL.iNet Puli (GL-XE300).
CPU: QCA9531. Memory / Storage: DDR2 128MB / NOR Flash 16MB + NAND Flash 128MB.
- GL.inet Mango (GL-MT300N-V2). 128 MB RAM / 16 MB FLASH.
- Ralink RT5350
https://www.olimex.com/Products/OLinuXino/RT5350F/RT5350F-OLinuXino-EVB/open-source-hardware
MIPS24KEc

New boards with under 512 MB RAM getting more rare though.

- STM32MP1 ist mostly 512 MB
- Raspberry PI Zero 512 MB

### Limitations of Unix port

Very limited hardware access

Not implemented:

- GPIO. machine.Pin / machine.PWM / machine.ADC
- Digital busses. machine.I2C / SPI / USART / USB
- Watchdog Timer. machine.WDT
- Power management. machine.lightsleep() / machine.deepsleep()
- Audio input/microphone
- Camera access

Would need to write C or Python modules for this.
Or call external programs.

GPIO in Linux is exposed in sysfs as files, can be done with pure Python 

### State of MicroPython packaged in embedded distros

- OpenWRT. Seems reasonably well maintained.
- Buildroot. Now ships 1.22 (released December 2023). Long lag before that
- Alpine. 1.24. But not built with TLS... Less useful
- Yocto/OpenEmbedded. External layer. Not updated for 3+ years



### Notes

Faster development
Ref Matt Trentini
Medical devices

Especially relevant for teams that already know Python.
Or where improving Python skills are useful
Python becoming a more common tooling and testing language
Also a data processing, data analysis tooling, engineering
And of course the predominant for Machine Learning



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


## MicroPython in PyScript

https://docs.pyscript.net/2024.11.1//user-guide/running-offline/#download-micropython-locally
Describes no

How to include modules?

External modules may work as-is?
Assuming that one builds a custom MicroPython for WASM.

https://github.com/micropython/micropython/blob/master/ports/webassembly/Makefile
uses generic stuff.
May support USER_C_MODULES ?

https://github.com/pyscript/MicroPyScript/blob/main/Makefile
example of including ulab


MICROPY_DIR=micropython/ mpbuild build webassembly
Sorry, builds are not supported for the webassembly port at this time

make USER_C_MODULES=./micropython-ulab/ -j4

Failed with
error: use of undeclared identifier 'MP_QSTR_linalg'

make USER_C_MODULES=./micropython-ulab/code/ -j4

Builds.
Need to use the module directory that contains micropython.mk/micropython.cmake

## MicroPython in JupyterLite

As of January, does not seem to be any well supported option?


https://github.com/kumekay/mpy-web-kernel
last updated in 2022

https://github.com/espressif/jupyter-lite-micropython
no actual commits yet

https://jupyterlite.readthedocs.io/en/latest/howto/configure/kernels.html

Neither pyiodine nor xeus seem to have MicroPython support?

