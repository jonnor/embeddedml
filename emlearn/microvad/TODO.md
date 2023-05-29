
## Motivation
- Improving emlearn library through a real-world usecase

## Goals

- Run efficiently on on small microcontrollers.
Primarily Cortex M4F/ESP32 class. HW FPU
Stretch: Cortex M0. No FPU
Ultra-stretch: AVR8
- Higher performance and lower computational costs than WebRTC VAD
- Demo on device. Battery power
- Demo in browser.

## TODO

- Setup WebRTC VAD / libfvad as reference
- Finish EmlSignalWindower
- Test emlearn in browser
- Finish proba support for eml_trees

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

Python API as a backup/test
