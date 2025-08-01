
import random
import array
import time

def quicksort_recursive(data):
    n : int = int(len(data))
    quicksort_inner(arr, 0, n-1)

@micropython.viper
def quicksort_inner(data, low : int, high : int):
    arr = ptr32(data)

    if low < high:
       # Partition
       pivot = arr[high]
       i = low - 1
       
       for j in range(low, high):
           if arr[j] <= pivot:
               i += 1
               arr[i], arr[j] = arr[j], arr[i]
       
       arr[i + 1], arr[high] = arr[high], arr[i + 1]
       pi = i + 1
       
       # Recursive calls
       quicksort_inner(arr, low, pi - 1)
       quicksort_inner(arr, pi + 1, high)



if hasattr(time, 'ticks_us'):
    def t():
        return time.ticks_us() / 1000000
else:
    def t():
        return time.time()


random.seed()
arr = array.array('L', [random.getrandbits(10) for _ in range(100)])
quicksort_recursive(arr)  # warm up
arr = array.array('L', [random.getrandbits(10) for _ in range(2000)])
s = t()
quicksort_recursive(arr)
e = t()
print(int((e - s) * 1000) / 1000)
#print(arr)
