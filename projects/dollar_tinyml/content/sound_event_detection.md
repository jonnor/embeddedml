
# Sound Event Detection

## Applications

Noise Monitoring
Counting cars
Counting beans cracking. LINK Roest
Voice Activity Detection
Brewing counting detection. Stack 3 frames. Maybe bandpass filter.
Audience clapping detection.

Related tasks
Keyword Spotting
Speech Command



## Ultra low cost Microphone

The go to options for a microphone for a microcontroller based system are 
digital MEMS (PDM/I2S/TDM protocl), analog MEMS or analog elecret microphone.

The ultra low cost microcontrollers we have found, do not have pheripherals for decoding I2S or PDM.
It is sometimes possible to decode I2S or PDM using fast interrupts/timers or a SPI pheriperal,
but usually at quite some difficulty and CPU usage.
Furthermore, the cheapest digital MEMS microphone we were able to find cost 66 cents.
This is too large part of our 100 cent budget, so a digital MEMS microphone is ruled out.

Below are some examples of analog microphones that could be used.
All prices are in quantity 1k, from LCSC.

MEMS analog. SMD mount

- LinkMEMS LMA2718T421-OA5 0.06 USD
- LinkMEMS LMA2718T421-OA1 0.08 USD 
- Goertek S15OT421-005     0.09 USD
- CMM-2718AT-42316-TR      0.47 USD

Analog elecret. Capsule

- INGHAi GMI6050  0.09 USD
- INGHAi GMI9767  0.09 USD 

So there looks to be multiple options within our budget.

## Analog pre-amplifier

Any analog microphone will need to have an external pre-amplifier
to bring the output up to a suitable level for the ADC of the microcontroller.

An opamp based pre-amplifier is the go-to solution for this.
The requirements for a suitable opamp can be found using the guide in
Analog Devices AN-1165, Op Amps for MEMS Microphone Preamp Circuits
https://www.analog.com/media/en/technical-documentation/application-notes/AN-1165.pdf

The key criteria, and their implications on opamp specifications are a follows:

- achieve the neccessary gain (Gain Bandwidth Product) 
- not introduce noise (Input Noise Density)
- flat frequency response (Gain Bandwidth Product)
- not introducing too much distortion (Slew Rate, THD)

Furthermore it must work at the voltages available in the system,
typically 3.3V from a regulator, or 3.0-4.2V from Li-ion battery.

Having an appropriate gain is especially important when ADC resolution is low.
Puya PY32V003 has a 12 bit resolution ADC.
This means a theoretical max dynamic range of 72 dB.
However some of the lower bits will likely be noise, reducing the effective range.
If we are not utilizing the higher ranges, that will further the practical range.

Standard for audio is 16 bit. Or 24 bits for high end audio.

10 bit 60 dB.
8 bit 42 dB.

?? what should the gain be
Speech. 50 dB(A) SPL for nomal speech level at 3 meters.
90 dB for shouting up close.

How much headroom, max versus average level? At least 10 dB? Maybe 20 dB?

TODO: check out dual-channel opamps. So we can have another stage with 20dB / 10x gain

## Audio input

Microphone  Goertek S15OT421-005	0.0888
Opamp       Gainsil GS8621	        0.0702

Totalt of 16 cents, rounding up to 20 cents with passives.


## Feature extraction: Spectrograms

ARM CMSIS

4kB RAM total. 1 kB RAM for feature extraction?

Audio buffer
FFT working buffers
Output buffer


## Kilobyte sized Neural Networks

Proven: RNNs

Unproven: DCT + MLP
Unproven: MLP frame-wise + MLP across frames

4 kB RAM total.
1-2 kB RAM for ML model


CMSIS-NN supports LSTM, but not GRU
