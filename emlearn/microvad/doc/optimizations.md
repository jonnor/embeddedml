
## Companding

The primary part of RAM usage is the storage of audio data.
When stored as int16, there is 16 bits per sample.
Using companding with A-law/mu-law is one way of getting this down to 8 bits per sample.
This can potentially halve the required RAM for audio samples, albeit at a degradation in quality.
It would also require smaller integer operations.
Advantage on 8-bit architectures (ex: AVR8), or it if enables SIMD (ex: NEON for ARM Cortex).
It might be possible to operate directly on such.

Definition is based on a logarithm. But there exists approximations which do not use this:
https://www.dspguide.com/ch22/5.htm
A typical scheme is to approximate the logarithmic curve with a group of 16 straight segments, called cords.
The first bit of the 8 bit output indicates if the input is positive or negative.
The next three bits identify which of the 8 positive or 8 negative cords is used.
The last four bits break each cord into 16 equally spaced increments.

The piecewise linear is also described in 
"Texas Instruments SPRA163A: A-Law and mu-Law Companding Implementations Using the TMS320C54x"


https://jonathanhays.me/2018/11/14/mu-law-and-a-law-compression-tutorial/
shows conversions using look up table.
Generally requires 256 bytes for encode and same for decode,
however A-law is done with 128 bytes.

https://www.dsprelated.com/showthread/speechcoding/73-1.php
shows an approach using 8 entry short / 16 bytes lookup.
THe likely source is linear2alaw in g711.c from G711 implementation by Sun Microsystems.
https://github.com/escrichov/G711/blob/master/g711.c
Which appears to be under a public domain license
