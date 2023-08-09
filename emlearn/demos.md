
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

Moved to [](./pulsemeter)

## Liquid detector

Existing project
https://docs.edgeimpulse.com/experts/prototype-and-concept-projects/liquid-classification-tinyml
Used turbidity and Total Dissolved Solids (TDS) sensors.
Turbidity is done using LED+photodiode.
This could be done with same tech as the LED color detector.
TDS is usually done by measuring conductivity.
Can be done by a fixed distance leads, and a voltage divider.
https://www.circuitbasics.com/arduino-ohm-meter/
Another approach would be a capacitor-discharge measurement with DC.
Or using capacitive sensing with AC at fixed frequency.
https://thecavepearlproject.org/2017/08/12/measuring-electrical-conductivity-with-an-arduino-part1-overview/
has overview of expected conductivities of different liquids
Suggests gold-plated pins or NiChrome wire as
Note that conductivity may be temperature dependent, and should be compensated
https://www.youtube.com/watch?v=vyQcmeR80XM
shows simple voltage divider type

## Cyclic behavior

Actuator that is driven. From state 1 to state 2, continious transition
Change in position should be even over time. For example a linear pattern, or linear angular
Would need to measure position... Then might also have PID.
Setpoint vs actual interesting variable to track

Could track amount of current to the motor. Should be approximately constant
Becomes more interesting with multiple motors/axes



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


## Secret knock detector

Fun and simple project
https://electronics.stackexchange.com/questions/190/how-do-i-detect-the-pattern-of-the-knock-on-a-door-and-use-it-as-a-signature-to

Has potential for usable pretrained models.

The simple-to-try case could be done with just a button.

Threshold analog signal to digital, and count time between pulses?
Might need a bit of debounce. Minimum on/off times.
Keep an sliding window of such values as the feature vector.
A distance metric would probably be the most effective ML solution
But maybe RandomForest can do OK still

Could do it with a piezo.
Would need some input protection and low-pass filtering.
Then can do sampling at 50 hz etc.

Or could do it with audio mic.
Doing same kind of low-pass/envelope et.c. in software.

Could count the times between knocks, use that as features.

## Physical Iris classifier

Mostly for the LOLs.

Using a digital caliper
Make some replicas of the leafs. 3d-print?
Order some real flowers.

The length and the width of the sepals and petals, in centimeters.

Digital calipers often have a port with serial interface.
Outputs measurement as 24 bits.
Runs on 1.5V, so need level converters to interface with 3.3V MCU.
But could run directly on that voltage, if using a 1.8V low-power MCU.
Could probably just sample via ADC also?
Could even run on the caliper battery??
Might need a step up to at 1.8V or 2.0V.
Might be needed to drive a LED anyways. Red LEDS should work from 1.8V. Maybe also at 1.5V.

https://www.robotroom.com/Caliper-Digital-Data-Port.html
https://sites.google.com/site/marthalprojects/home/arduino/arduino-reads-digital-caliper

Step up
https://www.analog.com/en/design-notes/tiny-synchronous-step-up-converter.html
LTC3526LB for 1.8V out

## Handwriting recognition
MNIST etc.

- Inertial. Uses accelerometer/gyro
- Computer vision using camera
- CV using LEDs matrix as sensing element
- Touchscreen. Capacitive/resistive
- TToF distance sensor.

Interial version basically same setup as for magic wand.
Simplest wiring, just I2C to accelerometer. Many options of those. Including on HW.

Real-Time Finger-Writing Character Recognition via ToF Sensors on Edge Deep Learning
https://www.mdpi.com/2079-9292/12/3/685

ToF sensors acquire distance values between sensors to a writing finger within a 9.5 × 15 cm square on a surface.
STM32F401.
Tested long short-term memory (LSTM), convolutional neural networks (CNNs) and bidirectional LSTM (BiLSTM).
Best result is extracted from the LSTM, with 98.31% accuracy and 50 ms of maximum latency.


https://antimatter15.com/2015/06/handwriting-recognition-with-microcontrollers/
LED matrix as CCD. 8x8. Used a light pen.

Static Hand Gesture Recognition Using Capacitive Sensing and Machine Learning
https://www.mdpi.com/1424-8220/23/7/3419

## DIY microphone

The carbon rod microphone was one of the first designs.
Predates the carbon granula "button" microphone.

Principle: The loose contact between two objects is suc
Carbon is practical because it does not oxidice,
and provices an inherent resistance.

https://onetuberadio.com/2015/11/23/science-fair-idea-homemade-microphones/
references November 1945 issue of Popular Science.
Microphone is made using 3 nails, 1 positioned on top of two others, on a sounding board.

http://www.vias.org/crowhurstba/crowhurst_basic_audio_vol1_035.html
Carbon rod vertically, loosely held between two plates 

https://simplifier.neocities.org/compound
Speech sounds pretty good! Clear and OK frequency balance. A bit boxy/resonant.
Uses a thin wood sheet as a diaphram.
Uses 4 carbon rods suspeneded between 2 carbon terminals.
Rods are connected 2 in series, 2 in parallell.
Good contender for making a 3d-printed replica

?? could one use a pencil, and just sharpen it in both ends with pencil sharpener?
Alternatively a pure graphite / charcol pencil, found in art supply stores

https://simplifier.neocities.org/carbon
Diaphragm is a piece of pine board,
with a 3 by 3 inch section milled down to a thickness of 1/16th of an inch.
The loose contact is made between two pieces of 1/4 inch graphite rod.
AC modulation 10mA p2p with normal speaking voice

Matchbox microphone
Many videos showing this on Youtube.
Sound quality tends to be pretty bad however.
Thin 0.5mm rods do not work.
Many recommend sanding the connecting surfaces flat.
Some just let the top electrode lie on top of the others - cannot be moved around.
Others led the top be tensioned slightly across the others - can be moved.

