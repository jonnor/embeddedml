
# Decision node optimizations

As of June 2023, the current layout is 

typedef struct _EmlTreesNode {
    int8_t feature;
    float value;
    int16_t left;
    int16_t right;
} EmlTreesNode;

That is 9 bytes of data.
But on many CPU architectures this will become 12 bytes,
because structs are 32-bit aligned by default.

### Use relative jumps

Right now the child node indices are using absolute addresses.
In order to support relatively big tree ensembles, 16 bits are used.
But most jumps are not that long.
So this is a waste of space.

Allows to reduce child indices from 16 to 8 bits.
This alone should make it possible to go from 9/12 bytes to 7/8 bytes.

In the rare case that a jump longer than 127 is needed,
then need to insert some jump nodes.

### Quantize thresholds
It is unlikely that thresholds actually need 32 bits of precision,
as the data probably does not have that level.

So it should be possible to quantize to 16 bits.

Math operations can still be done with 32 bit integers.


Should use a large amount of dataset to evaluate performance.

For example:
OpenML-CC18 Curated Classification benchmark
https://www.openml.org/search?type=study&study_type=task&id=99&sort=tasks_included

### Default to next on true comparison

Put either the right or left child always as the next item.
And in case of true comparison, just do +1 jump.
This allows to only store one side of the children.

Additionally, it should enable better cachability for the default case.
To maximize that effect, would want the next case to also be the most common case.
Need 1 bit to determine the direction of the operand.

When having a flippable operand, it would normally require one more comparison.
This may be possible to avoid using some magic to let the standard case be determined by the threshold data. 

### Combined gains

typedef struct _EmlTreesNode {
    int16_t value;
    int8_t right;
    int8_t feature;
} EmlTreesNode;

Fits into one 32 bits word.

# Leaf node optimizations

## Probability quantization

The leaf node deduplication implemented in emlearn works with identical leaf nodes.
This works great when leaves are class index, which naturally have a low set of unique values. 
When leaves are class probabilities (for exapmle 8bit fixed-point) then getting identical values is much less likely.
One could have an option to quantize the probabilities to lower amount of bits (1-7 bits).

Must then investigate how this influences predictive performance - and also how effective.

## Probability codebook

An alternative approach to quantize the class probabilities might be to use a codebook.
Where leaf nodes are selected to be a fixed subset that minimizes.

Vector quantization. Can easily be implemented using k-means.
Desire to have a small codebook. Say `K<<256`.
Alternative strategy for the de-duplication, using nearest vector instead of direct match.

Will need some way of specifying the parameters.
Codebook size is possible, but maximum error might be more understandable?
Expect to have interaction with number of classes, and class distribution/imbalance.
Must then investigate how it influences predictive performance - and savings.

## LUT lookup for probabilities

A typical probability might be bi-modal,
with most values being either low (close to 0.0) or high (close to 1.0).
At least we know that if the values are near the middle, it probably does not need so much precision.

Might be possible to use 4 bits per class/probabilty.
And then use for example a LUT with 4 bit in, 8 bit out.
Global lookup table for the entire model / for all classes.
Taking some 128 bytes.
Saving space if n_leafs*n_classes > 256, like 32 leaves a 8 classes

Maybe the fewer bits in leaf, will ensure that more of the leafs can be de-duplicated?



