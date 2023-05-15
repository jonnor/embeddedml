
# Voice Activity Detection

## Problem setup

Real-time versus offline.

https://www.sciencedirect.com/science/article/abs/pii/S0885230813000533
NIST
Compares with Statistical Model (SM) based VAD and Gaussian Mixture Model (GMM) based VAD

(1) noise reduction is vital for energy-based VAD under low SNR;
(3) spectral subtraction makes better use of background spectra
than the likelihood-ratio tests in the SM-based VAD

### References

https://wiki.aalto.fi/pages/viewpage.action?pageId=151500905
Very pedagogical.
Going through the definition of the task,
the evaluation setup,
compares energy-based model with linear predictive model (autocorrelation-based),

Describes post-processing heuristics. Such as "hangover".

Features for voice activity detection: a comparative analysis
https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-015-0277-z

### Implementations

### ITU-T G.729B

From 1996.

ITU-T G.729 Annex B introduces silence compression using a Voice Activity Detector (VAD).
Features
a) A spectral distortion
b) An energy difference
c) A low-band energy difference
d) A zero-crossing difference
Using fixed decision boundary in the space defined by these features.
Applies smoothing and adaptive correction as post-processing.

Described in https://ieeexplore.ieee.org/document/620527

### GSM / ETSI

The GSM standard includes two VAD alternatives.
Option 1.
Computes SNR in nine bands and applies a threshold to these values.


Option 2
Calculates different parameters: channel power, voice metrics, and noise power.
It then thresholds the voice metrics using a threshold that varies according to the estimated SNR.


### WebRTC VAD
Code exists inside the Chromium tree, under webrt/modules/audio_processing/vad

A fork has been created that separates out just the VAD as a C library. 
https://github.com/dpirch/libfvad

Available for Python in [py-webrtcvad](https://github.com/wiseman/py-webrtcvad).
Expects int16 input of the audio waveform.
Needs some massaging to work with typical floating point input. TODO, link

The WebRTC VAD model is described in 2.3 of
[Voice Activity Detection Scheme by Combining DNN Model with GMM Model](https://arxiv.org/abs/2005.08184).
Is based on a two-mixture Gaussian Mixture Model (noise and speech).
The input features are 6 frequency sub-bands.
Does online updating of the GMM, with different update coefficients for the GMM coefficients,
such that noise would increase slowly, but decrease quickly.
With the assumption that the sound is mostly noise, and occationally speech segments.

Uses 30 ms samples.

Works well at speech vs silence.
But does poorly with music or other noise, will often get flagged as speech.

### inaSpeechSegmenter
CNN-based audio segmentation toolkit.
Primarily for performing gender detection (tuned for French),
but has also a model that distinguishes between music, speech and noise.
Uses a 4 layer CNN per frame.
Per frame predictions are then combined using a Hidden Markov Model.
Has command-line tools for processing a whole batch.

https://github.com/ina-foss/inaSpeechSegmenter


### Opus VAD
The Opus audio codec includes a Voice / Music detector,
which is used in the encoder to switch between speech optimized encoding (SILK)
and music/general encoding (CELT).
In Opus v1.1 it used a multilayer perceptron followed by a Hidden Markov Model.
Since [Opus v1.3](https://jmvalin.ca/opus/opus-1.3/) (October 2018)
it is based on a RNN using Gated Recurrent Units.
The RNN has around 5000 weights, with 8 bit quantization.
This network has two outputs, one for Voice and one for Music.
So a low output on both

The [opus_sm](https://github.com/jzombi/opus_sm) fork has a commandline tool of the old Opus 1.1
sound/music detector.
No-one has described how to us the Opus 1.3 detector in another application?
One [question](http://lists.xiph.org/pipermail/opus/2019-September/004386.html) on mailing list.

### pyannote VAD

Pretrained model on Huggingface
https://huggingface.co/pyannote/voice-activity-detection
Requires accepting user conditions and giving out usage information

Tutorial for training a VAD model
https://github.com/pyannote/pyannote-audio/blob/develop/tutorials/voice_activity_detection.ipynb

Uses the AMI speech corpus

### speechbrain VAD

https://speechbrain.readthedocs.io/en/latest/API/speechbrain.pretrained.interfaces.html#speechbrain.pretrained.interfaces.VAD

CRDNN is convolutional recurrent model with DNN backbone (and optionally projections)
https://github.com/speechbrain/speechbrain/blob/develop/speechbrain/lobes/models/CRDNN.py

pretrained model on HuggingFace, 
https://huggingface.co/speechbrain/vad-crdnn-libriparty

Training recipie
https://github.com/speechbrain/speechbrain/tree/develop/recipes/LibriParty/VAD

Trained on "LibriParty" dataset.
https://github.com/speechbrain/speechbrain/tree/develop/recipes/LibriParty/generate_dataset

Tutorial on using for Voice Activity Detection
https://colab.research.google.com/drive/1Msk2cgSEw-jCuXHmz2_-iOrv-gJHCCxu?usp=sharing#scrollTo=S6JtQmHptzee
Also covers post-processing tools.
And combination with energy-based VAD, to get more fine-grained output.

### JorisCos/VAD_Net

VAD model trained using librimix recipe in Asteroid.
It was trained on the enh_single task of the Libri1Mix dataset.
https://huggingface.co/JorisCos/VAD_Net

This work "VAD_Net" is a derivative of LibriSpeech ASR corpus by Vassil Panayotov, used under CC BY 4.0;
of The DNS challenge noises, Attribution-ShareAlike 3.0 Unported.
"VAD_Net" is licensed under Attribution-ShareAlike 3.0 Unported by Joris Cosentino


LibriMix dataset
https://github.com/asteroid-team/asteroid/blob/bd3caa3963cf2f8756da17801958073001aaa0f2/asteroid/data/librimix_dataset.py#L17

https://github.com/asteroid-team/Libri_VAD
https://github.com/asteroid-team/asteroid/blob/bd3caa3963cf2f8756da17801958073001aaa0f2/asteroid/data/vad_dataset.py


### MarbleNet

MarbleNet: Deep 1D Time-Channel Separable Convolutional Neural Network for Voice Activity Detection
https://arxiv.org/abs/2010.13886
Uses 1D CNN with separable convolutions
On MFCCs or log mel-spectrogram.

2021.

When compared to a state-of-the-art VAD model, MarbleNet is able to achieve similar performance with roughly 1/10-th the parameter cost.

Available as part of NeMo
https://catalog.ngc.nvidia.com/orgs/nvidia/teams/nemo/models/vad_telephony_marblenet
https://colab.research.google.com/github/NVIDIA/NeMo/blob/r1.0.0rc1/tutorials/asr/06_Voice_Activiy_Detection.ipynb#scrollTo=HbCtcUUKA3al

Available as part of Malaya
https://malaya-speech.readthedocs.io/en/latest/load-vad.html

### Kaist VAD
https://github.com/jtkim-kaist/VAD
2019 ICASSP

Implemented in Python with Tensorflow 1.x

Multi-resolution cochleagram (MRCG) as feature.
Must be precomputed, quite slow.

Supports 4 different classifier models

- Adaptive context attention model (ACAM)
- Boosted deep neural network (bDNN) [2]
- Deep neural network (DNN) [2]
- Long short term memory recurrent neural network (LSTM-RNN) [3]

Where one can post-process according to application.



## Classic models

Many papers in 1990ies

#### A Statistical Model-Based Voice Activity Detection.
Sohn, 1999.
Over 1500 citations.

Hang-over correction using first-order Markov process modeling.

#### Robust Voice Activity Detection Using Long-Term Signal Variability
Ghosh, 2011
Over 200 citations


## Performance metrics

Different error cases

- FEC (Front End Clipping): clipping introduced in passing from noise to speech activity;
- MSC (Mid Speech Clipping): clipping due to speech misclassified as noise;
- OVER: noise interpreted as speech due to the VAD flag remaining active in passing from speech activity to noise;
- NDS (Noise Detected as Speech): noise interpreted as speech within a silence period.


## Features

### Features for voice activity detection: a comparative analysis
https://asp-eurasipjournals.springeropen.com/articles/10.1186/s13634-015-0277-z
2015.
Simon Graf, Tobias Herbig, Markus Buck & Gerhard Schmidt 
EURASIP Journal on Advances in Signal Processing.

Excellent review of features.
Good controlled comparisons between features.
Nice plots of the temporal activations of different methods.

Says modulation around 4 Hz is quite important for speech.
Can be used to discriminate against music.

### Investigating the Important Temporal Modulations for Deep-Learning-Based Speech Activity Detection
https://ieeexplore.ieee.org/abstract/document/10022462/authors#authors

We describe a learnable modulation spectrogram feature for speech activity detection (SAD).
Modulation features capture the temporal dynamics of each frequency subband.
We compute learnable modulation spectrogram features by first calculating the log-mel spectrogram.
Next, we filter each frequency subband with a bandpass filter that contains a learnable center frequency.
Experimental results showed that temporal modulations around the 4–6 Hz range are crucial for deep-learning-based SAD.
These experimental results align with previous studies that found slow temporal modulation to be most important for speech-processing tasks and speech intelligibility.
Additionally, we found that the learnable modulation spectrogram feature outperforms both
the standard log-mel and fixed modulation spectrogram features on the Fearless Steps Phase-04 SAD test set.

IDEA:
? could one learn a modulation feature direction on the waveform?
Using a convolutional neural network.
With a large hop and/or dilation to reduce number of computations.
Could this be faster than doing STFT/mel?



### Microcontroller device models

[Voice activity detection for low-resource settings](http://cs230.stanford.edu/projects_winter_2020/reports/32224732.pdf). Abhipray Sahoo, Stanford CS230.
Used a 3 layer RNN on log mel spectrogram with 40 bands, and using 32 ms windows.
Trained and evaluated on a dataset made by combining VCTK with Noisex-92.
Large improvements against WebRTC VAD under noisy conditions.


[Voice Activity Detector (VAD) Based on Long-Term Mel Frequency Band Features](https://link.springer.com/chapter/10.1007/978-3-319-45510-5_40).
VAD using long-term 200 ms Mel frequency band statistics, auditory masking, and a pre-trained two level decision tree ensemble based classifier.
Near 100 % acceptance of clear voice for English, Chinese, Russian, and Polish speech and 100 % rejection of stationary noises independently of loudness.
Reuses short-term FFT analysis (STFFT) from ASR frontend with additional 2 KB memory and 15 % complexity overhead.

[Voice Activity Detector for Device with Small Processor and Memory](https://ieeexplore.ieee.org/abstract/document/8907081).
Raw Speech Signal as input and Deep Neural Network as classifier.
The result is an architecture with only 3 layers, 130 neurons, 64 inputs, softmax activation function, Adam optimization, dropout rate 0.2, and batch size 64. The accuracy is 0.7406 for training and 0.7168 for validation.
?? did it use multiple-frames for temporal context

[Linear detector and neural networks in cascade for voice activity detection in hearing aids](https://www.sciencedirect.com/science/article/pii/S0003682X20309373).
Using a two-stage detector.
In the first stage, a linear system determines whether the detection can be easily carried out, or a second stage with a more complex neural-network-based detection is required.
The results show that the system error can be reduced up to 8.5% while using the same amount of resources.
Moreover, the error is the lowest among the proposals that are affordably implemented in hearing aids.

[](https://link.springer.com/chapter/10.1007/978-3-319-45510-5_40)
VAD using long-term 200 ms Mel frequency band statistics, auditory masking,
and a pre-trained two level decision tree ensemble based classifier.
Allows capturing syllable level structure of speech and discriminating it from common noises.
Proposed algorithm demonstrates on the test dataset almost 100 % acceptance of clear voice for English, Chinese, Russian, and Polish speech and 100 % rejection of stationary noises independently of loudness.
The algorithm is aimed to be used as a trigger for ASR.
It reuses short-term FFT analysis (STFT) from ASR frontend with additional 2 KB memory and 15 % complexity overhead.

Nuance SREC VAD. Latency 70 ms and analyses energy envelope statistics.

### gkonovalov/android-vad
https://github.com/gkonovalov/android-vad

Based on Google WebRTC VAD.
Real-time utilizing Gaussian Mixture Model (GMM).
Implemented in Java.
10-30 millisecond frame sizes.


### Hardware models

A 108-nW 0.8-mm2 Analog Voice Activity Detector (VAD)
Featuring a Time-Domain CNN with Sparsity-Aware Computation and Sparsified Quantization in 28-nm CMOS
90% (94%) speech (non-speech) hit rate on the TIMIT dataset.
It features a switched-capacitor circuit as the time-domain convolutional neural network (TD-CNN)
that extracts the 1-bit features for the subsequent binarized neural network (BNN) classifier.

### Speaker dependent models

[Personal VAD: Speaker-Conditioned Voice Activity Detection](https://arxiv.org/abs/1908.04284)
Personal VAD outputs the probabilities for three classes: non-speech, target speaker speech, and non-target speaker speech.
Combined with Speaker Verification System.
No online / real-time adaptation to speakers.
Seems to need to be pre-trained for a particular speaker.

## Papers

### ResectNet: An Efficient Architecture for Voice Activity Detection on Mobile Devices

https://www.isca-speech.org/archive/pdfs/interspeech_2022/kopuklu22_interspeech.pdf
2022.
Microsoft.

Achieves state-of-the-art performance with less than 12k parameters
Operates on raw audio signals and consists of sinc convolutions, depthwise convolutions,
grouped pointwise convolutions, frequency shift module and a gated recurrent unit.

Compares with MarbleNet. Better performance with 1/10 the number of parameters.
6.4 - 12.2 MFLOPS

The audios are sampled at 16 kHz.
We have used a 640-sample frame length (40 ms) with a 160-sample (10 ms) frame shift.

Using AVA speech and HAVIC datasets.

No code available.

### NAS-VAD: Neural Architecture Search for Voice Activity Detection

https://arxiv.org/abs/2201.09032

Model and training code available at
https://github.com/daniel03c1/NAS_VAD

Used the AVA [36] and ACAM datasets [6] as test datasets.


## Non-open
### Silero VAD
https://github.com/snakers4/silero-vad

Released as pretrained PyTorch models.
Training setup not released.
Train/test dataset not released.
Does not specify which PyTorch versions to use.
Not installable as a pip library.
Latest models ("big") not publically available.
Has some nice examples of real-time.

Can used either 30 ms, 100 ms or 250 ms windows.
Outperforms WebRTC by large margin.

### PicoVoice Cobra
https://github.com/Picovoice/Cobra

Raspberry Pi Zero, Cobra measured a realtime factor of 0.05.

Outperforms WebRTC by large margin.
Performs slightly worse than Silero, according to Silero benchmark. 

Has benchmark here.
https://github.com/Picovoice/voice-activity-benchmark
