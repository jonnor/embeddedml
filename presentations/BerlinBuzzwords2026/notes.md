
## About

7-9 June 2026 @Kulturbrauerei

> Berlin Buzzwords is Europe’s leading conference for modern data infrastructure,
> search and machine learning and is focused on open source software projects.

## Call for Proposals



https://program.berlinbuzzwords.de/bbuzz26/cfp

Berlin Buzzwords is looking for talks on

```
…any aspect of search: From search engines to relevance engineering, and more.
…Data Science and **Making sense of data**: AI, ML, Data Wrangling, Data Engineering, MLOps, A/B-testing, etc.
…everything related to stream processing.
…Operations / Infrastructure, including building and maintaining infrastructure, but also delivery and testing.
…Scaling up (taking better advantage of a single machine, with threads, accelerators, specialized libraries, …), scaling out (distribution) or even **scaling down**; including moving from centralized services to “on device”.
…Storing data and everything that entails.
…experiments, hacks and novel approaches, but also lessons learned, generally-useful algorithms, and experience reports.
…societal, environmental and ethical impact of tech.
…Management, Leadership, Team Culture and internal processes, as well as Open Source & Governance.
```


Guidelines

Make sure you take the following guidelines to heart:

```
Titles should be descriptive and be less than 60 characters long

The abstract should serve as a tl;dr for your session, giving a brief summary of the contents and what the audience can learn.

The session description is the most important part of your proposal, since talks will be rated by our program committee mainly on the basis of your description. A good description contains a detailed and focused outline of your talk, explains why your topic is relevant, what you will be talking about and what the audience will learn.

Please don’t include your biography or personal details in your abstract or description, since personal information will be removed before the review process starts to avoid bias.
Title, abstract, and description of your talk will be visible to everyone and will be used on our talk description pages if your proposal is accepted, so be sure to write a clear and concise text in full sentences and don’t exclusively use bullet points.
```

## Title
Data Science under 1 megabyte - for microcontrollers and browser

(with MicroPython and emlearn)


## Length
20 minutes. Alternatively: 40 minutes 

## Abstract

Python is the standard solution for many machine learning and data science applications,
from large cloud systems, to workstations, and even on larger embedded or robotics systems.
But as we move down into more constrained environments regular (C)Python starts to be a less good fit.
The MicroPython project provides a Python implementation that is tailored for such environments,
and this makes it possible scale down to microcontrollers with just a few megabytes of RAM (or less!).
As a bonus, MicroPython with WebAssembly also makes lightweight browser applications possible.
In this talk, we will discuss how to combine IoT devices, MicroPython and browser to build
stand-alone smart sensor systems and laboratory gear for physical data science.

Scaling down in terms of RAM and CPU requirements enables
massive scale.
Ubiquituous

Enable data scientist, software developers and

Deploy complete devices integrate sensors, data processing and user interfaces.
10 dollars.
Products.

## Description



## Notes

Regular PyData stack is a foundation for science, engineering and education around the globe.

MicroPython enables scienstics, engineers, makers and students to use their Python skills
also in the area of physical computing, embedded devices, etc

It is a solid alternative to Arduino etc.

## Takeaways

- MicroPython enables physical computing for those that know Python
- Applicable to many data-oriented applications. Especially incorporating sensors
- MicroPython enables scaling down to hardware that costs 10 USD
- Has
- emlearn-micropython enables running machine learning classifiers 
- Can also run in the browser. Interactive, data visualization, etc
- MicroPython in browser enables much faster loading compared to big Python

## TODO

- Submit abstract
- Test emlearn-micropython in browser
- Create some web demo


## Ideas

Concepts

- Serve MicroPython WASM from device. To do learning in browser. Send model back?
- Doing data labeling in browser
- Doing data curation/cleaning in browser
- Doing training in browser

Usecases

- Lab gear. For scientific/engineering uses
- Wireless Sensor Networks. Ref EuroScipy Krakow 2025
- Educational lab exercises.
- Robotics.
- DIY/Maker/kits. For niche cases. Or open-ended.

Demos

- Motion classification
- Audio analysis / Sound Event Detection
- UV-Vis-NIR spectroscopy
- Gesture recognition. With built-in learning. Datavis in browser
- Indoor localization and mapping

Random

- Reference Amy, and their in browser ?


## MicroPython and emlearn in browser

- Make a browser demo for inference. Basically same kind of model as on device.
- Browser demo, heavier model, running on instances on-device model flagged of interest
- Make a brower demo for labeling
- Make a browser demo of training
- Make a browser demo for train-in-browser + deploy-on-device

## Stand-alone devices for physical data science

Plug & play.

- Without needing any cloud connectivity.
- Without 

- Keeps the user in control
- 

Aspects

- Measure using sensors
- Store the data
- Connectivity using WiFi
- Discovery using mDNS
- Settings/configuration/control via webui
- Automated continious data processing/analysis. DSP and ML
- Interactive data analysis, served via webui. Lookup, visualization, faceting, clustering
- Raw data storage/sampling, for building/monitoring ML datasets
- Labeling for ML models, via webui. Few-shot learning?
- Optional integration. Pull using HTTP API (same as webui). Push using Webhooks, MQTT

Details

- asyncio concurrency


## Searching in the context of IoT standalone devices, private and open

- Searching through large amounts of information is a key facet of todays IoT and cloud systems
- Often this is done by transmitting all the IoT data to a centralized (and propriertary) cloud service, which then can do the search
- This is bad in terms of privacy. Consumers also have no recourse
- Do we actually *need* to send the data away to enable such usecases?
- What can be done with existing low-cost hardware and open-source software?
- Example. Smart doorbell. Security camera.
Want to do event detection, to annotate timeline. But also search to find things of interest
- Storing embedding vectors.
- Storing features.
- Searching over features and embedding vectors.
- What about multi-device? Can expose API. Allow a central device phone or PC, to pull from all/multiple sources.
- On-edge storage.
- What can be done on ESP32 class hardware? Or RPI grade.
Do some benchmarking. Of 
- My interests right now. Not so much the computer vision or smart doorbell.
More interested in applying it to Sound Event Detection.

## Related fundamentals

- Time-series storage / data-warehouse for MicroPython 
- Both for features and vectors. Ex: Parquet. Or Arrow.
- Also web APIs to access this, with MicroDot
- Approximate Neigbors vector search would also be interesting.
Maybe Locality Sensitive Hashing? Or Product Quantization (PQ). Or HNSW.
- Indexing for features also interesting.
Inverted Index with Bucketing.
VA-File (Vector Approximation).
R-Tree*
- Multi-step temporal aggregation also interesting.
- Data-thinning strategies with implementations.
- Data-sampling strategies with implementations.

NOTE: Indexing strategies must be suitable for incremental/continious indexing,
and work with low memory.


## Performance boundaries

How much data do we have, with time-series

- 1 second resolution over 1 year, 31 M datapoints. 1 GB at 32 bytes/sample
- 1 minute resolution over 1 year, 0.5 M datapoints. 16 MB
- 1 second resolution over 3 months, 7 M datapoints. 250 MB

> Here's the result for the onboard flash on an ESP32-S3-MINI-N8R2:
> 
> Write: 4.25 MB, 78.510 secs, 55.43243 kB/sec
> Read: 4.25 MB,  4.294 sec, 1013.507 kB/sec
> 
> It's running in quad mode and 80 MHz.
> 
> Was able to get 10 MB/sec, with some tweaks to block sizes.
>
> https://github.com/orgs/micropython/discussions/14130

On STM32, people were able to read SDcard at 10 MB/S

> https://github.com/micropython/micropython/issues/2648

Assuming we can read 1 MB/second.
At 100 bytes/sample, 10k samples/second.
With 8 MB PSRAM, could theoretically keep 1MB+ data in-memory.

Only dynamic/parametric queries makes sens to do after-the-fact.
Other things are better to do on a continual basis.



