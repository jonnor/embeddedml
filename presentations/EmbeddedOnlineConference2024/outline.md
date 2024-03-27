
## Format
5-10 minute

## Audience

Embedded Software Engineers
Maybe some DSP background

## Communication goals

- ML is useful in embedded systems for analyzing sensor data
- emlearn is project that implements classical ML algorithms
- Can deploy models to microcontroller by generating C code
- Supports classification, regression, anomaly detection

Basically 2 minutes on each point. = 8 minutes
2-3 slides per point?

## Outline

ML is useful

- Sensor data analysis
- TinyML concept. Inference on device
- Real-world examples

emlearn project

- Open source. MIT licensed
- Implemented in C99. No dynamic allocations
- Works on any platform. make, cmake, etc.
- Models can be loaded at runtime, OR
- generate "inline" C code for a specific model
- Takes under 2 KB FLASH under 1 kB RAM. For the smallest systems
- Implemented with fixed-point mostly. FPU optional

Deploy

EXAMPLE CODE

- Simple classification. Core concepts
- Bit more involved / realistic.
Involving feature pre-processing, and maybe post-processing ?



## Abstract promises

- TinyML enabling new applications
- Examples relevant to embedded systems
- Python-based workflow
- Demonstrate classification, regression, AD

## Scope

Keep to the "deploy to microcontroller" phase
Assume that dataset has been collected.
Have some setup for model development in Python.

Focus on classical ML.
Feature Engineering / preprocessing + model.

Out-of-scope

- Data collection / design of experiments
- Monitoring while deployed
- Neural networks


