
# Human Activity Recognition

## Terms used

Human Acitivity Recognition (HAR) is also known as

* Activity Recognition / human activity recognition (AR) 
* Activities of Daily Living (ADL).
* Action recognition
* Fall detection. (FD)

## Datasets

* [UniMiB SHAR](http://www.sal.disco.unimib.it/technologies/unimib-shar/)
11,771 samples of human activities and falls. 30 subjects, aged 18 to 60 years. 
17 fine grained classes grouped in two coarse grained classes. 9 types of activities of daily living (ADL), 8 types of falls.
* [UCI: ADL Recognition with Wrist-worn Accelerometer](https://archive.ics.uci.edu/ml/datasets/Dataset+for+ADL+Recognition+with+Wrist-worn+Accelerometer). 16 volunteers performing 14 Activities of Daily Living
* [UCI: Activity Recognition from Single Chest-Mounted Accelerometer](https://archive.ics.uci.edu/ml/datasets/Activity+Recognition+from+Single+Chest-Mounted+Accelerometer). 15 participantes performing 7 activities. 52Hz. 7 classes.
* [PAMAP2 Physical Activity Monitoring Data Set](https://archive.ics.uci.edu/ml/datasets/PAMAP2+Physical+Activity+Monitoring).
100 Hz, 3 IMUs: wrist,chest,ankle. Heartrate 9Hz. 18 physical activities, performed by 9 subjects 
* [LingAcceleration](http://www.ccs.neu.edu/home/intille/data/BaoIntilleData04.html). 20 activities, 20 subjects
* [UCI: Smartphone-Based Recognition of Human Activities and Postural Transitions Data Set](http://archive.ics.uci.edu/ml/datasets/Smartphone-Based+Recognition+of+Human+Activities+and+Postural+Transitions). 30 volunteers age 19-48 years. Six basic activities.
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

## Existing work

* [Efficient Activity Recognition and Fall Detection](https://dis.ijs.si/ami-repository/datasets/14/Kozina-Efficient_Activity_Recognition_and_Fall_Detection_Using_Accelerometers.pdf)
* [Limitations with Activity Recognition Methodology & Data Set](http://www.cis.fordham.edu/wisdm/Lockhart_Weiss_HASCA.pdf).
Focuses on model type, how AR training and test data are partitioned, and how AR models are evaluated.
personal, hybrid, and impersonal/universal models yield dramatically different performance.
* [Transfer Learning for Activity Recognition: A Survey](http://eecs.wsu.edu/~cook/pubs/kais12.pdf).
Summarizes 30+ papers using transfer learning.
