import random
import array
import time

if hasattr(time, 'ticks_us'):
    def t():
        return time.ticks_us() / 1000000
else:
    def t():
        return time.time()

# The Viper emitter compiles down to native code, making use of type hints
@micropython.viper
def bubble_sort(data):
    arr = ptr32(data)
    n : int = int(len(data))
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]


random.seed()
arr = array.array('L', [random.getrandbits(10) for _ in range(100)])
bubble_sort(arr)  # warm up
arr = array.array('L', [random.getrandbits(10) for _ in range(2000)])
s = t()
bubble_sort(arr)
e = t()
print(int((e - s) * 1000) / 1000)
