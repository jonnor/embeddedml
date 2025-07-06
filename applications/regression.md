
Temperature compensation

## Temperature compensation for load cells

Noticable temperature effect. Varies between units.
Can be compensated using linear factors.
There is also a gain offset, per unit. Can be compensated in same way.

https://www.phidgets.com/?view=articles&article=LoadCellCorrection

If you plan to run your load cells for longer periods of time,
we recommend using a temperature probe.
Preferably a small RTD (though a thermocouple will also work), to measure the temperature of the load cell directly for temperature compensation.

Worst case uncompensated error measured here is 0.3% of full-scale over 5°C.
With temperature compensation, this has been reduced to 1 gram of error as a worst-case on all scales, or 0.02% full scale.


M5Stack has very nice hardware units for load cells.
https://docs.m5stack.com/en/unit/Unit-Mini%20Scales
https://docs.m5stack.com/en/unit/UNIT%20Scales
https://docs.m5stack.com/en/app/scales_kit
Temperature sensor not included.

## Torque estimation

Measure current and voltage. Estimate torque from this.
Should also measure rotation speed RPM.
Use a brake dynanometer to generate different torques.
Brake on brushless motor with ESC in brake mode.
Use a loadcell on a lever mounted to break, to measure the torque.
Brake motor must be able to rotate slightly. Use bearings for this.
Can also learn the ESC setting to torque mapping?


## Windspeed using heated wire (Thermo anemomemeter)

The technique is called as “hot-wire” technique,
and involves heating an element to a constant temperature and then measuring the electrical power that is required to maintain the heated element at temperature as the wind changes. 


Possible reference devices

- RS PRO RS-72H Hotwire Probe
- Extech SDL350
- https://wiki.dfrobot.com/F1031V_Mass_Air_Flow_Sensor_SKU_SEN0360 gives SLM, temperature compensated

Can be done with ICs also.
CG-Anem by ClimateGuard. I2C interface. Designed to be used in air duct.
https://www.tindie.com/products/climateguard/wind-sensor-with-i2c-anemometr-arduino/

https://moderndevice.com/products/wind-sensor
Schematics available under Creative Commons SA
Uses 10k PTC. And a ? regular resistor?
Outputs both raw voltage from bridge.
Outputs a conditioned voltage, with zero offset comp? And some gain.
Outputs temperature from 
Assumes 5 volt regulated input.
Notes that device can be used periodically. But 10 second settling time needed.
Current consumption will be naturally windspeed dependent.

https://moderndevice.com/products/wind-sensor-rev-p
Designed for 12v operation. Up to 40 mA consumption.
Switch mode step-down to 9 for powering sensing element.
3V3 regulator for analog IO interfacing.
One opamp used for the bridge servo. Other 3 for output conditioning.
Schematics available under Creative Commons SA
10k PTC as sensing element.
Added IC temperature sensor on sensing fingers, for ambient compensation.
Uses gaps in the PCB (to sense also wind from below?),
as well as offset between fingers (to prevent heating in the flow?).


#### Informational references
 

Anemometer, Introduction to Air Velocity Measurement
https://www.dwyeromega.com/en-us/resources/anemometers

Constant-temperature anemometers are popular because of their high-frequency response, low electronic noise level, immunity from sensor burnout when airflow suddenly drops, compatibility with hotfilm sensors, and their applicability to liquid or gas flows.

Constant-power anemometers do not have a feedback system. Temperature is simply proportional to flowrate. They are less popular because their zero-flow reading is not stable, temperature and velocity response is slow, and temperature compensation is limited.


Windspeed Indicator Circuit using Inexpensive Diodes, MTM Scientific, Inc 
https://www.mtmscientific.com/anem.html

Using 2 diodes, and a DC amplifier chip.
One diode is exposed to airstream, other is not.

Thermal anemometers, Amateur design report by Johan Liljencrants
http://www.fonema.se/anemom/anemom.html
Tested many different configurations of diodes, transistors and heating.

Use a heated diode as a flow sensor
https://www.edn.com/use-a-heated-diode-as-a-flow-sensor/
Used heater wire wrapped around the diode.

Thermal Minutes, Understanding Hot-Wire Anemometry
https://www.mouser.com/catalog/additional/ATS_Qpedia_Dec07_Understanding%20hot%20wire%20amemometry9.pdf

Most hot-wire anemometers are used in a constant temperature configuration.
Wheatstone bridge. One resistor is the hot wire. One resistor is adjustment.

King’s Law. To calibrate the hot-wire anemometer,
the second power of the measured values for the current I2 are plotted vs. the square
root of corresponding known velocities.

Non-bridge NTC thermistor anemometer with programmable sensitivity
https://www.sciencedirect.com/science/article/abs/pii/S0955598624000244
Using an MCU to regulate.

https://www.electronics-lab.com/page/96/?blog%2Fpage%2F154%2F&m=..
The hot-film type sensor is more common. It consists of a heating element (typically a temperature-dependent, low-ohm platinum resistor) and an additional temperature sensor. 


Mass airflow sensor MFA is similar principle.
Used in cars to measure air going into motor.

## Windspeed using strain gauge

Measures in multiple directions, to also get wind direction.
Need to thermally compensate.
Both strain gauge and the material itself has thermal effects.
https://www.youtube.com/watch?v=VRTdikyyJBE
https://smartsolutions4home.com/ss4h-wg-wind-gauge/

