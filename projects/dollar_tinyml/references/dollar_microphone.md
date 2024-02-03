
## Microphone

### Analog MEMS microphone

https://www.lcsc.com/products/Audio-Components-Vibration-Motors_385.html
Both MEMS and elecret microphone below 0.1 USD

MEMS microphones down to 0.03 USD @ 1k

LinkMems
LMA2718B381 / LMA2718T421
200μA, -42 dB sensitivity
LCSC, US$0.0326 @ 1k


### Top port 1.85x2.75mm, 4 pin

Same size:
https://www.digikey.com/en/products/filter/microphones/158?s=N4IgjCBcoCwdIDGUBmBDANgZwKYBoQB7KAbRAGYxyB2KkAXQIAcAXKEAZRYCcBLAOwDmIAL4EYANiihkkdNnxFS4AAxqArA2ZtInHgOFiQADjDwZqTLgLFIZOOWMAmTYxCt2XPkNFGpCXgATdgBaMBUIbXYQAgBHFgBPdnC1GJBEphx2NCxkEREgA

! Note: 4 pin is only one pinout variation.

Lowest cost: LMA2718T421, LCSC. 0.03 USD @ 1k

Compatible

- Goertek S15OT421-005
- CMM-2718AT-42316-TR
- LMA2718T421

specifications



### Bottom port 1.85x2.75mm.

Correct size:
https://www.digikey.com/en/products/filter/microphones/158?s=N4IgjCBcoCwdIDGUBmBDANgZwKYBoQB7KAbRAGYxyB2KkAXQIAcAXKEAZRYCcBLAOwDmIAL4EYANiihkkdNnxFS4AAxqArA2ZtInHgOFiQADjDwZqTLgLFIZcgCYHlCIxCt2XPkNFGpCXgATdgBaMBUIbXYQAgBHFgBPdnC1GJBEphx2NCxkEREgA

Lowest cost: LMA2718B381-OA5-2, LCSC 0.03 USD @ 1k.

Compatible:

- 


### Analog elecret microphones


INGHAi GMI6050  0.0899 
INGHAi GMI9767  0.0844 


### Analog opamp

SOT23-5 options under 0.1 USD
https://www.lcsc.com/products/Operational-Amplifier-Comparator_515.html

Single channel SOT32-5. 2.75x3.0mm
SO70-5 would be alternative. Bit smaller size. 2.1x2.0 mm
SO-8 dual is the old standard. Much bigger. Approx 6x5 mm

Conclusion for single amplifier
A GS8621 class device is needed. Costs 0.07 USD @ 1k. 250 uA consumption.
LMV321 class opamp is limited by GBP, and has slightly too high input noise.
Would probably limit microphone performance a little bit.

Can work around the GBP by using dual opamp.
But will not solve the noise.
Power requirements and.
If not concerned with these, might be able to get dual opamp in SOIC-8
with same specs for better price. More flexible in the design.

MD1621 very similar to GS8621
NCS20061, MCP6476 might also be similar

TL08x and TL07x only work from 4.5V.
Not working on lipo battery.
Is an option on USB powered.


## Opamp specifications and selection

Analog Devices AN-1165, Op Amps for MEMS Microphone Preamp Circuits
InverSense AN-1165, Op Amps for MEMS Microphone Preamp Circuits

Matching the peaks of the microphone’s signal level to the full-scale
input voltage of an ADC makes maximum use of the ADC’s dynamic range,
and reduces the noise that subsequent processing may add to the signal

Op amp’s voltage noise in a preamp design. noise density unit of nV/√Hz.

The current noise becomes limiting in the design only when high value resistors are used
To keep low, typically resistors with values less than 10 kΩ are used.

Assuming uniform noise spectrum, to get the device noise in the bandwidth of interest,
multiply this noise density by the square root of the bandwidth.
For 20 kHz bandwidth, this multiplication factor is 141

Noise density plot. Want that the 1/f range is below 20Hz.
And reasonably flat in audible range.

Microphone self noise. Noise floor given by sensitivity and SNR.

Op amp should be to be significantly quieter than microphone. At at least 10 dB quieter.

Typical gain for MEMS microphones. Usually below 40 dB of gain, which is a factor of 100.
Recommends designing for 50 kHz bandwith, 2.5x safety factor

Common-mode rejection (CMRR) is a spec that is of more concern for noninverting circuits than for inverting topologies.

Invering. R1 resistor forms a voltage divider with the MEMS microphone output
Neds to be high enough not to load the microphone output, but not so high that it adds unnecessary noise to the circuit.
The analog MEMS microphones typically have an output impedance of 200 Ω.
If R1 is chosen to be 2.0 kΩ, the resulting voltage divider reduces gain by under 10%.

Select the cutoff frequency at least one octave below that of the microphone.


## Programmable Gain Amplifiers

12 bit up to 72 dB  dynamic range,
and 16 bits up to 96 dB dynamic range.

### Digital potmeter

https://www.lcsc.com/products/Digital-Potentiometers_620.html
MCP4017T-502E/LT
US$0.4519 
Too expensive in this project.

### Switched resistor gain

Programmable Gain Amplifier. Using switching of resistors.
JFET recommended. Or integrated analog switch.
Should be done in second stage, to avoid introducing noise.

Analog switches
SN74LVC1G66 0.0432 @ 1k

Is an acceptable cost.
20 dB is 4 bits gain.
Alternative is an 16 bit ADC, over SPI.

ES7243E
Low noise PGA
24-bit, 8 to 48 kHz sampling frequency
I2S output
Auto level control (ALC) and noise gate
USD 0.2514 @ 1k

MCP3461/MCP3462
SPI interface 
Programmable Gain: 0.33x to 64x




### ADC multiplexiing

Use 2 ADC inputs on the microcontroller?
Each to a different gain stage.
Switch between them as needed.



## Output

Sound Event to MIDI?
DIN-5 connectors around US$0.1698
For plugging into music instruments, front-of-house, DMX lighting controllers etc

MIDI uses 31250 baud.
5 volts. Can be done with just NPN.
But optocoupler preferred for input/output.
https://www.pjrc.com/teensy/td_libs_MIDI.html
MIDI sometimes using TRS. However there are two different pinouts. And it is still less common?

DMX for lighting control.
Uses RS-485. Off the shelf tranceivers

RS1905 0.0759 USD

I2C at 1 meter. Should be OK with shielded cable. Would benefit from a bus extender.
For example PCA9617A. Or the older PCA9515. Or 

https://www.reddit.com/r/AskElectronics/comments/hq1vyh/why_does_my_i2c_bus_perform_worse_with_shielded/

> I've recently done a test board to try and use the PCA9615 or P82b96 in a noisy (automotive) environment
> specifically to avoid putting a micro at the "far" end
> but came to the conclusion that they are a pain in the arse
> and not worth the effort over putting a small low-power micro and a cheap RS485 chip down.

