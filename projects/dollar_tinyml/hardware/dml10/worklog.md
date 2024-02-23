
## Subsystems to test

- Charger/regulator
- Microphone+amp
- Microcontroller
- BLE module
- Accelerometer
- LEDs

## TODO

Tests

- Try flash microcontroller over SWD
- Solder on BLE module. Try communication over I2C
- Try talk to accelerometer over I2C

Fixes

- Try rotate LED
- Try debug MEMS microphone

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

## Issues

- R15 unpopulated. Resistor for red LED
- Blue LED wrong way
- C2 and C11 populated. Should not have been
- R5 populated. Should not have been

- Battery regulator not working without battery connected. Lots of noise on VDD.

MAYBE.

Other LEDs wrong way around?
