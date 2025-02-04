
# Status

Not submitted. It was too late :((

# Talk

### Computationally efficient tree-based ensemble models


## Takeaways

- scikit-learn defaults will create very large models,
and this is *sometimes* (but not always) problematic
- It is often possible to
- Optimize trees/width and depth jointly
- RandomForest is suitable for extremely efficient models
- emlearn is a C library for deploying tree-based models to microcontrollers
- Can run on microcontrollers with a few kB of RAM, few milliwatts of power, under 1 dollar.

## Title

Tree-based ensembles

## Abstract

Tree-based ensembles such as Random Forest are incredibly useful predictive models for classification and regression tasks.
These kinds of models tend to give very good predictive results with little hyperparameter tuning,
usually at quite acceptable computational costs (inference time, disk space, and RAM usage).
However, it can occationally happen that your model is much slower or larger than you need.
In this talk we teach you avoid or fix these problems,
and how to make tree-based ensemble models that are highly computationally efficient.

We will do this by taking a look at how tree-based ensemble models work under-the-hood,
understand their computational footprints,
and discuss various techniques to optimize inference time and model size.
We will use as the Random Forest implementation in scikit-learn as a starting point,
but also look into alternative implementations.
In the most extreme cases, we will demonstrate how tree-based-models can be useful
on devices which have just a few kilobytes of memory and run for multiple years on a small battery.

Some of the concepts and techniques we will cover are:

- How model complexity is influenced by hyperparameters regulating number of trees (width), and tree depth 
- How the model complexity drives computational costs (model size, inference time)
- Practical strategies for tuning hyperparameters that take computational costs into account
- How to joinly optimize width+depth to get good regularization/generalization at low model complexity
- Using batches with predict() to get good inference times
- Reducing model sizes on disk using joblib or skopt instead of pickle
- Reducing RAM usage with treelite
- How to deploy tree-based models microcontrollers and embedded devices using emlearn
- How feature quantization and integer-only computations reduce model size and inference time
- How leaf quantization, leaf de-duplication and leaf clustering reduces model size



250 to 2100 characters.

## Brainstorming
Based on the CFP prompts
https://ep2025.europython.eu/programme/cfp/

- What problem does your session address?
Computiational efficiency of tree-based models.

- Why is this interesting to the Python community?
Lacking documentation for best practices for computationally efficient tree-based ensemble models.

- What’s your perspective on this problem?
Deploy models on to small embedded systems and tiny microcontrollers,
where computational efficiency is key.
Have collected best practices and developed techniques for tree-based models (in emlearn project).

- What will the audience take away?

## Motivation

Share learnings from making highly efficient tree-based models.
Tell people about emlearn.
And recent paper on Random Forest optimizations.
Maybe also about.


# Story arc

To be decided...

Ideas:

- Take a model from a default scikit-learn implementation,
make it 100x smaller to run on a microcontroller grade device (with emlearn).
Ideally related to sensor data, relevant to run on embedded device.
Maybe like ? 
- Task idea
Water quality estimation? Kaggle dataset.
Human Activity Recognition?
Air quality estimation?
https://archive.ics.uci.edu/dataset/360/air+quality
electronic nose?
https://ieee-dataport.org/documents/dataset-electronic-nose-various-beef-cuts

# Outline

TODO: clean up. Create a better structure.
Maybe focusing on Inference time, disk size, RAM usage as 3 separate threads?
And have a common start and ending section around that.

Core concepts

- Predictive performance.
- Computational COST. Inference time, disk size, RAM usage
- Hard constraints. VS optimizing target.
- Pareto frontier / pareto optimal.

Pragmatic goal setting

- Setting predictive performance targets.
- Setting cost targets
- Good enough? You are done!
- Expectation setting for RF performance with scikit-learn

Prediction time improvements

- Batch processing. Very important!
- Parallel computing.

Model size

- persistence/serialization options

Model training
- Width (n_estimators) vs depth
- Width selection.
Claim: diminishing returns predictive performance as n_estimators gets large.
IF regularization is suitable. 
Show with and without depth tuning?
- Depth selectors. Depth-first approaches
- Depth selectors. Best-first (max_leaf_nodes)
- Feature subsetting. max features
!! Interaction with number of trees
Low probability of getting the informative features
But also reduces tree diversity - can give too little regularization

emlearn
- tree-based models for
- optimizations.
Feature quantization.
Leaf de-duplication.
Leaf quantization
Leaf clustering

Implementing classification trees in hardware
Ref hwtrees.
Stretch


### In scope
Covering. Random Forest, ExtraTrees

#### Maybe

Visualize forest/trees structure

#### Out of scope

- How to best use multiprocessing to improve inference time?
Not so relevant for embedded
- Feature engineering? Domain/data dependent
- Gradient boosted trees




## Notes

### Computational costs for tree ensembles



### Hyperparameter selection

Strong interactions between several parameters.
Number of trees interacts with everything.
May want to limite the number of configuration tried for trees.
Then tune the others variables specifically for each tree width.

Or rather, depth regularizer is as conditional on trees.
Do trees in log2 steps. Ex: 100,50,25,12,6
Examples in emlearn is decent starting point 
Also want to cover feature selection


### Serialization options for scikit-learn RandomForest

```
pickle
joblib
cloudpickle
dill
skops, https://skops.readthedocs.io/en/stable/
treelite, https://github.com/dmlc/treelite
```

Calling getstate/setstate manually...
https://github.com/scikit-learn/scikit-learn/discussions/25902
Or maybe `get_params()`, and `set_params()` ?

Do not use pickle!

joblib, with `compress` option gives much smaller files.


### RAM usage

scikit-learn has a very high base cost.
Can be over 100 MB to just load RandomForestClassifier.

May interact badly with `multiprocessing` for CPU concurrency,
as this base cost can get multiplied for each process.
! at least use bounded concurrency. Ie a pool with workers smaller than CPU cores.

! there are much more RAM efficient options available
treelite
emlearn


# Poster: 
