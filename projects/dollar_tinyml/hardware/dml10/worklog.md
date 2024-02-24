
## Subsystems to test

- Charger/regulator
- Microphone+amp
- Microcontroller
- BLE module
- Accelerometer
- LEDs

## TODO

- Add case, test USB connection
- Debug MEMS microphone. Try again on board only exposed to 3.3V

Fixes

- Try rotate LED
- Remove battery charger to avoid BLE module overload

Firmware

- Get I2C working generally
- Get BLE module to send advertising data
- Get accel reading at 100 hz
- Get ADC reading from mic at 8 kHz. Preferably with DMA 

## Found issues

- BLE and MEMS microphone is connected to up to 4.2V VDD. Has 3.6V as absolute maximum rating. Needs 3.3v regulator
- R15 unpopulated. Resistor for white LED
- Blue LED wrong way
- C2 and C11 populated. Should not have been
- R5 populated. Should not have been
- Battery regulator not working without battery connected. Lots of noise on VDD.

MAYBE.

- Other LEDs also wrong way around?

# References

Nice experiments with I2C in a cable
https://axotron.se/blog/crosstalk-problems-when-running-i2c-signals-in-a-cable/

# Worklog

## 23.02.2024


#### Powering up

Board is straight from producer.
BLE module not populated

Powering USB connector. With 5.0 volt

VDD should be charge. Is 4.2 V. OK

Checked VDD and MIC power at all major components. 4.2V OK everywhere

#### Charging battery

Connected LIR1220 battery. Was at 3.0V.
Instantly jumped up to 4.2 V.
OK

Connected LIR2450 battery. Was at 0.0V.
Instantly jumped to 4.125V
Then gradually increases by some millivolts.
OK

#### Powering from battery
! not tested


#### Amplifier

Powering VBUS with 5.0V
DC voltage in analog path should be VDD/2
Measured from mic to AUDIO_HIGH.
All at 2.1V. OK

Checking with Bitscope.
AUDIO_LOW triangular waves 500 us period. 1 volt peak to peak
AUDIO_HIGH square wave. Same period. 4.2 volt peak to peak
500 us period is 2 kHz

Measuring from micorphone. At C12.
No signal that seems to correlate with activity?

!! suddenly 4.0V at the analog points

Tested another card. Back to the triangle waves.
Seems like there miiight be a tiny bit of signal when snapping fingers etc.
At C12

C12 mic side is 0.8V DC.
! Expected to be Vdd/2
? possible microphone orientation wrong, or pinout error?

Removed C2 and C11. Still getting oscillations

Removed mic. Oscillations disappeared

! something wrong with microphone 

Inject 10 mV sinewave. See if amplified correctly

Playing 100 Hz from phone.
Approx 50 mV pp at input. But noisy, hard to say.
Measured 1200 mV pp at
24x gain calculated
Expected gain 20.8
OK. Likely within measurement error

! Seing superimposed 500hz / 2 kHz triangle waves.
Similar to before.

Scoped VDD. Seeing 100 mV of that triangular wave.
VBUS looks clean.
Likely the battery charger.
Coupled in via opamp virtual reference?
Mechanism not so important, have to have higher quality power supply.

Connect LIR1220 battery to charger.
Noise dissappears. OK

Connected 22 ohm resistor dummy load
Batt output got 1.0V
Mangled sinewave signal
Probably too low current setting for this resistor

With 470ohm resistor, 100 uF + 10 uF.
Still messed up sinewave

Testing with elecret microphone. Tiny shotgun used for video, with 3.5 mm jack.
Used external resistor. Tried both 2.2k and 4.7k.
DC voltage at elecret was 2.6V.
Whistling a tone very close to the mic.
Get 500 mV peak to peak at AUDIO_LOW.

## 24.02.2024


#### Accelerometer I2C testing

Using ESP32-S3 with MicroPython
Tried communicating with LIS3DH
Tried communicating with BC7161
Just getting ENODEV or ETIMEOUT
Both on 100 and 400 kHz

Observing SDA and SCL lines on scope.
! Seeing rise times of close to 1500 ns
Out of specification. Need 1000 ns for 100kHz

Have 3k3 pull up.
With 1.2 us time constant, that would be
Effective capacitance of 454.545 pF.
! seems very high. Expected 10-100 pF max

Adding additiona 3.3k pullups
Now rise time is 1000 ns approx
Still not working

Seing sent data being decoded on scope
71 for Holtek
18 for LIS3DH
Not working either on 10 kHz

LIS3DH address.
0x18 is SA0 is low
0x19 if SA0 is high (default)

ACC_CS is 3.2v
1: SPI idle mode / I2C communication enabled
OK

Pinout compared with datasheet.
All looks OK

Accelerometer looks to be oriented correctly.
Pin 1 top right

MicroPython code for LIS3DH works with LIS2DH breakout
Rise time is over 2 us
First transaction is
W:18 A8 R:18 00 FE

LIS2DH Gravity board (working).
Has pull-down for address selection
https://wiki.dfrobot.com/Gravity__I2C_Triple_Axis_Accelerometer_-_LIS2DH_SKU_SEN0224

! we do not have any resistor
In LIS3DH is internally pulled up
Might be the address is 0x19

Changing address=0x19 in code - can read data!

#### BLE I2C testing

Implemented some test code in MicroPython to try to wakeup and run I2C.
Could not get it to respond.
Always EONDEV.
By scope it looked like wakeup sequence was according to spec
But there was no ACK on I2C from device after writing address

? does it actually go out of deep sleep ?
Could try from hard power on

xtal should be ON in light sleep
? probe it

After adding this probe, and powering back on, I2C communication started working.
Not sure why...

#### Flashing microcontroller

Used SDK https://github.com/IOsetting/py32f0-template
Used daplink programmer. With PyOCD
Connected board over SWD
Changed LED blink example from PA0 to PA6

Was able to flash. OK
Was able to toggle GPIO out. OK



