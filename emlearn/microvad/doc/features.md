
# Feature extraction


## Polyphase filterbanks

Performing the STFT followed by mel-filtering mapping to a low number of bands,
might be computationally wasteful compared to a more direct implementation.
One candidate is a polyphase filterbank.

WebRTC uses 6 frequency bands, implemented using multi-rate filterbank.
It *might* be implemented using polyphase filterbank.

https://github.com/kastnerkyle/kastnerkyle.github.io/blob/master/posts/polyphase-signal-processing/polyphase-signal-processing.ipynb
Shows Python code for polyphase filterbank

> A typical rule is that filters up to around 64 taps are faster to apply in the time domain,
> while > 64 taps can typically be applied faster using an fftconvolve routine.
> This is highly platform dependent, but can serve as a decent guideline.


https://github.com/GuitarsAI/MRSP_Notebooks/blob/master/MRSP_Optimization_FilterBanks.ipynb

> Obtain a filter bank from our structure or product ....,
> which has "good" subband filters,
> i.e. a good or sufficient stopband attenuation and not much pass band attenuation.
> An example could be a desired stopband attenuation of -60dB and a pass band attenuation of less than -3dB.

Multirate Signal Processing with Python Examples - Full Course - Ilmenau University of Technology 
https://www.youtube.com/watch?v=eHZgdfDLWhU

Polyphase Filter Bank implementation in C++
https://github.com/alexranaldi/PolyphaseFilterBank

## FFT

### FFT performance on ESP32
esp-fft
https://github.com/fakufaku/esp32-fft

Performance:
```
radix-2	Real	FFT	256	0.197360
```
Source: https://github.com/fakufaku/esp32-fft/blob/master/performance/performance.csv


However someone else reported much slower numbers, 5-8x as slow
```
256,1.5ms
2048,10.96ms
4096,21ms
```
Source: https://medium.com/swlh/how-to-perform-fft-onboard-esp32-and-get-both-frequency-and-amplitude-45ec5712d7da


https://github.com/espressif/esp-dsp
Official DSP library. Including FFT functions

https://espressif-docs.readthedocs-hosted.com/projects/esp-dsp/en/latest/esp-dsp-benchmarks.html

```
dsps_fft2r_sc16 for 256 complex points 
ESP32 = 45755 cycles
0.60 ms at 80 Mhz.

dsps_fft4r_fc32 for 256 complex points
ESP32 = 15551 cycles
0.20 ms at 80 Mhz
```

80 Mhz is nominal frequency of ESP32.
Can go down to 10mhz, and up to 240 mhz.

ESP32S3 has 10x speed-up for fixed-point 16bit FFT
and up to 20x for 8/16 bit dot products
