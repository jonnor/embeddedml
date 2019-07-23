
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

