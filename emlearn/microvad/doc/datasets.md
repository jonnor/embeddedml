
# Datasets for Voice Activity Detection

## Synthetizing datasets

- Speech aduio

Such datasets may be tailored to.
For example the kind of background noise.

There are tools made to assist such dataset creation.
For example scaper, https://github.com/justinsalamon/scaper

## Complete datasets

### AVA

AVA-Speech: A Densely Labeled Dataset of Speech Activity in Movies
https://arxiv.org/abs/1808.00606
2018

Citations. https://scholar.google.com/scholar?cites=11984861534098647309&as_sdt=2005&sciodt=0,5&hl=no

Dataset
https://github.com/cvdfoundation/ava-dataset

Ddensely labeled speech activity in YouTube videos, with the goal of creating a shared, available dataset for this task.
The labels in the dataset annotate three different speech activity conditions: 
- clean speech
- speech co-occurring with music
- speech co-occurring with noise

We report benchmark performance numbers on AVA-Speech
using off-the-shelf, state-of-the-art audio and vision models that serve as a baseline to facilitate future research.


AVASpeech-SMAD: A Strongly Labelled Speech and Music Activity Detection Dataset with Label Co-Occurrence
https://arxiv.org/abs/2111.01320


### RealVAD

Dataset: https://zenodo.org/record/3928151
Paper: https://www.researchgate.net/publication/342729178_RealVAD_A_Real-world_Dataset_and_A_Method_for_Voice_Activity_Detection_by_Body_Motion_Analysis

RealVAD dataset is constructed from a YouTube video composed of a panel discussion lasting approx. 83 minutes.
The audio is available from a single channel.
There is one static camera capturing all panelists, the moderator and audiences.

- Associated VAD ground-truth (speaking, not-speaking) for nine panelists.
- Acoustic features extracted from the video: MFCC and raw filterbank energies.

Notes:

- Dataset designed for using a visual approach to VAD.
Acoustic usage is secondary.

Questions

- Can audio be retrieved from the Youtube video?
To do own feature extaction


## Background noise data

### MUSAN: A Music, Speech, and Noise Corpus

http://www.openslr.org/17/
https://arxiv.org/abs/1510.08484

