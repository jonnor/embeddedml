
## Smallest footprint
Have example of simple CNN for MNIST that runs on Arduino Uno (Atmega328), with `<2 kB` RAM.
Uses int8 computations. Takes around 50 ms per instance.

```
mnist: 28x28x1 input,4->8->16, pad valid
mnist_q_valid.h 2.4KB Flash 1.4KB RAM
suit for MCU have >=16KB Flash, >=2KB RAM
```

A Cortex M0 ran this in 23 ms.

Provides extensive benchmarks.
https://github.com/sipeed/TinyMaix/blob/main/benchmark.md

## Porting
Have a porting guide, standard process for including new port.
Have port to ESP32-S3 - BUT not using any of the DSP instructions.
Could to a port to Puya PY32? Run the MNIST CNN that is designed for Arduino.

## How it works

#### Configuring
Switching between quantiziation/data types.
? using a preprocessor define
A `tm_port.h` file is expected to set appropriate defines.

#### Model definition.
Has its own "tmdl" files.
Seems to be a direct definition of the C structs for different layers/operations.
Likely non-portable (architecure/compiler/port/settings specific). 
Has tools to convert tflite and keras h5 files to this format.

Constructs a model at runtime using `tm_load()`.
Function does just very basic checks on the file.
Majority of code is done during `tm_run`, which "interprets" the files layer by layer.

Uses malloc/free during `tm_load`, optionally. Can pass static buffer instead. Excellent!
Are used via tm_malloc / tm_free defines. Can be re-defined. Great!

#### Preprocessing

Supports a preprocessing pass.
? Baked into the model
using tm_preprocess

## Usage

#### Installing

Not installable as a Python package.
Have to use a git submodule?

Tools require
`"tensorflow-cpu<2.14.1"`
pillow

There are command line tools implemented in Python in tools/
? no instructions on how to use them

Some CI tests in examples/auto_test

Non-quantized FP32
    cmd="cd ../../tools/ && python3 h5_to_tflite.py h5/mnist_valid.h5 tflite/mnist_valid_f.tflite 0
        && python3 tflite2tmdl.py tflite/mnist_valid_f.tflite tmdl/mnist_valid_f.tmdl fp32 1 28,28,1 10"

    cmd="cd ../mnist &&
        sed -i 's/#define TM_MDL_TYPE     TM_MDL_INT8/#define TM_MDL_TYPE     TM_MDL_FP32/g' ../../include/tm_port.h &&
        rm -rf build && mkdir build && cd build && cmake .. && make && ./mnist"

Quantized version, INT8

    cmd="cd ../../tools/ && python3 h5_to_tflite.py h5/mnist_valid.h5 tflite/mnist_valid_q.tflite 1 quant_img_mnist/ 0to1
        && python3 tflite2tmdl.py tflite/mnist_valid_q.tflite tmdl/mnist_valid_q.tmdl int8 1 28,28,1 10"

    cmd="cd ../mnist && sed -i 's/#define TM_MDL_TYPE     TM_MDL_FP32/#define TM_MDL_TYPE     TM_MDL_INT8/g' ../../include/tm_port.h
        && rm -rf build && mkdir build && cd build && cmake .. && make && ./mnist"

There are warnings regarding TF1 compat

```
This API was designed for TensorFlow v1. See https://www.tensorflow.org/guide/migrate for instructions on how to migrate your code to TensorFlow v2.
```

```
  File "/home/jon/projects/embeddedml/handson/tinymaix-models/TinyMaix/tools/tflite2tmdl.py", line 24, in <module>
    from tflite_reader import read_tflite
  File "/home/jon/projects/embeddedml/handson/tinymaix-models/TinyMaix/tools/tflite_reader.py", line 25, in <module>
    from keras.utils import np_utils
ImportError: cannot import name 'np_utils' from 'keras.utils' (/home/jon/projects/embeddedml/handson/tinymaix-models/venv/lib/python3.11/site-packages/keras/utils/__init__.py)
```


