
## Research question
Can we build a TinyML accelerator/implementation on TinyTapeout?

## Type of accelerator

A co-processor, where input data is set to ASIC, and results returned,
would be a cool proof of concept and great learning exercise.

However the communication overhead will be considerable,
probably more than will be gained in offloading.
So in the ideal scenario, sensor input would go to this ASIC,
the feature extration be done in there,
and also the classification.

However the classification and feature should be parametric,
so that it can be updated to do different inference tasks.

Since this is a rather complex system, it may require multiple iterations
- and may even need multiple TinyTapeout tiles.

## Usecase

PDM microphone?
Would need to generate a clock. 768 kHz - 3.0 MHz
Would need to read input at the same rate.
Need either to 

Analog microphone?
Would need to do feature extraction in analog domain.
Or to implement an ADC.

Analog accelerometer.
Lower sampling rate.

## Constraints

### Memory
https://tinytapeout.com/specs/memory/

Alternatives

- Register based ram. Up to 40 bytes of memory. 32 bytes at 70% utilization of 1 tile.
- RAM32 macro. 128 bytes arranged as 32x32 bits, 50% utilization of 3x2 tiles.
- External SPI RAM. Takes 4 pins of IO

SPI RAM.

Emulation using RP2040. Available on TinyTapeout.
https://github.com/MichaelBell/spi-ram-emu
12.5 MHz read.

## Analog input

Mixed signal is possible since early 2024.
But beta, much less experience.

## Clock

System clock between 3 Hz and 66.5 MHz.
? can one do readout in 1 Mhz range

## Digital IO pins

Standard pinouts designed for I2C, SPI
https://tinytapeout.com/specs/pinouts/



## Feature extraction

Digital IIR filters.
Statistical summaries?
Level crossing. Very efficient

# Sketches

Decision tree.
With RAM32 macro can get 128 bytes.
Say 16 bytes for input features,
and 4 bytes for output probabilities.
Would only get approx 100 bytes or 800 bits for decision nodes, if stored in RAM.
Each node. 8 bits feature data, 4 bits+ left jump, 4 bits feature index, 2 bits for flags. Implicit "next" node.
Say 16 bits total. Gives some 50 decision nodes. Probably a single tree, no ensembles.
Enough for technical tests. Possibly some trivial demos. But probably not for any real application.s

Using SPI RAM would allow microcontroller-sized decision tree ensembles.
Inference time would very likely be bottlenecked by RAM latency/throughput.
A small cache could potentially help, to do burst reads? Say 16 bytes.

Our goal is to use a signal processing frontend to compute features at a reasonable rate.
Say we want to run inference every 10 ms.
With a max depth of 10. With 4 bytes per node. Expect to read 40 bytes.
In 10 transactions a 4 bytes in the simple case.
Gives 1000 us per transaction. At 10 Mhz clock that is 10k clock cycles.
Should be doable with maybe 100x margin.

Would need to prototype and validate it on an FPGA first.

# Relevant works


### 8-bit SAR ADC. TinyTapeOut 6.
https://github.com/wulffern/tt06-sar/blob/main/docs/info.md
4 Mhz samplerate!
Utilization not specified.
Carsten Wulff at Nordic Semiconductor / NTNU.


### DecisionTrees 
https://github.com/fpgasystems/DecisionTrees
Verilog code. GPL.
Very little documentation.

### brandon9838/Verilog-Implementation-of-Decision-Tree-Accelerator

https://github.com/brandon9838/Verilog-Implementation-of-Decision-Tree-Accelerator/tree/main
Verilog code. No license
Good visualiziation of system in slides.

### 15418-Vivek_Krishnan
http://vrkrishn.github.io/15418-Vivek_Krishnan/design_docs.html
Shows very simple for the core decision node logic

### Anomaly detection using Isolation trees (TinyTapeout 6)
https://github.com/Lefteris-B/i_tree/blob/main/docs/info.md


### PDM microphone input

https://github.com/kazkojima/pdmmic-example


