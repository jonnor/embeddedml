
## TODO

- Send slides for review
- Do a talk-through of entire presentation. Check timing
- Fixup the result plots
- Add some demo image / data. Audio + FFT + RF
- Send final slides

## Goals

- Shine positively on Soundsensing.
Mention at least 2 times in talk. Intro + case.
Also tie in EARONEDGE project
- Establish emlearn as a serious project
Relevance. Usefulness.
Core values. Tiny models, easy-to-use, efficient (compute/power)

## Format

20-25 minutes + 5 minutes QA.

2x sessions between 10:50 am to 11:40
https://www.tinyml.org/event/emea-2024/

## Audience

Expecting mostly TinyML practitioners and technologists.

- ML engineers. With embedded/sensors background mostly?
- ML researchers. Academic and industry. Core and applied.
- ML/DS team/tech leads. 
- CTOs. 

Focus: Practical, technical.
Voicing: Concrete. Substantiated.

### What we promised

- showcase a selection usecases, and discuss their impact
- latest improvements in emlearn
Optimized decision tree ensembles, native support for MicroPython

## Talking points

- "A scikit-learn for microcontrollers"
Established methods.
Some relevant surrounding tooling

- Decision trees are very powerful and efficient
REF. Papers showing more efficient than DL. HAR
Comparison with emlearn 2019 ?

- emlearn optimized for the tinyest systems
Example: 1DollarML.
TODO: make demo/showcase on that platform

- emlearn has most efficient decision trees out there
REF. Benchmarks vs other alternatives.
TODO: make benchmark

- emlearn is used in real-world project
REF. papers applying it. Select 2-3.
DONE: reach out to authors
TODO: get info from authors. Maybe reminder

- emlearn + MicroPython enables pure-Python TinyML applications
Very convenient. Just mip install it
CLAIM. Can do accel / sound / image
TODO: Fix the bugs/crashes

## Call to Action

Go to the Github repository

## Outline

Slides

1
- Intro. About Soundsensing

5
- emlearn. Overview. A scikit-learn for microcontrollers
- emlearn. Supported tasks
- emlearn. Supported models

5
- emlearn. Tree ensemble usefulness
- emlearn. Tree ensemble implementation benefits
- emlearn. Tree ensemble next gen perf

5
- In use. Project 1
- In use. Project 2
- In use. Project 3
- 1DollarML. Introduction. A sensor node running emlearn
- 1DollarML. Example/demo

5
- Python as the lingua franca for DS/ML
- MicroPython. What is it
- emlearn-micropython. What it provides
- emlearn-micropython. Example application
- emlearn-micropython. Performance wrt pure Python/others

1
- Summary.


#### Soundsensing

Soundsensing provides an end-to-end solution for Condition Monitoring of technial machinery in commercial buildings.
Primarily this is the systems for Heating, Cooling and Air Conditioning.

Over the last 3 years,
many of the largest commercial building operators in Norway are our customers.

We use a combination of vibration and sound-based monitoring.
For us TinyML is primarily a way to run advanced and adaptive feature extraction on our sensors. Which can be sent in an energy efficient way over Bluetooth,
for doing continious Anomaly Detection and healt estimates in the cloud.

#### Outline

Today I will talk about the emlearn project.
An open-source software for TinyML on microcontrollers.

1. Quick introduction.
2. Shine a focus on a very useful: tree-based ensembles (Random Forest etc)
3. Mention a couple of projects using emlearn
4. How we enable application developers to make TinyML purely in Python


#### Sensor data analysis with Machine Learning

Key aspect:
Size of the information out << sensor data in.

emlearn primarily provides tools to deploy the Trained Model (blue).

Smaller data amounts.
Much easier to integrate into existing system.
BLE beacons 27 bytes.
Modbus RTU 2-100 bytes.
< 10 bytes per second.


#### Applications

No single killer application
- thousands of smaller applications, across dozens of industries.

Applications are basically everywhere.
TinyML is like electricity, like wireless connectivity, like microcontrollers.
A key part of the engineering toolbox.
But mostly a piece of a larger puzzle, to unlock actual benefits for end users.

Will mention a couple of concrete examples later in this talk.


#### emlearn introducion

2 main parts.
Reflects the two parts of creating a TinyML system.
Training. On a host computer.
Running. Inference, on a microcontroller.

Make this quite seamless. Ideally same person can do both.
We take care of the nitty gritty for you.


#### Supported tasks

Most common...


#### Supported models

Selction of embedded friendly models...

#### How to use

....


#### Train and export

Train using standard library
...


Clean C code.

#### Using the C code

Include the generated header file

Call predict function

#### Tree based models

Tree based models are probably the most popular in emlearn.
Excellent properties for TinyML usecases.

- Powerful. Can handle non-linear data of decent complexity
- Easy to use. Little overfitting, little hyperparameter tuning to get good results. Scaling invariant.
- Very fast inference. Microseconds, even on few Mhz CPU without FPU
- Very low RAM requirements - basically nothing apart from the input data / feature vector

#### Tree based relevance

Low complexity.
....
Neural networks overkill.
More trouble than they are worth.

Medium complexity.
....
Can be an alternative to deep learning in some cases.
! requires strong feature engineering
Human Activity Detection


High complexity.
Can be used toteg
Especially in a continious monitoring scenario.
Might have 99% where almost nothing of interest happens.
And some classes/events of interest can also be relatively simple to detect.

### emlearn trees

emlearn implements some optimizations for TinyML uses.
One of these is leaf de-duplication.

So a decision tree ensemble, such as Random Foress, consists of two parts:
1) decision nodes. 3) the leaves.

Decision nodes are basically IF statements. Is feature A larger than 1?
Outcome decides which node to go to next.

The leaves store the final outcome. Class information, or regression target information.
Where as most of the logic is in the decision nodes, there is still quite a lot of leaves.

scikit-learn stores class probabilities in these leaves.
But when tree growth is restricted, get different values.
Improves inference time, model size, improves generalization.

emlearn has since 2019 implemented hard voting with leaf-deduplication.
Saves 50-80% of the model size.

! but might reduce predictive performance in some cases.
Will see later how we are improving on this.

#### Inference modes

emlearn supports two ways of actually running inference for a tree-based model.
What we call inference modes.

Data structure. Only supports one data type.
Code generation. Outputs C code.

Not a clear winner. Recommend trying both.


#### Fixed point for loadable

Quantization is a well known tool in TinyML space.
Experience with the "inline" generation has shown that integer computations is enough.
Supported by several papers.
Also did an experiement on OpenML CC18 with 48 classification datasets.
Practically no change in predictive performance.

Decision boundaries of an individual tree is quite coarse.

Reduces model size by 33% on 32 bit platforms.

So upcoming versions of emlearn will switch from float to int16.
Much improved inference speed and code size for microcontrollers without an FPU.


#### K means clustering

I mentioned that the hard voting / storing only argmax can lead to reduced predictive performance.

But we want a solution that still allows the model size optimization of de-duplication.
Not just store all the class probabilities naively.

Tested quantization of the probabilities to 8 and 4 bits. This was quite beneficial compared to 32 bit float.
Wanted to see if we could do even better.
Why not use clustering to learn a small set of values to use?

Experiments on OpenML CC18.
75% of datasets had more than 1 percentage point drop in performance
with argmax / hard majority voting. BLUE line
With 8 leaves per class, 0% of datasets missed.
Majority of datasets OK with just 2 leaves per class.

!! cluster all the leaf values together.
The _per class_ was just a convenient way of setting the number of clusters
As most likely, more classes needs more values


These are preliminary results. Paper to follow.
Plan to implement this in emlearn.
Allowing an adaptable size/performance tradeoff. Tunable with a hyperparameter.

#### Projects

emlearn was started in 2018. Always been open source.

Quite good considering we never did any marketing for it.
In fact, this is my first presentation about the project at a physical conference.
And I only did one digital earlier this year, at Embedded Online Conference.

#### Cattle project

...

#### Earable

...

**REGRESSION**. Not classification

#### Grid

Fault in power lines for electrical grid.
Causes a wave that spreads from where the fault happened.

Means that one can monitoring at only a few points in the network, but still be able to localize.

Not so critical that the system is so "tiny".
Microcontrollers have very good and affortable sensor interfacing methods.
And very practial to build a standalone plug & play system.


#### 1 dollar TinyML 1/2

TinyML is about massive scale.
Adressing huge range of usecases.
Low cost is a key enabler.

Electronics and IoT prices are falling continiously.

How low-cost can TinyML actually be, right now? What does this say about the future?

1 dollar here is an arbitary target/constraints.

10 dollars is trivial.
Can get off-the-shelf complete BLE beacon with sensors for that price.

Doing it on a 1 USD microcontroller.
Easy - can get RP2040 with 100 Mhz+ and tons of SRAM/FLASH.

Adding TinyML for +1 USD.
Also quite easy.
Can get a huge boost in microcontroller capability, or MEMS sensing capability.



!! this is not the cheapest hardware.
Found a 30 cent microcontroller with built-in BLE and USB. And a lot more RAM/FLASH.
But - SDK had very little documentation in English.


#### 1 dollar TinyML 2/2

I made an initial development board earlier this year.
Have assembled them and tested basics to be working.

I realized that accelerometer data can be done easily.
Human Activity Detection etc, just requires 100 Hz sampling.
So I decided to go straight for a more difficult problem: audio TinyML.
80x the data rate.

Got audio to work via ADC.
Quality is currently very poor - needs some debugging.

But confident that can do

- basic anomaly detection
- basic speech commands
- basic sound event detection. Plops from beer brewing

CONCLUSION:
Hardware cost barriers to TinyML are VERY LOW. And will continue going down.


#### MicroPython

....

#### emlearn-micropython

....


Also saw there was a lack of efficient modules in MicroPython for typical pre-processing tasks.
Therefore also provides IIR filters, FFT transformation.

Just as a simple comparison, did some tests on the digits dataset.
Compared with everywhereml and m2cgen - which generate plain Python code.
Inference time expected to improve by 5x on Cortex M0 devices when moving to int16

? size comparison. Maybe do a spot check

#### emlearn-micropython. Install and export

Training is done in the standard way.

Support a CSV format, which can be loaded at runtime.
Stored on disk, loaded into efficient in-memory format.

Copy model to device.
Copy library to device. Architecture-specific binary module.


FIXME: skip
Simple, not really optimized for size.
But since MicroPython devices are typically high RAM/FLASH, not a bit deal.
(will improve with int16 trees also)
(! interesting to include in comparison with other frameworks )

### emlearn-micropython. Load and run

Create the model.
Load the weights.
Make predictions by passing sensor data.

Hope this.
To speed up prototyping for experienced embedded engineers.
To enable DS/ML engineers with primarily Python skills to make TinyML applications.
Make it for those learning TinyML - by using a high-level language like Python
- which has tons more learning resources than C or C++.

#### Summary

1, 2, 3

CALL TO ACTION
Anyone interested in talking to me about any of these topics.
Come find me in the break.
 

## Misc

### Applications

Pragmatic,
Everywhere we have sensors today, there are opportunities to improve with TinyML.

Improvements in
wireless connectivity, energy storage or havesting, sensor technology, data availability.

Hardware-based cycles.
Look for impact on the 10-30 year scale.
No overnight breakthroughs.
Mostly quite boring - solving same problems we had before, but better or slightly differently.

### Most efficient decision tree ensembles


Node size reduction.
Martin pointed out large size on 32 bit systems due to aligment/packing.
Reduced from N bytes to N bytes.
Also pointed out that one can used an implicit next node of +1.
This optimization is not yet in use.

From float to 16 bits.
Bascically no drop in predictive performance.
Should give large improvement in execution speed on systems without FPU.
Also reduced code size.


### The tinyiest systems

? 8 bit.
AVR tested, original Arduino.
Should work on more estoretic platforms, SDCC.


# Misc

## Adaptive Random Forests for Energy-Efficient Inference on Microcontrollers
May 2022. 
Torino / Bologna 
https://arxiv.org/pdf/2205.13838

energy reduction ranging from 38% to 90% with less than 0.5% accuracy drop.

Evaluates tree by tree, in batches of 2/4. By applying mean over probabilities.
Checks aggregated output (so far) against a confidence threshold.

Use an implicit left node.
16-bit thresholds
output probabilities are quantized to 16-bit
feature index field as 16 bit
child is 16 bit absolute


## Two-stage Human Activity Recognition on Microcontrollers with Decision Trees and CNNs
June 2022
2022 IEEE International Conference on Ph. D. Research in Microelectronics and Electronics (PRIME)
Francesco Daghero, Daniele Jahier Pagliari, Massimo Poncino

https://arxiv.org/abs/2206.07652

save up to 67.7% energy


## Dynamic Decision Tree Ensembles for Energy-Efficient Inference on IoT Edge Nodes
2023
https://arxiv.org/pdf/2306.09789

dynamic RFs and GBTs on three state-of-the-art IoT-relevant data sets
GAP8 as the target platform
Early stopping mechanisms, energy reduction of up to 37.9% with respect to static GBTs
 and 41.7% with respect to static RFs.

Tested smart ordering of trees. Negative results:
none of the proposed “smart” orders outperform the randomly generated ones,
and the original training order falls in the middle of the multiple random curves


## Benchmarking

https://github.com/BayesWitnesses/m2cgen
https://github.com/nok/sklearn-porter   X no C for RandomForest, only DecisionTrees
micromlgen
emlearn 0.1.x



