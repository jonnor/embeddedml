
# Platform support

Documented on https://emlearn.readthedocs.io/en/latest/platform_support.html

## Arduino

Advantages

- Popular getting-started platform. Minimal setup, people often have a board lying around
- Lots of very accessible examples out there

Disadvantages

- APIs are not that well designed
- Lots of beginners that may need a lot of hand-holding

Improvements

- TODO: Automate creation of Arduino package as part of CI/CD

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
2https://github.com/platformio/platform-nordicnrf52/issues/141

Can hook in custom build steps

- https://docs.platformio.org/en/latest/scripting/custom_targets.html
- https://docs.platformio.org/en/latest/scripting/index.html

Could be natural place to integrate the emlearn Python scripts that generate C code

Improvements

- Documentation on how to use it, https://github.com/emlearn/emlearn/issues/101

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

- Practical examples. https://github.com/emlearn/emlearn/issues/108

