
"""
Color quantization
"""

import array


def euclidean_distances_3(vectors : array.array, v : array.array, distances : array.array):

    channels = len(v)
    assert len(vectors) % channels == 0, len(vectors)

    elements = len(vectors) // channels

    assert channels == 3, "specialized/unrolled for 3 channels"

    min_idx = 0
    min_value = 0
    for i in range(elements):
        c = vectors[i]
        d = (c[0] - v[0])**2 + (c[1] - v[1])**2 + (c[2] - v[2])**2
        distances[i] = d

    # FIXME: avoid storing the distances


def apply_palette(img, quant, palette, rowstride):

    rows = len(img) // (rowstride * 3)
    for row in 

    pass

def make_image(width, height, channels=3, typecode='B', value=0):
    """Utility to create image stored as 1d buffer/array"""
    
    elements = width * height * channels
    img = array.array(typecode, (value for _ in range(elements)))

    return img

# RAL Standard Color Table
# https://gist.github.com/nichtich/4a8a110a4d3f8f0e2baa593f26d50d9d
# RAL classic color table
# https://gist.github.com/lunohodov/1995178
# EGA 64
# https://en.wikipedia.org/wiki/List_of_8-bit_computer_hardware_graphics
# https://en.wikipedia.org/wiki/List_of_16-bit_computer_color_palettes
PALETTE_EGA16_HEX = [
    '#ffffff',
    '#000000',
    '#0000aa',
    '#00aa00',
    '#00aaaa',
    '#aa0000',
    '#aa00aa',
    '#aa5500',
    '#aaaaaa',
    '#555555',
    '#5555ff',
    '#55ff55',
    '#55ffff',
    '#ff5555',
    '#ff55ff',
    '#ffff55',
]

def hex_to_rgb8(s : str) -> tuple:
    assert s[0] == '#'

    r = int(s[1:3], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return r, g, b

# Load a fixed palette
palette = make_image(1, 16)
for i, h in enumerate(PALETTE_EGA16_HEX):
    rgb = hex_to_rgb8(h)
    print(rgb)
    palette[i:i+3] = array.array('B', rgb)

print(palette)

RESOLUTION_CIF = (352, 288) # ~100k pixels
res = RESOLUTION_CIF
img = make_image(*res)

quant = make_image(*res)

apply_palette(img, quant, palette, rowstride=res[1])

# TODO: complete fixed palette case
# TODO: test performance on ESP32
# TODO: implement dynamic palettes using k-means++

# https://github.com/robert-ancell/pygif
# works with MicroPython ?
# has write-color table

