

### Capacity modelling tools

Purpose: Check if a proposed model fits within contraints.
Model storage, memory usage, inference time, CPU "utilization"
Allow to declare budgets, function for checking if over?

Device benchmark:

eml_bench_device
    multiply_adds/second,
    convolutions_3x3/second
    node_evaluations/second (trees)
    ffts/second (melspec)

    Average, standard deviation, 75%, 95%

Ran for each supported hardware. Publish numbers

Perf modelling.
 
    takes perf constants from benchmark
    + ML model 
    => estimate model size, mem use, inference time 

Model benchmark

    Test the real model.
    Verify against Perf model.
    Do this for a set of example models, publish numbers


Models:

    Generic linear model. SVC,LogisticRegression
    Kernel. SVM

On-line DSP tools:

    Streaming summarizers/estimators. min/max, mean/std, median
    Reservoir sampling.
    Voice Activity Detection
    Sound level. Incl IEC A-weighting

Transformers:

    Scalers: Standard,MinMax
    Dimensionality: PCA,NMF

Perf:

    8/16bit weights. NNs
    Integer-math only for compiled trees. 32bit/8bit
    Support sparse models. Autoreduce during conversion?
    Sparse dictionary representations

Advanced stuffs

    Audio beamforming.


