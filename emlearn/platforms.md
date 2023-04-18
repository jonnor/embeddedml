
# Platform support

Documented on https://emlearn.readthedocs.io/en/latest/platform_support.html

## Arduino

Advantages

- Popular getting-started platform. Minimal setup, people often have a board lying around
- Lots of very accessible examples out there

Disadvantages

- APIs are not that well designed

Improvements

- TODO: Publish an Arduino package, that can be installed.
Avoids having to manually copy emlearn files into Arduino "libraries" 

## PlatformIO Core

Benefits

- Supports many embedded platforms. Including Arduino, Zephyr, ESP IDF
- Can be pip installed!! Same tools needed for emlearn.
- Has simavr and qemu targets supported
- Has a unit-test runner for on-device remote execution. Supports Unity (and others)
- Has integration with IDEs. VS Code recommended
- Has static analysis runner. cppcheck

Disadvantages

- Zephyr OS support stuck at 2.x.
Not supporting NRF53 etc?
https://github.com/platformio/platform-nordicnrf52/issues/141

Can hook in custom build steps

- https://docs.platformio.org/en/latest/scripting/custom_targets.html
- https://docs.platformio.org/en/latest/scripting/index.html

Could be natural place to integrate the emlearn Python scripts that generate C code

Improvements

- TODO: Publish emlearn as installable package PlatformIO package.

## Zephyr RTOS

Benefits

- Has nice standardized driver API for low-rate sensors. Indepentent of bus I2C/SPI et.c.
- Has compile-time definition of boards and pheripherals
- Has standardized driver API for digital microphones. dmic. On some platforms
- Good support for NRF52 and NRF53 device

Disadvantages

- No good API or drivers for high-speed IMU/accelerometers 
- dmic interface not supported on ESP32 / ESP-IDF ?

Improvements

- TODO: document/example how to use emlearn with Zephyr

