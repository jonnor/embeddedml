
# Device Support

## Nordic NRF52

PDM support limited to 1.0-1.3 Mhz.
Limits possible microphone choices.
Unable to use low-power microphone modes (768 kHz).
EasyDMA always takes 1.2 mA.

https://github.com/zephyrproject-rtos/zephyr/tree/main/samples/subsys/usb/audio/headphones_microphone

256 STFT with ARM CMSIS
```
Board 	                                    f32 time 	q15 time
Arduino Nano 33 IoT (Cortex-M0+ @ 48 MHz) 	21784 us 	1720 us
Arduino Nano 33 BLE (Cortex-M4F @ 64 MHz) 	541 us 	    393 us
Teensy 4.0 (Cortex-M7F @ 600 MHz) 	        24 us 	    19 us
```
https://towardsdatascience.com/fixed-point-dsp-for-data-scientists-d773a4271f7f


## Nordic NRF53

PCM/I2S and ADC all suitable for audio-rate input.

## RP2040

Can do audio input on analog ADC or PDM microphone using
https://github.com/ArmDeveloperEcosystem/microphone-library-for-pico

133 Mhz. Cortex M0+, no FPU.

## ESP32

PDM/I2S support in ESP-IDF.

10ms @ 16kHz with 256 FFT on 40 Mhz clock, expected 0.39-1.13 ms with esp-dsp
6 IIR float32 biquads in approx the same time.
https://docs.espressif.com/projects/esp-dsp/en/latest/esp32/esp-dsp-benchmarks.html

## STM32

PDM/I2S and ADC all capable of efficient audio-rate input.
Some models with DFSDM capable of ultra-low-power audio readout.

## AVR8

These devices are on the smaller side of what microvad aims to support,
as they have very little RAM, no FPU and generally very low CPU performance.
But it should still be possible to run very simple things at 8 kHz samplerate.

No support for PDM/I2S.
ADC can only to 10 bit.
No DMA, CPU has to fetch every sample.

AtMega32u4 has native USB support.
LUFA project implements USB 1.0 Audio class device.
The `AudioInput` example implements reads from ADC channel 1 (microphone or similar). 
https://github.com/adafruit/lufa-lib/blob/master/trunk/Demos/Device/ClassDriver/AudioInput/AudioInput.c

https://github.com/Klafyvel/AVR-FFT
contains FFT implementations, tested up to length 256.
Fastest is 11.6 ms for int8 and 30 ms for int16.

https://github.com/bradley219/avr_fft
8-bit AVR ATmega328P running at 20MHz.
Audio is sampled at 40.3kHz by the AVR's built-in 10-bit analog-to-digital converter.
Implements real-time spectrum display, using FFT.
Got the following results
;  Points:   Input, Execute,  Output,    Total:  Throughput
;   64pts:   .17ms,   2.0ms,   1.2ms,    3.4ms:   19.0kpps
;  128pts:   .33ms,   4.6ms,   2.4ms,    7.3ms:   17.5kpps
;  256pts:   .66ms,  10.4ms,   4.9ms,   15.9ms:   16.1kpps
;  512pts:   1.3ms,  23.2ms,   9.7ms,   34.2ms:   14.9kpps
; 1024pts:   2.7ms,  51.7ms,  19.4ms,   73.7ms:   13.9kpps

These seem just barely enough to handle 8 kHz sample rate at real-time,
with over 50% CPU usage.


Coding 16-bit (8:8) IIR filters in Assembler, allowed to run
10 2-pole IIR filters or 8 4-pole Butterworth band pass filters at a sample rate of 8KHz.
But the limited precsion means one cannot use very narrow filters,
and filter accuracy must be verified
https://people.ece.cornell.edu/land/courses/ece4760/Math/DigitalFiltersVersion2.pdf

With a 6 band IIR filterbank, fvad might be able to run?

Power consumption at typical 5V and 16 Mhz is approx 10 mA for ATmega328P and 15mA for AtMega32u4.
Cannot sleep/idle much when doing audio processing.
For the newer Attiny3216, at typical 5V and 20 Mhz is 10 mA.

ADC should be set to free-running mode.
And then using a timer at 8Khz to read out samples.
http://www.openmusiclabs.com/learning/digital/atmega-adc/
http://wiki.openmusiclabs.com/wiki/MiniArDSP
