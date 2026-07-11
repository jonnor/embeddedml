
# Wokwi

Using [Wokwi](https://wokwi.com/) as the simulator for the tutorial.
Here are some notes for that.

### Status

Have selected Pico W as the base.
Developing examples at
https://wokwi.com/projects/465018105144566785

### Open questions

Nice-to-have

- Can we get mip installed files/libraries to persist, avoid redownloading?
- Can we get WiFi setup to be faster. Right now delays startup by 5 seconds.
Using the REPL for interactive work is a workaround.

Not working

- Can we run MicroDot and access webserver?
No - not without IoT gateway.
Run locally with micropython-unix instead

### WiFi credentials

Android phone does not allow empty password.
Must have minimum 8 characters.
But Wokwi seemingly allows any password.

### Wokwi HTTP

My example
https://wokwi.com/projects/468563618722295809

Fun API services, open without signup

- https://jsonblob.com/api - JSON key-value/document store
- https://ntfy.sh/wokwi-11 - notifications

### Wokwi MQTT

My example
https://wokwi.com/projects/468550810100303873

TODO: make it a bit more interesting
Maybe have all send messages to related topics, subscribe to all

Original example, weather logger
https://wokwi.com/projects/322577683855704658
! mqtt.simple is not provided in RP2 port

### Wokwi asyncio

LEDs with different blinking rates, using asyncio
https://wokwi.com/projects/468550810100303873

### Wokwi SSD1306

My example
https://wokwi.com/projects/467997034556625921

Existing example - works
https://wokwi.com/projects/359558101922696193

### Wokwi MPU6050

My example
https://wokwi.com/projects/467997034556625921

Based on
https://wokwi.com/projects/337973173314126419

Original had issues
```
Traceback (most recent call last):
  File "main.py", line 15, in <module>
  File "MPU6050.py", line 8, in __init__
OSError: I2C operation not supported
```


### Wokwi HTTP server

Requires the private IoT gateway
Which requires each user to have a paid plan :(
https://docs.wokwi.com/guides/esp32-wifi#the-private-gateway


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

- Pushbutton. 12 mm. Can trigger actions
- Potmeter. Can set continious value
- LED. Basic blink.
- Buzzer. Audible feedback. Was used in toothbrush project
- Photoresistor. 4-pin breakout. Both analog and digital value
- Analog Temperature Sensor (NTC). 10k-10k
- Accelerometer/IMU. MPU6050. GY-521. I2C mode. Manual orientation control, not motion
- BMP180. Barometric pressure and temperature sensor. I2C
- Rotary encoder. KY-040
- SSD1306 OLED / SH1107 OLED
- PIR Motion Sensor
- DHT22. Temperature and humidity. ! custom protocol, not I2C
- DS1307 RTC

https://docs.wokwi.com/getting-started/supported-hardware#microcontrollers

Rotary encoder example
https://wokwi.com/projects/370831322835154945

Buzzer example
https://wokwi.com/projects/425638032299541505

### Serial plotter
There serial monitor can plot values over time
https://docs.wokwi.com/guides/serial-monitor

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


## Communicating over network

IoT gateway

- https://docs.wokwi.com/guides/esp32-wifi#internet-access
