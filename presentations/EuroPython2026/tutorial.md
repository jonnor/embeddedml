
# Developing IoT sensors with MicroPython


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

- Doing basic physical input/output using GPIO
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

Hardware

- Pico 2W ? No sensors. No stock extension
- M5StickC PLUS 2? Familiar. Grove extension. Accel. Buzzer. Button. Qwiic adapter possible. Simple PMIC.
! no microphone
! no analog sensors
Relatively costly. Already have 5+
https://www.digikey.no/no/products/detail/m5stack-technology-co-ltd/K016-P2/22015383

Strategy

- Build up step by step
Start single file.
asyncio at the main, with tasks (initially one)

Take-aways

- asyncio is cooperative multitasking.
Delays will happen. Avoid holding loop too long. Yield.


#### Practicals

Do most of the development on PC using the Unix port.
Runs on Linux, Mac OS and Windows (using Windows Subsystem for Linux)
Particpants must have Python 3.12 or later setup.
In a dedicated virtualenv.

