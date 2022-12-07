
# Fall detection using wearable accelerometer


## Explainers

### Detecting Human Falls with a 3-Axis Digital Accelerometer

https://www.analog.com/en/analog-dialogue/articles/detecting-falls-3-axis-digital-accelerometer.html

## Papers

### Fall Detection for the Elderly Based on 3-Axis Accelerometer and Depth Sensor Fusion with Random Forest Classifier
https://ieeexplore.ieee.org/document/8856698
2019
Kijung Kim; Guhnoo Yun; Sung-Kee Park; Dong Hwan Kim


### Fall Detection Monitoring System Based on MEMS Sensor
2020 International Conference on Applied Physics and Computing (ICAPC 2020)
STM32F103RET6
Custom dataset. 4 ADL classes, 4 fall classes
Average accuracy 0.949

### Accelerometer-Based Fall Detection Using Machine Learning: Training and Testing on Real-World Falls
Luca Palmerini, Jochen Klenk, Clemens Becker, and Lorenzo Chiari

The most promising method obtained a
sensitivity higher than 80%, a false alarm rate per hour of 0.56, and an F-measure of 64.6%
Support vector machines and features from the multiphase fall model

Aanalyzed 143 fall recordings from 40 subjects.
Most of the fall recordings were 40 min long, 20 min before and 20 min after IS
Activities of daily living (ADLs) from 15 subjects, to compare and differentiate ADLs to/from falls.
The ADL recordings were 12 h long and collected during daytime hours with the same types of systems described above.
Nine of these subjects also had falls analyzed in this study


### Support Vector Machine Classifiers Show High Generalizability in Automatic Fall Detection in Older Adults
https://pubmed.ncbi.nlm.nih.gov/34770473/
https://www.mdpi.com/1424-8220/21/21/7166
Compard Support Vector Machine (SVM), k-Nearest Neighbors (kNN), and Random Forest (RF)
Trained on intentional falls (SisFall), validated on real-world accidental fall events of elderly people (FARSEEING).
Non-overlapping segments of 2.5 s length, segments of equal length with 50% overlap.


https://www.academia.edu/56919940/Towards_an_Accelerometer_Based_Elderly_Fall_Detection_System_Using_Cross_Disciplinary_Time_Series_Features
SIGNAL MAGNITUDE VECTOR
Tested on UR Fall, UP FAll, MOBILFALL
Used HCTSA to generated many features - https://github.com/benfulcher/hctsa
then feature selection to reduce
Tried LR,DT,RF,KNN models
Better performance using generated features than direct magnitude


## Datasets

Lists 16 different public datasets
https://www.frontiersin.org/files/Articles/692865/fnagi-13-692865-HTML/image_m/fnagi-13-692865-t001.jpg


### ShimFall&ADL

ShimFall&ADL: Triaxial accelerometer fall and activities of daily living detection dataset
https://zenodo.org/record/3901285
MATLAB .dat files
1.5 MB zip2
35 individuals
Acquired using a chest-strapped Shimmer v2 tri-axial accelerometer, recording at a 50Hz sampling rate

### FARSEEING

http://farseeingresearch.eu/the-farseeing-real-world-fall-repository-a-large-scale-collaborative-database-to-collect-and-share-sensor-signals-from-real-world-falls/

Between January 2012 and December 2015 more than 300 real-world fall events have been recorded.
A signal processing and fall validation procedure has been developed and applied to the data.
About 200 validated real-world fall events are available for analyses, now.
These fall events have been recorded within several studies, with different methods, and in different populations.
All sensor signals include accelerometer measurements and 58% additionally gyroscope and magnetometer measurements.
The FARSEEING consortium aims to share the collected real-world falls data with other researchers on request.
A dataset of 20 selected fall events is now available for researchers on request

### SisFall

SisFall: A Fall and Movement Dataset
https://pubmed.ncbi.nlm.nih.gov/28117691/
https://www.mdpi.com/1424-8220/17/1/198
19 ADLs and 15 fall types performed by 23 young adults
Test the dataset with widely used feature extraction,
and a simple to implement threshold based classification, achieving up to 96% of accuracy in fall detection.
Validation tests with elderly people significantly reduced the fall detection performance of the tested features.

http://sistemic.udea.edu.co/en/investigacion/proyectos/english-falls/
! download link broken !!


### MobiFall
24 volunteers (22 to 42 years old) performed nine types of ADLs and four of falls using a Samsung Galaxy smartphone, Samsung, Seoul, South Korea.
Nine subjects performed falls and ADLs, while 15 performed only falls (three trials each).
https://bmi.hmu.gr/the-mobifall-and-mobiact-datasets-2/
Non-commercial. On request only.
https://www.researchgate.net/publication/308538296_The_MobiFall_Dataset_Fall_Detection_and_Classification_with_a_Smartphone

### tFall

ten participants between 20 and 42 years old
They recorded eight types of falls (503 total recordings with two smartphones)
and one week of continuous ADL recordings with all participants carrying smartphones in the pockets and a handbag.
The ADL trials were not identified by activity.

### DLR
Sixteen subjects (23 to 50 years old).
They recorded six types of ADLs, and the authors did not specify the conditions of the falls (they belong to a single group).
Short files??

### Project gravity
3 participants (ages 22, 26, and 32) performed 12 types of falls and seven types of ADLs with a smartphone in the pocket.


### SHAPES
17 subjects have performed 9 exercises divided between Falls and ADLs to build this dataset
https://arcoresearch.com/2021/04/16/dataset-for-fall-detection/
CSV files
Waist mounted sensor
30 MB zip

### UP-Fall

UP-Fall Detection Dataset: A Multimodal Approach 
https://www.mdpi.com/1424-8220/19/9/1988/htm
2019
17 healthy young individuals without any impairment that performed 11 activities and falls, with three attempts each

### UMAFall

https://www.sciencedirect.com/science/article/pii/S1877050917312899
http://webpersonal.uma.es/de/ECASILARI/Fall_ADL_Traces/UMA_FALL_ADL_dataset.html
2017
19 experimental subjects that emulated a set of predetermined ADL (Activities of Daily Life) and falls
SensorTag and Smartphones
75 MB zip
CSV files

### FallAllD

https://ieee-dataport.org/open-access/fallalld-comprehensive-dataset-human-falls-and-activities-daily-living
Human falls and activities of daily living simulated by 15 participants.
FallAllD consists of 26420 files collected using three data-loggers worn on the waist, wrist and neck of the subjects.
Motion signals are captured using an accelerometer, gyroscope, magnetometer and barometer
CSV files
400 MB zip

### KFall

A Large-Scale Open Motion Dataset (KFall) and Benchmark Algorithms for Detecting Pre-impact Fall of the Elderly Using Wearable Inertial Sensors
https://www.frontiersin.org/articles/10.3389/fnagi.2021.692865/full


https://sites.google.com/view/kfalldataset?pli=1
“KFall” which was developed from 32 Korean participants
while wearing an inertial sensor on the low back and
performing 21 types of activities of daily living
and 15 types of simulated falls.

Using the KFall dataset for pre-impact fall detection so that researchers and practitioners can flexibly choose the corresponding algorithm.
Deep learning algorithm achieved both high overall accuracy and balanced sensitivity (99.32%) and specificity (99.01%)
Support vector machine also demonstrated a good performance with a sensitivity of 99.77% and specificity of 94.87%
Threshold-based algorithm showed specificity (83.43%) was much lower than the sensitivity (95.50%).

On-request only

## Unrelated

### TSFuse
Automatic time-series feature construction

https://github.com/arnedb/tsfuse

TSFuse: automated feature construction for multiple time series data
https://link.springer.com/article/10.1007/s10994-021-06096-2

TSFuse results in a significantly more accurate model
in 8 datasets compared to catch22,
and in 5 datasets compared to tsfresh.
TSFuse is slower than catch22 on all datasets
and slower than tsfresh in 7 out of 14 datasets when using the default setting
At prediction time,
TSFuse is on average 29.4 times faster than tsfresh.
The catch22 baseline is at least an order of magnitude faster than both tsfresh and TSFuse with the default setting.
1NN-DTW is uniformly worse than the other approaches on these dataset
TSFuse outperforms this baseline on 10 out of 13 classification datasets


