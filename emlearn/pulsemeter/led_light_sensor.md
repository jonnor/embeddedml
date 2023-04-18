
# LED as light detector

Principles

- Measure photovoltage. High impedance.
- Measure photodiode current
- Measure voltage drop after applying reverse voltage 

## Resources

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

## Bidirectional communication using LED capacitive discharge

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

##

https://www.electroschematics.com/led-2/

Based on the paper by MITSUBISHI.
Uses
LED is mounted between two pins. One analog, one digital.
Analog pin also used in digital mode to drive.
Has a 210 ohm in series with LED. 150Ω to 470Ω recommended.
Has complete example Arduino code.
Uses delay() a lot...

### Multi-Touch Sensing through LED Matrix Displays 
https://cs.nyu.edu/~jhan/ledtouch/index.html
http://www.touchuserinterface.com/2010/02/led-matrix-as-light-touch-sensor.html

Gives 8x8 optical detection.
Used for multi-touch sensing of fingers.

Could be used for "image detection", ie MNIST digits or similar.



### Blinkenlight: LED Camera
https://blog.blinkenlight.net/experiments/measurements/led-camera/
Using 20 LEDs to make a 20 pixel "camera".
Provides some Arduino code.

### Make: How to Use LEDs to Detect Light 
https://makezine.com/projects/make-36-boards/how-to-use-leds-to-detect-light/

Using opamp circuit.

LEDs are not as sensitive to light as most silicon photodiodes.
LEDs are sensitive to temperature. 
One solution is to mount a temperature sensor close to the LED so a correction signal can be applied in real time or when the data are processed.
Some LEDs I’ve tested do gradually lose their sensitivity.

In my experience, the sensitivity of red “super-bright” and AlGaAs LEDs and similar near-IR LEDS is very stable over many years of use.
Green LEDS made from gallium phosphide (GaP) are also very stable.
However, a blue LED made from GaN has declined in sensitivity more than any LED I have used.


### Myzen: LED sensing
http://www.thebox.myzen.co.uk/Workshop/LED_Sensing.html
Shows schematics for Arduino. Uses 220 ohm series resistors, and LED connected to digital and analog ports.

Code does a global disable of pullup resistors.
_SFR_IO8(0x35) |= 0x10;   // global disable pull up resistors

Describes the process

1. Light up the LED by making the anode positive (logic one) and the cathode negative (logic zero)
This fully discharges the LED as a capacitor.
2. Charge up the capacitor by making the anode negative and the cathode positive.
As this is a small capacitor it will take no time at all in other words for as short a time as you can.
3. Put the diode into the measurement mode,
By making the anode negative (it already is) and the cathode connected to an analogue input.
4. Make a measurement of the analogue voltage.
This is a reference level to be used later.
5. Wait while the photon current is integrated - the longer the more sensitive but too long and effects other than photo current dominate.
6. Measure the voltage again and subtract it from the reference value you took before the integration time. This figure is your light reading.

You can apply this to many LEDs.
However, I have found that when you apply it to many LEDs they can interact.
That is cover up one and the readings from the others do down a bit.
This interaction comes about because of the multiplexer inside the Arduino that switches the separate inputs to the one analogue to digital converter (A/D). 
asically there is charge left in the system from the measurement of the previous sensor messing up the next reading.
Therefore there are a few other tricks in the code to minimise the interaction like:
juggling about with the order in which they are scanned,
and discharging the A/D input after the reading has been made.

Finally, as LEDs are not designed as light sensors, the light sensing ability varies from LED to LED.
Red LEDs are the best as they will be sensitive to all colours of light
Blue LEDs will be sensitive to only blue light.
Worst of all are white LEDs some types will only respond to UV light.
The junction size is important so the smaller an LED is the more sensitive it will be,
as the capacitance is smaller and it takes less photons to discharge it.
Finally a clear package will let more light in than a coloured one.
If you want to use LED light sensors as touch sensors then surface mount LEDs are probably best.

The proper way of color detection.
https://electronics.stackexchange.com/a/554074/192064
Using photodiode and optical passband filters on top.
Says that cheap translucent colored plastics can be used in a pinch.

### Arduino Playground: LedSensor

https://playground.arduino.cc/Learning/LEDSensor/
Connects the diode between two digital pins.
Using a 100 ohm diode in series.
Uses plain pinMode/digitalWrite/digitalRead


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


