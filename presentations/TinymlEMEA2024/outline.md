
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


### Summary

emlearn is a TinyML library that
implements classic Machine Learning methods for microcontrollers and embedded systems.

Tree-based models are very useful for TinyML type applications.

emlearn has the best tree ensemble models for microcontrollers.

emlearn and MicroPython
can be used to build complete TinyML applications in Python.



@app.route("<room>:{living_room,kitchen}/temperature")
def receive_temperature_data(room):
    ...

@app.route("<room>:{living_room,kitchen}/temperature")
def receive_temperature_data(room):
    ...

@app.route("<room>:{living_room,kitchen}/temperature", include_raw=True)
def receive_temperature_data(room, topic, message):
    ...

### The power of decision tree ensembles


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



# Read raw data
sensor.fifo_read(samples)

# Preprocess features
preprocessor.run(samples, features)

# Run model
out = model.predict(features)


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


#include <eml_trees.h>
  
static const EmlTreesNode xor_model_nodes[14] = {
  { 1, 0.197349f, 1, 2 },
  { 0, 0.466316f, -1, -2 },
  .........
  { 0, 0.421164f, -2, -1 } 
};
static const int32_t xor_model_tree_roots[3] = { 0, 5, 9 };
static const uint8_t xor_model_leaves[2] = { 0, 1 };

EmlTrees xor_model = { \
    14, (EmlTreesNode *)(xor_model_nodes),        
    3, (int32_t *)(xor_model_tree_roots),
    2, (uint8_t *)(xor_model_leaves),
    0, 2, 2
};


static inline int32_t xor_model_tree_0(const float *features, int32_t features_length)
{
      if (features[1] < 0.197349f) {
          if (features[0] < 0.466316f) {
              return 0;
          } else {
              return 1;
          }
      } else {
          if (features[1] < 0.256702f) {
              if (features[0] < 0.464752f) {
                  return 0;
              } else {
                  return 1;
              }
          } else {
....
}


static int32_t
eml_trees_predict_tree(const EmlTrees *forest, int32_t tree_root,
                        const int16_t *features, int8_t features_length)
{
    int32_t node_idx = tree_root;
    while (node_idx >= 0) {
        const int16_t value = features[forest->nodes[node_idx].feature];
        const int16_t point = forest->nodes[node_idx].value;
        const int16_t child = (value < point) ? forest->nodes[node_idx].left : forest->nodes[node_idx].right;
        if (child >= 0) {
            node_idx += child;
        } else {
            node_idx = child; // leaf node
        }
    }
    const int16_t leaf = -node_idx-1;
    return leaf;
}

