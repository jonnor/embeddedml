
# Demos

!!! not the same as an example

Examples:

- Showing how to do common tasks.
- Not supposed to be a real solution. Or to be impressive.
- Making deliberate (over)simplification.
- Can use synthetic data.
- Can use no hardware, trivial hardware setup just to demonstrate simple thing.

Demos are:

- Focused on a real-world usecase or application.
- Tackling at least realistic conditions.
- Usually done on real data.
- Can be ran on real hardware.
- Might need to be quite complex (depending on application)

## Priority

**Examples** are more important than demos.
Can maybe have 1 or 2 demos just for marketing purposes.
Or to use demo development as a way to ensure that the neccesary tooling is in place and ergonomical.

## Goals

- Encourages people to try out emlearn for their problem
- Inspires people to make things with emlearn
- Learn some concept or technique that applies in embedded/TinyML

## Requirements

- Easy to reproduce.
Needing no or minimal special hardware, or long setup
- Easy to verify that one has done it correctly.
Provide expected results, allow simple comparison
- Can be used as starting point for other projects

## Established applications

- Fall detection. Using accelerometer
- Voice Activity Detection. Using microphone
- Human activity recognition. Using accerelometer.
- Gesture recognition. Using accelerometer.
- Audio Event Detection (simple). Gunshot/impulse sound
- Presence/occupancy detection.

Using emlearn on top of a deep neural network library.
To handle more complex cases.
Example: Tensorflow Lite for Microcontrollers

## Out-of-scope

Should be done with deep neural networks instead.

- Voice command/control audio.
- Object recognition image.
- Wakeword/keyword spotting audio.


# Available materials

- Microcontroller devboard. eg Arduino Uno, or ESP32, or RP2040
- Core passive components. Resistors,capacitors,LEDs,wires,diodes,BJT/MOSFET
- Low-rate analog sensors. Connecting via ADC. Temp/gas.
- Digital sensors. I2C is easiest. Accelerometer, temp/humidity, light. 


# Fun projects

## Component classifier

See [emlearn-component-tester project](https://github.com/emlearn/emlearn-component-tester).

## Photovoltaic detector

Two LEDs facing eachother. Transmissive
Or two LEDs facing same direction. Reflective
Measure voltage across one LED
Control other LED on or with PWM.
Put LED on/off.
Use low state as reference. Compute difference with when on.
Put item in front of sensor -> should be classified as present.
Can be done over time, for pass-by object detection.
Does not really require machine learning though - thresholding will do OK in many cases.
Could go further with LEDs/photodetector to identifying color.
Using then to outlines / transmissive shapes, using an array.
And then add a lens, to create a super basic camera.
Or use UV and IR to create basic hyperspectral detector.

## Temperature sensor

Showing how to implement temperature sensor with standard electronics components.
Without a specialized component.

Regression task.

Diode voltage drop. Ie 1N4007. Depends almost linearly on temperature. 
Similar might also be for a Base-Emitter pair in a bipolar transistor?

Humidity. Capacitors capacitance are dependent on relative humidity.
Probably also has some temperature dependence. May need to be corrected for!

Probably has some component variation also. Would be nice to map out.

Should collect data in environmental chamber.
Using one or more standardized devices as a reference.

Minituarization. Could put on board with an small microcontroller.
Implement a sensor protocol, like I2C or OneWire.
Implement same protocol/format as some other common devices.


## Cyclic behavior

Actuator that is driven. From state 1 to state 2, continious transition
Change in position should be even over time. For example a linear pattern, or linear angular
Would need to measure position... Then might also have PID.
Setpoint vs actual interesting variable to track

Could track amount of current to the motor. Should be approximately constant
Becomes more interesting with multiple motors/axes

## Activity Recognition using wrist-mounted accelerometer
Using tri-axial accelerometer.

Several standard hardware devices available.

- LilyGo TTGO T-Watch. ESP32
- Pine64 [PineTime](https://www.pine64.org/pinetime/). nRF52832, BMA425
- Any smartphone

[Energy-efficient activity recognition framework using wearable accelerometers](https://doi.org/10.1016/j.jnca.2020.102770).
Uses 50/100 hz, int8. 256 samples long windows, with 50% overlap.
Computes from this basic features.
Classified with RandomForest
Gets F1 scores of 90%, 70% on participants not in training set.
Code available here, including C feature extraction, Python feature extraction and datasets.
https://github.com/atiselsts/feature-group-selection

Can maybe be extended to gesture recognition later.

Being able to store/annotate activities on the go would be great.
To build up datasets.
Chose between pre-defined classes.
Have a couple of user-definable classes.
1/2/3/4 or blue/red/green/yellow 
Pre-annotate class, before starting activity. 
Post-annotate after doing activity / event happened.

Should be able to store raw data from accelerometer.
Maybe use some simple compression. Like gzip/deflate
Store files to be synced as time-stamped.
Maybe one per 60 seconds or so.

On-device few-shot learning of these would also be very cool.
kNN the most simple algorithm for this.
Just need to store feature vectors somewhere. FLASH/SDCARD
And keep number managable, so not too slow things down too much.
Need to have a good feature extraction system.

DynamicTimeWarping kNN one alternative for few-shot.
https://sequentia.readthedocs.io/en/latest/sections/classifiers/knn.html
https://github.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/
https://github.com/datashinobi/K-nearest-neighbors-with-dynamic-time-wrapping/blob/master/knndtw.py
https://github.com/MaxBenChrist/mlpy-plus-dtw/blob/master/mlpy/dtw/cdtw.c

## Condition monitoring moveable machine using accelerometer

Raise an alarm.
E.g send via WiFi to user. ESP32 etc

Accelerometer on head.

+ single sensor for motion on all 3 axis
+ standardized, commodity sensor 
+ easy to adapt to other cases of moving machinery 

Example washing machine

- Idle. No vibrations
- Running. Some vibrations
- Anomaly. Vibrating too much. One of the legs mis-adjusted

Example. 3d-printer
simple anomalies.
hitting object too hard with nozzle. eg from overextrusion

## Capacitive sensing

### Object classification from cap sensors

Position 9 cap sensors in a grid
Maybe 10 x 10 cm area. 3 cm between each


### XY position from cap sensors

Place 4 sensor electrodes in a square.
For example by taping wires to a piece of paper.
Then try to measure the.

Regression problem. 2-outputs.

In theory does not need ML to solve.
But the function to get positions from the sensor data may in practice be hard to find / deviate from theory.

Can use capacitive sensing code from rebirth project.


## Material identificator

"whats in the glass"
Like a Tricorder from Star Trek.

## Goal
Be able to detect/classify anything that can fill a glass,
that one can buy in a store or find around the house.
Using non-contact sensing. Does not touch the thing being measured.


## Things to test

Some ideas

Liquids

- water
- juice
- coca-cola
- sprite
- coffee
- milk
- oil
- soap
- carbonated vs non-carbonated drink
- carbonated drink of different colors
- alcoholic vs non-alchol drink
- white vs red wine
- different red wines against eachother
- white rum vs brown rum

Non-liquids

- sand
- larger vs smaller pebbles
- moist sand versus dry
- rice/wheat grains

## Measurable properties

- light reflection
- light transmission. with IR,UV,visible
- infrared emission
- gases emitted. VOC, alcohol, ?
- weight. with standardized level (and container) -> density
- conductivity/resistivity
- capactivity
- heat capacity
- heat conductivity
- acoustic reflectivity? ultrasound

## Form factors

Should have a glass size that is standardised size,
easy to get a hold of, affordable, can be closed, has level indicators.

### Glass hanger

PCB/device hang onto glass beaker.
Simpler, only a single unit.

Top has gas sensors
Mid/lower has LED/light sensors
Capacitive sensor vertically down.

Cannot measure weight/density though.
Could be an add-on.

### Coffee dispenser

Sensors on two sides, over top and the on bottom.
Larger / more complicated build.

Sides

- LEDs + light sensors. Including IR and UV, ideally
- Capacitive sensors.

Bottom

- Weight cell


## Dataset building

Register the bar-code when labeling data?

