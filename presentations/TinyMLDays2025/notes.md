
# TinyML Days 2025 Aarhus

https://events.au.dk/tinymldays/conference

10.30 - 12.30: Workshop 1:  EM Learn - Jon Nordby, SoundSensing

## Format

## TODO

Now

- Advertise the event on Discord. EDGE AI, 
- Advertise the event on LinkedIn
- Finalize workshop design

Prep before event

- HAR. Support dataset definitions as a file
- HAR. Add frequency/FFT features
- Send out instructions for setup
- Do a trial run of workshop at Bitraf


## Goals

At the end of the workshop, each of the participants shall:

Must

- Have setup a functioning emlearn and MicroPython development environment on computer
- Have deployed a model onto device. M5StickC
- Understand how continious classification works.
Pipeline (pre, model, post).
Prediction form. Window splitting. Relation/Difference to event detection, sequence modelling.
Data/labeling requirements/setup
- Understand what TinyML is, what it is used for, benefits/drawbacks
- Understand what emlearn is

Maybe

- Adapted the example code to do something different with prediction outputs
- Have collected their own data, trained and deploying a model
- Understand key elements of data collection and curation

Bonus

- Understand model optimization and tradeoffs

Out-of-scope

- Other sensor modalities. Audio/image.
Participants can follow examples on their own


## Things to do with model outputs predictions 

- Send data to computer, do something on the computer.
WiFi MQTT, via broker on Internet
https://test.mosquitto.org/
Receive in Python ?
Receive in Javascript / WebSocket
- Log the data on device.
File system, CSV file etc
- Send data to mobile phone, do something there
MQTT? BLE?
- Indicate to user via LEDs
- Indicate to user via screen

## Fun things to do

- Exercise tracker. Put everyones output on a webpage

## Dataset building

- Mapping out possible factors
- Generalized performance - dataset splitting
- Estimating required amounts of data
- Error analysis -> identify gaps in data
- Pre-labeling vs post-labeling




