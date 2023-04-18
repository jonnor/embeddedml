
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

## Pulse sensor / heartbeat monitor

Sensor principle is measuring reflected/absorbed light
Easy with dedicated electronics.
https://lastminuteengineers.com/pulse-sensor-arduino-tutorial/

Can it be done with simple components found in an Arduino starter kit?
Like a LED and LDR, or two LEDs? 

Someone did it with LDR. And lots of op amps. Analog comparator. No active light source.
https://www.hackster.io/104829/detecting-heart-rate-with-a-photoresistor-680b58

Someone did it with infrared 
KY-039 / KY-03 / KY-39 IR transmissive sensor
Arduino code and DSP explanations. Incl demo video
https://projecthub.arduino.cc/Johan_Ha/8c660b94-ae6c-4b1b-b8c9-477facc50262


Could use detected beat events to trigger LEDs in sync with beat 
Demo could be exercising to increase
Can use commercial BMP monitor on wristband/smartwatch as reference

Can also hold finger to throat, and tap the pulse.
For example on a capacitive input!!

Also exists simple I2C chips that can be used to get it programatically.
Like MAX30100

BPM range. 30-200 BPM, 0.5 - 3.3 Hz
Well under line frequency 50-60Hz.
Should probably low-pass to reject that, somewhere between 6.25,12.5,25Hz (3-1 octave, giving 24 to 6 dB rejection)

Can probably be generalized to other low-rate event detection problems
Assuming adjustable parameters in the pipeline

How to place the electronics?
Use some plastelina etc.

Make a dataset. Vary

- Heartrate

Co-variates 

- Placement on finger
- Which finger
- Person
- Ambient light
- Ambient temperature
- Skin moisture
- Skin temperature

What if one would vary the sensor construction also.
Is it realistic to have an universal model?

Note that it is normal to have some variation between beats.
Termed. Heartrate Variability

Later

Potential of on-device learning / calibration.
Potential for integration into single board with I2C/interrupt
Running on some small microcontroller. AtTiny etc

### LED as light detector

Principles

- Measure photovoltage. High impedance.
- Measure photodiode current
- Measure voltage drop after applying reverse voltage 

#### Robotroom: Reversed LED photodiode
https://www.robotroom.com/ReversedLED2.html
Schematic based on an opamp. 3x 10megaohm as feedback resistor
LEDs are connected in reverse to input.
Says to use ultrabright LEDs with clear lenses for highest current.
Old LEDs tinted/diffuse lenses won’t provide enough current to work at all.
Suggests using multiple LEDs to increase current flow.

https://www.robotroom.com/ReversedLED3.html
has results.
Just the LED was 1.5 to 2.5 volts range with increasing amount of light
Only shows digital output from amplifier circuit.

#### EEEWeb: Using LED As A Light Sensor
https://www.eeweb.com/using-led-as-a-light-sensor/

Uses LED in forward?
Uses JFET omamp to amplify. TL071

#### Analog electronics lab: LED as light sensor - ADALM2000
https://wiki.analog.com/university/courses/electronics/electronics-lab-led-sensor

Using a LED in reverse, combined with a standard NPN transitor (2N3904).
Seems to show voltages of 4.5V with low light, to 120 mV with full light.
Pretty good range?


Also suggests using a darlington pair intead.


## Sparkfun: T³: Using LEDs as Light Sensors

Uses a LED connected in reverse directly to Arduino pins.
Measures the discharge time after applying a voltage
If more light falls on the LED, it will discharge very quickly. In darkness, it will discharge very slowly.

Notes that input LEDs need to be fairly close to the microcontroller's pins to work.
Originally tried wiring the sense LED to a breadboard from the Arduino,
but the inductance and capacitance from the wires and breadboard threw the readings way off.

IDEA: add another input to compensate?
A wire following the same path, but no LED.
Sampled in the same way as LED. Use the difference as basis for the value?

IDEA: use multiple LEDs to increase sensitivity?

## 2003 paper on using LED capacitive discharge

Paper: Very Low-Cost Sensing and Communication Using Bidirectional LEDs
Paul Dietz, William Yerazunis, Darren Leigh
2003.
MITSUBISHI ELECTRIC RESEARCH LABORATORIES
Demonstrated communication over a few centimeters range,
with bitrate of 250 bits/second.
https://www.merl.com/publications/docs/TR2003-35.pdf

Shows voltage dropping 5 volts in 100 us when shining on with LED,
and 1.2 volts drop with ambient room lights.
Would require some 10-100khz sampling to do analog.

### Arduino examples uinsg LED capacitive discharge

https://github.com/ForrestErickson/LEDasSensor
https://www.instructables.com/Bi-directional-LED-Sensing-Try-out/


### Matched JFET photodiode opamp 
https://www.electronicdesign.com/technologies/analog/article/21806128/matched-jfets-improve-photodiode-amplifier
Using matched JFETs in front of opamp to boost performance.
High end AC photodiode applications

## Using capacitive touch libraries

Could one use the popular Arduino libraries for capacitive touch sensing,
to measure the LED photo-diode?
Is conceptually the same thing

https://github.com/MrYsLab/OnePinCapSense



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

