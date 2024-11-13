
# Python devroom proposal
https://lists.fosdem.org/pipermail/fosdem/2024q4/003564.html

## Topics
* Data science, AI and Machine Learning
* MicroPython, CircuitPython, embedded software

## Format
25 minutes presentation, including Q&A, if any.

## Title
Sensing the world with MicroPython and microcontrollers

## Abstract

Being able to measure physical phenomena is critical to many areas of science and engineering; from measuring pollution in public spaces to monitoring of critical infrastructure. Over the last decades, the capabilities and costs of sensor system has become much better, driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication. Thanks to this Wireless Sensor Networks and "Internet of Things" (IoT) sensor systems are becoming common.

Typical sensor nodes use microcontroller-based hardware, and the firmware developed primarily using C (or C++). However, it is now becoming feasible to write microcontroller firmware using Python. This is thanks to the MicroPython project, combined with affordable and powerful hardware from the last couple of years. Using the familiar and high-level Python programming language makes the process of creating sensor nodes more accessible to an engineer or scientist.

In this talk we will discuss developing microcontroller-based sensors using MicroPython. This includes a brief introduction to MicroPython, best practices for high-rate data processing in limited RAM/FLASH/CPU, and energy efficiency wrt to wireless protocols.
We will share our experience applying this to process accelerometer, image, and microphone data; using both Digital Signal Processing and Machine Learning techniques. We will apply some functionality, techniques, and lessons learned from the emlearn-micropython project - a Machine Learning and Digital Signal Processing library for MicroPython. Code available at: https://github.com/emlearn/emlearn-micropython

Intended audience: Any developer or data scientist curious about sensor data processing, IoT, and how Python scales down to the smallest of devices.

## Notes
Improved version of a talk given at PyConZA 2024.

## Call to Action
Try building sensors. It is fun and practical!
You can use the Python that you already know!

## Outline

Start from PyData Global 2024, or PyCon ZA 2024.
Add in a practical bit? Demo/walkthrough. With ViperIDE.


# Low level AI hacking devroom


## Call

https://aifoundry.org/fosdem-2025-low-level-ai-engineering-hacking-dev-room

We are  bringing together the top developers working on the essential “plumbing” of the AI industry:
hardware accelerators, math kernel libraries, model quantization techniques, low-level inference, fine-tuning engines, distributed and rack-scale computing, and more
 Together, we will spend the day discussing core designs and collaborating to solve governance problems. 

We are looking for low-level AI core open source project maintainers and committers (such as ggml, llama.cpp and llamafile),
downstream projects building on top of these (for example,  ollama, ramalama and Podman AI Lab),
as well as end-users of AI stacks to speak about their work and expertise.

## Format
Single track, 10 - 20 minute technical session

## Abstract



## Takeaways


### Notes

Quick introduction to the emlearn project
TinyML. Very small models. High energy efficiency. Computational efficiency in terms of RAM.
Massive scale in terms of number.
Measurig and analzying the world continiously.

We believe there are collaboration opportunities

Over 30 billion microcontrollers are shipped annually


TinyML market will grow from 15.2 million shipments in 2020 to 2.5 billion in 2030. 
https://www.abiresearch.com/press/tinyml-device-shipments-grow-25-billion-2030-15-million-2020/

TinyML device installs will increase from nearly 2 billion in 2022 to over 11 billion in 2027
https://www.abiresearch.com/press/11-billion-tinyml-device-installs-481-million-5g-advanced-devices-in-2027-and-35-other-transformative-technology-stats-you-need-to-know/

Keyword spotting.
Wearable devices.
Sleep quality tracking.

<1 USD microcontroller
<1 USD MEMS sensor

emlearn since 2018


Efficiency has improved a lot
https://www.sciencedirect.com/science/article/pii/S2210537923000124
2012 -> 2022. 1.0 to 1000.0 GFLOPS
56% to 90% top1 accuracy
At 1 GFLOP, up to 82% in 2020

10x improvement in GFLOPS/watt



## Embedded devroom
https://lists.fosdem.org/pipermail/fosdem/2024q4/003575.html

## Title
MicroPython - Python for microcontrollers and Embedded Linux

### Abstract

MicroPython is a tiny implementation of Python,
designed for very contrained environments such as microcontrollers and embedded devices.
It can run on devices with a little as 64 kB of RAM and 256 kB of FLASH.
Over the last 10 years, MicroPython has become a productive development environment and mature platform for firmware development.
It has been used in a wide range of applications - and has been deployed on everything from smartwatches to medical devices and sattelites.

In this talk will discuss some of the features of MicroPython and the surrounding ecosystem,
with an emphasis on applications for Internet of Things (IoT) sensors.
This includes the for example: writing efficient code using JIT compilation and C modules,
using the built-in file systems, installing packages via package manager,
communication over WiFi/Ethernet/BLE/USB/etc,
interactive programming via REPL, automated testing on PC and device,
and probably some more things.


### Outline


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


FROM openwrt/rootfs:latest
RUN mkdir /var/lock/ && opkg update && opkg install micropython
ENTRYPOINT ["micropython"]

Can make HTTPS requests


# Aside - YouTube video - TinyML zero to hero
From nothing to running a (premade) TinyML example.
With MicroPython, emlearn and ViperIDE - on ESP32.

Script.

- Select a ready-made device. ESP32. LilyGO / M5Stack
- Order it. Online. Wait some days
- Unbox. Plug it in. Shows USB device
- pip install esptool
- Flash with esptool
- Open browser, ViperIDE
- Connect to device - MicroPython terminal. Make LED blink?
- Open example.
