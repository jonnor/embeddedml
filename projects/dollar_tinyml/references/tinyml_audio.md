
# Puya PY32

## General overheads between 0.5-1 kB

!! py32f template uses lots of RAM?
2280 bytes by default with HAL
1760 bytes with LL

[jon@jon-thinkpad py32f0-template]$ arm-none-eabi-size -A Build/app.elf 
Build/app.elf  :
section               size        addr
.ram_vector            192   536870912
.isr_vector            192   134217728
.text                 6808   134217920
.rodata                140   134224728
.init_array              4   134224868
.fini_array              4   134224872
.data                  104   536871104
.bss                   444   536871208
._user_heap_stack     1540   536871652

.bss, .data and .ram_vector go into RAM. Total of 740 bytes

_user_heap_stack represents left over space. Actually not used?

avr-nm -Crtd --size-sort the_program.elf | grep -i ' [dbv] '

[jon@jon-thinkpad py32f0-template]$ arm-none-eabi-nm -td -r --size-sort Build/app.elf | grep ' B '
00000312 B __sf
00000076 B DebugUartHandle
00000004 B uwTick
00000004 B __stdio_exit_handler
00000004 B __malloc_sbrk_start
00000004 B __malloc_free_list
00000004 B errno

__sf is for printf support, it has stdout/stderr/stdin I think

Seems prudent to budget at least 1 kB RAM to system things

## CMSIS-DSP RFFT tables too big

CMSIS-DSP RFFT tables are always 8192 long?
Two tables a 16 bit. Takes 32 kB FLASH !!!
https://arm-software.github.io/CMSIS-DSP/latest/group__RealFFT__Table.html#gaf8699e77c7774359b96ef388efa7d453

Looks like one would need to generate those tables oneself, in a smaller size

Remaining code size is 44kB - 32kB = 12 kB. Seems acceptable

arm_mfcc_q15 needs a q31 temporary, 2x the length

arm_mfcc_q15 can be used as reference code, even though we do not want the mel filter part
https://github.com/ARM-software/CMSIS-DSP/blob/647b755ad80d53ecca56a555508084663f97c0eb/Source/TransformFunctions/arm_mfcc_q15.c

## ADC

https://github.com/IOsetting/py32f0-template/tree/main/Examples/PY32F0xx/HAL/ADC/ContinuousConversion_DMA

Uses DMA.
Has a comment re ADC performance. "/* Valid resolution is around 8 bit */"
DMA pheripheral sets a flag. Checking this in main to get the data.
Has a buffer of 1024 32 bit values.
? not clear how many are filled per
? not clear how the samplerate/sampling time is configured

## I2C

Lots of examples of sensor readout available. Including multiple accelerometers.
Nothing for LIS3xx/LI2xx. But ADXL345 etc.

None using DMA though. Would be ideal.
But when reading say 32 samples at 50 Hz, it is not problematic to use I2C blocking read either.
Will just take ~1 millisecond every 500 milliseconds.
Should even be possible to sleep a lot in between?

## Sleep

LL_LPM_EnableDeepSleep();
__WFI();

Examples using low-power timer and RTC:

https://github.com/IOsetting/py32f0-template/blob/2d13ff9f5a0d90ef11de90bd7367093f79dfc82e/Examples/PY32F0xx/LL/LPTIM/LPTIM1_Wakeup/main.c#L36
https://github.com/IOsetting/py32f0-template/blob/2d13ff9f5a0d90ef11de90bd7367093f79dfc82e/Examples/PY32F0xx/LL/RTC/Alarm_Wakeup/main.c#L132

Stop and sleep wakeup is under 10 microseconds.

# Feature processing

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

https://github.com/dpirch/libfvad/
Uses efficient IIR filterbank. Operates on 8 kHz natively.
`VadInstT.feature_vector` exposes the filterbank energy.
Supports a couple of different window lengths, 

# Deep Neural Networks

TinyMaix.
Can run 3 layer CNN with INT8 in under 2 kB of RAM on Puya PY32F0xx.
https://github.com/sipeed/TinyMaix/tree/main/examples/mnist
Runs in 44 ms, over 20 instances per second.
https://github.com/sipeed/TinyMaix/pull/74

Takes 28x28x1 as input (MNIST).
Can maybe go up to 32x32 in similar RAM use?
256 samples @ 8 kHz is 32 ms.
With 32 samples that is a 1024 ms window.
Similar to what is used for Speech Commands.
Maybe it can be sufficient to be useful?


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

#### kahrendt/microWakeWord
https://github.com/kahrendt/microWakeWord

Open source project implementing wake word detection for microcontrollers
Using Tensorflow Lite for Microcontrollers
Has benchmarks and provides result for multiple phrases


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




##### Streaming keyword spotting on mobile devices
https://arxiv.org/pdf/2005.06720.pdf

Converts CNNs and RNNs to streaming
Tests on Google Speech Commands dataset
Focus is on improving latency
Memory usage not much mentioned?




