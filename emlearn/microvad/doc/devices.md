
# Device Support

## Nordic NRF52

PDM support limited to particular frequencies.
Limits possible microphone choices a lot.

## Nordic NRF53

PCM/I2S and ADC all suitable for audio-rate input.

## ESP32

PDM/I2S support in ESP-IDF.

## STM32

PDM/I2S and ADC all capable of efficient audio-rate input.

## AVR8

These devices are on the smaller side of what microvad aims to support,
as they have very little RAM, no FPU and generally very low CPU performance.
But it should still be possible to run very simple things at 8 kHz samplerate.

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
