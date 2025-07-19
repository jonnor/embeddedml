
### Quick demo

- Show results on screen
- Make short demo video. 1 minute

### Video script

I recently added support for linear regression for emlearn-micropython,
a machine learning package for MicroPython.

Regression is useful for a bunch of sensor-related tasks,
as a mapping from quantities that we can measure,
to the quantity we are interested in estimating.

To test this out I made a Lux light meter.
Lux measurements are intended to match how the eyes experience light intensitives.
So it uses the photopic luminosity function to weight different wavelengths.
IMAGE: Lux function potted on wavelengths
.. CIE 1931

To measure the light I use a AS7443 spectral sensor.
This sensor can measure light, and has 11 narrow channels in the visible spectrum.
In theory one could apply the photopic function directly.
However one would have to account for the different sensitivities of the different channels.

So instead I opted to try to use machine learning to learn how to sum the different channels to become a Lux value.
I collected data using a variation of light intensities and spectrums, using an cheap Lux meter as a reference.
I used both particular colors by setting the hue setting of the RGB light,
as well as white with different color temperatures.

The test results are pretty good, with under +-50 lux across the range.

And by using emlearn-micropython I can deploy this to my microcontroller,
and now have a Lux meter I can program to do things like logging, sending data via WiFi/BLE, et.c,
or use it in a robotics or control applications.

However I did notice that it does not work well for light coming in at an angle.
The proper Lux meter has a dome that enables catching light from roughly 180 degrees in all directions.
My currently lacks this dome, so is only correct for light coming in from the front.

### Baseline comparison

Normalize the channels based on their specified sensitivity.
And weight the normalized responses by the Lux curve.
Compare the results with linear regression straight.

Might want to try dropping out F5?

### On-device learning

- Try to re-implement the learning in MicroPython, run on-device
MinMaxScaler
Random sampling from files?
train_test split. Ideally respecting groups
RMSE error reporting
r2 metric calculation
- ? positive constraint in emlearn_linreg ?

### More functional Lux meter
Main problem: Only really accepts light straigth from the front
! angle(s) becomes new factors in data collection and test

- Try make a plastic dome. 3d-print and sand
- Disable the red power LED



### Ambient light sensing with basic components

Showcasing linear regression.
Without using any special components.

#### Video script
Did you know you can measure light with an LED?
Using a microcontroller we energize the LED in the reverse direction for brief time.
Then we switches the pin to input mode, to sense voltage over the LED.
After a short time the voltage drops such that the GPIO pin registers as low.
The discharge time is proportional to the amount of light that comes in.
More light, faster discharge.
By measuring at a couple of different datapoint and collecting reference data from a Lux meter, we can use regression to map the values into Lux.

However the values from LED is quite temperature dependent.
Good thing that a regular diode can measure temperature.
The forward voltage decreases with increasing temperature. 
Show graph of this line. And comparison with or without correction.

!! the threshold for the digital pin might also be temperature dependent
Should perhaps measure microcontroller internal temperature sensor also.

An ADC might also be temperature dependent, but is usually designed to minimize.

> The temperature has a major influence on ADC accuracy.
> Mainly it leads to two major errors:
> offset error drift and gain error drift.
> Those errors can be compensated in the microcontroller firmware.
> 
> The maximum error values specified in the device datasheet are the worst error values,
>measured in a laboratory test environment over the given voltage and temperature range

STM32F411 ADC does not specify temp dependency of ADC.
Offset error is max +- 3 LSB.
Gain error max +- 6 LSB for 36 Mhz (!), but +- 3 LSB at 18 Mhz.

Reference voltage has specified Temperature coefficient of 50 ppm/C.
0.005 V, 5 mV, over 100 C range.


### Data collection

#### Things to measure

temp_diode_volts
led_discharge_time_us
micro_temp,
lightmeter_lux
thermometer_c
Light settings. distance,r,g,b,power
temp_ambient_c

! wavelength dependent. Start with a single color.
Ex using RGB led with particular values.

Get internal temperature in MicroPython
esp32.raw_temperature()

### Controlled temperature

Peltier TEC can do heating and cooling.
Would want to find an option that can do both.
MAX1968/MAX1969 is a TEC controller IC. Reference designs for combined heating/cooling systems.
https://www.analog.com/en/products/max1968.html

XH-W1504 has bidirectional TEC control. Relay based.
Can also drive auxilally heating/cooling elements. Like fan.

BTS7960 module would be a good H-bridge for a custom system.

Must avoid frequent polarity changes. Several seconds between each, ideally.
Must have a deadband around the switching point.

Use hot/cold water to create different temperatures.
Or use a glass cube in water, to create enclosed heated/cooled chamber?
Measurement part of reference needs to fit inside. Upside down?
Can use phone to flip readings

Alterntative. Have a heatsink into water, to place electronics on.
Insulate with Kapton/PET. Dont have a heatsink. More complicated...
A metal box would be a compromise. But need a transparent lid. Ex: cookiejar

Solder LEDs and diodes to M5StickC protoboard.
After brief check on breadboard, of diode.
! only 3 GPIO on M5StickC hat connector.


