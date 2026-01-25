
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
and to be able to re-use it with consecutive inputs?


## Design considerations

Different goals would require different designs.
High throughput, low power, or high completeness focus?

For high throughput would want to the application microcontroller to do more computations per second.
That likely means pushing data in/out from host as fast as possible.
And also something that is fairly complex in terms of arithmetic operations,
so that an ASIC actually has an advantage.
TinyTapeout has limited I/O speed due to limited clock speed.
64 Mbit/s (1 bit SPI) - 32 MB/s (4 bit parallel I/O or QSPI).

For low power for the system overall,
would want the application microcontroller to sleep as much as possible,
and the ASIC to use a low amount of power.
And possibly also reduce the gate count on the ASIC?
Possibly means minimizing the amount of data that needs to be sent.

Means that the ASIC could do multiple passes over the data,
before application processor comes back.
Would need to be able to store these input data (in RAM),
and intermediate results (in RAM).

Would make the most sense for low data rate applications?
Ie HAR.
Where sensor sample rate might be under 50 Hz, and output prediction rate might be under 2 Hz.
Data is tri-axial and 8 bit minimum, context window of 1 second.

Gate count is inherently limited on TinyTapeout.
About 1000 digital logic gates per tile.

Arithmetic needs to be low-precision integers.


## Background

#### Sensor interfacing

I2S mixer
https://github.com/cnasenbe/tt03-chnasenb-i2s

#### Maximum I/O throughput on TinyTapeout

Assuming a RP2040 as the controller.

RP2040 max is freq/2, or 62.5 Mbps by standard.
But TinyTapeout max is 40 Mhz, or 40 Mbps for single-bit SPI.


#### Internal RAM constrains on TinyTapeout

- [urish tt06-256-bits-dff-mem](https://github.com/TinyTapeout/tt06-256-bits-dff-mem).
264 DFFs (32 bytes of memory + 8 bits for the output register), and utilizes 70% area of 1 tile
- [MichaelBell/tt06-memory/](https://github.com/MichaelBell/tt06-memory/).
64 byte RAM implemented using 512 latches.
Uses 88% of a single tile area.
- RAM32 macro.
128 bytes arranged as 32x32 bits (32 words of 32 bits each) with a single read/write port (1RW).
Uses an area of 401 x 136 um, which fits in 3x2 tiles and uses about 54% of the area.


### SIMD vector operations

The DSP extension for ARM Cortex M provides SIMD instructions.
Typically present in Cortex M4F designs.
Includes 4x8 bit instructions, which can give a 4-5x speedup for convolutional neural networks on ARM Cortex M4.

https://arm-software.github.io/CMSIS_5/Core/html/group__intrinsic__SIMD__gr.html

The Helium SIMD instructions found on ARM Cortex M52 / M55 / M85 further extends this.


### Matrix matrix multiplications

#### Revenantx86/TinyTPU

https://github.com/Revenantx86/tt07-tinytpu

Implements 2x2 matrix multiplication


https://github.com/Revenantx86/tt09-TinyTPU-Reforged

Looks to be very similar to tt07-tinytpu?
Maybe bugfix release. Not immediately clear from documentation.

Seems to be able to load multiple bits at a time? in_x,in_y,out_z
Seems to be for 8 bit numbers.

#### SkillSurf/tt09-matmul-system
https://github.com/SkillSurf/tt09-matmul-system/blob/main/docs/info.md
https://github.com/SkillSurf/tinytapout-matmul-system/blob/main/docs/info.md
matrix-vector multiplication.
Communication via UART. As a AXI-Stream ?
https://en.wikipedia.org/wiki/Advanced_eXtensible_Interface

Seems to be for 8 bit numbers.

#### tiny-asic-1_58bit-matrix-mul
https://tinytapeout.com/runs/tt06/tt_um_rejunity_fp4_mul_i8
https://github.com/rejunity/tiny-asic-1_58bit-matrix-mul
Uses 6 tiles.

## Coarse-Grain Reconfigurable Arrays (CGRAs)

See [cgra.md](cgra.md)

## Dot product

Only 1 output. Nx2 inputs.
Possibly N inputs and N coefficients if re-using coefficients and storing them in RAM.

ChatGPT says 8 bit dot product is doable in 850-1200 gates,
using a 1 shared multiply unit, and 1 shared add unit.
Computation takes N cycles.
Say 16 cycles.

16-element 8-bit dot product on RP2040, single-cycle multiplier.
Around 100 instructions.


#### Fountaincoder/multimac
https://github.com/Fountaincoder/multimac/blob/main/docs/info.md

Up to 40 elements.
4 bit inputs, 12 bit output.
Needs at least 16 clock cycles to produce answer.

Designed as a "coprocessor" for vector calculations,
for driving with RP2040.
Can also compute minimum and maximums.



https://app.tinytapeout.com/projects/1507

#### TinyTPU

https://github.com/eevaain/tiny-tpu
Simple systolic array.
With custom instruction set.
Implemented in Verilog.
Not for TinyTapeout.



#### IIR filters

https://github.com/Durkhai/biquad_mpw7
12 bit data with 16 bit coefficients
based on
https://opencores.org/projects/biquad

#### Multiply Add

FMAC in STM32.
Can be used both for IIR and FIR filters.
Quite memory layout and configuration
https://notblackmagic.com/bitsnpieces/dsp-accelerators/
Was only slightly faster than ARM CPU though?

### Multiply Accumulate peripheral

A low-precision MAC operation could be used to speed up operations such as FIR, dot-product, convolution.
Maybe implement as a TinyQV peripheral, as part of the RISC-V peripheral competition.

Questions:

- What can one fit in 1-2 tiles?
- What kind of unit-of-operation makes sense? Can one do say 4xint8 in one operation (operating on "packed" 32 bit)?
- How does theoretical throughput compare with what TinyQV can do with its standard ADD/Mul operations?
https://github.com/MichaelBell/tinyQV?tab=readme-ov-file#instruction-timing
Need to take into account store/load from peripheral
Note that instructions are 8 clocks
- How would the peripheral be used in practice via the instruction? X stores, then X nop for a fixed number of cycles, before loading result?
- What level of serial/parallel to use in adder/multiplication unit? TinyQV itself is 4bit. Full serial 1 bit is most space efficient?
- What is the packing format to use for int8 in 32 bits on TinyQV / RISC-V?
- Can we implement SMMUL8 / KDOT8? And be faster? 4 packed 8x8, 32 bit output, with saturation?
4 muls, 4 adds. Saturation operation.
Compare design options. Fully-serial 1-bit shift-add. 2-bit. 4-bit. Full parallel, 8-bit
- ? how would one do pipelining? Such that one can do say 4 KDOT8 in 4 cycles. Probably avoided first time. But interesting to contemplate.

Theoretical speedups possible, due to IO limits
(4*2+4*1)*8 / ((1+3)*8) = 3.0

Brainstorming
https://chatgpt.com/c/6876318c-cba8-8007-a94b-85c8127019cc

Demos

- Audio filters using FIR
- Image classification using CNN
- MLP for classification
- Wrap it in MicroPython C module?

Goal. At least 2x throughput improvement

### PDM input peripheral

Outputs PCM samples from a digital PDM microphone.

- Clock generation. Ideally configurable. 
- CIC filter with decimiation
- 1 clock output
- 2 inputs

Configuration

- Clock.
64 MHz nominal in. But might be lower??
Out. 1024 kHz nominal. 3 Mhz max. 
- Scaling
Allow to shift by ?
- Oversampling ratio. Fixed 64x ? Maybe also 128x
- Channels. Single mono only.
?? Selectable clock edge?
- CLK pin selection. 7 pins
- DATA pin selection. 7 pins

## References

- STM32 DFSDM
https://st-onlinetraining.s3.amazonaws.com/STM32L4_System_Digital_Filter_for_SD_Modulators_interface_(DFSDM)/index.html
Supports both SPI mode, clock+data and 1-wire Manchester mode
Min/max detection. Interrupts on faults.
Configurable oversampling 1-1024.
Support up to 24 bits
- ESP32 I2S, also used for PDM
https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-reference/peripherals/i2s.html
Only supports 16 bit.
Two oversampling settings, 64x and 128x

## ADPCM Compressor with CIC filtering ASIC for Tiny Tapeout 06
https://github.com/hesscharlie/tt06-ADPCM-Compressor
https://tinytapeout.com/runs/tt06/tt_um_ADPCM_COMPRESSOR
Takes PDM microphone input. Outputs ADPCM 4-bit samples.
Decimate by a factor of 64
Needs slow_clk, a clock 8x slower than clk 
Took 4 tiles. ? not sure how much CIC vs ADPCM
Uses 3 sections. Full parallell. ADPCM uses lookup table

CIC filter. Under 8 bit paralell output?
https://github.com/gfg-development/tt-micro-tiles-cic/blob/main/src/tt_um_micro_cic.v


https://github.com/arghunter/Supermic-tt08/blob/main/docs/info.md
8 channel beamformer.
PDM input. 3Mhz.
Each mic signal passed through a third order CIC (Cascading Integrator Comb) Filter to convert it from PDM (Pulse Density Modulation) format to PCM.
Took 8x2 slices. Outputs I2S.


Should be able to read out 16 bits at a time. Not have to split into bytes.

Peripheral interface 4 MB/sec maximum throughput.
We just need 32 kB/sec for 16 bit @ 16 Khz, or 96 kB/sec at 48 Khz.
If one uses full 32 bit words to transfer, still OK by a large margin.
CPU runs at 64 Mhz clock, but only does 8 M instructions per second.
For 16 Khz, would need to read out samples every 500 instruction.
So can do a few 100x compute instructions per sample. OK for many applications.

Questions

- Does one need some buffer? To let microcontroller read out sample(s) after an interrupt
- Can it fit into 1-2 tiles?
- How to do control/settings, in addition to data readout?

Demos

- Audio recording to a file
- Audio processing. Incl DSP and/or ML
- Combine with MAC


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
