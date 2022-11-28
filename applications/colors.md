
# Using LEDs to detect color
Idea for fun emlearn demo project.

## Capacitive charge method
Requires microcontroller, but very little hardware.
Either just the LED, or a small resistor and LED.

https://www.electronicdesign.com/markets/lighting/article/21777096/single-led-takes-on-both-lightemitting-and-detecting-duties

LED photodiodes are considerably less sensitive than commercial photodiodes
(with a photocurrent about 10 to 100 times smaller),
direct measurement of the photocurrent is difficult without amplification.
Using bidirectional I/O ports with configurable internal pull-ups or tri-state (high-impedance) inputs.
Using a high-impedance input, the circuit can make a very accurate and precise measurement of the photocurrent
by employing a simple threshold technique and the microcontroller's built-in timer-counter.


https://electronics.stackexchange.com/a/905/192064
Essentially a reverse biased led will act as a capacititor,
if it is then disconnected the charge will drain at a rate roughly proportional to the light hitting it.


https://thecavepearlproject.org/2019/08/30/creating-a-normalized-vegetation-index-sensor-with-two-leds/
Using PTFE tape as diffuser

discharge-time readings follow an exponential decay curve,
so we need to take the log of those readings to linearize the data before scaling

Comparing readings from two IR sensors with one at the 940nm H20 absorption peak and another sensor at 890nm,
would let you derive water content.

generally finding that
the blue emitter shifts into UV-A 320-400 nm detection range
the green emitter shifts down to about 440-460 nm
the red LED channel shifts down to ~680nm

Timing an LED light-sensor with Pin Change Interrupts
https://thecavepearlproject.org/2021/05/10/timing-an-led-light-sensor-with-pin-change-interrupts/

Also ton of information on the focusing etc of LEDs when used as solar detectors
Calibrating wrt BH170 (Lux)

## Current flow method
Requires some kind of external amplifier circuitry.
But does not require microcontroller.

https://wiki.analog.com/university/courses/electronics/electronics-lab-led-sensor
BJT/Darlington as amplifier

https://makezine.com/projects/how-to-use-leds-to-detect-light/
LT1006 single-supply op-amp

https://www.eeweb.com/using-led-as-a-light-sensor/
TL071

## Temperature sensing

For a regular diode, Vf/If changes with temperature
Both in forward and reverse direction
Can be used to measure temperature
https://www.semiconductorforu.com/effect-temperature-v-characteristics/


Silicon diode (1n4148 or 1n4007),
when directly biased the voltage between the anode and catode decreases of 2.2mV /°C. 
https://create.arduino.cc/projecthub/microst/thermometer-diode-based-524613

Using reverse current, with discharge method
1n5819 Schottky Diode
1n1418 diode
https://thecavepearlproject.org/2019/11/04/single-diode-temperature-sensor-with-arduino-icu-via-reverse-bias-leakage/
! Add black heat-shrink around  diodes with clear encapsulation. Otherwise will be light sensitive also
1n1418 is better sensor overall because it won’t drop below the Arduino’s timing capability at natural environment temperatures, and it’s discharge takes long enough that jitter becomes an insignificant source of error.

Used SI7051 as a reference temperature sensor, for calibration.

Used NTC calculator to create
And then standard Steinhart-Hart equation

Another potential problem is moisture accumulating on surfaces -
which could provide an alternate current path to discharge the diode.
So as with our LED light sensing, desiccants are required inside the logger housing


## Data collection

Setup

- A standard RGB color sensor would be used as reference.
- Using RGB LED lights as the stimuli.
- Program a sequence that covers the whole RGB space
- Record the data

Ideally able to get 1 sample in 10 ms.

10 samples per dim in under 1 minute
((10**3)*10e-3)/60 = 0.16666666666666666

70 samples per dim in 1 hour
((70**3)*10e-3)/60 = 57.166666666666664

Might want multiple repetitions.
Probably do not need so many levels.
So maybe 20 samples per dim, and 5 repetitions is better.

Potentially under different environmental conditions:
- temperature
- humidity
- voltage levels

## Regression demo

Output the RGB color when given a light stimuli

Output the RGB color when given an object stimuli.
Must then trigger a white high-quality LED
Could use a paper swatch for different colors

## Classification demo

Use for object classification.
Single pixel "camera".
Put objects of different color in front of sensors.
Fire a white light at object. Record stimuli from sensor elements

## Integration demo

Could put everything on a single board
Using small microcontroller. AtTiny etc
APA102 RGB LED as output indicator
Some way of triggering measurement
Maybe put into a DIL form-factor? With castellation
Maybe have I2C output. Compatible with some existing sensor

## Reference sensor

SparkFun RGB Light Sensor - ISL29125
https://www.sparkfun.com/products/12829
I2C, 3.3V. Tiny package.

RGB Color Sensor with IR filter and White LED - TCS34725
https://www.adafruit.com/product/1334

Adafruit AS7262 6-Channel Visible Light / Color Sensor Breakout
https://www.adafruit.com/product/3779

