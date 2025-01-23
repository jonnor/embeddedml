
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
Single track, 10 - 20 minute technical session

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

ML is not only huge, complex, expensive systems. TinyML is an alternative
Physical systems, not just abstract. Devices that you can interact with.
Can make useful solutions for niche/personal applications.
Do not need huge amounts of data. Can collect it oneself.
Off the shelf hardware is available. Accessible without eletronics expertize
Low cost enables large scale in diversity of applications, and in number-of-units

#### Smaller points

- TinyML is about deploying ML inference for small microcontroller systems, usually combined with physical sensors
- Wide range of applications across all industries
- Typical TinyML systems are under under 1 watt, under 1 MB of RAM and FLASH, under 10 USD bill-of-materials
- Massive scale. Hundreds of millions of devices shipped anually
- emlearn is a project providing ML implementations for microcontrollers
- emlearn also has a MicroPython API. Enables usage from Python on microcontrollers
- computational efficiency has been improved 10-100x before,
it is possible also for large language models.


### Notes

Quick introduction to the emlearn project
TinyML. Very small models. High energy efficiency. Computational efficiency in terms of RAM.
Massive scale in terms of number.
Measurig and analzying the world continiously.

We believe there are collaboration opportunities

Over 30 billion microcontrollers are shipped annually


TinyML market will grow from 15.2 million shipments in 2020 to 2.5 billion in 2030. 
https://www.abiresearch.com/press/tinyml-device-shipments-grow-25-billion-2030-15-million-2020/

TinyML device installs will increase from nearly 2 billion in 2022 to over 11 billion in 2027
https://www.abiresearch.com/press/11-billion-tinyml-device-installs-481-million-5g-advanced-devices-in-2027-and-35-other-transformative-technology-stats-you-need-to-know/

Keyword spotting.
Wearable devices.
Sleep quality tracking.

<1 USD microcontroller
<1 USD MEMS sensor

emlearn since 2018


Efficiency has improved a lot
https://www.sciencedirect.com/science/article/pii/S2210537923000124
2012 -> 2022. 1.0 to 1000.0 GFLOPS
56% to 90% top1 accuracy
At 1 GFLOP, up to 82% in 2020

10x improvement in GFLOPS/watt
