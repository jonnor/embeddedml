
import array
import time
import gc


def median_plain(data):
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2

"""
@micropython.viper
def median_viper(data):
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2
"""

@micropython.native
def median_native(data):
    data = sorted(data)
    n = len(data)
    if n % 2 == 1:
        return data[n//2]
    else:
        i = n//2
        return (data[i - 1] + data[i])/2

# FIXME: also compare using list as input
# FIXME: compare float vs integers
# FIXME: also compare a mean/average
# ? or is RMS a better example ?


def test():
    length = 10
    repetitions = 10000

    data = array.array('H', (0 for _ in range(length)))

    FUNCS = {
        'median_plain': median_plain,
        #'median_viper': median_viper,
        'median_native': median_native,
    }

    for name, func in FUNCS.items(): 

        gc.collect()
        start = time.ticks_ms()
        for _ in range(repetitions):
            out = func(data)

        duration = time.ticks_diff(time.ticks_ms(), start)
        print(name, duration)

test()

