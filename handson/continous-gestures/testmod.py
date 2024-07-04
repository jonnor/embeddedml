import gc
import array
from distance import euclidean_argmin

# Test using the function
print(euclidean_argmin)

vv = array.array('B', [0, 0, 0, 1, 1, 1, 2, 2, 2])
p = array.array('B', [1, 1, 1])

idx, dist = euclidean_argmin(vv, p)
print(idx, dist)
# Works as expected, prints "1 0"

# Do some unrelated things that allocate/free memory
unrelated = array.array('B', (1337 for _ in range(100)))
gc.collect()

PALETTE_EGA16_HEX = [
    '#ffffff',
    '#aa0000',
    '#ff55ff',
    '#ffff55',
]

def hex_to_rgb8(s : str) -> tuple:
    assert s[0] == '#'

    r = int(s[1:3], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return r, g, b

data = []
for h in PALETTE_EGA16_HEX:
    data.append(hex_to_rgb8(h))

# Try using the function in the same way
# Get errors like: 'slice' object isn't callable
# or it just crashes the interpreter
print(euclidean_argmin)
idx, dist = euclidean_argmin(vv, p)
print(idx, dist)
