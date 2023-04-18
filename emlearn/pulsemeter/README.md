
Sensor principle is measuring reflected/absorbed light
Easy with dedicated electronics.
https://lastminuteengineers.com/pulse-sensor-arduino-tutorial/

Can it be done with simple components found in an Arduino starter kit?
Like a LED and LDR, or two LEDs? 




## Demo

Could use detected beat events to trigger LEDs in sync with beat 
Demo could be exercising to increase
Can use commercial BMP monitor on wristband/smartwatch as reference

## Requirements

BPM range heartbeat. 30-200 BPM, 0.5 - 3.3 Hz
Well under line frequency 50-60Hz.
Should probably low-pass to reject that, somewhere between 6.25,12.5,25Hz (3-1 octave, giving 24 to 6 dB rejection)
Should sample at maybe 100Hz. 10 ms max aquisition time.


## Hardware
How to place the electronics?
Use some plastelina etc.

### Light sensing mechanism

Trying to use an LED as the light sensor.
See [led_light_sensor.md](./led_light_sensor.md)



# Scope

## Out of scope

Later: Integration

- Potential for integration into single board with I2C/interrupt
- Running on some small microcontroller. AtTiny etc

Later: on-device learning

- Potential of on-device learning / calibration.

Later: generalized event detection

- Can probably be generalized to other low-rate event detection problems
- Assuming adjustable parameters in the pipeline

# Background

## Prior work
Other examples of making heartbeat detector / pulse sensor

### Leonov
Someone did it with LDR. And lots of op amps. Analog comparator. No active light source.
https://www.hackster.io/104829/detecting-heart-rate-with-a-photoresistor-680b58

### Johan_Ha
Someone did it with infrared 
KY-039 / KY-03 / KY-39 IR transmissive sensor
Arduino code and DSP explanations. Incl demo video
https://projecthub.arduino.cc/Johan_Ha/8c660b94-ae6c-4b1b-b8c9-477facc50262

### PulseSensor
Great candidate for a reference design.

https://pulsesensor.com/
Is a DIY commercial board that is open hardware.
https://pulsesensor.com/pages/open-hardware
Designed to be connected to Arduino etc.
Outputs a signal conditioned analog voltage referenced around Vcc/2.
Uses an analog ambient light sensor, and a ultrabright green LED.

Has also 3d-printable thing for positioning on finger
https://www.thingiverse.com/thing:5649384
Uses a LED and a photo-diode
Uses velcro strap around finger

# Worklog


Arduino Playground LedSensor approach.
Tested with `ledsensor.ino`

- 11 ohm series resistor
- 5 mm clear red LED

```
condition,milliseconds
coverhands,600
ambient,180
phonescreen,50
LED direct,5
```

# TODO

- Switch to green LEDs
- Switch to analog sensing
- Make a holder for light+sensor
- Get readout time down to 10ms.
- Plot data. Verify can get 50 hz ambient. Verify can get pulse signal

