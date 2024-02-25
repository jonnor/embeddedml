
# Sound Event Detection

## Applications

Noise Monitoring
Counting cars
Counting beans cracking. LINK Roest
Voice Activity Detection
Brewing counting detection. Stack 3 frames. Maybe bandpass filter.
Audience clapping detection.

Related tasks
Keyword Spotting
Speech Command


## general overheads
!! py32f template uses lots of RAM?
2280 bytes by default with HAL
1760 bytes with LL

[jon@jon-thinkpad py32f0-template]$ arm-none-eabi-size -A Build/app.elf 
Build/app.elf  :
section               size        addr
.ram_vector            192   536870912
.isr_vector            192   134217728
.text                 6808   134217920
.rodata                140   134224728
.init_array              4   134224868
.fini_array              4   134224872
.data                  104   536871104
.bss                   444   536871208
._user_heap_stack     1540   536871652

.bss, .data and .ram_vector go into RAM. Total of 740 bytes

_user_heap_stack represents left over space. Actually not used?

avr-nm -Crtd --size-sort the_program.elf | grep -i ' [dbv] '

[jon@jon-thinkpad py32f0-template]$ arm-none-eabi-nm -td -r --size-sort Build/app.elf | grep ' B '
00000312 B __sf
00000076 B DebugUartHandle
00000004 B uwTick
00000004 B __stdio_exit_handler
00000004 B __malloc_sbrk_start
00000004 B __malloc_free_list
00000004 B errno

__sf is for printf support, it has stdout/stderr/stdin I think

Seems prudent to budget at least 1 kB RAM to system things

## Feature extraction: Spectrograms

ARM CMSIS

4kB RAM total. 1 kB RAM for feature extraction?

Audio buffer
FFT working buffers
Output buffer


## Kilobyte sized Neural Networks

Proven: RNNs

Unproven: DCT + MLP
Unproven: MLP frame-wise + MLP across frames

4 kB RAM total.
1-2 kB RAM for ML model


CMSIS-NN supports LSTM, but not GRU

FIXME: add issue in emlearn for recurrent support, LINK here 
