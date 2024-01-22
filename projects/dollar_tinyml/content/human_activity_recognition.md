
# Activity Recognition using accelerometer with tree-based ML models 

### Summary

This should be a just-barely-doable task on the chosen microcontroller (4 kB RAM and 32 kB FLASH).
Expected RAM usage is between 0.5 kB to 3.0 kB,
and FLASH usage between 10 kB to 32 kB FLASH.
There are accelerometers available that add 20 to 30 cents USD to the Bill-of-Materials.
Random Forest on time-domain features can do a good job at Activity Recognition.
emlearn has efficient Random Forest implementation for microcontrollers
https://github.com/emlearn/emlearn

### Applications for Activity Recognition

The most common sub-task for Activity Recognition using accelerometers is Human Activity Recognition (HAR).
It can be used for Activities of Daily Living (ADL) recognition
such as walking, sitting/standing, running, biking etc,
which is now a standard feature on fitness watches and smartphones etc.

But there are ranges of other use-cases that are more specialized

- Tracking sleep quality (calm vs restless motion during sleep)
- Detecting exercise type counting repetitions
- Tracking activities of free-roaming domestic animals
- Fall detection etc as alerting system in elderly care

### Ultra low cost accelerometers

To have a sub 1 USD sensor that can perform this task,
we naturally need a very low cost accelerometer.

Looking at LCSC (in January 2024), we can find

- Silan SC7A20 `0.18 USD @ 1k`
- ST LIS2DH12 `0.26 USD @ 1k`
- ST LIS3DH `0.26 USD @ 1k`
- ST LIS2DW12 `0.29 @ 1k`

The Silan SC7A20 chip is said to be a clone of LIS2DH.
https://patchwork.kernel.org/project/linux-iio/patch/20200811134846.3981475-3-daniel@0x0f.com/

So there looks to be several options in the 20-30 cent USD range.
Combined with a 20 cent microcontroller, we are still below 50% of our 1 dollar budget.

### Resource constraints

It seems that our project will have a 32-bit microcontroller
with around 4 kB RAM and 32 kB FLASH (such as the Puya PY32F003x6).
This sets the contraints that our entire firmware needs to fit inside.
The firmware needs to collect data from the sensors, process the sensor data, run the Machine Learning model, and then transmit (or store) the output data.
Would like to use under 50% of RAM and FLASH for buffers and for model combined,
so **under 2 kB RAM** and **under 16 kB FLASH**.

### Overall system architecture

We are considering an ML architecture where accelerometer samples are collected into
fixed-length windows (typically a few seconds long) that are classified independently.
Simple features are extracted from each of the windows,
and a Random Forest is used for classification.

IMAGE: 
A systematic review of smartphone-based human activity recognition methods for health research
https://www.nature.com/articles/s41746-021-00514-4

This kind of architecture was used for in the paper
Are Microcontrollers Ready for Deep Learning-Based Human Activity Recognition? 
https://www.mdpi.com/2079-9292/10/21/2640
which shows that it was able to perform similarly to a deep-learning approach,
but with resource usage that was 10x to 100x better.
They were able to run on Cortex-M3, Cortex-M4F and Cortex M7 microcontrollers with 
at least 96 kB RAM and 512 kB FLASH.
We need to fit into 5% of that resource budget.

### Data buffers

The input buffers, intermediate buffers, tends to take up a considerable amount of RAM.
So an appropriate tradeoff between sampling rate, precision (bit width) and length (in time) needs to be found.

In this table we can see the RAM usage for input buffers to hold the sensor data from an accelerometer.
Because we are continiously sampling and also processing the data on-the-run, double-buffering may be needed.
The first two configurations were used in the previously mentioned paper:

<table border="1" class="dataframe">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th></th>\n      <th>samples</th>\n      <th>size</th>\n      <th>percent</th>\n    </tr>\n    <tr>\n      <th>buffers</th>\n      <th>channels</th>\n      <th>bits</th>\n      <th>samplerate</th>\n      <th>duration</th>\n      <th></th>\n      <th></th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th rowspan="4" valign="top">2.00</th>\n      <th rowspan="4" valign="top">3</th>\n      <th rowspan="2" valign="top">16</th>\n      <th rowspan="2" valign="top">100</th>\n      <th>1.28</th>\n      <td>128</td>\n      <td>1536</td>\n      <td>37.5%</td>\n    </tr>\n    <tr>\n      <th>2.56</th>\n      <td>256</td>\n      <td>3072</td>\n      <td>75.0%</td>\n    </tr>\n    <tr>\n      <th rowspan="2" valign="top">8</th>\n      <th rowspan="2" valign="top">50</th>\n      <th>1.28</th>\n      <td>64</td>\n      <td>384</td>\n      <td>9.4%</td>\n    </tr>\n    <tr>\n      <th>2.56</th>\n      <td>128</td>\n      <td>768</td>\n      <td>18.8%</td>\n    </tr>\n    <tr>\n      <th>1.25</th>\n      <th>3</th>\n      <th>8</th>\n      <th>50</th>\n      <th>2.56</th>\n      <td>128</td>\n      <td>480</td>\n      <td>11.7%</td>\n    </tr>\n  </tbody>\n</table>

16 bit is the typical full range of accelerometers, so it preserves all the data.
It may be possible to reduce this down to 8 bit with sacrificing much performance.
This can be done by scaling the data linearly, or implementing a non-linear transform
such as square-root or logarithm to reduce the range of values needed.

Using 50 Hz sampling rate would also be very beneficial to reduce RAM usage.
Assuming that feature processing is quite fast, it should also be possible to not use full double-buffering.

It may also be possible to keep a buffer of computed features (much smaller in size) for the windows and classify them together.
This would allow to reduce the window size, but maintain infomation from a similar amount of time in order to keep performance up.

So it seems feasible to find a configuration under 2 kB RAM that has good performance.

### Feature extraction

In the previously referenced paper they used 9 features.
These compute simple statistics directly on each window.
No FFT or similar heavy processing is used.
This should have a neglible RAM (under 256 bytes) and FLASH usage (under 5kB).

IMAGE: feature extraction illustrated


### Random Forest classifier

The previously mentioned paper tested using 10-100 trees, with a max_depth of 9.
Found after 50 trees, marginal improvements in F1 score
Reported 10 trees using 10kB FLASH, and 50 trees appear to be around 50 kB FLASH.
Assume that this is only counting the size of the model, and not the feature processing code.

However it does not appear that they did any hyperparameter optimization to find smaller models.
Therefore I forked the git repository with the experimenents
https://github.com/jonnor/feature-on-board-activities
and added my own tuning by varying the depth of the trees

IMAGE: 

The original performance (50 trees, max_depth=9) is marked with a green dot.
We can see that 5 trees can just barely hit the same performance levels,
and that 10 trees is able to improve the performance.
And that the model size can be 4-10x with no or marginal degradation in performance.

The size estimates in the plot are for the "loadable" inference strategy in emlearn.
Benchmarks show that when using the "inline" inference strategy with 8-bit integers,
then model size is approximately half.
LINK: https://emlearn.readthedocs.io/en/latest/auto_examples/trees_feature_quantization.html#sphx-glr-auto-examples-trees-feature-quantization-py

So the models that take 20 kB in the plot should in practice take around 10 kB.
These matches performance of the untuned model, and fit in our 16 kB FLASH budget.



## References

A systematic review of smartphone-based human activity recognition methods for health research
https://www.nature.com/articles/s41746-021-00514-4

A Comprehensive Study of Activity Recognition Using Accelerometers 
https://www.mdpi.com/2227-9709/5/2/27
