
# Datasets

Audio Classification datasets that are useful for practical tasks
that can be perform on microcontrollers and small embedded systems.

Relevant tasks:

* Wakeword detection
* Keyword spotting
* Speech Command Recognition
* Noise source identification
* Smart home event detection. Firealarm,babycry etc 

Not so relevant:

* (general) Automatic Speech Recognition
* Speaker recognition/identification

## To be reviewed.

* DCASE 2016.

## Not relevant 

* [NOIZEUS: A noisy speech corpus for evaluation of speech enhancement algorithms](http://ecs.utdallas.edu/loizou/speech/noizeus/)
30 sentences corrupted by 8 real-world noises. 
* [VoxCeleb](http://www.robots.ox.ac.uk/~vgg/data/voxceleb/), 100k utterances for 1251 celebrities.
Task: Speaker Reconition.
* [Speakers in the Wild](https://www.sri.com/work/publications/speakers-wild-sitw-speaker-recognition-database)
Task: Speaker Reconition.
* [Google AudioSet](https://research.google.com/audioset/).
2,084,320 human-labeled 10-second sounds, 632 audio event classes. 
Based on YouTube videos.
* Whale Detection Challenge. https://www.kaggle.com/c/whale-detection-challenge
* Mozilla [Common Voice](https://voice.mozilla.org), crowd sourcing.
Compiled dataset [on Kaggle](https://www.kaggle.com/mozillaorg/common-voice), 
500 hours of transcribed sentences.
Has speaker demographics.
Task: Automatic Speech Recognition.
Not something to do on microcontroller.
Could maybe be used for Transfer Learning for more relevant speech tasks.
* DCASE2018 Task 5.
Domestic activities. 
10 second segments. 9 classes.
From 4 separate microphone arrays (in single room).
Each array has 4 microphones

## Relevant but lacking

* Hey Snips. https://github.com/snipsco/keyword-spotting-research-datasets
Task: Wakeword detetion, Vocal Activity Detection.
Restricted licencese terms. Academic/research use only.
Must contact via email for download.
By Snips, developing Private-by-Design, decentralized, open source voice assistants.

## Relevant

### TUT Rare Sound Events 2017

Used for DCASE2017 Task 2.
Baby crying, Glass Breaking, Gunshot.
3 classes, but separate binary classifiers encouraged.
Part of TUT Acoustic Scenes 2016.
Train 100 hours. Approx 100 sound examples per class isolated, 500 mixtures (weakly labeled).
Event detection.  Event-based error rate. Onset only. 500 ms collar. Also F1 score.
Baseline system available. FC DNN. 40 bands melspec, 5 frames. F1 0.72
Around 11 other systems submitted. Ranging 0.65-0.93 F1 score.
http://www.cs.tut.fi/sgn/arg/dcase2017/challenge/task-rare-sound-event-detection

Relevant as examples of single-function systems, security


## YorNoise
Dataset from York with "traffic" and "rail" classes.
Same structure as Urbansoun8k dataset.
1527 samples a 4 seconds. Split into 10 folds.
https://github.com/fadymedhat/YorNoise

## DCASE2018 Task 2, General Purpose Audio Tagging
Task: Acoustic event tagging.
Based on FreeSound data.
41 classes. Using AudioNet ontology
9.5k samples train, ~3.7k manually-verified annotations and ~5.8k non-verified annotations. 
Test  ~1.6k manually-verified annotations.
Systems reach 0.90-0.95 mAP@3.
Baseline CNN on log melspec. 0.70 mAP@3

Relevant for: context-aware-computing, smarthome?

## DCASE2018 Task3, Bird Audio Detection.
Binary classification.

Relevant for on-edge pre-processing / efficient data collection.

## DCASE2018 Task4
Event Detection with precise time information.
Events from domestic tasks. 10 classes.
Subset of Audioset.

Relevant for: smarthome and context-aware-computing


## TUT Urban Acoustic Scenes 2018
Used in DCASE2018 Task 1.

Task: Acoustic Scene Classification.
10 classes. airport,shopping_mall,metro_station
About 30GB of data, around 24 hours training.
One variant dataset has parallel recording with multiple devices, for testing mismatched case.

Relevant for: context-aware-computing?

## TUT Acoustic Scenes 2017. Used for DCASE2017 Task 1.
Scenes from urban environments.
15 classes.
10 second segments.
Baseline system available. 18% F1
Relatively hard, systems achieved 35-55% F1.

Relevant for context-aware-computing?

## DCASE2017 Task 4, Large Scale Sound Event detection
http://www.cs.tut.fi/sgn/arg/dcase2017/challenge/task-large-scale-sound-event-detection
17 classes from 2 categories, Warning sounds and Vehicle sounds.

Relevant for autonomous vehicles?

## TUT Sound Events 2017
Used for DCASE2017 Task 3, Sound event detection in real life audio

Events related to car/driving.
6 classes.
Multiple overlapping events present. Both in training and testing.
Hard, systems only achieved 40%-45% F1.
Quite small. 2 GB dataset total.
Relevant for autonomous vehicles?



