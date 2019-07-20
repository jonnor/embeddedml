
# Cache and Memory Compression Techniques
July 19.
Per Stenstrom.

Studying memory systems within microprocessors since 1980s.
Wanted to do thesis on cache coherence protocols.
Around 20 years ago started to research compression in memory hierarcies.

L1/L2/L3 cache hierarchy.
L3 shared among multiple cores.
Want L3 to be as big as possible.
To avoid DRAM.
50% of CPU transistor budget typically used for L3.

Compression can improve utilization of cache and DRAM.

Compression is used everywhere. In storage & communication. Media.
Problem: Lossy, domain-specific. Requires sequential access. Relatively slow.
Must: Be lossless. Fast and energy-efficient. Area-efficient. Random-access.
! research topic. Compute directly on compressed data. Without decompressing.

Literature.
"A primer on Compression in the Memory Hierarchy"
Morgan & Claypool.

### Outline

- Compression algorithms
- Cache compression
- Memory compression
- Link (bandwidth) compression

Full

### Locality

Key property that makes memory hierarchies

Reference locality

- Temporal locality. Likely to access an address again
- Spatial locality. Likely to access nearby addresses

Value locality. Less commonly applied!

- Temporal. Likely to use a value multiple times
- Sptial. Likely to access similar values

### Value-aware cache

Observation: Values in cache are not uniformly distributed.

Theoretical idea. Cache that only stores a certain value once.
Motivational data study. 'a case for value-aware cache'
MKPI. Misses per 1k instructions. Want to minimize.

Theoretical result: Same MKPI with 1/16x the cache size.
In practice still at 2-3x.

Challenge:

- Now need many-to-one mapping between address and data.
- Metadata storage blows up, reduces possible gain

### Compression Algorithm Taxonomy

- General purpose vs special purpose.
- Temporal-value vs spatial-Value based
- Static vs dynamic.
If encoding changes during execution of program

Ex special-purpose.
Instruction compression, floating-point compression

### Run-length encoding

Typically combined with other approaches.
For example dictionary-based.

### Lempel-Zip (LZ)
gzip

Dictionary based.
Entry for longest unique substrings encountered.

Tried by IBM. MXT technology.

### Huffman coding

Assign shorter codes to more common symbols.
Built using a tree.

Used in "SC2 statistcal compresec caches" paper.

VFT. Value Frequency Table.

Only put things in hardware that happends often.
Rare can be done in software.

Compressor was OK fast.
Lookup in table via hashing.
Decompression was more challening.
Eventually got 64-byte block in 10 cycles on 4Ghz,32nm.
3-stage pipeline.

L2 cache hit typical 4-5 cycles.
L3 cache around 10 cycles.
Decompression must in the 10 cycle ballpark.

!! are compression techniques used in embedded?
FLASH size dominates costs...


### Base-Delta Immediate (BDI)

Store deltas to one or more base values.
Based on findings of clusters of values in caches.

Using 0 as base. And the first-nonzero value as second base.
Just compressing 0 can get 20% improvement.
Small integers also very common.

BDI in hardware very simple.
Compress: Subtract base value.
Decompress: Add base value.
Can be done in parallell.

### Frequent Pattern Compression (FPC)

Go after common patterns.
0 values, narrow integers.
3-bit prefis codes.
000-ZZZ zero run
001-SSS
110-RRR repeated bytes
111-    uncompressed

### C-PACK (Cache Packer)

Combines pattern-based with dictionary.
2-bit prefix codes.

### Deduplication

- Can be used at coarse level. Blocks, pages

Easy with read-only data.
For writes need Copy-on-Write.


### Floating-point compression

Challenge: Multiple pieces `sign,exponent,mantissa`
`FP-H`. Huffman applied to exponent and mantissa.

HyComp. 
Predicting the datatype of a block in cache. 85% or more.
Classify word as pointer, floating-point, etc..
Combining 4 different compression techniques.
Pointers. BDI.

### Metrics

- Compresison ratio.
- Latency of comp/decomp units.
- Bandwidth of comp/decomp units. ! Must match memory bandwidth
- Energy consumption
- Chip area
- Security

### Cache compaction

Once block is compressed it is not of the block size anymore.
Variable size. Fragmentation problem.

Cache compaction is task to reduce fragmentation.
Half-block. Sub-block. Byte.
Superblock. Common tag for 2/4 consecutive blocks.

Taxonomy.
! good thing with taxonomies. Put existing work into taxonomy. Open areas are candidates for new research.
Flynn. MISD.
Did not make sense for a long time?
But might make sense now in ML. Multiple operands on single data.
Technique: Systolic array, Systolic Execution

### Adaptive cacha managemnts

If `avoided_miss * miss_penalty > penalized_hits * decompression_latency`
then compress cache blocks.
Alamelden,Wood: Estimate `avoided_miss` using LRU stack.

### Case study, SC2

Semi-dynamic Huffman.

1. Aquire statistics. Analyze.
2. Perform compression

Step 1. Assess potential.

How often to re-fetch statistics?
Approx every 1 second.
Does not seem to be much benefit to do it more often.

Rule of thumb.
Double size of cache.
miss rate go down by sqrt(2)

Larger physical cache can be slower! Becaue latency for hit get higher.
SC2 outperforms using a bigger cache.
10% performance increase mixed loads.
50% less energy than 4x cache size increase.


### Memory compressions

30% of server costs is memory.
Similar for mobile phones.

Swap-space compression.
Established in most operating systems.
Even with software compression can be worthwhile.
But swap is not much used, so limited gain.

Want to compress the entire memory.
Should be transparent to OS. Easier adoption.
Do it in the hardware.

Pages have variable size.
Virtual to physical address translation not enough. Need another layer.
Got order of 100 cycles.

NVM.
Non-volatile data almost as fast as DRAM.
Factor 10x.
Might change how operating system are built.
Especially paging mechanism.
Cost of disk VS memory changed.

Lempel-Ziv hard to get fast.

### Link compression
Between main memory and cache hierarchy.
Systems are bandwidth constrainted.


MemZip. HPCA 2014
In-place compression. Avoids extra translation to find compressed blocks.

CRAM: Efficient Hardware-Based Memory Compression for Bandwidth Enhancement
https://arxiv.org/abs/1807.07685
Average speedup 6%.

### ZeroPoint
https://wp.zptcorp.com/

Misson: Embrace memory compression
Business perspective:
Need a product which interfaces easily with customer projects. 

Ziptillion IP block.
Sits between memory controller and processor.
Propriatary compression algorithm.
Software side.
Statistical data analysis in sofware driver.
Able to double memory capacity and bandwidth.

Go to market phase.
Ready Q4 this year.
Ship products next year.
12 people team.
Grown over 4 years.

A research presentation is basically marketing why your research are important.


# Own findings

## Microcontroller compression

https://blog.segger.com/smash-an-efficient-compression-algorithm-for-microcontrollers/
explains DEFLATE, LZMA, LZJU90, LZ4
introduces SMASH.
Can be used for decompression of constants and code copied to RAM during startup.
Also in emCompress, general purpose compression for embedded.

#### Neural network compression?

How much to gain from compression (quantizied) weight?
Zero-value compression should fit well with sparse matrices.

Challenge: Need weights fast during compute.
Good: predictable access. Can be prefetched.

## Z4
https://lz4.github.io/lz4/

- Compression speed > 500 MB/s per core (>0.15 Bytes/cycle). 
- Decoder, with speed in multiple GB/s per core (~1 Byte/cycle)
- LZ4_HC. Trading customizable CPU time for compression ratio
- BSD license.
- Tons of ports to different languages. Incl x86 assembler

Can it be implemented in hardware?

Xilinx FPGA LZ4
https://github.com/Xilinx/Applications/tree/master/data_compression/xil_lz4

LZ4m: A Fast Compression Algorithm for In-Memory Data
http://csl.skku.edu/papers/icce17.pdf
Optimized for small block sizes.
Maximal offset is 270. LZ4 is 65535. 

Design of Hardware Accelerator for Lempel-Ziv 4 (LZ4) Compression
https://doi.org/10.1587/elex.14.20170399

Accelerator is verified using FPGA and fabricated using 65nm CMOS technology.

- Supports up to 4Gbit/s compression with 75MHz clock
- 392 K gate counts
- Compression ratio is measured up to 2.69

Data Compression Device based on Modified LZ4 Algorithm
https://doi.org/10.1109/TCE.2018.2810480

nicknamed MLZ4

high throughput
of up to 1.92Gbps with a compression ratio of up to 2.05.
On 260MHz FPGA.
