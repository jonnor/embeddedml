
# Human Activity Detection using accelerometer and tree-based ML models 

TLDR: This should be a barely-doable task on the chosen microcontroller (4 kB RAM and 32 kB FLASH).
Expected RAM usage is between 0.5 kB to 3.0 kB,
and FLASH usage between 10 kB to 32 kB FLASH.

### Human Activity Detection

Human Activity Detection (HAR).
TODO: write about about 

Task
Human Activity Detection

Have a wide range of applications.
Medical, health, exercise, elderly care etc
Not just human activities, also animals
Wrist mounted device. Smart watch. Fitness bracelet etc.


### Resource constraints

It seems that our project will have a 32-bit microcontroller
with around 4 kB RAM and 32 kB FLASH (such as the Puya PY32F003x6).
This sets the contraints that our entire firmware needs to fit inside.
The firmware needs to collect data from the sensors, process the sensor data, run the Machine Learning model, and then transmit (or store) the output data.
Would like to use under 50% of RAM and FLASH for buffers and for model combined.

### Overall system architecture

We are considering an ML architecture where accelerometer samples are collected into
fixed-length windows (typically a few seconds long) that are classified independently.
Simple features are extracted from each of the windows,
and a Random Forest is used for classification.

This kind of architecture was used for example in the paper
Are Microcontrollers Ready for Deep Learning-Based Human Activity Recognition? 
https://www.mdpi.com/2079-9292/10/21/2640
which shows that it was able to perform similarly to a deep-learning approach,
but with resource usage that was 10x to 100x better.
They were able to run on Cortex-M3, Cortex-M4F and Cortex M7 microcontrollers with 
at least 96 kB RAM and 512 kB FLASH.

Using the optimized Random Forest implementation in emlearn,
we should be able to fit this on microcontrollers that have only 5% of these resources.
https://github.com/emlearn/emlearn

### Data buffers

The input buffers, intermediate buffers, tends to take up a considerable amount of RAM.
So an appropriate tradeoff between sampling rate, precision (bit width) and length (in time) needs to be found.

In this table we can see the RAM usage for input buffers to hold the sensor data from an accelerometer.
Because we are continiously sampling and also processing the data on-the-run, double-buffering may be needed.
The first two configurations were used in the previously mentioned paper:

<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th>samples</th>\n      <th>size</th>\n      <th>percent</th>\n    </tr>\n    <tr>\n      <th>buffers</th>\n      <th>channels</th>\n      <th>bits</th>\n      <th>samplerate</th>\n      <th>duration</th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th rowspan="4" valign="top">2</th>\n      <th rowspan="4" valign="top">3</th>\n      <th rowspan="2" valign="top">16</th>\n      <th rowspan="2" valign="top">100</th>\n      <th>1.28</th>\n      <td>128</td>\n      <td>1536</td>\n      <td>37.5%</td>\n    </tr>\n    <tr>\n      <th>2.56</th>\n      <td>256</td>\n      <td>3072</td>\n      <td>75.0%</td>\n    </tr>\n    <tr>\n      <th rowspan="2" valign="top">8</th>\n      <th rowspan="2" valign="top">50</th>\n      <th>1.28</th>\n      <td>64</td>\n      <td>384</td>\n      <td>9.4%</td>\n    </tr>\n    <tr>\n      <th>2.56</th>\n      <td>128</td>\n      <td>768</td>\n      <td>18.8%</td>\n    </tr>\n  </tbody>\n</table>

16 bit is the typical full range of accelerometers, so it preserves all the data.
It may be possible to reduce this down to 8 bit with sacrificing much performance.
This can be done by scaling the data linearly, or implementing a non-linear transform
such as square-root or logarithm to reduce the range of values needed.

Being able to use 50 Hz sampling rate would also be very beneficial to reduce RAM usage.
Assuming that feature processing is quite fast, it should also be possible to not use full double-buffering.

It may also be possible to keep a buffer of computed features (much smaller in size) for the windows and classify them together.
This would allow to reduce the window size, but maintain infomation from a similar amount of time in order to keep performance up.

### Feature extraction

In the previously referenced paper they used 9 features.
These have neglible RAM and FLASH usage.

IMAGE: feature extraction illustrated

### Random Forest classifier

Just 9 features
max_depth 9.

The previously mentioned paper tested using 10-100 trees, with a max_depth of 9.
After 50 trees, marginal improvements in F1 score
At 10 trees, used 10kB FLASH for model.
At 100 trees, used nearly 100 kB FLASH
50 trees appear to be around 50 kB FLAH


! did not try different depth limits based on trees.
Possible that smaller amount of trees could have performed better with more regularization
! used floating point, not integers

! Not clear if feature compute code size is counted.

According to benchmarks in emlearn,
when using integers the code size for model is approximately halved.
Would be 25 kB instead of 50 kB.
A forest with average tree depth of 7.78 and 50 trees took under 11 kB with uint8_t on Cortex-M0




Decision tree ensemble



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





