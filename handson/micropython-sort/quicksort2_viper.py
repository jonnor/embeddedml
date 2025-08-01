
import random
import array
import time

def quicksort(arr):
    n : int = int(len(arr))
    if n <= 1:
        return

    # Preallocate stack with max depth needed
    # Worst case depth is n, but typically much less
    stack = array.array('i', [0] * (n * 2))  # pairs of (low, high)

    quicksort_inner(arr, stack, n)

@micropython.viper
def quicksort_inner(data, dstack, n : int):

    arr = ptr32(data)
    stack = ptr32(dstack)

    stack_top = 0
    
    # Push initial range
    stack[stack_top] = 0
    stack[stack_top + 1] = n - 1
    stack_top += 2
    
    while stack_top > 0:
        # Pop
        stack_top -= 2
        low = stack[stack_top]
        high = stack[stack_top + 1]
        
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
            
            # Push sub-arrays to stack
            stack[stack_top] = low
            stack[stack_top + 1] = pi - 1
            stack_top += 2
            
            stack[stack_top] = pi + 1
            stack[stack_top + 1] = high
            stack_top += 2

if hasattr(time, 'ticks_us'):
    def t():
        return time.ticks_us() / 1000000
else:
    def t():
        return time.time()


random.seed()
arr = array.array('L', [random.getrandbits(10) for _ in range(100)])
quicksort(arr)  # warm up
arr = array.array('L', [random.getrandbits(10) for _ in range(2000)])
s = t()
quicksort(arr)
e = t()
print(int((e - s) * 1000) / 1000)
#print(arr)
