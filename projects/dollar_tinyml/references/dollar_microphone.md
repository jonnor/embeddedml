
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


INGHAi GMI6050
INGHAi GMI9767


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

