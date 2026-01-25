
## Coarse-Grain Reconfigurable Arrays (CGRAs)

CGRAs comprise a 2D array of processing elements (PEs), tightly integrated to execute arithmetic and logic operations, offering strong programmability with ASIC-like performance
Each PE is typically equipped with a register file, an arithmetic logic unit, and local memory interfaces. CGRA topologies vary, encompassing mesh, ring, bus, and NoC-based interconnects.

Can theoretically effectively accelerate loops with low parallelism.

Efficient mapping of loops or dataflow graphs (DFG) onto CGRA fabrics is combinatorially challenging.
Modulo scheduling.

CGRAs support both spatial and time-multiplexed execution.


## CGRA on TinyTapeout

## TT07 480 : Mini AIE: 2x2 CGRA with Ring-NoC

https://www.tinytapeout.com/chips/tt07/tt_um_mini_aie_2x2
https://github.com/vrteee/tt07-mini-aie-cgra

The design draws inspiration from the architecture of Versal ACAP Versal AI Engine architecture.

? No details on the instruction set. Nor the operations supported

## CGRA compiler


### Evaluation of CGRA Toolchains
https://arxiv.org/abs/2502.19114
February 2025.

Compared CGRA-Flow, Morpher, CGRA-ME, Pillars
Benchmarked GEMM, ATAX, GESUMMV, MVT, TRISOLV from the Polybench suite

> Several CGRA toolchains do not accept as input a multidimensional loop nest directly,
> but require flattening

Morpher did the best.

## CGRA design software

### Versat - compiler that transforms a high-level specification into a custom CGRA
https://github.com/IObundle/iob-versat

Integrated into [iob-soc](https://github.com/IObundle/iob-soc)
IOb-SoC is a System-on-Chip (SoC) described in Python, using the Py2HWSW framework.
VexRiscv CPU.

### garnet - Next generation CGRA generator 
https://github.com/StanfordAHA/garnet

### VectorCGRA - CGRA framework with vectorization support
https://github.com/tancheng/VectorCGRA

Generates Verilog.

### CGRA-ME 2.0 - modelling and exploring coarse-grained reconfigurable architectures and CAD
https://cgra-me.ece.utoronto.ca/

Uses C++ for specification.

## Instruction sets

### PEak
PEak is a python-embedded DSL that describes a PE's instruction set architecture (ISA) as well as its functional model.

PEak: A Single Source of Truth for Hardware Design and Verification.
https://arxiv.org/abs/2308.13106


## References

https://labs.engineering.asu.edu/mps-lab/research/coarse-grained-reconfigurable-arrays/

https://aha.stanford.edu/research/cgra-architecture-and-tools

### Introduction to CGRA Accelerators

https://www.youtube.com/watch?v=4h2Po78be-Q

- Operating principle
- How CGRA executes loops illustrated

### Democratizing Coarse Grained Reconfigurable Arrays by Cheng Tan 
https://www.youtube.com/watch?v=1P17ERtNQCU

Designing CGRA for particular application is large hardware+software engineering effort.
Tool for exploring different architecture options.
Cycle level modelling. Register Transfer Level modelling.
Evaluate wrt area budget, power budget.

###  SNAFU: An Ultra-low-power, Energy-Minimal CGRA Generation Framework and Architecture 
https://www.youtube.com/watch?v=vaFeXqoIG6o

! code not available?
