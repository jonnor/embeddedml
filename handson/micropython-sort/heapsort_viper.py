
import random
import array
import time

if hasattr(time, 'ticks_us'):
    def t():
        return time.ticks_us() / 1000000
else:
    def t():
        return time.time()

@micropython.viper
def heapsort(data):
   n : int = int(len(data))
   arr = ptr32(data)

   # Build max heap
   for i in range(n//2 - 1, -1, -1):
       # Heapify iteratively
       parent = i
       while True:
           largest = parent
           left = 2 * parent + 1
           right = 2 * parent + 2
           
           if left < n and arr[left] > arr[largest]:
               largest = left
           if right < n and arr[right] > arr[largest]:
               largest = right
               
           if largest == parent:
               break
           
           # Swap
           arr[parent], arr[largest] = arr[largest], arr[parent]
           parent = largest
   
   # Extract elements from heap
   for i in range(n - 1, 0, -1):
       # Swap root with last element
       arr[0], arr[i] = arr[i], arr[0]
       
       # Heapify root iteratively
       parent = 0
       while True:
           largest = parent
           left = 2 * parent + 1
           right = 2 * parent + 2
           
           if left < i and arr[left] > arr[largest]:
               largest = left
           if right < i and arr[right] > arr[largest]:
               largest = right
               
           if largest == parent:
               break
           
           arr[parent], arr[largest] = arr[largest], arr[parent]
           parent = largest



random.seed()
arr = array.array('L', [random.getrandbits(10) for _ in range(100)])
heapsort(arr)  # warm up
arr = array.array('L', [random.getrandbits(10) for _ in range(2000)])
s = t()
heapsort(arr)
e = t()
print(int((e - s) * 1000) / 1000)
#print(arr)
