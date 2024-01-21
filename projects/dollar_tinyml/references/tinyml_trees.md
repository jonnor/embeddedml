
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

According to benchmarks in emlearn,
when using integers the code size for model is approximately halved.
Would be 25 kB instead of 50 kB.
A forest with average tree depth of 7.78 and 50 trees took under 11 kB with uint8_t on Cortex-M0

Tested 128 and 256 samples window size
1.5kB or 3.0 kB for triaxial int16 data
!! a bit high for our RAM
Can we go down to 8 bit? Potentially applying some non-linear compression, like pow

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





