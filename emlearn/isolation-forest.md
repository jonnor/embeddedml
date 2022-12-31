
# IsolationForest for emlearn

## Inference support
Note: see branch `isolationforest`
 
Modify `eml_trees_predict_tree` to compute the prediction depth.
Return the depth, probably using an out argument.
Maybe standardize on returning EmlError at the same time,
and provide value also as an out arg.

Add testcase, to test_trees.py
Following AD example in test_gaussian_mixture_equals_sklearn

Add to the anomaly_detection.py example

Probably need to adapt trees.py a bit as well,
similar as to when adding regression support

## Learning support

### Data loader API
Also needed by other on-device learning needs.

API to load samples iteratively from where the data is stored.

    Should be easy to plug in typical storage mechanisms.
    Ie internal FLASH, SDcard, internal, SRAM, external I2C&SPI FLASH/SRAM
    Should work natively in chunks of (contigious) samples.
    
! think I have notes on this somewhere...

### Iterative feature summarizer
Must have at least max/min, as that is what IsolationForest learning needs.
But this is also desirable as a feature extractor in general,
for example to compute stats on time-series windows.

Should work for N features

    float minimums[n_features];
    float maximums[n_features];

Should also support mean/std summarization.
Allow switch features to compute on/off. In particular to preserve memory. 

Use something similar to SummaryStatistics as a starting-point, generalize for N features.

### Pseudo random number generator

Needed to fetch random subsets of data, and to make random splits.

Using something similar to lcg_rand

Will be useful also for other learning algorithms, including RandomForest/ExtraTrees.

### Implementation

Learning algorithm should build a EmlTrees object.
Which can then do IsolationForest inference as if built by Python etc.
Need to configure a maximum number of trees, and total number of nodes.
API consumer needs to provide memory for nodes and tree roots.
EmlTreesNode *nodes;
int32_t *tree_roots;

Using the iterative feature summarizer to determine min/max values (for all features).
And random number generator to select features/splits, etc.

Needs to determine the number of samples that matches a given split.
The basic approach requires doing multiple passes over the (entire) dataset. 
Might limit usage to in-memory datasets or online learning at low-rates,
but probably that covers a large amount of usecases anyway?

For each tree in ensemble.

    Fetch a random (complete) subset of samples to start with
    Choose feature to split on (at random).
    Choose point to split feature, randomly between the min/max of the feature values *of the data subset*
    Continue splitting, until N samples remain (fully isolated)


Should expose this learner to Python.
Use an interface compatible with scikit-learn (as far as possible).
Data loader should just access the provided numpy array data. 

### Feature thresholding in data store
Potential optimization for large datasets.

If one could search dataset by feature-aligned threshold constraints, that should make determining splits more efficient.
`feature1<T1 && feature2<T2 && ...`. As in Parquet etc.
This would means implementing some kind of indexing (at least covering max/in) in the data store. 

Especially beneficial for online learning, if the index can be incrementally updated (stored between learning). 
