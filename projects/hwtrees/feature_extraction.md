
# Feature extraction

Could one do a medium complexity algorithm?
Like FFT on 8 bit values?
Or IIR filter?
Of course it will be rather slow...
Since each memory access needs SPI.
But is it a problem to practical uses?
Can one match microcontroller speed? Or improve on it?

Cases with higher computational intensity (relative to I/O) would do better.
Like a multi-stage IIR/biquad, if the coefficients can be put into internal RAM/registers. 


Ideally would be able to store coefficients in internal RAM,
and to be able to re-use it with consecutive inputs.

## Background

#### IIR filters

https://github.com/Durkhai/biquad_mpw7
12 bit data with 16 bit coefficients
based on
https://opencores.org/projects/biquad

#### Temporal Convolutional Network

Compact output. n_channels
Compact weights. Can be computed with model.count_params() with keras-tcn. 

```
inputs = tf.keras.layers.Input(shape=(32, 3), name='input')
tcn_mod = TCN(nb_filters=3,
    use_batch_norm=False,
    use_layer_norm=False,
    use_weight_norm=False,
    use_skip_connections=True,
    dilations=(2,4),
    kernel_size=4,
    nb_stacks=1,
    activation='relu',
)
tcn_out = tcn_mod(inputs)
model = tf.keras.Model(inputs=inputs, outputs=tcn_out)
print('receptive field', tcn_mod.receptive_field)
print('params', model.count_params())

receptive field 37
params 156
```
Still a more than feasible on TinyTapeout.
Also 3 outputs for 32x3 inputs is possibly to much data compression.

```
inputs = tf.keras.layers.Input(shape=(32, 3), name='input')
tcn_mod = TCN(nb_filters=3,
    use_batch_norm=False,
    use_layer_norm=False,
    use_weight_norm=False,
    use_skip_connections=True,
    dilations=(2,),
    kernel_size=3,
    nb_stacks=1,
    activation='relu',
)
tcn_out = tcn_mod(inputs)
model = tf.keras.Model(inputs=inputs, outputs=tcn_out)
```
receptive field 9
params 60

3x9 -> 1x3 dimensionality reduction.
More relevant.
Can then run this on consecutive inputs to get for example 3x54 samples
(~1 second at 50 Hz for HAR) -> 6*3=18 features. Classify with Random Forest.

But maybe the hardware accelerator should be a more generic 1d with stride/dilation.
Or even have conv2d support, with 1d being just a special case?
SeparableConv2D

#### Convolutional Neural Network
Fundamentally a FIR type operation.


```
model = keras.Sequential([
        keras.Input(shape=(32, 1, 3)),
        layers.SeparableConv2D(3, kernel_size=(5, 1), strides=(3, 2), activation="relu"),
        layers.SeparableConv2D(3, kernel_size=(5, 1), strides=(3, 2), activation="relu"),
        layers.Flatten(),
])
```
Is just 27 parameters. Dimensionality 6 out.
Including input, output, temporary buffers, should be doable in under 100 bytes of RAM?

```
model = keras.Sequential([
        keras.Input(shape=(32, 32, 1)),
        layers.SeparableConv2D(3, kernel_size=(3, 3), strides=(3, 3), activation="relu"),
        layers.SeparableConv2D(3, kernel_size=(3, 3), strides=(3, 3), activation="relu"),
        layers.Flatten(),
])
``
Only 54 parameters. Dimensionality 27 out.
Idea is that a 3x3=9 input block would be sufficient to keep in cached RAM. 
