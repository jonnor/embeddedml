
# The convergence between supercomputing and IoT nodes: design concepts and their application
Mauro Olivieri. Sapienza, Universita di Roma


Historically: Exponential growth in power efficiency.
2017, above 10 GFLOPS/watt.
Expected between 33 and 50 GFLOPS/watt in 5-7 nm,
with extensive use of hardware accelerators.
Now have hit the power law. Need to specialize.
First example, GPUs.


Local processing to reduce communication overhead.

IoT and supercomputer technologies are "touching".


## Supercomputer architecture

- Core
- Multi-core chip.
- Multi-chip node. + accelerator chips
- Multi-node rack.


## Execution time

    T_exec = N * CPI * T_ck
    
    N: operation count. Changed by changing program
    CPI: clock cycles per op. Hardware architecture, compiler.
    T_ck: Clock cycle time. Fabrication process 

Always limited by Amdahls law

## Speedup possible

def amdahl(p, s):
    return 1/((1-p))+(p/s)

amdahl(0.4, 1)

> 1.706 

## Power law

Dynamic power dominates.

    P = C_eff * V**2 * 1/T_ck

    C_eff. Effective (average) capacitance. Silicon, microarchitecture.
    V. Supply voltage. Process improvement. Propagation delay, signal/noise constrained.
    T_ck. Cycle clock time. Silicon improvement. Microarchitecture

## Propagation time

Kurodas alpha power model

    t_pHL = C_l * V_dd / 2 * K_n (V_dd - V_t)^a

Depends very strongly on voltage.
FO4 delay: 1 INV cell driving 4 identical INV cells.
Process parameter.

## Optimizing power efficiency

Assumption: Software/algorithm is optimal

Possible strategies:

- Pipelining your core.
- Paralellizing with multi-core
- Hardware accellerator.

## Pipelining

Adding pipeline stages and registers

- Reducing Vdd.
- However Ceff increases due to more gates.
- And CPI increases due to more pipelines stalls.

There exists a minimum.

## Multi-core parallism

Going from 1 to M cores

Find Tck such that execution time is same as original
Find a new Vdd using FO4.
Try for M=4

Old case. Ceff * V**2 * CPI

Goal: find improvement/new power efficiency


## Specialization

- General purpose microprocessors.
0.1 MOPS/mW
- Digital Signal Processors.
1 MOPS/mW - 10x
- Dedicated hardware (and ultra-low-power micros).
100 MOPS/mW. 10 pJ/op - 100x 

May reach 1pJ order for low-precision neural networks.


## Accelerator types

No standard naming convention. Not so easy to classify.

Broadly

- Instruction mapped. Pass an (complex) instruction to accelerator. Tight coupling.
- Memory mapped.  Loose coupling.

Accelerator can be private to a core, to a thread, or shared among multiple cores.


## European Processor Initiative Acceleration Tile

European Processor Initiative.
120 M EUR project.
26 project partners.

Targeting supercomputer.
Also very high performance needs in automotive cars.

- Multi-core machine.
- Hetrogenous tiles. ARM Cortex, FPGA, vector extension
- 

RISC-V vector extension.

- 32 vector registers
- 64 bit element size. 2x32, 4x16, 8x8 bit
- 8 vector lanes

## Klessendra embedded processor core family

Targeting Embedded applications
Presented at Zurich 2019 RISC-V workshop
Space and avionics.
Sattelites. Fault tolerance.

Compatible with PULPino microcontroller platform.
RI5CY, Zero-, micro-.
Available on Github!

- Klessyndra S0. Verification only.
- Klessyndra T02x and T03x. Multi-threaded
- Klessyndra T13. Parametric, hardware accelerators

Bare metal. Hardware thread support.
Interleaved multithreading.
Every-other instruction is different thread.
Minimum and maximum of threads.
Right now min_thread=3 (from number of pipelines stages).
Max_threads=16
Hart = hardware thread (RISC-V terminology)

32x32-bit integer registers
No floating point.

Interrupts 16x. Compatible with Pulpino.
Software interrupt. Sent by software threads.

### S0
2-stage pipeline.
Single thread execution.

### T0x
Multiple program counters.
One per active threads.


### T13x

Scratchpad memory. Parametrics, default=512 bytes.
Like a cache, but managed by software.
Used for acceleration units.
Instructions for storing/loading from scratchpad.
Instructions for vector/DSP. SIMD.


## Accelerator example

Problem: Edge detection.
Baseline. Compiled to RISC-V integer instructions

Memory mapped accelerator.
Communication with core using shared memory.

Accelerator IP.
Using a state machine.

Actions executed in same clock cycle as state check.
Algorithmic state machine (ASM) diagram.



