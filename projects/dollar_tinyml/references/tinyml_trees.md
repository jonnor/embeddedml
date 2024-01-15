
## Post

Constraints
Under 50% of RAM and FLASH for ML model
2 kB of RAM and 16 kB FLASH
Preferably would like to be closer to 25%, ie half this

Task
Human Activity Detection

Have a wide range of applications.
Medical, health, exercise, elderly care etc
Not just human activities, also animals
Wrist mounted device. Smart watch. Fitness bracelet etc.

Sample rates of around 100 Hz

How to realize
Feature computations

IMAGE: feature extraction illustrated

Decision tree ensemble
TODO: Estimate model size for Cortex M0+ with emlearn using integers



IMAGE: decision tree forest



## References

### Are Microcontrollers Ready for Deep Learning-Based Human Activity Recognition?
https://www.mdpi.com/2079-9292/10/21/2640

Just 9 features
max_depth 9.
Used 10-100 trees. After 50 trees, marginal improvements in F1 score
! did not try different depth limits based on trees.
Possible that smaller amount of trees could have performed better with more regularization
! used floating point, not integers

At 10 trees, used 10kB FLASH for model.
At 100 trees, used nearly 100 kB FLASH
50 trees appear to be around 50 kB FLAH
! Not clear if feature compute code size is counted.

Running on NRF5340
Inference time of approx 1ms
9 features selected

Experiemental setup is well described, and sensible.
Subject-based cross evaluation. Wrist accelerometer only

Their feature selection code is at
https://github.com/atiselsts/feature-group-selection

The experimental code _might_ be at
https://github.com/atiselsts/feature-on-board-activities/blob/main/rf/ml_state.py

Some odd remapping of classes, into 12 classes total?
https://github.com/atiselsts/feature-on-board-activities/blob/main/cnn/datasets.py#L54



