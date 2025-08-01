
# Benchmarking MicroPython sorting

A recent blogpost by Miguel Ginberg (author of the excellent MicroDot web framework for MicroPython), posted some benchmarks of compute operations on MicroPython.
https://blog.miguelgrinberg.com/post/benchmarking-micropython

It illustrated well how microcontrollers are much slower than PCs.
However, it did not illustrate so well how quickly MicroPython can do these operations.

Below illustrates how to do the same sorting operation (of 2000) numbers
between 100 and 1000x faster, with simple changes to the MicroPython code.

## Experiments

#### [bubble.py](./bubble.py)

Original code by Miguel, unchanged.


#### [bubble_native.py](./bubble_native.py)

- Added micropython.native emitter as function decorator.

#### [bubble_viper.py](./bubble_viper.py)

- Added micropython.native emitter
- Swithed to array.array instead of list
- Used 32bit memoryview with ptr32 
- Type annotation to have int length

#### [heapsort_viper.py](./heapsort_viper.py)

- Switch from bubble sort `O(N**2)` to heapsort `O(n log n)`
- Still using micropython.viper code emitter

WARNING: Hastily made by Claude.
I only did a quick spotcheck that the array does seem to get sorted.

#### dynamic native C module

MicroPython can also use C modules.
This is as an exercise for the reader :)

## Run

```
mpremote run bubble.py
mpremote run bubble_native.py
mpremote run bubble_viper.py
mpremote run heapsort_viper.py
```

## Results

On ESP32S3 (on a M5Stick AtomS3U), running MicroPython 1.24.1.

```
bubble.py                   19.119
bubble_native.py            9.482
bubble_viper.py             0.904
heapsort_viper.py           0.02
```


## References

Maximising MicroPython speed
https://docs.micropython.org/en/latest/reference/speed_python.html

