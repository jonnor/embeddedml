
# Efficient signal processing with MicroPython and emlearn

Would be nice to write a bit about 
Maybe a blog-post

## Motivation

Demonstrate that MicroPython can be used for intensive computations,
and give insights into how.
Advertise emlearn FFT and emlearn IIR.
And of course emlearn also classifiers.

## Keywords

Numerical computations.
Digital Signal Processing.
Machine Learning.

### Compare the various approaches

- Python. Reducing allocations. Arrays over lists.
- Viper emitter
- Native emitter
- C extensions. ulab, emlearn

### Existing resources

Refer to existing resources

- Maximising MicroPython speed
https://docs.micropython.org/en/latest/reference/speed_python.html
- Writing fast and efficient MicroPython, PyCON AU 2028
https://www.youtube.com/watch?v=hHec4qL00x0


### Assembly emitters

Viper features and limitations.
https://docs.micropython.org/en/v1.9.3/pyboard/reference/speed_python.html#the-viper-code-emitter
!! does not have an example for numeric code or arrays
Just saying "must implement buffer protocol"

### Usecases

Show a few typical usecases.

- Audio processing
- Vibration analysis
- Image processing

Some concrete examples

- rgb2y
- RMS
- A-weigthing using IIR/sosfilt
- Mels/Octave-band estimation using FFT


