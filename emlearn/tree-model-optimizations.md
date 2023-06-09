
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



