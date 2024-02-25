
# Audio input for 20 cents USD

TLDR: Using analog MEMS microphone with an analog opamp amplifier, it is possible to add audio processing to our sensor. The added BOM cost for audio input is estimated to be 20 cents USD.
A two-stage amplifier with software selectable high/low gain used to get the most of limited performance of the internal microcontroller ADC.
The quality is not expected to be Hi-Fi, but hopefully enough for many practical Audio Machine Learning tasks.

## Ultra low cost microphones

The go-to options for a microphone for a microcontroller based system are 
digital MEMS (PDM/I2S/TDM protocl), analog MEMS, or analog elecret microphone.

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
- CUI CMM-2718AT-42316-TR  0.47 USD

Analog elecret. Capsule

- INGHAi GMI6050  0.09 USD
- INGHAi GMI9767  0.09 USD 

So there looks to be multiple options within our budget.

The sensitivity of the MEMS microphones are typically -38 dBV to -42 dBV,
and have noise floors of around 30-39 dB(A) SPL.

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

## ADC considerations

The standard bit-depth for audio is 16 bit, or 24 bits for high end audio.
To cover the full audioble range, samplerate should be 44.1/48 kHz,
however for many Machine Learning tasks 16 kHz is sufficient.
Speech is sometimes processed at just 8 kHz, so this can also be used.

Puya PY32V003 datasheet says specify power consumption at 750k samples per second.
However ADC conversion takes 12 cycles, and the ADC clock is only guaranteed to be 1 Mhz (typical is 4-8 Mhz).
That would leave 83k samples per second in the worst case, which is sufficient for audio.
In fact we could use an oversampling ratio of 4x or more - if we have enough CPU capacity.

The ADC resolution is specified as 12 bit. This means a theoretical max dynamic range of 72 dB.
However some of the lower bits will be noise, reducing the effective bit-depth.
Realistically we are probably looking at an effective bitrate between 10 bit (60 dB) and 8 bit (42 dB).

Practical sound levels at a microphone input vary quite a lot in practice.
The sound sources of interest may vary a lot in loudness, and the distance from source to sensor also has large influence.
Especially for low dynamic range, this is a challenge:
If the input signal is low, we will a have poor Signal to Noise Ratio, due to quantization and ADC noise.
If the input signal is high, we risk clipping due to maxing out the ADC.


## Finding the gain

The gain is a critical parameter for amplifier design, as it influences almost all other requirements.

If we look at speech as reference. Normal speech level at 3 meters is approximately 50 dB(A) SPL, and up to 90 dB(A) SPL for shouting up close.
These are short-time average levels. And because the sound pressure is not constant, the max level (which system also needs to represent) is quite a lot higher.

Given a microphone with a sensitivity of -38 dBV, and allowing for 20 dB headroom, the ideal gains would be between 65 dB (1800x) and 25 dB (18x).

<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>preamp_gain</th>\n    </tr>\n    <tr>\n      <th>level</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>50.0</th>\n      <td>65.52</td>\n    </tr>\n    <tr>\n      <th>60.0</th>\n      <td>55.52</td>\n    </tr>\n    <tr>\n      <th>70.0</th>\n      <td>45.52</td>\n    </tr>\n    <tr>\n      <th>80.0</th>\n      <td>35.52</td>\n    </tr>\n    <tr>\n      <th>90.0</th>\n      <td>25.52</td>\n    </tr>\n  </tbody>\n</table>

## A two-stage amplifier, selectable gain

Intergrated Circuits for operational amplifiers come with either 1, 2, or 4 opamps. It turns out that a chip with 2 opamps can be had for basically the same price as 1. It is generally a good idea to split amplification into multiple stages, as this is less likely to hit the limits of the Gain Bandwidth Product of the opamp.
However in this case we can get another benefit which is more important: the ability to have two different gains. By providing them both to the microcontroller as separate ADC channels, we can switch between them in software.
This can either be used statically in form of a high/low switch.
Or it could be done dynamically by monitoring the inputs, as a very crude form for Automatic Gain Control (AGC).


IMAGE: schematic of audio amplifier


## Selecting the operational amplifier

Now we know all the parameters to select opamp.

- Gain needed. Up to 40 dB / 100x (per stage).
- Bandwidth. Audio range, 20 kHz.
- Mic noise floor. -102 dBV
- Output voltage. 3.0V peak to peak

From this we can compute the key opamp specs.
Equations are covered in the reference design.

- Gain Bandwith Product (GBP). 2 Mhz
- Noise density. 20 nV/Hz
- Slew rate. 0.25 V/us

I reviewed a bunch of cheap opamps at LCSC, that can run on the relevant voltages.
Their specifications can be seen in the following table:

'<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th></th>\n      <th>cost</th>\n      <th>current</th>\n      <th>noise_density</th>\n      <th>slewrate</th>\n      <th>gbp</th>\n    </tr>\n    <tr>\n      <th>part</th>\n      <th>manufacturer</th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>LMV321IDBVR</th>\n      <th>UMW</th>\n      <td>0.0290</td>\n      <td>0.06</td>\n      <td>27.0</td>\n      <td>0.52</td>\n      <td>1.00</td>\n    </tr>\n    <tr>\n      <th>TLV333</th>\n      <th>TI</th>\n      <td>0.2085</td>\n      <td>0.06</td>\n      <td>55.0</td>\n      <td>0.16</td>\n      <td>0.35</td>\n    </tr>\n    <tr>\n      <th>LM321LVIDBVR</th>\n      <th>TI</th>\n      <td>0.0320</td>\n      <td>0.09</td>\n      <td>40.0</td>\n      <td>1.50</td>\n      <td>1.00</td>\n    </tr>\n    <tr>\n      <th>GS8621</th>\n      <th>Gainsil</th>\n      <td>0.0702</td>\n      <td>0.25</td>\n      <td>18.0</td>\n      <td>1.66</td>\n      <td>3.00</td>\n    </tr>\n    <tr>\n      <th>GS8721</th>\n      <th>Gailsil</th>\n      <td>0.0847</td>\n      <td>1.50</td>\n      <td>12.0</td>\n      <td>9.00</td>\n      <td>11.00</td>\n    </tr>\n    <tr>\n      <th>LMV721</th>\n      <th>Tokmas</th>\n      <td>0.0732</td>\n      <td>1.50</td>\n      <td>11.5</td>\n      <td>9.00</td>\n      <td>11.00</td>\n    </tr>\n  </tbody>\n</table>'

We see that the commodity low-cost, low-power LMV321 type chips are slightly out of spec,
in both noise density and gain bandwidth product.
The LMV721 class of devices have more-than-good enough performance.
The GS8621 is a good alternative that has lower power consumption.


## Audio input BOM

Microphone  Goertek S15OT421-005	0.0888 USD
Opamp       Gainsil GS8632	        0.0789 USD

Totalt of 16 cents, rounding up to 20 cents with capacitors and resistors.

## Next

Now that we have established that the hardware should be able to receive the audio,
we need to validate that we are able to process the audio signal with our rather weak microcontroller. That will be the topic of an upcoming post.



