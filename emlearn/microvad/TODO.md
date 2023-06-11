
## Motivation
- Improving emlearn library through a real-world usecase

## Goals

- Demo on device. Portable / battery powered
- Demo in browser. Visualize input audio and detections

## TODO

First model results

- Implement an baseline method. RNN on mel-spectrogram ?
Try search for lower feature resolutions.
- Implement evaluation into PicoVoice voice-activity-benchmark
- Run quality comparisons with libfvad and SileroVAD/CobraPicoVoice

Computational comparison

- Try to compile and run libfvad on microcontroller
- Compare libfvad compute time to emlearn STFT/mel-filterbank
- Setup automatic compute time for all methods
- Running SileroVAD in C++ instead of Python
- Running PicoVoice in C/C++

C model deployment

- Finish EmlSignalWindower
- Implement the feature extraction methods
- Finish proba support for eml_trees

Testing dataset

- Record some audio representative for the usecase
A wearable device.
Annotate with wearer-speech|other-speech|nospeech
TTGO T-WATCH V3 microphone to SD card?
https://github.com/Xinyuan-LilyGO/TTGO_TWatch_Library/blob/master/examples/BasicUnit/TwatcV3Special/Microphone/Microphone.ino

Device demo

- Select a demo board and SW platform.
NRF52/Thingy52 with Zephyr OS?
- Get microphone input working on board

Browser demo

- Setup microphone input in browser.
- Setup Emscripten build for C code


## DONE

### Test emlearn in browser

Works quite nicely.
Documented at https://emlearn.readthedocs.io/en/latest/getting_started_browser.html

### Testing PicoVoice benchmark

```
python benchmark.py --librispeech_dataset_path /data/emlearn/microvad/data/LibriSpeech/test-clean/ --demand_dataset_path /data/emlearn/microvad/data/demand/ --engine WebRTC

export COBRA_ACCESS_KEY=

python benchmark.py --librispeech_dataset_path /data/emlearn/microvad/data/LibriSpeech/test-clean/ --demand_dataset_path /data/emlearn/microvad/data/demand/ --engine Cobra --access_key ${COBRA_ACCESS_KEY}
```

Seems to work OK.
Takes some 3 minutes to load the data.
WebRTC runs in approx 1 minute. 4 different levels.
Cobra takes approx 20 minutes. 200 levels.

To support a custom method, would need to add to engine.py
Does a sweep over different thresholds

### Testing some references
Run Silero VAD. In Python on 16 second clip
prediction time 476.6662120819092 ms

Run fvaf/WebRTCVAD. In C on 16 second clip
processing took 50.015 ms

Run PicoVoice Cobra. In Python on 16 second clip
Processing time 67.93 ms
Processing time 30.0 ms
! very fast
But seems to give very low probabilities

## Overall

- Small dataset
- Feature extraction. 
- Windower
- _proba() support for trees
- post processing
- Audio support on real hw

## Details

### Dataset

Earlier approaches used small eval sets by mixing clean speech and noise from databases, at different SNR levels

https://arxiv.org/abs/2104.04045
evaluates on AMI, DIEHARD 3, VoxConverse

VoxConverse. Not available for download??
AMI. Annoying to download form official. But is on HuggingFace,
https://huggingface.co/datasets/ami 

https://github.com/Picovoice/voice-activity-benchmark
Mixes speech from LibreSpeech with noise from Demand
! is at 0 dB. Quite challenging task
Compare with WebRTCVAD 


### Baselines

WebRTC VAD. Available
https://github.com/dpirch/libfvad/tree/master

Silero VAD. PyTorch, JIT/ONNX compiled. Model code not available
https://github.com/snakers4/silero-vad 

Moattar, M. Homayounpour
A simple but efficient real-time Voice Activity Detection algorithm, 2009
https://github.com/shriphani/Listener/blob/master/VAD.py

Pyannote Audio
https://herve.niderb.fr/fastpages/2021/08/05/Streaming-voice-activity-detection-with-pyannote.html

Kaldi.
https://www.idiap.ch/software/bob/docs/bob/bob.kaldi/master/guide.html#energy-based

Audiotok, energy-based
https://github.com/amsehili/auditok

ITU-T G.729B. Hard to find?
ETSI AMR1. Hard to find?
ETSI AMR2. Hard to find?

RNNoise. Contains a VAD. Not exposed?
Opus. Contains a VAD. Not exposed?

### Post processing

Hangout. Look ahead, look-behind
https://wiki.aalto.fi/pages/viewpage.action?pageId=151500905

https://github.com/jtkim-kaist/VAD#post-processing
FEC: hang_before
MSC: off_on_length
OVER: hang_over
NDS: on_off_length

median filtering
HMM-GMM

### Feature Extraction

Prefer low complexity features
Time based

Zero Crossing Rate
Energy, dB RMS
Bandpass IIR ?

https://www.researchgate.net/publication/314194549_Spectrum_energy_based_voice_activity_detection

https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-015-0277-z

https://maelfabien.github.io/machinelearning/Speech4/#
speech band set to 300-3000 hz

### Windower

Streaming splitting of (audio) input stream into (potentially overlapping) chunks.
Each output chunks will then be processed in one go. 

Take multiple columns in/out

Support multiple data types?
uint8, uint16, int32, float


## Proba trees

To enable adjusting decision threshold. Tuning for high recall.
https://github.com/emlearn/emlearn/issues/12

Alternatives

- Use MLP, has proba support
- Add Logistic regression with proba support
- Add SVC with proba support

## Demo hardware with audio support

Nordic Thingy52 / 53.
Zephyr with PDM. Quite easy to run. Get reproducible. Nice interface for audio.

Alternative: ESP32 with Espressif IDF

## Tools

Could have PortAudio support also for portability / support Embedded Linux

Python API as a backup/testH
