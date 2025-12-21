

# Demo ideas

## Detect events and sonify them

Make some emlearn-micropython project with audio synthesizer 
Interactive art installation? 
Digital wind chimes. Using accelerometer

Virtual drums using accelerometers? Virtual "maracas"?
https://github.com/adafruit/Adafruit_CircuitPython_BLE_MIDI
SAM has Castanets. And Maracas in drum table

MIDI Unit. With synthesizer.
Could alternatively use Amy, on an ESP32 board (with amplifier)
https://github.com/shorepine/amy 

## Audio visualizer

Using emlearn_fft to get spectrum/spectrogram.
Show using Neopixels.

## DTMF decoding

Can of course be done with a hardcoded method.
But could be fun to learn it?
Using FFT+quant+RF ?

## Recognize machine complete sound

Tone detection in sounds

> I have a machine that rings when it has finished its work
https://github.com/orgs/micropython/discussions/16622

Test with example off Youtube.
Test with washing machine at home.

Template-based approaches.
Can it be done with just FFT+KNN?
Normalized cross-correclation on spectrogram.

## Speech commands

Recogniting speech commands from limited vocabulary.
Standard dataset/task. Google Speech Recognition dataset.

## Voice activity detection

Another standard task.
Mostly relevant as a component in a bigger system.
For example for keyword spotting.


## On-device Acoustic Anomaly/novelty Detection

Implement a baseline say from DCASE into emlearn-micropython.


## Data sampling methods

Trigger to store audio of interest. audio on-demand, review after.
Reservoir sampling.
spectrum+histogram, spectrogram. wasserstein kNN.

Combine and contrast other trigger techniques.

- regular time sampling
- random sampling
- "interestingness"/SNR sampling
- overall soundlevel sampling
- soundlevel sampling in specific freq band(s)

# Related

- noise-monitoring.md

MicroPython and emlearn-micropython audio ecosystem

- MicroPython. Make a mini wavefile module.
- MicroPython. wavfile module. Stdlib compatible (at least subset/core). 
- MicroPython. Tools for storing audio
- Mel filterbank implementation
- Third/octave filterbank implementation
https://chatgpt.com/c/685a772f-9c44-8007-83f9-e9383b101591
- MicroPython. PDM microphone support for ESP32 
- MicroPython. Microphone support for Unix, using miniaudio
- Spectrogram implementation. Hann windowing.
- Test ulab spectrogram
https://micropython-ulab.readthedocs.io/en/latest/ulab-utils.html#spectrogram

