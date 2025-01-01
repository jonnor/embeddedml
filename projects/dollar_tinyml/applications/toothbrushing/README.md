
# Automatic toothbrush timer

This toothbrush timer tracks how long you spend on actively brushing your teeth.
It uses an accelerometer to measure motion, and analyzes it using a simple machine learning model.
The device helps you get to the 2 minute mark, which is the recommend duration!

This is a demo project for [emlearn-micropython](https://github.com/emlearn/emlearn-micropython),
a library efficient Machine Learning and Digital Signal Processing for [MicroPython](https://micropython.org/).
The intent is to be a fun but realistic application of machine learning on microcontrollers,
in the area of Human Activity Recognition.

## Status
***EXPERIMENTAL***.
Proof of Concept is being actively developed.
***NOT READY FOR OTHERS TO USE***.

## License
MIT

## Pre-requisites

Hardware

- M5Stick C PLUS2 from M5Stack
- 3d-printed toothbrush holder
- Zipties


## Installing

#### Development environment

```
pip install -r requirements.txt
```

#### Flash MicroPython

Uses MicroPython 1.24 for ESP32

```
mpflash flash --version 1.24
```

#### Copy dependencies

```
mpremote mip install https://emlearn.github.io/emlearn-micropython/builds/master/xtensawin_6.3/emlearn_trees.mpy
mpremote mip install github:jonnor/micropython-npyfile
mpremote mip install github:jonnor/micropython-mpu6886

mpremote mip install https://github.com/emlearn/emlearn-micropython/raw/refs/heads/master/examples/har_trees/recorder.py
mpremote mip install https://github.com/emlearn/emlearn-micropython/raw/refs/heads/master/examples/har_trees/timebased.py

mpremote mip install https://raw.githubusercontent.com/emlearn/emlearn-micropython/refs/heads/master/examples/har_trees/color_setup.py
mpremote mip install "github:peterhinch/micropython-nano-gui/drivers/st7789"
mpremote mip install "github:peterhinch/micropython-nano-gui"
mpremote mip install "github:peterhinch/micropython-async/v3/primitives"
```

The GUI libraries are not used by the main firmware,
but is used by some of the tools like for data-recording.

#### Copy the application

```
TODO: document
```
