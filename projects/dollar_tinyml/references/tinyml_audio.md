
## FFT tiny

https://www.embedded.com/develop-fft-apps-on-low-power-mcus/
Need 2N 16-bit variables for FFT data
For 256 length FFT, needs 1,024 bytes of RAM
radix-2 is a reasonable base
possible to optimize for real-valued FFT
LUT for cos+sine. Needs 2 x N/2 int16 values, or approx NFFT bytes

arm_rfft_q15 is probably a good starting point for a test

