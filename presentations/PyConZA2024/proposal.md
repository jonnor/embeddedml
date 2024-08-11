
## About
https://za.pycon.org/talks/how-to-submit-a-talk/

## Title

Sensor data processing on microcontrollers with MicroPython

## Abstract

Being able to measure physical phenomena is critical to many areas of science and engineering;
from measuring pollution in public spaces to monitorning of critical machinery.
Over the last decades the capabilities and costs of sensor system has become much better,
driven by improvements in microprocessors, MEMS sensor technology, and low-energy wireless communication.
Thanks to this Wireless Sensor Networks and "Internet of Things" (IoT) sensor systems are becoming common.

Typical sensor nodes use microcontroller-based hardware, and the firmware developed primarily using C (or C++).
However, it is now becoming feasible to write microcontroller firmware using Python.
This is thanks to the MicroPython project, combined with affordable and powerful hardware from the last couple of years.
Using the familiar and high-level Python programming language makes the process of creating sensor nodes
more accessible to an engineer or scientist.

In this talk we will discuss developing microcontroller-based sensors using MicroPython.
This includes a brief introduction to MicroPython, how to do efficient data processing,
and share our experience applying this to process accelerometer and microphone data,
using both Digital Signal Processing and Machine Learning techniques.

Intended audience: Any developer or data scientist curious about sensor data processing, IoT,
and how Python scales down to the smallest of devices.

Related open-source project: https://github.com/emlearn/emlearn-micropython

## Format

Remote Talk: A conference talk that will be presented remotely.
Talk slots are 30 minutes long, with an additional 10 minutes for discussion at the end.

## Categories

- Data Science: Talks on using Python to process and extract meaning from data. 
- Scientific Computing: Using python for scientific computing applications, not covered by the Data Science track 


## Bio

Jon is a Machine Learning Engineer specialized in IoT systems.
He has a Master in Data Science and a Bachelor in Electronics Engineering,
and has published several papers on applied Machine Learning,
including topics like TinyML, Wireless Sensor Systems and Audio Classification.

These days Jon is co-founder and Head of Data Science at Soundsensing,
a leading provider for condition monitoring solutions for commercial buildings and HVAC systems.
He is also the creator and maintainer of emlearn,
an open-source inference engine for microcontrollers and embedded systems.


## Description

Here is an overview of the topics you can learn about in this presentation.

#### Sensor nodes and Wireless Sensor Networks

A sensor node is a combined hardware + software system that can sense things in the physical world.
It uses sensor elements such as camera, microphone, accelerometer, radar, temperature et.c.
A node has a microcontroller that does data aquition and processing, and also some way of storing data,
or transmitting it to another system for further processing and storage.
The typical functional blocks of firmware for a sensor node are:

- Data readout. Fetching data from each of the attached sensors.
- Processing. Extracting useful information from the data.
- Data storage. Storing either for long term, or as a transmission buffer.
- Data transmission. Sending the extracted information to external systems.
- Power management. Transitioning between sleep and aware as needed.

For low cost installation and operation,
many sensor nodes are battery-powered and use wireless connectivity.
And they are often deployed together as part of larger Wireless Sensor Networks.

### About MicroPython
MicroPython is an implementation of Python that runs on practically all microcontrollers with 16kB+ RAM.
It provides access to the microcontroller hardware, functions for interacting with sensors and external pheripherals,
as well as connectivity options such as WiFi, Ethernet, Bluetooth Low Energy, etc.

While MicroPython (and the emlearn library) can target a very wide range of hardware,
we will focus on the Espressif ESP32 family of devices.
These are very powerful and affordable, with good WiFi+BLE connectivity support,
gpod open-source toolchains, are very popular both among hobbyist and companies,
and have many good ready-to-use hardware development kits.

#### Challenges and constraints of microcontroller-based sensor nodes
While microcontrollers are getting more powerful year by year,
it is still important to fit within the limited RAM, program size and CPU time available.
For sensors with low datarates (like accelerometers) this is rather doable,
but for higher datarates such as audio or images good practices can be critical.
Furthermore we may wish to operate on low-power with long battery life.
In that case it is critical to maximize sleeping, which means to reduce device wakeups,
and to quickly return back to sleep.
Ensuring that we stay within the resource budgets requires some care (in any programming language),
and a high-level language like Python poses some particular challenges.

#### Tools and practices for efficient sensor data processing in MicroPython
We will go through the tools which MicroPython provides for efficient sensor data processing.
This includes:

- Ways of writing (Micro)Python code that are faster. For example reducing allocations
- Optimizing subsets of Python using the @native and @viper code emitters
- The built-in Python-based assembler for ARM Cortex M chip
- Dynamic native C modules. Can be installed at runtime
- User C modules. Can be baked into a custom MicroPython image

We will compare these approaches on a few algorithms that are often used of typical sensor data processing.
This includes algorithms from the world of Digital Signal Processing as well as Machine Learning.
Candidates include Fast Fourier Transform (FFT), Root Mean Square (RMS),
Convolutional Neural Network (CNN), and Random Forest (RF).

The emlearn-micropython packages provided a set of MicroPython modules
that can be installed onto a device, without having to recompile any C code.
This preserves the ease-of-use that Python developers are used to on a desktop system.
Compared to pure-Python approaches, the emlearn-micropython modules are typically 10-100x faster.

#### Intended audience and expected background

Any developer or data scientist curious about sensor data processing, IoT,
and how Python scales down to the smallest of devices.

The audience is expected to have a basic literacy in Python, proficiency in programming,
and know the basics of data processing.
Some familiarity in time-series processing, Digital Signal Processing or 
Machine Learning, will make the talk much more relevant to you.
Familiarity with microcontrollers and embedded systems is of course an advantage
- but the talk should be approachable to those who are new to this area.

#### Focus and scope of the talk
The main part of the talk will be how to write efficient sensor processing code with MicroPython,
to document just how much is actually doable on a tiny system using Python.

The general introduction to MicroPython will be kept rather brief,
as there are many resources for this available already.

How to aquire data from sensors (such as accelerometer or microphone),
and how transmit data (using BLE or WiFi) will be covered very briefly.
An emphasis will be on techiques and practices that enable efficiency.

#### Resources

Extending MicroPython in C
https://docs.micropython.org/en/latest/develop/extendingmicropython.html

Maximising MicroPython speed
https://docs.micropython.org/en/latest/reference/speed_python.html

emlearn - Machine Learning and Digital Signal Processing modules for MicroPython
https://github.com/emlearn/emlearn-micropython


## Outline

- BRIEF. (Wireless) Sensor Network concept. 
Wireless communication. Battery power.
- BRIEF.Sensor node concept.
Readout. Processing. Storage/buffering. Transmission
- BRIEF. MicroPython introduction. 
Purpose. Compat. Libraries.
- MAIN. Efficient data processing in MicroPython.
Cases. DSP and ML techniques. FFT, RMS, CNN, RF.
Show benchmarks. Compute time. Memory usage. 
Plain Python perf dos and dont. Avoid/reduce allocations!
@micropython.native and @viper annotators
User C modules.
Dynamic native modules.
emlearn.
ulab.
- BRIEF. Reading data
Accelerometer, microphone. (camera?)
- BRIEF. Storing data
Internal FLASH. Memory card
- BRIEF. Sending data
MQTT, HTTP, BLE. LoRa ?

Maybe show a simple end-to-end example.
Putting all the pieces together.

## Demo
IoT sound sensor.
M5StickC as reference hardware.
Press for screen to come alive.

## Notes

What grew into the emlearn project was first presented at EuroScipy 2018,
in the talk Machine Learning for microcontrollers with Python and C (Jon Nordby). 
https://www.euroscipy.org/2018/descriptions/Machine%20Learning%20for%20microcontrollers%20with%20Python%20and%20C.html
Since then the tool has been used in a range of projects and cited in dozens of scientific papers.
MicroPython bindings for the library is a new addition, added in 2023.



