
# Motivation

Running Machine Learning inference directly on (MEMS) sensors is attractive
for TinyML applications to reducing the amount of data that needs to be transported,
which typically has power efficiency benefits.

We would like to research how one could implement hardware-acceleration blocks,
as using a general-purpose CPU might not be as power efficient.

Specifically we are focusing on decision tree ensembles,
as these are quite powerful, computationally efficient,
and may be suited for a compact implementation in hardware.

Looking to deploy into silicon using the [TinyTapeout project](https://tinytapeout.com/).

# Design

## Operating principle

Acts as an accelerator/co-processor for a CPU, with communication happening via RAM.
Conceptually this would be on the CPU memory bus.
For the initial development, an external (SPI) RAM will be used,
which may be accessed via a SPI peripheral instead of being memory-mapped.

The CPU configures the peripheral via RAM.
Both defining the model (forest of decision trees), providing the input (features), reading the output.

Puts in data in RAM, triggers the RF engine, waits for completion, reads out result from RAM. Uses/checks the result.

The accelerator also has a CLOCK pin, and a RESET pin.
Possibly also a RUN pin, and a INT pin for signalling.

## Scope
Random Forest multi-class classification.

- Addresses of all data specified via RAM
- Support multiple trees, executing all in one run.
- Specific root node address/offset? 
- Support multiple tree outputs.
- Can be used with SPI RAM emulated by RP2040. 64 kB
- Works with a standard microcontroller, like RP2040

#### Not sure

- Can be used with QSPI RAM provided by PMOD. 8 MB ?
Maybe QSPI should actually be later... Just plain SPI, 16 bit for now?

#### Stretch

- Match performance of just-doing-it-in-CPU-instructions
- Works with a TinyTape microcontroller. Like tt06 tinyQV
- Output aggregated prediction of entire forest. Argmax or proba.
Fallback. Output prediction from each tree separately.
Leaf handling and aggregation done on CPU side.

#### Non goals / out of scope

- Parallel execution of trees

## Requirements

- Multi-class. Minimum 8 classes
- 8 bit integer features and thresholds. Signed?
- Minimum 8 features. Ideally 32-64
- Minimum 4 trees. Ideally 10.
- Configuration via "memory mapped" peripheral
- Support peripheral base address via pins.
- Data addresses. Minimum 23 bit (8 MB address range)
- Set SPI pins as inouts when in reset/disable!
Important to allow others to write/read from SRAM.


## Register map

- Status. 1 byte?
- Output address. 3 bytes
- Input address. 3 bytes
- Roots address. 3 bytes
- Nodes address. 3 bytes

QUESTION:
Do we need lengths???
Or is host responsible for verifying?
And nodes encode how much is used?
Should the length be a fixed number of bytes at specified address?
Or the peripheral itself.


## TODO 

#### PoC accelerator implemented in C

Two microcontroller CPUs connected to shared external QSPI PSRAM.
Controlling/test CPU. RP2040, running MicroPython.
Accelerator CPU. RP2040, running C.

Implement the accelerator in C.
Write test programs in MicroPython.
Those can be carried forward to FPGA and ASIC implementation.

Using the QSPI PMOD for communication.
https://store.tinytapeout.com/products/QSPI-Pmod-p716541602

Ordering

- QSPI PMOD. Done, January
- Pico-ice. 2x or 3x
- 2-3x https://no.mouser.com/ProductDetail/Digilent/410-135?qs=s%2FdyVPQMB4x84ELO7yakDg%3D%3D
- 2-3x https://no.mouser.com/ProductDetail/Digilent/240-110?qs=AQlKX63v8RsQhpXXNV1xkA%3D%3D

Ref proto.c

Accessing external PSRAM

- Standard SPI commands should work? At least for not-so-fast clocks, and single SPI?
- QSPI require using PIO.
- https://github.com/MichaelBell/tinyQV/blob/main/pico_ice/micropython/run_tinyqv.py has a qspi_read - but no qspi_write...
- tjaekel implemented QSPI with PIO. MicroPython code at https://forums.raspberrypi.com/viewtopic.php?t=376964
- 4 bit sdcard SDIO with PIO. Should be adaptable to QSPI, in theory.
https://github.com/raspberrypi/pico-extras/blob/master/src/rp2_common/pico_sd_card/sd_card.pio
- SPI only, but high frequency. https://github.com/polpo/rp2040-psram


#### Implementing in FPGA

- Setup Verilog toolchain, including test bench execution 
- Be able to read values from RAM, modify and write to another RAM location 

Decision step

- Define RAM structure for features and nodes, and some output location
- Read a node, the feature value, write output based on if it was higher or lower

Decision tree

- Same base as decision step. But instead take new node value and use it to read next node. Iterate until node is a leaf. Write leaf index as output

Physical verification 

- Order an FPGA for real tests. ICE40 board. pico ice?
- Run on FPGA 


#### Use as co-accelerator for TinyTape CPU


Tech demo/test

- Get a hold of a TTO CPU
- Get it to run code
- Create a demo that uses the RF accelerator to classify data 

Application demo

- Read sensor int CPU accelerometer
- Perform feature extraction on CPU
- Pass features to RF accelerator to classify
- Do something fun with the output


# Background

## Interoperating with CPUs from TinyTapeout


### FazyRV-ExoTiny

https://github.com/meiniKi/FazyRV-ExoTiny
https://github.com/meiniKi/fazyrv

Uses external

### tt06 tinyQV

By Mike Bell.

https://github.com/MichaelBell/tinyQV/
https://github.com/MichaelBell/tt06-tinyQV/

Uses this PMOD, https://github.com/mole99/qspi-pmod
with SPI Flash and two PSRAMs.
8MB of PSRAM.
Seems to have 23 bits for the RAM?

! use this pinout and PMOD for the RAM?

Is in TinyTapeout store.
https://store.tinytapeout.com/products/QSPI-Pmod-p716541602

tinyQV Has documented address map

```
0x0000000 - 0x0FFFFFF: Flash (CS0)
0x1000000 - 0x17FFFFF: RAM A (CS1)
0x1800000 - 0x1FFFFFF: RAM B (CS2)
0x8000000 - 0x80007FF: Peripheral registers (see TT06 repo)
```

PSRAM to in QSPI mode.

Did testing on Pico-Ice.
https://pico-ice.tinyvision.ai/
Uses MicroPython (on the RP2040, presumably), to load program into the QSPI, and then starting the FPGA (with the CPU core, presumably).
 
https://github.com/MichaelBell/tinyQV/blob/main/pico_ice/micropython/run_tinyqv.py

Sets up the external RAM and FLASH, over QSPI.
Seems to use RP2040 also to run the clock?
Pulls the reset and waits for a DONE pin.
Does not seem to use RAM much?

Here is code for testing read/write to RAM, from RP2040.
https://github.com/MichaelBell/tinyQV/blob/main/pico_ice/micropython/test_psram.py

Has code for an external SPI peripheral.
https://github.com/MichaelBell/tinyQV/blob/main/peri/spi/spi.v
But the code used for QSPI RAM/FLASH seems to be
https://github.com/MichaelBell/tinyQV/blob/main/cpu/qspi_ctrl.v

! no TT06 development board in the store? Only ASIC kit... :(

Can run at 64 Mhz.
Can do 1 instruction per 4/8 cycles.

! should be able to run at 64 Mhz (or more)

Uses a Python-based testing tool, https://www.cocotb.org/

cocotb is an open source coroutine-based cosimulation testbench environment
for verifying VHDL and SystemVerilog RTL using Python. 


### tt07 KianV RISC-V RV32E

https://github.com/splinedrive/RISCV-KianV-BareMetalStyle/blob/main/docs/info.md

Uses PMOD Flash + PSRAM.

Use 8MB of PSRAM address.

As of Jan 2025, very sparse documentation.

### TT05 KianV-RV32IMA-RISC-V-uLinux-SoC


https://tinytapeout.com/runs/tt05/tt_um_kianV_rv32ima_uLinux_SoC
https://github.com/splinedrive/KianV-RV32IMA-RISC-V-uLinux-SoC
https://github.com/splinedrive/kianRiscV

Defines an address map. PSRAM mapped at 0x8000000

16 MiB of external SPI flash memory, 8 MiB of external PSRAM


## RAM requirements

Example design constraints

- 8 bit features
- 10 trees.
- 64 features
- 1000 decison nodes total
- 256 leaf max

RAM requirements minimum

- Status: 1-8 bytes?
- Out (leaf indices): 1 per tree. 10 bytes
- Input. 1 per feature. 64 bytes
- Nodes. 7 bits feature, 1 bit leaf, 8 bits threshold, 8 bits next - 3 bytes.
Could be smaller, but then not byte aligned anymore. 3000 bytes for 1k nodes.

Space is sominated by decision nodes.
Can do quite a lot with 4 kB!
Even 512bytes-2kB could be used. But also as large as 32kB, for 10k nodes.

FPGA chips often provides SRAM blocks.
ICE40 ERB has 4Kbit/512byte, between 8 and 32 of them, depending on device.
And Ultraplus has 256Kbit/8kB blocks, 4x of them.

External RAM is available.
For example 8 MB PSRAM PMOD used by RISC-V CPUs.

SPI RAM externally is provided on the standard test setup.
By RPi Pico, with emulated SPI RAM.
https://tinytapeout.com/specs/memory/
64 kB maximum


# Findings

ChatGPT **seems** to be decently at generating example Verilog code?


## Implementation

#### Pinouts

How to trigger start? Via IO pins or SRAM?
TRIG pin low?

How to signal completion? Via IO pins or SRAM
INT pin low? Status in SRAM?

#### RAM access

How to read/write SPI SRAM? In Verilog, compatible with TinyTapout

#### Forest
Need to define decision node format in-memory.

#### Probability aggregation
Need to do a streaming mean operation.
Need to define storage for leaf nodes.

#### Argmax aggregation

Need to pick largest of N numbers.
Proba values minimum 4 bits. Maybe 8?


## Next step: Feature extraction

Dream design is to have an ASIC with complete ML inference capabitilies.
From sensor input to classification output.
Possibly having a simple CPU for coordination,
but main part of data flow being done with accelerated blocks.

Would like to try to build this out incrementally.
Create more and more accelerated blocks.
Reduce how much is done by CPU.

Could one do a medium complexity algorithm?
Like FFT on 8 bit values?
Or IIR filter?
Of course it will be rather slow...
Since each memory access needs SPI.
But is it a problem to practical uses?
Can one match microcontroller speed? Or improve on it?

## Open questions


How to be a useful building block for later?
Bot for oneself - building towards a complete TinyML ASIC flow.
But also for others? Allowing reuse.
Relevant interop type projects.


#### What other projects exist that could be relevant to interoperate with?

- Input data. ADC, digital peripherals/protocols
- Feature extraction/processing blocks. IIR, FIR, FFT
- CPUs. RISC-V etc

#### Are there existing projects that put/read data from RAM?
Others than the CPUs?

#### Could we interoperate (via RAM) with one of the microcontrollers?
Typ RISC-V.
Theoretically this seems feasible?!
But have not seen any examples of that yet.

#### How to act nice with a shared SPI RAM?

Input pins that specify the start address?
8 input only pins. Allows 256 options.
If 64 kB range, allows specifying down to 256 byte location.
Would probably want to block off the memory region used in firmware program, say using a linker script.


