
## Differential Programming

Enable full pipeline from raw sensor data to high-level task output,
that can be learned end-to-end.
But where it is possible to also existing fixed-function or special-purpose blocks,
that are known be relevant and work well to the task.

In the context of machine learning for sensor data,
and in particular for computationally constrained settings
and low-resource data domains.

Benefit. Can convert some hyper-parameters to parameters.
Directly learn/optimize instead of having to run many independent experiments.


## Usecases of interest

Applications/tasks

- Brewing. Audio input to number of plops.
- Rowing counter. Accelerometer to counter of numbre of strokes.


- Optimize samplerate. For example via a bandpass
- Optimize number of filters in a filterbank
- Use an approximate computation instead of exact, maybe with lower precision, lower computational intensity, or utilizing matmul/NN accelerated hardware.
For example, time-domain filterbank instead of FFT+reduction
- Induce structure into our problem to make it more interpretable/robust or sample/data-efficient
- Use high-level loss function to reduce effort needed to label data. See also weak-labeling

## Components of interest

- FFT.
- Spectrum reduction. Mel filters etc
- IIR filters. Especially high/low-pass and bandpass are commonly useful.
- Counting events.
- Convolution operators.

### Differentiable blocks

Differentiable filterbank.
[SincNet](https://github.com/mravanelli/SincNet). Parametrized sinc functions, which implement band-pass filters. Can be used as alternative to FFT+mel-filterbank

Filters.
[torchaudio.functional.biquad](https://docs.pytorch.org/audio/main/generated/torchaudio.functional.biquad.html) and generators to setup bandpass/highpass/lowpass,
like [torchaudio.functional.bandpass_biquad](https://docs.pytorch.org/audio/main/generated/torchaudio.functional.bandpass_biquad.html).


## Implementation options

Important that the inference-only (forward-pass, no gradients) is efficient,
both in terms of memory usage, compute time and program space.

#### Implicit dynamic compute graphs versus static

Tensorflow 1.x was primarily a compute-graph library,
where the operations would build up a DAG representation, which then could be evaluated with data to flow though it.

PyTorch and JAX instead creates an implicit compute graph, defined at execution time.

ExecuTorch converts a PyTorch implicit compute graph into a static one,
so that it can then be compiled to a target which does not.
TorchScript on the other hand is a runtime that can run (some) PyTorch code
using the C++ runtime only, without needing Python.

#### On-device autograd

Have an autograd system that can be used both on-device, and also on-PC for the training.
Avoids the "two worlds" problem - that the training setting uses a different libraries, programming language and tooling.
Might mean that.
Likely means having to use other tools that what "regular" deep learning / differentiable programming is doing.

Would want to have relatively a high-level language.
And ability to reuse tooling code from existing ecosystems as much as possible.


#### Compiling autograd models

Using an existing established framework on the PC for training, like PyTorch or JAX.
Then compiling the entire end-to-end pipeline to optimized code for running on the target device.

Can do things like fuse multiple operations into one,
to reduce memory usage, computation, improve memory locality.

Important that it can handle the general-purpose / Turing-complete parts.
Might still need a non-trivial runtime.

## Educational materials

#### TinyTorch via MLSysBook 
https://mlsysbook.ai/tinytorch/getting-started.html

Could one one enable running them with MicroPython?


## Deployment software

NOTE: initial notes. Still sketching out this space.

#### TinyAD
https://github.com/patr-schm/TinyAD
TinyAD is a C++ header-only library for second-order automatic differentiation.
Small dense problems are differentiated in forward mode, which allows unrestricted looping and branching.

#### XNNPACK

C code. Is used by Executorch.
Architecture specific? Has ARM support and RISC-V.
Does it have portable reference code?
But not targeted to microcontroller-grade devices?
https://github.com/google/XNNPACK/tree/master

#### Executorch
Has ARM Cortex M support. Though it focuses much more on Ethos-U.
https://github.com/pytorch/executorch/tree/913436a44b877259169e79e6a061f75638336b55/examples/arm
As-of 2025, "WIP. This is a temporary/placeholder backend for Cortex-M CPUs. It is not intended to be used in production, but rather as a proof of concept."
https://github.com/pytorch/executorch/tree/913436a44b877259169e79e6a061f75638336b55/backends/cortex_m


# Background

Courses

- [UCSD CSE 291: Differentiable Programming (Spring 2025)](https://cseweb.ucsd.edu/~tzli/cse291/sp2025/)
- [UCSD CSE 291: Differentiable Programming (Spring 2024)](https://cseweb.ucsd.edu/~tzli/cse291/sp2024)
- [CMSC 838B / 498Z (Fall 2025): Differentiable Programming](https://www.cs.umd.edu/class/fall2025/cmsc838B)
- Differentiable programming at Institute of Computing for Climate Science Summer School 2025.
[Overview](https://iccs.cam.ac.uk/events/institute-computing-climate-science-annual-summer-school-2025)
[Youtube playlist](https://www.youtube.com/playlist?list=PL3PByZO-B6dODVXyQcfKEDnIldqReFryp)
- [Github repo](https://github.com/Cambridge-ICCS/differentiable-programming-summer-school-2026?tab=readme-ov-file)
- [CS 8803 - Differentiable and Probabilistic Programming Languages -Spring 2025](https://jsl1994.github.io/course/cs8803-Sp25/course.html). Focused on papers.

Lectures

- [Differentiable Programming for Data-driven Modeling, Optimization, and Control](https://www.youtube.com/watch?v=VrVxMs5vd-4).
Jan Drgona, Pacific Northwest National Laboratory.
- [Differentiable Programming for Data-driven Modeling, Optimization, and Control](https://www.youtube.com/watch?v=s0lI3RroPqA).
Ján Drgoňa, PNNL, Johns Hopkins University (JHU). Nov 19, 2024.
- [Neuromancer: Differentiable Programming Library for Data-Driven Modeling and Control](https://www.youtube.com/watch?v=cTCIf7YEu68)

Software

- [NeuroMANCER](https://github.com/pnnl/neuromancer).
Neural Modules with Adaptive Nonlinear Constraints and Efficient Regularizations (NeuroMANCER)
is an open-source differentiable programming (DP) library for solving parametric constrained optimization problems,
physics-informed system identification, and parametric model-based optimal control.
- [deluca](https://www.deluca.fyi/). jax-based library that provides differentiable environments,
control algorithms that take advantage of such environments. Focus on reinforcement learning and robotics.
https://www.deluca.fyi/

Books

- [Physics-based Deep Learning Book](https://physicsbaseddeeplearning.org/intro.html)
By TU Munich.

Unrelated

- [Random Forests & Other Random Thoughts](https://www.youtube.com/watch?v=FsxiQKXO0UU&list=PL3PByZO-B6dODVXyQcfKEDnIldqReFryp&index=21).
Fundamentals of random forests and related tree models from first principles, their strengths and weaknesses, and methods for understanding their sensitivity.
Weakness: Clips outside of input data domains, not suitable for extrapolation.

