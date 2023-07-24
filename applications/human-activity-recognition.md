
# Human Activity Recognition

## Terms used

Human Activity Recognition (HAR) is also known as

* Activity Recognition / human activity recognition (AR) 
* Activities of Daily Living (ADL).
* Action recognition
* Fall detection. (FD)
* Exercise recognition


## Datasets

* [UniMiB SHAR](http://www.sal.disco.unimib.it/technologies/unimib-shar/)
11,771 samples of human activities and falls. 30 subjects, aged 18 to 60 years. 
17 fine grained classes grouped in two coarse grained classes. 9 types of activities of daily living (ADL), 8 types of falls.
* [UCI: ADL Recognition with Wrist-worn Accelerometer](https://archive.ics.uci.edu/dataset/283/dataset+for+adl+recognition+with+wrist+worn+accelerometer).
16 volunteers performing 14 Activities of Daily Living
Classes: (brush_teeth, climb_stairs, comb_hair, descend_stairs, drink_glass, eat_meat, eat_soup, getup_bed, liedown_bed, pour_water, sitdown_chair, standup_chair, use_telephone, walk).
* [UCI: Activity Recognition from Single Chest-Mounted Accelerometer](https://archive.ics.uci.edu/ml/datasets/Activity+Recognition+from+Single+Chest-Mounted+Accelerometer).
15 participantes performing 7 activities.
52Hz.
Working at Computer, Standing Up/Walking/Going up\down stairs, Standing, Walking, Going Up\Down Stairs, Walking and Talking with Someone, Talking while Standing
* [PAMAP2 Physical Activity Monitoring Data Set](https://archive.ics.uci.edu/ml/datasets/PAMAP2+Physical+Activity+Monitoring).
100 Hz, 3 IMUs: wrist,chest,ankle. Heartrate 9Hz. 18 physical activities, performed by 9 subjects 
* [LingAcceleration](http://www.ccs.neu.edu/home/intille/data/BaoIntilleData04.html). 20 activities, 20 subjects
* [UCI: Daily and Sports Activities](https://archive.ics.uci.edu/dataset/256/daily+and+sports+activities).
19 daily and sports activities.
8 subjects in their own style. 5 minutes per parcicipant.
Five Xsens MTx units are used on the torso, arms, and legs.
* [UCI: Smartphone-Based Recognition of Human Activities and Postural Transitions Data Set](http://archive.ics.uci.edu/ml/datasets/Smartphone-Based+Recognition+of+Human+Activities+and+Postural+Transitions).
Smartphone (Samsung Galaxy S II) on the waist.
30 volunteers age 19-48 years. Six basic activities.
Preprocessed into 2.56 sec sliding windows with 50% overlap (128 readings/window), time+frequency based features.
Total 561 features, 10k instances.
* [UCI: OPPORTUNITY Activity Recognition Data Set](https://archive.ics.uci.edu/ml/datasets/OPPORTUNITY+Activity+Recognition)
Scripted execution with 4 users, 6 runs per user.
7 IMUs plus bunch of other sensors on body and around. 5 tracks of labels. 242 features, 2551 instances.
* [WISDM: Activity prediction](http://www.cis.fordham.edu/wisdm/dataset.php) in lab conditions.
Raw set 6 features, 1M instances, 6 classes.
Preprocessed set 46 fetures, 5k instances.
* [WISDM: Actitracer](www.cis.fordham.edu/wisdm/dataset.php#actitracker), real world data. 0.5% labeled data, rest unlabeled.
500 users. Available both as raw motion and preprocessed. Preprocessed data has 5k labeled classes. 6 basic classes.
* [Exercise Recognition from Wearable Sensors dataset](https://github.com/microsoft/Exercise-Recognition-from-Wearable-Sensors).
Arm-worn inertial sensor. Triaxial accelerometer plus gyro.
13 exercises. 114 participants over 146 sessions.
Stored in Matlab .m file.
* [MM-Fit](https://mmfit.github.io/).
2 smartwatches, 2 smartphones, 1 earbud, 1 camera.
10 exercises.
800 minutes.
* [Capture-24: Activity tracker dataset for human activity recognition](https://ora.ox.ac.uk/objects/uuid:99d7c092-d865-4a19-b096-cc16440cd001).
Axivity AX3 wrist-worn activity tracker.
151 participants
Around 24 hours, total of almost 4,000 hours.
More than 2,500 hours of labelled data.
Academic Use Licence 1.1. Non-commercial.
* [motion sense](https://github.com/mmalekzadeh/motion-sense).
Smartphone in trouser pocket.
6 activities.
24 data subjects.



## Existing work

* [Efficient Activity Recognition and Fall Detection](https://dis.ijs.si/ami-repository/datasets/14/Kozina-Efficient_Activity_Recognition_and_Fall_Detection_Using_Accelerometers.pdf)
* [Limitations with Activity Recognition Methodology & Data Set](http://www.cis.fordham.edu/wisdm/Lockhart_Weiss_HASCA.pdf).
Focuses on model type, how AR training and test data are partitioned, and how AR models are evaluated.
personal, hybrid, and impersonal/universal models yield dramatically different performance.
* [Transfer Learning for Activity Recognition: A Survey](http://eecs.wsu.edu/~cook/pubs/kais12.pdf).
Summarizes 30+ papers using transfer learning.
* [RecoFit: using a wearable sensor to find, recognize, and count repetitive exercises](). 2014.
Handles 3 tasks: 1) segmenting exercise from intermittent non-exercise periods, (2) recognizing which exercise is being performed, and (3) counting repetitions.
* [Towards a Complete Set of Gym Exercises Detection Using Smartphone Sensors](https://www.hindawi.com/journals/sp/2020/6471438/).
Reviewed 25 studies between 2006–2018
6 of 25 research studies related to gym exercises,
while the remaining 19 of 25 research papers were about daily life physical activities, emotional recognition, and elderly fall detection

