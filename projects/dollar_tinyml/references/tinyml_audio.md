
## FFT tiny

https://www.embedded.com/develop-fft-apps-on-low-power-mcus/
Need 2N 16-bit variables for FFT data
For 256 length FFT, needs 1,024 bytes of RAM
radix-2 is a reasonable base
possible to optimize for real-valued FFT
LUT for cos+sine. Needs 2 x N/2 int16 values, or approx NFFT bytes

arm_rfft_q15 is probably a good starting point for a test

Existing tests of arm_rfft_q15
https://m0agx.eu/practical-fft-on-microcontrollers-using-cmsis-dsp.html

Used a Cortex-M3
FFT size: 256, CPU cycles to do the FFT: 31919
Was able to process 8 kHz signal with 2% CPU, on 48 Mhz chip

Probably slower on ARM Cortex M0 grade hardware.
But sounds like it could be doable in under 20% CPU on 24 Mhz RISC-V/CortexM0

