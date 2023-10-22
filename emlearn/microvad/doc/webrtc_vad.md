
# WebRTC VAD

## Where to find it
Code exists inside the Chromium tree, under webrt/modules/audio_processing/vad

## How to use it

### Accessing in C

A fork has been created that separates out just the VAD as a C library. 
https://github.com/dpirch/libfvad

### Accessing in Python

Available for Python in [py-webrtcvad](https://github.com/wiseman/py-webrtcvad).
Expects int16 input of the audio waveform.
Needs some massaging to work with typical floating point input. TODO, link

## How does it work

The WebRTC VAD model is described in 2.3 of
[Voice Activity Detection Scheme by Combining DNN Model with GMM Model](https://arxiv.org/abs/2005.08184).
Is based on a two-mixture Gaussian Mixture Model (noise and speech).
The input features are 6 frequency sub-bands.
Does online updating of the GMM, with different update coefficients for the GMM coefficients,
such that noise would increase slowly, but decrease quickly.
With the assumption that the sound is mostly noise, and occationally speech segments.

Implementation:
https://github.com/dpirch/libfvad/blob/master/src/vad/vad_filterbank.c

### Filterbank

The 6 frequency sub-bands are computed using splitting filters,
operating at progressively smaller sample rate.

- Energy in 3000 Hz - 4000 Hz.
- Energy in 2000 Hz - 3000 Hz.
- Energy in 1000 Hz - 2000 Hz.
- Energy in 500 Hz - 1000 Hz.
- Energy in 250 Hz - 500 Hz.
- Energy in 80 Hz - 250 Hz.


? is it a analysis filterbank / transmultiplexer / transmux / polyphase filterbank ?

### Samplerate adapation

Input is resampled to 8 kHz before entering the feature pre-processing.
Uses 30 ms samples.


### Gaussian Mixture Model

There are 2 GMMs (speech and noise), for each of the 6 bands, each with 2 Gaussian components
A total of 24 gaussian components. Each Gaussian has a mean and std, for total of 48 parameters.

Noise vector uses long-term feature minimums.

// WebRtcVad_FindMinimum
// inserts into low_value_vector
// if it is one of the 16 smallest values the last 100 frames
// Returns the median of the five smallest values.

### Update rule

### Power
TODO: describe how the soundlevel / total power feature is used


## Optimizations

Uses int16 all the way for audio samples.
Uses fixed-point integer math everywhere.
LogOfEnergy has some tricks to compute decibel in fixed-point without using a logarithm.

Uses a multi-rate filterbank
https://www.dsprelated.com/freebooks/sasp/Multirate_Filter_Banks.html
https://ccrma.stanford.edu/~jos/sasp/Multirate_Filter_Banks.html
This reduces the number of computations needed


## Limitations

Works well at speech vs silence.
But does poorly with music or other noise, will often get flagged as speech.

Essentially operates as acoustic novelty detector.


## Implementation details

Order used for the GMM parts means/std

```c
for (channel = 0; channel < kNumChannels; channel++) {
  for (k = 0; k < kNumGaussians; k++) {
    gaussian = channel + k * kNumChannels;
    self->noise_means[gaussian],
    self->noise_stds[gaussian],
```

Fixed-point representations
```
// m = |mean| (Q7)
// s = |std| (Q7)
```

noise_band{X}_component{C}_std
noise_band{X}_component{C}_mean
speech_band{X}_component{C}_std
speech_band{X}_component{C}_mean



