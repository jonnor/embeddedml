
## Origins
- 1984.  European Center for Parellism.
- 2004. Spanish National Lab for Supercomputing

BCN-CNS

- Supercomputing services to Spanish and EU researches
- RnD in computer, Life, Earth and Engineering Sciences
- Phd programme. 100 Phds
- 2019=600 employees.

Departments

- Computer Sciences
- Earth Sciences
- Life Sciences. Personalised medicine
- CASE. Engineering SW

Supercomputer

- MareNostrum1. 2004. First commodity hardware and Linux supercomputer.
- MareNostrum2, MareNostrum3.
- MareNostrum4. 11 petaflops CPU.

- Yearly summerschool on CUDA. 90+ students.
- CSRankings. UPC. Several top rankings.
Computer Architecture. 1 in Eyrope, 3 in the world since 1980.

## ACM
Oldest and largest computer science organisation.

ACM Europe.
Running summerschools.
Data Science.

ACM Europe Conference 2017.

# Past, Present, Future of Computer Architecture
Mateo Valero.

Superscalar processors.
Instructino Set Architecture.
Pipeline. Inspired by car manufacturing.
Problem: Conditionsals. Branches.
Don't know what execution path will be taken.
Branch predictors. 
Execute out-of-order.
Decode in-order. Commit in-order.
Latency hiding.
Often waiting for LOADs.

### Contributions by UPC

Memory wall

- Kilo Instructinon Processor.
- Virtual-Physical registers. Using virtual instead of physical registers for in-flight instructions.
- Distant Parallelism. Had to fight current dogma: Never add instructions (to ISA).

Power wall

- Direct Wakeup. Pointer-based instruction queue design.
- Content-aware register file.
- Fuzzy computation.
Dynamic adaptation of bitwidth in hardware.
Now known as Approximate Computing (HPC) / Reduced Precision (ML)

Symmetric Multithreading

- Dymically Controlled Resource Allocation.
- Quality of Service in SMTs
- Runahead threads for SMT

Statically scheduled VLIW architecture.
Intel Itanium project. Failed.
Needed to change the compiler.
Relevant for Embedded.

Vector Architectures. Memory latency and power.
Statement: All high performance CPUs will be vector-based. 1998.
Today (2018) this is true. Short-vectors (SIMD).
Cross-pollination between superscalar and vector processor research.

New instructions for specific use-cases.

Multi-core era.
Unable to utilize efficiently the transistors added. Moores-law.
Challenge: Programming (heterogenous) multi-core systems.
Single-execution-path.
OmpSs. Data-flow execution of sequaltial programs.
Using OMP annotations to specify dependencies.
Compiler or hardware can rewrite the execution.
OmpSs was forerunner OpenMP. OMP3.0, 4.0, 5.0 etc 
PyCOMPS : OmpSs for Python.
Talk by Jesus Labarta.

Hundreds of papers on cache. WHY?
Cause no information in hardware about the software/problem needs.

### Present
- Runtime-aware architures.
Application -> Runtime -> Hardware.
- Superscalar vision at Multicore level.

### Future
New Golden age.

- Domain-specific L and architectures.
- Open software and open hardware. Low barriers.
- Security. !! Speculation. Need to undo predictions

HW-SW codesign. Neural Networks. Pruning. Compression.
Non-volatile mermories.
NVM cheaper than RAM.

Quantum computing??? So many promises...

### Machine Learning
Applied to hardware design. To software design.
To optimize archtiectures, programs...

In Europe we are not so good at computers.
Compared to US, China, Japan.
ARM was result of EU projects.
But ARM has been sold to Softbank!
But we should have our own processors.

BSC working since 2011 on ARM for supercomputer.
Software stack making ready for when performance .

Need the Linux project for the CPU!
Open Source hardware.
RISC-V.
Exascale supercomputing initiative.
"Join us!". Hiring 30 people.
7nm initial target.

How to do it?
Dan Brown Origin written about MareNostrum.
Next one will go into Sagrada Familia.
3 euros extra ticket to visit.
