
# Developing IoT sensors with MicroPython

## Status
Accepted for EuroPython. 2 sessions

- Program: https://programme.europython.eu/europython-2026/talk/NQGSY7/

```
2026-07-13 09:30–11:00, Conference Hall Complex A (S4A)
2026-07-13 11:15–12:45, Conference Hall Complex A (S4A)
```

Same workshop will also be at EuroScipy:
https://github.com/jonnor/embeddedml/tree/master/presentations/euroscipy2026/tutorial


## Proposal


## Abstract
Min 250 chars.


## Outline

Describe a rough structure of your proposal, including the time per topic.
Between 100 and 2000 characters.

Part I: MicroPython development, 1 hour

- Introduction to MicroPython. 5 minutes
- Developing with MicroPython on PC using Unix port. 15 min
- Serving data and handling requests using MicroDot HTTP server. 10 min
- Storing/loading sensor data using on-board filesystem. 5 min
- Using frontend/browser for user interfaces. 20 min
- Sending data to external servers using HTTP. 5 min

Part II: Deploying on device

- Deploying our server on device. WiFi setup etc. 30 min
- Physical input/output using GPIO. 10 min
- Reading digital sensors using I2C. 10 min
- Sending data to shared MQTT broker. 10 min

Part III: Open hacking

- Extend the application skeleton.
Pick one of 3 provided ideas (TBD).



## Why qualified

Active MicroPython community member and contributors since 2024.
Running monthly MicroPython usergroup events in Oslo since mid 2025.

## Tweet abstract



## Notes

In the process we will covered the following:

- Doing basic physical input/output using GPIO. Analog and digital
- Reading digital sensors using I2C
- Storing/loading sensor data using on-board filesystem
- Serving data and handling requests using MicroDot HTTP server
- Using browser with JavaScript for user interfaces
- Communicating with external servers using HTTP or MQTT

Key things but woven in

- Running locally with micropython binary
- Running on device with mpremote mounts
- Managing concurrent tasks using asyncio
- Installing libraries using mip package manager
- Persisting our application onto device. Copying files with mpremote

Mentioned in brief

- Automated testing, pytest style
- Using interrupts for high-priority work
- Execution time optimization using native/viper decorators (numba JIT style)
- Fast extensions using C modules
- Fast iteration of on-device code using mpremote mount

Out-of-scope

- Power management
- Bluetooth Low Energy
- IDE setup
- Type hinting and static checking with micropython-stubs and mypy 
- Developing drivers using I2C etc
- Driving actuators/motors etc
- Working with display/UI
- 

IoT topologies

- Standalone device. Device acts as HTTP server, serves webui etc
- Many-to-many communication. Using a MQTT broker

MAYBE

- Using htmx or datastar for interactive UI driven from device-side MicroPython
- Client-side development in Python using PyScript + MicroPython

Doing development on-PC

- Emulate sensor on machine.I2C level?
https://github.com/planetinnovation/micropython-mock-machine
- Emulate sensor by a custom mocked class
- Use a separate asyncio task for generating the sensor data


Strategy

- Build up step by step
Start single file.
asyncio at the main, with tasks (initially one)

Take-aways

- asyncio is cooperative multitasking.
Delays will happen. Avoid holding loop too long. Yield.


## From simulation to hardware

?? Use WokWi as a base?
Create a project that is our real hardware board.
So each can develop against that, and then deploy on matching real-hardware.

## Wokwi testing

Support both Arduino and MicroPython

Has ESP32 board - which??

Has Pico W. But not Pico 2 W?

### Wokwi MicroPython version

! default MicroPython versions were old
```
"attrs": { "env": "micropython-20231005-v1.21.0" }
```
https://wokwi.com/projects/305568836183130690

Pico example currently uses 1.24.1 by default
https://wokwi.com/projects/new/micropython-pi-pico

Updating to 1.25.0 worked
```
    { "id": "pico", "type": "wokwi-pi-pico", "attrs": { "env": "micropython-20250415-v1.25.0" } }
```

The provided firmwares seem to be here:
https://github.com/wokwi/firmware-assets/tree/gh-pages/micropython

The lastest is 1.25.0 for pico, and 1.22 for esp32
u prefix was deprecated in MicroPython v1.21.0.
1.25 was first version supported by emlearn-micropython. But maybe not for RP2040??

Feature request for newer versions
https://github.com/wokwi/wokwi-features/issues/1115

Resolved on May 25, 2026 - can now use MicroPython 1.28.0
```
"attrs": { "env": "micropython-20260406-v1.28.0" }
```


### More info
Uri Shaked is one of developers. Have a lot of talks
https://urish.org/#talks

https://www.youtube.com/watch?v=8PTYnNFK1pw
Wokwi can be used locally also, with VSCode extension
Can also be used with a commandline tool, wokwi-cli.
Especially for test-automation.
Can use same tests with hardware-in-the-loop

https://www.youtube.com/watch?v=q31782Wtj6M
Shows the Wokwi logic analyser. A component that can capture. Gives out .vcd file, to be opened in PulseView etc.

Custom peripherals ("chips") can be provided by third party.
Write code in C - compiles to WASM.
Or in Verilog.

### Board support

https://github.com/wokwi/wokwi-boards/tree/main/boards
Many official ESP32 boards.
Has XIAO ESP32 S3/C6/C3
Has PICO and PICO W
! no PICO 2 W

Virtual WiFi seems to work also on RPI Pico
https://wokwi.com/projects/360519097147837441
Has MicroPython 1.24.1 by default
WiFi worked when updating 1.25.0

https://docs.wokwi.com/guides/esp32#micropython

### Peripheral support

- Pushbutton
- Potmeter
- LED
- Rotary encoder
- SSD1306 OLED / SH1107 OLED
- Analog Temperature Sensor (NTC). 10k-10k
- PIR Motion Sensor
- Photoresistor. Analog and digital value
- DHT22
- BMP180. Barometric pressure and temperature sensor with I2C interface

- Accelerometer/IMU. MPU6050

https://docs.wokwi.com/getting-started/supported-hardware#microcontrollers


### Using files/libraries

Code .py be added manually to project as files.
Example:
https://wokwi.com/projects/305568836183130690

Open feature request for package management install:
https://github.com/wokwi/wokwi-features/issues/276

Tested install and run of regular MicroPython .py libraries. WORKS
https://wokwi.com/projects/465000314609795073

Tested install and run of native C modules .npy. WORKS
https://wokwi.com/projects/465000960050404353


Open questions

- Can we get custom files/libraries to persist, avoid redownloading?
- Which board should we use? Pico W or some ESP32
- Which sensors would we use?
- Does asyncio work as it should?
- Can we run MicroDot and access webserver?

## Communicating over network

IoT gateway

- https://docs.wokwi.com/guides/esp32-wifi#internet-access

## Hardware

Must-have

- Well supported chip. ESP32 or RP2
- Good WiFi-support. ESP32 vanilla/S3/C3/C6. Pico W RP2024

Want to have

- Analog sensor
- Accelerometer/IMU
- I2C extension port



### Alternatives

#### XIAO with base board?

! ESP32 wokwi is very old
Buzzer, push button
I2C extension connectors
SSD1306 OLED

#### M5StickC PLUS 2?
Out of production!!
Familiar. Grove extension. Accel. Buzzer. Button. Qwiic adapter possible. Simple PMIC.
! no microphone
! no analog sensors
Relatively costly. Already have 5+
https://www.digikey.no/no/products/detail/m5stack-technology-co-ltd/K016-P2/22015383

#### Pico W with expansion board?

https://www.digikey.no/no/products/detail/raspberry-pi/SC0918/16608263

Expansion board
Would be nice if it maps quite nicely to Pico headers.
So that participants can see the mapping easily.
! will need to expand VCC and GND connections

https://www.digikey.no/no/products/detail/dfrobot/DFR0836/15283076
https://www.digikey.no/no/products/detail/sb-components-ltd/SKU20812/16836957?s=N4IgTCBcDaIAoEsDGB7ABAUQB4AcCGAdgM4IoFoBCKeATgCZoDicAkgPIgC6AvkA

And associated Wokwi modules?


#### Pico 2W
No Wokwi!
No sensors. No extension port.


## Unrelated

Low-power Lora with Zephyr etc

https://www.seeedstudio.com/Wio-E5-LE-mini-Dev-Board-STM32WLE5JC-p-5764.html
https://forum.seeedstudio.com/t/programming-lora-e5-with-arduino-comparison-of-lora-e5-and-lora-e5-le-transmit-currents/274869
https://forum.seeedstudio.com/t/programming-lora-e5-with-arduino-grove-lora-e5-sleep-current-0-7ua/274845

LoRa-E5-LE mini. 25mA send.
Compared to the E5 model’s 85mA.

https://forum.seeedstudio.com/t/shutdown-current-of-lora-e5-mini-from-72ua-to-3ua-by-replacing-ldo-and-diode/275044
Got shutdown current down from 75uA to 10uA to 3uA.



#### Practicals

Do most of the development on PC using the Unix port.
Runs on Linux, Mac OS and Windows (using Windows Subsystem for Linux)
Particpants must have Python 3.12 or later setup.
In a dedicated virtualenv.

