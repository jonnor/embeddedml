
# Low level AI hacking devroom

## Call

https://aifoundry.org/fosdem-2025-low-level-ai-engineering-hacking-dev-room

We are  bringing together the top developers working on the essential “plumbing” of the AI industry:
hardware accelerators, math kernel libraries, model quantization techniques, low-level inference, fine-tuning engines, distributed and rack-scale computing, and more
Together, we will spend the day discussing core designs and collaborating to solve governance problems. 

We are looking for low-level AI core open source project maintainers and committers (such as ggml, llama.cpp and llamafile),
downstream projects building on top of these (for example,  ollama, ramalama and Podman AI Lab),
as well as end-users of AI stacks to speak about their work and expertise.

## Format
20 minute technical session

## Abstract

It the recent year, generative AI models have come to dominate the discourse around artificial intelligence and machine learning.
Both Large Language Models and other generative models for image/video/sound use huge deep learning models, running on expensive and energy intensive GPUs.
However there are several other application areas of machine learning, operating under other contraints.
One of these is the area of "TinyML", where machine learning is used to analyze sensor data on microcontroller-grade systems.
A typical TinyML system is under 1 watt, under 1 MB of RAM and FLASH and under 10 USD bill-of-materials.

emlearn is an open-source project started in 2018,
which provides machine learning inference implementations for microcontrollers.
It is written in portable C99 code, and supports models trained with scikit-learn and Tensorflow/Keras.
Since 2023 the emlearn project also provides bindings for MicroPython, a Python for microcontrollers.

In this talk we will talk about machine learning on microcontrollers;
the applications, and developments in the field over the last years, and current trends.
This niche of machine learning is extremely concerned with computational efficiency,
and we believe that these perspectives and experiences may be useful also to others at the developer room.


## Takeaways

#### Main communication goals

- ML is not only huge, complex, expensive systems. TinyML is an alternative
- Focus on physical systems, not just abstract. Devices that you can interact with.
- Can make useful solutions for niche/personal applications.
- Do not need huge amounts of data. Can collect it oneself.
- Off the shelf hardware is available. Accessible without eletronics expertice
- Low cost enables large scale in diversity of applications, and in number-of-units deployed

#### Smaller points

- TinyML is about deploying ML inference for small microcontroller systems, usually combined with physical sensors
- Wide range of applications across all industries
- Large TinyML systems are under 1 watt, under 1 MB of RAM and FLASH, under 10 USD bill-of-materials
- Battery powered applications often target under 1 milli-watt.
- Some practical application possible under 10 kB RAM and 100 kB FLASH, down to 1 USD BOM.
- Massive scale. Hundreds of millions of devices shipped anually
- emlearn is a project providing ML implementations for microcontrollers
- emlearn also has a MicroPython API. Enables usage from Python on microcontrollers

#### Asides

Computational efficiency of ML systems has been improved 10-100x before.
Well demonstrated for computer vision tasks.
It is possible also for large language models.

## Call to action

Interested in using ML for sensors/IoT/electronics and deploying to a microcontroller?
Try out the emlearn library.
Either using C, or using MicroPython.



### Outline

- What is TinyML? 
Measuring and analzying the world continiously.
High energy efficiency. Low-cost hardware. Very small models, RAM/ROM/CPU. 
Often massive scale in terms of number of devices.
- Quick introduction to the emlearn project



### Energy requirements for battery powered

- ER14505 (AA sized). 2400 mAh. For 1 year, 0.9 mW.
- CR2032 coincell. 235 mAh. Over 3 years, 0.025 mW
- LIR1025 rechargable. 6 mAh. 1 month. 0.025 mW. 8 uA average.


### Toothbrush power consumption optimized

PY003F power consumption

- STOP. 6 uA 
- LSI SLEEP. 96-170 uA, 32 kHz
- HSI SLEEP. 0.35-1.0 mA, 4-24 Mhz. ! Almost identical to RUN
- HSI RUN. 0.35mA-1.5 mA, 4-24 Mhz 
- HSI RUN at default 8 Mhz, 0.70 mA

LPTIM can be used to create a tick that wakes up from STOP.
For example at 1 kHz, 100, or 10 Hz.
Wakeup time is 6us.

LIS2DH12.
- 20 uA at 100 Hz.
- 6 uA at 25 Hz.

Assuming 1% CPU utilization for feature plus classification.
1 ms every 100 ms.
RUN. (0.7 * 1/100) * 1000 = 7 uA

Buzzer.
10 seconds active per 2 min session.
3 sessions per day.
10 mA active.
((10*30)/(24*3600))*1000
3.5 uA

Total budget, 40 uA average 

- Accelerometer 10 uA
- uC stop 10 uA
- uC run 10 uA
- Buzzer/LED. 10 uA

Over 6 days runtime for LIR1025.


### Massive scale

- Over 30 billion microcontrollers are shipped annually
- Over 1 billion cows in the world.
- Over 1 billion sheep.
- Over 5 million Air Conditioning systems shipped anually, in USA alone.

TinyML market will grow from 15.2 million shipments in 2020 to 2.5 billion in 2030. 
https://www.abiresearch.com/press/tinyml-device-shipments-grow-25-billion-2030-15-million-2020/

TinyML device installs will increase from nearly 2 billion in 2022 to over 11 billion in 2027
https://www.abiresearch.com/press/11-billion-tinyml-device-installs-481-million-5g-advanced-devices-in-2027-and-35-other-transformative-technology-stats-you-need-to-know/


### Common applications

In consumer electronics

- Keyword spotting.
- Wearable devices.
- Sleep quality tracking.

<1 USD microcontroller
<1 USD MEMS sensor

### Efficiency changes of deep learning models

Efficiency has improved a lot over the last 10 years.
https://www.sciencedirect.com/science/article/pii/S2210537923000124

Reviewes data from 2012 -> 2022.

Top perf requires more compute

- 1.0 to 1000.0 GFLOPS for biggest models
- 56% to 90% top1 accuracy overall

But near-top perf requires much less

- At 1 GFLOP, from 60% in 2012 to 82% in 2020
- Also a 10x improvement in GFLOPS/watt, from 20 GFLOPS/watt to 200 GFLOPS/watt


