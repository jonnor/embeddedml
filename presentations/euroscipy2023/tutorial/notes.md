
# Planning 

## TODO

Decide reference hardware platform

- Test ESP32 with MicroPython
- Order M5StickC
- Evaluate/test M5StickC

Make reference project

- Decide project and scope
- Implement device code
- Implement training code
- Test the models on simple dataset

Make tutorial

- Run trials with few friends
- Run tutorial locally
- Order kits for the reference hardware

### MAYBE

Switch from C to MicroPython

- Support classifier as micropython module
- Support preprocessing as micropython module
- Reimplement device code in MicroPython

## Needs

Neccesary

- A well-defined reference hardware platform
- Working and well-tested example(s) / project.
Tested on real hardware.
- Working getting-started process
Tested with real people.
Do some trial runs? 2-3 times before hand
- Hardware for running code on.
Keep low by sharing in groups? 2-5 persons per group
Potential income by allowing people to buy kit.
Sell half of the kits, at 100% markup = pay for kits in 1 round.
8 kits a 250 NOK = 2000 NOK.

Wanted

- MicroPython support in emlearn
Not strictly neccesary because will provide example.
Will make it more interesting for people to participate - do more with their exisiting skills.
Enable easier experimentation with changing provided code.
Easier in terms of tooling? No need for cross-compiler / device SDK setup.

### Project

Basic classification project? Then time-series?
Or jump straight to time-series. Just treat non-time series as simplified case.

Accelerometer data is medium data-rate, easy to work with.
Can do fun physical things with it.
Some might be relatable.
Gesture recognition? Human Activity Detection?

Personal computing
Industrial applications


### Trial run sessions

First with a few friends?
Can be 1-on-1 or 1-on-few.
Jensa? Trygvis? Elias H.? At local meetup in Oslo.

At Bitraf. Do a public course. With say 10 people.

### Hardware platform

Needs

* Basic on-device outputs. 2 LEDs+
* Basic on-device inputs. 1 button+
* At least one sensor. Accelerometer.
* No need for external programmer/debugger

Want

* Good MicroPython support
* Microphone and accelerometer
* Hard to mess up. Maybe enclosed board
* Multiple LED(s), RGB

Nice-to-have

- LCD screen

HW platforms

- ESP32
- NRF52
- RP2
- STM32

Candidate boards

- M5Stick-C
- pyboard
- MicroBit
- RPi Pico
- Arduno Nano33 Sense


https://micropython.org/download/arduino_nano_33_ble_sense/

M5Stick-C Pico Min
https://www.adafruit.com/product/4290 - 25 USD.
Has casing.
Has a watch strap option. 30 USD

https://shop.m5stack.com/products/stick-c
15 USD from offical store
Has onboard accel and mic. Onboard button. Onboard LCD. WiFi and BLE. Captouch. Grove connector.


https://shop.m5stack.com/products/m5stickc-plus-with-watch-accessories

Kit also available on Digikey, 250 NOK
https://www.digikey.no/no/products/detail/m5stack-technology-co-ltd/K016-H/15771301


!! M5StickC and M5StickCplus don't have SPIRAM. Only 520K RAM

Thread says esp32/GENERIC firmware works
https://forum.micropython.org/viewtopic.php?f=18&t=10117#p69640

https://micropython.org/download/esp32/


### micropython support

Audio via I2S for since 2021 https://github.com/miketeachman/micropython-i2s-examples
on ESP32, NRF and STM32
PDM mic not so good?

touch on ESP32. Via machine.TouchPad

esp32-s2. No Bluetooth, WiFi only. ESP32-C3 and ESP32-S3 do have BLE

https://docs.espressif.com/projects/esp-idf/en/v4.3/esp32s2/hw-reference/chip-series-comparison.html


## Existing TinyML on micropython


https://dev.to/tkeyo/tinyml-machine-learning-on-esp32-with-micropython-38a6
Jul 1, 2021
https://github.com/tkeyo/tinyml-esp

was able to read 100 Hz from accelerometer
used m2gen to generate Python code
separate X, Y and Circle gestures
Using RandomForest
Inference time with 10 estimators is approximately 4ms which is viable even at 10 ms sampling period
! no feature engineerng, using samples directly ?
used 660 ms window
! detection performance not so good

https://eloquentarduino.com/micropython-machine-learning/
using everywhereml to generate Python
shows usage on some MNIST data

https://medium.com/@subirmaity/a-simple-neural-network-implementation-approach-in-micropython-for-deep-learning-application-760ab35cb538
pure MicroPython implementation of a simple MLP


