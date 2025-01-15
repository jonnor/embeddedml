

## Findings

ChstGPT seems to be good at Verilog

SPI RAM externally is provided. By RPi Pico
https://tinytapeout.com/specs/memory/
64 kB maximum

## Open questions

How to read/write SPI SRAM? In Verilog, compatible with TinyTapout

What limitations are there in SRAM computations?
Are there any blockers to our RF engine design?
Could one do a medium complexity algorithm? Like FFT on 8 bit values?
Of course it will be rather slow... Since each memory access needs SPI. But is it a problem to practical uses - being able to match microcontroller speed?

How to trigger start? Via IO pins or SRAM?
TRIG pin low?

How to signal completion? Via IO pins or SRAM
INT pin low? Status in SRAM?

How to be a useful building block for later?
Bot for oneself - building towards a complete TinyML ASIC flow.
But also for others? Allowing reuse.
Relevant interop type projects.
Input data. ADC, digital peripherals/protocols. Feature extraction/processing blocks. IIR, FIR, FFT, 
Are there existing projects that put/read data from RAM?

Could we interoperate (via RAM) with one of the microcontrollers? Typ RISCV

How to act nice with a shared SPI RAM?

Input pins that specify the start address?
8 input only pins. 64 kB range. Allows specifying down to 256 byte location
Allows us to be a "shared memory" peripheral

Set SPI pins as inouts when in reset/disable!
Important to allow others to write/read from SRAM

Alternative to having inputs and outputs be values, would be that they are addresses...
They would need to be larger to have a useful reach. Like 16 bits to support 64kB memory space?
But! Someone likely needs to orchestrate the data, trigger running, handle outputs etc.
So probably a copy of input and output is no big deal...
But having the nodes start be a configurable address could be nice!?
Allows a much more compact I/O block for the peripheral.
Maybe inputs can be an address also.
Status. 1 byte?
Output address. 2 bytes
Input address. 2 bytes
Nodes address. 2 bytes
Do we need lengths??? Or is host responsible for verifying? And nodes encode how much is used?

#### How much SPI RAM memory do we need?

8 bits
10 trees.
64 features
1000 decison nodes total
256 leaf max

Status: 1-8 bytes?
Out (leaf indices): 1 per tree. 10 bytes
Input. 1 per feature. 64 bytes
Nodes. 7 bits feature, 1 bit leaf, 8 bits threshold, 8 bits next - 3 bytes. Could be smaller, but then not byte aligned anymore. 3000 bytes for 1k nodes.

Space is sominated by decision nodes.
Can do quite a lot with 4 kB! Even 512bytes-2kB could be used. But also as large as 32kB, for 10k nodes.

FPGA chips often provides SRAM blocks.
ICE40 ERB has 4Kbit/512byte, between 8 and 32 of them, depending on device. And Ultraplus has 256Kbit/8kB blocks, 4x of them.

## Operating principle

RF engine uses an external RAM block
Communication with the RF engine happens though this RAM
Both defining the model (forest of decision trees), providing the input (features), reading the output

## Scope
Random Forest multi-class classification.

Ideally give final output prediction of entire forest. Stretch. Fallback, do this on the microcontroller side
Leaf handling and aggregation
Iterating the trees. 
Support multiple trees. To avoid having to change the tree.
Specific root node address/offset? 
Support multiple tree outputs. So entire forest can run to completion in one go.

## Non goals / out of scope
Parallel execution

## Requirements
Multi-class. Minimum 8 classes
8 bit features and thresholds
Minimum 8 features. Ideally 32-64

Minimum 4 trees. Ideally 10.

Forest.
Need to define storage for root
Probability aggregation. Need to do a streaming mean operation. Need to define storage for leaf nodes.
Argmax aggregation. Need to pick largest of N numbers.
Proba values minimum 4 bits. Maybe 8?


## Testing setup
SPI RAM
Microcontroller uses RF engine.
Puts in data in RSM, triggers the RF engine, waits for completion, reads out result from RAM. Uses/checks the result

## IO

SPI RAM takes 8

## TODO 
- Setup Verilog toolchain, including test bench execution 
- Be able to read values from RAM, modify and write to another RAM location 


Decision step
- Define RAM structure for features and nodes, and some output location
- Read a node, the feature value, write output based on if it was higher or lower

Decision tree
- Same base as decision step. But instead take new node value and use it to read next node. Iterate until node is a leaf. Write leaf index as output

Physical verification 
- Order an FPGA for real tests. Ice40?
- Run on FPGA 
