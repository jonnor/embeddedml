
# Human Activity Recognition

Using tri-axial accelerometer.
For example wrist-mounted, like a smart-watch / fitness watch / pulse-watch.

Several standard hardware devices available.

- LilyGo TTGO T-Watch. ESP32
- Pine64 [PineTime](https://www.pine64.org/pinetime/). nRF52832, BMA425
- Any smartphone

Related tasks.
Fine-grained activity detection.
For example which fitness exercise.

Gesture recognition later.
Intentional. Usually to trigger some action.

## Existing works


#### Energy-efficient activity recognition framework using wearable accelerometers
https://doi.org/10.1016/j.jnca.2020.102770
Uses 50/100 hz, int8. 256 samples long windows, with 50% overlap.
Computes from this basic features.
Classified with RandomForest
Gets F1 scores of 90%, 70% on participants not in training set.
Code available here, including C feature extraction, Python feature extraction and datasets.
https://github.com/atiselsts/feature-group-selection


https://github.com/STMicroelectronics/STMems_Machine_Learning_Core

Uses statistical feature summaries, plus decision tree.
Sample rates between 26 and 104 Hz,
windows between 0.6 and 3 seconds long.

Head gestures. Sensor mounted on head.
Nod, Shake, Stationary, Swing, Walk

Yoga poses. Sensor mounted on front calf, just below the knee.
Classes: Boat Pose, Bow Pose, Bridge, Child's Pose, Cobra's Pose, Downward-Facing Dog,
Meditation Pose, Plank, Seated Forward Bend, Standing in Motion, Standing Still,
The Extended Side Angle, The Tree, Upward Plank



## On-device learning

Being able to store/annotate activities on the go would be great.
To build up datasets.
Chose between pre-defined classes.
Have a couple of user-definable classes.
1/2/3/4 or blue/red/green/yellow 
Pre-annotate class, before starting activity. 
Post-annotate after doing activity / event happened.

Should be able to store raw data from accelerometer.
Maybe use some simple compression. Like gzip/deflate
Store files to be synced as time-stamped.
Maybe one per 60 seconds or so.

On-device few-shot learning of these would also be very cool.
kNN the most simple algorithm for this.
Just need to store feature vectors somewhere. FLASH/SDCARD
And keep number managable, so not too slow things down too much.
Need to have a good feature extraction system.

## Models

#### DTW kNN

DynamicTimeWarping kNN one alternative for few-shot.
https://sequentia.readthedocs.io/en/latest/sections/classifiers/knn.html
https://github.com/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/
https://github.com/datashinobi/K-nearest-neighbors-with-dynamic-time-wrapping/blob/master/knndtw.py
https://github.com/MaxBenChrist/mlpy-plus-dtw/blob/master/mlpy/dtw/cdtw.c
