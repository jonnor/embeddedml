
## FFT tiny

https://www.embedded.com/develop-fft-apps-on-low-power-mcus/
Need 2N 16-bit variables for FFT data
For 256 length FFT, needs 1,024 bytes of RAM
radix-2 is a reasonable base
possible to optimize for real-valued FFT
LUT for cos+sine. Needs 2 x N/2 int16 values, or approx NFFT bytes

arm_rfft_q15 is probably a good starting point for a test

Existing tests of arm_rfft_q15
https://m0agx.eu/practical-fft-on-microcontrollers-using-cmsis-dsp.html

Used a Cortex-M3
FFT size: 256, CPU cycles to do the FFT: 31919
Was able to process 8 kHz signal with 2% CPU, on 48 Mhz chip

Probably slower on ARM Cortex M0+ grade hardware.
But sounds like it could be doable in under 20% CPU on 24 Mhz RISC-V/CortexM0


https://community.st.com/t5/stm32-mcus-products/fft-in-stm32f0/td-p/453552
256-FFT (Complex in Q15 Format)
Cortex-M0   : 175 375
Cortex-M0+  : 136 296 cycles
Cortex-M3   :  41 430 cycles
Cortex-M4   :  18 480 cycles

>>> 1000*(136296/24e6)
5.679 milliseconds

At 16 kHz, 256 samples is 16 ms. At 25% CPU. But with 50% overlap, looking at 50% CPU
At 8 kHz, 256 samples is 8 ms. Then 25% CPU total. OK

## IIR filterbank


https://notblackmagic.com/bitsnpieces/digital-filters/
STM32F103 Cortex M3 @ 72 Mhz
1024 samples in 4.5 ms
Fourth order IIR in q15

IF the M0+ at 24Mhz is same speed as M3 (it is not),
then 16 IIR filters would take
>>> 4.500*((72/24)*1)*(256/1024)*16
54.0 ms


## Audio Anomaly detection

There is an MLP example in DCASE baselines.
Can we get it down to kilobyte size?


## Keyword spotting / Spoken Word Recognition / Speech Commands 

Extremely well researched.
Lots of examples online. Including easily accessible tutorials etc.
Can be extended to general Audio Classification at ~1 second resolution is OK.

Audio duration needed
Minimum 1 second. Enough for single-words like in Google Speech Commands dataset.


MFCC 13 coeffs
20 ms = 50 frames
13x50 = 650.
Can work within 1 kB buffer. If using 8 bits.

https://github.com/KinWaiCheuk/AudioLoader/blob/master/AudioLoader/speech/speech_README.md#SpeechCommandsv2


#### Keyword Spotting System using Low-complexity Feature Extraction and Quantized LSTM

MFCC feature extraction usually the most power-consuming block of the system
Using a filter bank composed of 16 channels with a quality factor of 1.3 to compute a spectrogram
90.45% accuracy on 12 classes of the Google Speech Command Dataset,
using an LSTM network of 64 hidden units,
with weights and activation quantized to 9 bits and inputs quantized to 8 bits.
Logarithmic scaling input before 8 bit conversion.
Center frequencies spread from 50 Hz to 5 kHz.
Third-order bandpass filters.
25 ms frames, with 12.5 ms overlap.
Proposes filterbank to be implemented in hardware.
? is this approach faster when done in pure SW?
16 instances of third order IIR vs one FFT.
Probably not, at least without implementing multirate

#### Integer-Only Approximated MFCC for Ultra-Low Power Audio NN Processing on Multi-Core MCUs

32 bit integer MFCC approxmimation. Same accuracy as floats.
Using 16 bit, only 0.3% drop.
Tested on Google Speech Commands.




