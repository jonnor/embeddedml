
# TODO

- Join the Discord
- Create all skeleton slides
- Fill inn all code examples

- Full rehearsal


- Install Discord desktop app
- Test video sharing in Discord app



# Planning

#### Intended audience and expected background

Any developer or data scientist curious about sensor data processing, IoT,
and how Python scales down to the smallest of devices.

The audience is expected to have a basic literacy in Python, proficiency in programming,
and know the basics of data processing.
Some familiarity in time-series processing, Digital Signal Processing or 
Machine Learning, will make the talk much more relevant to you.

Talk should be approachable for those who are new to microcontrollers and embedded systems.

#### Focus and scope of the talk
The main part of the talk will be how to write efficient sensor processing code with MicroPython,
to document just how much is actually doable on a tiny system using Python.

The general introduction to MicroPython will be kept rather brief,
as there are many resources for this available already.

How to aquire data from sensors (such as accelerometer or microphone),
and how transmit data (using BLE or WiFi) will be covered very briefly.
An emphasis will be on techiques and practices that enable efficiency.

#### Take-aways

- Sensor processing applications cover a wide range of usecases.
- Python is a productive environment on microcontrollers. Thanks to MicroPython
- For under 20 USD you get a complete device that runs MicroPython. With WiFI+BLE and sensors. ESP32
- It is easy to get started with MicroPython. Flash firmware, get a terminal. mpremote tool. mip install libraries. Thonny as a simple IDE

- MicroPython has a range of tools for efficient code execution. ABC
- Accelerometer/IMU data processing can be done entirely in Python.
For gesture detection, activity detection, sleep tracking, et.c.
- Audio processing needs C modules for effiency.
- Images also needs C modules for efficiency. And keeping image resolution low.
- emlearn-micropython is an efficient MicroPython library
for Digital Signal Processing and Machine Learning algorithms.


#### Resources

Docs: Extending MicroPython in C
https://docs.micropython.org/en/latest/develop/extendingmicropython.html

Docs: Maximising MicroPython speed
https://docs.micropython.org/en/latest/reference/speed_python.html

PyConAU 2018: Writing fast and efficient MicroPython (Damien George)
https://www.youtube.com/watch?v=hHec4qL00x0

PyConAU 2019: Extending MicroPython: Using C for good!" (Matt Trentini)
https://www.youtube.com/watch?v=437CZBnK8vI

PyConAU 2018: Asyncio in (Micro)Python (Matt Trentini)
https://www.youtube.com/watch?v=tIgu7q38bUw&t=830s

emlearn - Machine Learning and Digital Signal Processing modules for MicroPython
https://github.com/emlearn/emlearn-micropython

# Outline

Maybe start with an end-to-end demo/usecase?
Then discuss the various pieces.
KEY: keep the efficient data processing as the core

- Motivation. Sensor usecases. Measuring, logging, acting, regulating.

- BRIEF. (Wireless) Sensor Network concept. 
Wireless communication. Battery power.
- BRIEF. Sensor node concept.
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

## Example cases, by increasing levels of complexity

MISSING

- Inline Assembler. Not supported on ESP32 / xtensawin
https://docs.micropython.org/en/latest/pyboard/tutorial/assembler.html
@micropython.asm_thumb

Temperature sensor

- Analog/digital read
- Non-blocking wait? state-machine or asyncio
- ? 

Activity detection

- Block readout with FIFO
- .mpy dynamic native module. For emlearn RandomForest

Noise sensor

- Block readout with I2S peripheral
- Compare emlearn with ulab. IIR ? For A weighting filter. 
- FFT ? For spectrogram

Image classification

- C module. mp_camera for ESP32

OpenMV. 
https://docs.openmv.io/library/index.html
Compact in-memory representation of images. RGB565
Rescaling. Color conversions.
Image encoding and decoding. JPEG/PNG.
Camera drivers.

#### Temperature sensor

Phenomena is inherently slow.
Values change seldom. Want 1 value that represents a long-ish time interval.

- Strategy: Sample, filter, transmit, sleep/repeat.
- Data rate in. Under 10 bytes per 1 minute
- Data rate out. Under 1 byte per 1 minute
- Data aqucition.
N measurements with a bit of spacing. Blocking read often OK. Non-blocking also quite easy. Optional: Use async
- Processing.
Reject outliers. Median

Other similar examples.
- Waterflow/pressure in continious running pump system.
- Electricity consumptions for continious running systems

Trivially doable in pure Python.

https://carbon.now.sh/?bg=rgba%28171%2C+184%2C+195%2C+1%29&t=one-light&wt=none&l=python&width=680&ds=false&dsyoff=20px&dsblur=68px&wc=false&wa=true&pv=0px&ph=0px&ln=false&fl=1&fm=Hack&fs=17.5px&lh=148%25&si=false&es=2x&wm=false&code=import%2520machine%250A%250AN_SAMPLES%2520%253D%252010%250ASAMPLE_INTERVAL%2520%253D%25201.0%250ASLEEP_INTERVAL%2520%253D%252060.0%250A%250Aanalog_input%2520%253D%2520machine.ADC%28machine.Pin%2822%29%29%250Asamples%2520%253D%2520array.array%28%27H%27%29%2520%2523%2520raw%2520values%2520from%2520ADC%252C%2520as%2520uint16%250Ameasurement_no%2520%253D%25200%250A%250Awhile%2520True%253A%250A%250A%2520%2520%2520%2520%2523%2520collect%2520data%2520for%2520measurement%250A%2520%2520%2520%2520for%2520i%2520in%2520range%28N_SAMPLES%29%253A%250A%2520%2520%2520%2520%2520%2520%2520%2520samples%255Bi%255D%2520%253D%2520adc.read_u16%28%29%250A%2520%2520%2520%2520%2520%2520%2520%2520time.sleep%28SAMPLE_INTERVAL%29%250A%250A%2520%2520%2520%2520%2523%2520aggregate%2520samples%252C%2520convert%2520to%2520temperature%250A%2520%2520%2520%2520raw%2520%253D%2520median%28samples%29%250A%2520%2520%2520%2520temperature%2520%253D%2520%28raw%2520*%25200.323%29%2520-%252050.0%2520%2523%2520calculation%2520depends%2520on%2520type%2520of%2520analog%2520sensor%250A%250A%2520%2520%2520%2520%2523%2520Do%2520something%2520with%2520the%2520measurement%250A%2520%2520%2520%2520send_bluetooth_le%28measurement_no%252C%2520temperature%29%250A%250A%2520%2520%2520%2520%2523%2520sleep%2520until%2520next%2520time%2520to%2520collect%2520new%2520measurement%250A%2520%2520%2520%2520machine.lightsleep%28int%28SLEEP_INTERVAL*1000%29%29%250A%2520%2520%2520%2520measurement_no%2520%252B%253D%25201%250A%250A



```
import machine

N_SAMPLES = 10
SAMPLE_INTERVAL = 1.0
SLEEP_INTERVAL = 60.0

analog_input = machine.ADC(machine.Pin(22))
samples = array.array('H') # raw values from ADC, as uint16
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

```


```
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
```


#### Human/Animal Activity Detection.
Accelerometer

Accelerometer generally processing doable in pure Python.
ML classification can be a bit slow though.
Better energy efficiency and more precise models by using C module from emlearn-micropython


- HW. MEMS accelerometer / IMU. I2C
- Strategy: Start, filter, transmit, sleep/repeat.
- Data rate in. Under 10 bytes per 1 minute
- Data rate out. Under 1 byte per 1 minute
- Data aqucition.
Use the FIFO buffer in the MEMS sensor.
Check regularly samples are ready.
Sleep in-between.
When enough samples, process it.

- Processing.
Feature extraction. Statistical / FFT.
Simple Machine Learning model classify activity. RandomForest
Possible to generate Python code for such a model.
Using

But considerably faster if using a native .mpy module


At 50 Hz, 20 ms per sample. Can get away with polling every.
But much better is to use the FIFO buffer in the MEMS sensor.








#### Noise sensor



Sound Event Detection. Microphone



#### Camera

! SKIP mostly






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




