
## TODO

Materials

- Add digital and analog IO examples
- Add filesystem example
- Add MicroDot example, for running locally

Hardware

- Wire up 1 unit like in Wokwi simulation.
Test using same code on device.
Focus on sensor-related hardware.
Analog sensor.
Digital sensor.
Keep LEDs for liveness

Deploy on device

- Finish install instructions
- Find out / document how to download from Wokwi to locally
- Do a check on device

Milestone: Bitraf / MicroPython Oslo test run 

- Test PWM analog with LED on device
- Test PWM analog with LED in Wokwi



Later

- Test micropython JIT in Wokwi
- Try ViperIDE in Firefox - new WebSerial??

EuroPython

- Try to find a few testers for day-before
- Try to find one or two volunteers

## Interaction

Use the conference chat to share resources.
Back and forth

Example. Send link to Wokwi sketches


## Outline

!! using Wokwi it is possible to do the physical/IO bits more step wise
!! critical, that MicroDot/HTTP works in wokwi

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
