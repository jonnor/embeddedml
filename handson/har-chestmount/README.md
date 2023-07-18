
Dataset URL:
https://archive-beta.ics.uci.edu/dataset/287/activity+recognition+from+single+chest+mounted+accelerometer

Classes
```
1: Working at Computer
2: Standing Up, Walking and Going updown stairs
3: Standing
4: Walking
5: Going UpDown Stairs
6: Walking and Talking with Someone
7: Talking while Standing
```

Download URL
https://archive.ics.uci.edu/ml/machine-learning-databases/00287/Activity%20Recognition%20from%20Single%20Chest-Mounted%20Accelerometer.zip

Alternative download
https://www.kaggle.com/datasets/imsparsh/single-chestmounted-accelerometer

11 MB zipped archive.

```
Sampling frequency of the accelerometer: 52 Hz
Accelerometer Data are Uncalibrated
Number of Participants: 15
Number of Activities: 7
Data Format: CSV
```

## Work by others

#### Human Activity Recognition from Accelerometer Data Using a Wearable Device
https://link.springer.com/chapter/10.1007/978-3-642-21257-4_36
Original paper that made the dataset.
Pierluigi Casale, Oriol Pujol, and Petia Radeva.
2011.
PDF link: https://www.researchgate.net/profile/Pierluigi-Casale/publication/221258784_Human_Activity_Recognition_from_Accelerometer_Data_Using_a_Wearable_Device/links/59e46abf458515393d60e25a/Human-Activity-Recognition-from-Accelerometer-Data-Using-a-Wearable-Device.pdf

> New set of 20 computationally efficient features and the Random Forest classifier
> We obtain very encouraging results with classification accuracy of
> human activities recognition of up to 94%.

Sensor is mounted on chest.
Y is upwards, Z is forward, X is sideways.

Computed also the magnitude from the tri-axial data.
Processed each axis samples with a high-pass filter, with cut-off frequency set to 1Hz.
Using windows of 52 samples (1 second), with 50% of overlapping between windows.

- root mean squared value of integration of acceleration in a window (velocity).
Integral has been approximated using running sums with step equals to 10 samples
- mean value of Minmax sums.
Minmax sums computed as the sum of all the differences of the ordered pairs of the peaks of the time series.
Computed features:
mean value, standard deviation, skewness, kurtosis, correlation between each pairwise of accelerometer axis
(not including magnitude), energy of coefficients of seven level wavelet decomposition.

Constructed a 319 dimensional feature vector.
Then selected 20 features using RF feature importance.

Validated by 5-fold cross validation.
!! no mention of how the folds were constructed.
!! High risk of data leakage considering the overlapped windows.
!! Generalizability to wearer/user unknown.
Reports accuracy of 94%.


#### machinelearningmastery.com
https://machinelearningmastery.com/how-to-load-and-explore-a-standard-human-activity-recognition-problem/



#### mayank1897
https://github.com/mayank1897/Activity-Recognition-from-a-Single-Chest-Mounted-Accelerometer/blob/main/Activity_Recognition_from_a_Single_Chest_Mounted_Accelerometer.ipynb

- nice barplot of participant+classes duration

