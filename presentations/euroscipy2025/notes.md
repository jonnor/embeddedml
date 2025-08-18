
## Concept

Focus on scientific application of (IoT) sensor-nodes,
and how they are used.
Highligh how this can be implemented using emlearn + MicroPython.

## The talk

Wednesday, August 20, 1:30 PM
Room 1.19 (Ground Floor)
Computational Tools and Scientific Python Infrastructure

30 minutes slot.
20-25 minutes + QA.

## Communication goals

> You as a scientist, or engineer supporting scientists,

> become familiar with how to create custom sensor systems
> using microcontrollers and (Micro)Python

> including on-sensor data processing
> like digital signal procesing and machine learning
> using emlearn


### Take aways

- Many scientific applications rely on collecting a lot of physical data
- Wireless communication and battery operation often highly desirable for low-cost, scaling deployments
- Wireless sensor nodes are typically using a microcontroller
- Microcontrollers can be programmed in Python using MicroPython
- Microcontrollers can do a decent amount of data processing,
Including audio and image datam and machine learning inference
- MicroPython has good tools for sensor data processing,
including connectivity, storage, performance (Viper/ASM/C modules)
- There are good ecosystem of libraries
Including ulab, emlearn, OpenMV et.c.


## Outline

See also [proposal.md](./proposal.md)

Broad categories

- Scientific applications
- Sensor nodes and Wireless Sensor Networks
- About MicroPython
- Tools and practices for efficient sensor data processing in MicroPython

## Scope

Out-of-scope / scope limitations

Tradeoffs/strategies for different wireless protocols
Just mention that the relevant options are generally supported in MicroPython

Explanation of how the different optimizations work
Cover briefly. Refer to PyConZA presentation for details.

## Planning

### About MicroPython
Pick from existing presentations. Ex FOSDEM.

### Tools and practices for efficient sensor data processing in MicroPython
Pick from PyConZA presentation



### MicroPython Data Science ecosystem

? 

ulab
emlearn
micropython-npyfile

OpenMV
https://github.com/sparkfun/micropython-opencv


### Sensor nodes and Wireless Sensor Networks

Existing slide(s)

- ML-powered sensor node. Architecture
- Microcontrollers, what are they.

Add a bit more.
Especially things that make later parts more relevant.

- Wireless sensor networks. Principle. Deployed in a large area.
Communication to a central point. Via gateway or not.
Non-connected loggers. Storing to SDcard etc. Hybrid, raw data on SD.
- Common wireless protocols.
Typical ranges. Typical data rates. Typical power.
Could be in terms of "typical architectures"?
Motivation for ML on edge: Being able to transmit
- MEMS sensors ? Could be covered under applications also
- Batching of data. Very beneficial. Reducing wakeup times.



####  WiFi
Very easy. Very well supported.
Not power efficient. WiFi 6 improves


#### Cellular
LTE CAT M1 / LTE CAT NB "narrowband iot"
PPP over Serial (PPPoS)
machine.PPP 
https://docs.micropython.org/en/latest/library/network.PPP.html

#### BLE
Ex to mobile phone, or gateway
! NRF52 not so well supported right now.
Zephyr port is improving this.
One of the best low-power BLE chips.
ESP32 not that low power

#### LoRa
LoraWAN.
Public network like ThingsNet
Private network using gateways
https://github.com/micropython/micropython-lib/tree/34c4ee1647ac4b177ae40adf0ec514660e433dc0/micropython/lora
Support bunch of the most common modules from Semtech SX1262 

- Duty cycle limits: EU has 1% duty cycle restriction (36 seconds/hour transmission time)
- Fair Access Policy: TTN limits to 30 seconds uplink airtime per device per day
- Typical use: Most applications work well with 10-50 byte payloads sent every 15-60 minutes
- Recommendation: Use SF7-SF9 with 20-50 byte payloads

airtime calculator
https://www.thethingsnetwork.org/airtime-calculator
51 bytes SF7, 125 khz, EU686. 118 ms.
With 30 seconds daily, 11 per hour avg
5 minute interval
Might need to go down to 1/2 of this

LoraWAN packet overhead. 13 bytes minimum ?
EU868 SF12: 51 bytes max → 38 bytes application data

Confirmed ACK in LoRaWAN:
Set ADR bit in FCtrl to request confirmation
Device sends uplink with "confirmed" flag
Network server responds with downlink ACK
If no ACK received, device retransmits (up to 8 times default).

Coverage on public network
https://www.thethingsnetwork.org/map
Krakow has 3 gateways nearby conference center
Oslo have

#### Thread
IP-based. 6LoWPAN / IEEE 802.15.4.
Zigbee uses same transports.



### Scientific applications

Environmental Sciences

Meteorology - weather stations, satellites
Oceanography - buoys, underwater sensors
Ecology - wildlife tracking, environmental monitoring

Earth Sciences

Seismology - earthquake detection
Geology - ground movement, volcanic activity
Hydrology - water flow, quality monitoring

Life Sciences

Physiology - heart rate, brain activity, blood chemistry
Neuroscience - EEG, fMRI, neural implants
Biology - microscopy sensors, DNA sequencers

Physics & Engineering

Particle Physics - detectors in accelerators
Astronomy - telescopes, space-based sensors
Materials Science - stress, temperature, electromagnetic properties

Applied Fields

Medicine - diagnostic imaging, patient monitoring
Agriculture - soil sensors, crop monitoring
Transportation - GPS, speed sensors, collision detection

### WSN applications

Especially relevant when measuring at many locations
And want coverage over time

*Spatio-temporal* data


### Examples at different complexity levels

Output data rate on LoRaWAN ex,
40 bytes every 10 minutes


- Low datarate logging
Sleep, measure+send, sleep
No or very simple data processing on edge. Basic averaging/filters etc.
No particular benefit of doing more advanced.

- Med



#### For sound

Usecases

- Understanding wildlife behavior
- Illegal logging detection
- Noise monitoring

Tasks

- Birdsong detection & classification
- Dolphin/whale

#### For accelerometer

Usecases

- Sleep quality tracking
- Monitoring cows/sheep

Tasks

- Human Activity Detection
- 

#### For image

- Wildlife cameras

#### Other

## Unrelated

#### Building C programs and running in browser

For usage with Jupyter Lite for emlearn tutorials etc.

Would need to create a Python module, build it with PyScript,
and expose an API that allows to compile a file.


xcc
https://github.com/tyfkda/xcc
Standalone C compiler/assembler/linker/libc for x86-64/aarch64/riscv64/wasm 
Has browser demo of compiling C to WASM and running it


tcc
https://repo.or.cz/tinycc.git/
https://github.com/TinyCC/tinycc
No WASM backend?

wasmtime/cranelift
https://github.com/bytecodealliance/wasmtime/issues/2566
No WASM backend?

lcc
https://github.com/drh/lcc
C89 only, not C99



Server-side approaches with APIs

https://github.com/compiler-explorer/compiler-explorer

https://github.com/judge0/judge0


