

- Power revolution
- Computing revolution
- Data revolution
- Programming revolution

What is a revolution?

Mindset of people before vs mindsent of people after. 

Before. Latency centric.
Now. Throughput centric.

Multicore, memory revolution.

Before. ISA abstraction was solid.
Multicore makes ISA abstraction leak?
Have to know architecture details to make efficient application

## Programming model.
High-level interface to re-introduce good abstractions for applications.
So that the application can automatically be portable and make use of hardware improvements.
Uses a (software) runtime under the hood.

## StarSs family

- Sequential task-bsed program
- Single address space
- Directionarlity annotations.
- Specify tasks, inputs, outputs. 
- Executes in parallel

## OpenMP and OmpSs

https://www.bsc.es/research-development/research-areas/programming-models/the-ompss-programming-model
https://pm.bsc.es/ompss


    OmpSs main goal is to act as a forefront and nursery of ideas for
    a data-flow task-based programming model
    so these ideas can ultimately be incorporated in the OpenMP industrial standard.

Both use annotations in the code.

    #pragma omp task in[A][B] inout[C]


In OpenMP threads are visible. Leaky!
Directly specifying a team of threads.
Restrictive.

Recommend not using `thread` based API.

OmpSs does not specify resources used.
Specify constraints only.

## OmpSs-2

Key features.

- Region dependencies (overlapping ares).
Can be expressed in pragmas
- Nesting of tasks. Flattening dependencies across tasks.
Allows to express hierachical programs.
Can exploit "small parallism" (ex N=3) from different levels.
Tasks do not need to know eachother.
Scheduled at runtime.
- Weak dependencies
- MPI and OpenMP interoperability

## Hybrid programming
Combine inter-process with intra-process concurrency.
Many nodes, many processors.
MPI and OpenMP.

