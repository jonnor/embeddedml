
"""
Color quantization
"""

import array
import time

@micropython.native
def argmin_euclidean3(vectors, v0, v1, v2):
    """Find the closest"""

    channels = 3
    #assert len(vectors) % channels == 0, len(vectors)
    elements = int(len(vectors)) // channels

    #print('ee', elements)

    min_idx = 0
    min_value = int(3*(255**2)) # initialize to max
    for i in range(elements):
        c0 = vectors[i+0]
        c1 = vectors[i+1]
        c2 = vectors[i+2]

        d = 0

        # euclidean distance
        # d = (v0 - c0)**2 + (v1 - c1)**2 + (v2 - c2)**2

        # euclidean distance written out. Fastest
        #d = int(((v0 - c0)*(v0 - c0)) + ((v1 - c1)*(v1 - c1)) + ((v2 - c2)*(v2 - c2)))

        # manhattan distance. Slower than Euclidean??
        #d = int(abs(v0 - c0) + abs(v1 - c1) + abs(v2 - c2))

        if d < min_value:
            min_value = d
            min_idx = i

    return min_idx, min_value

def apply_palette(img, quant, palette, rowstride):

    # check palette
    channels = 3
    assert len(palette) % channels == 0, len(palette)
    n_palette = len(palette) // channels
    assert n_palette >= 2
    assert n_palette <= 256

    # check images
    assert len(img) % (channels*rowstride) == 0, len(img)
    assert len(quant) % (channels*rowstride) == 0, len(quant)

    rows = len(img) // (rowstride * 3)
    for row in range(rows):
        for col in range(rowstride):
            i = (row*col*3)
            #rgb = img[i:i+3]
            r = img[i+0]
            g = img[i+1]
            b = img[i+2]
            #continue

            # find closest value in palette
            palette_idx, distance = argmin_euclidean3(palette, r, g, b)

            #palette_idx, distance = 0, 0

            # copy the palette value
            p = palette_idx*3
            quant[i+0] = palette[p+0]
            quant[i+1] = palette[p+1]
            quant[i+2] = palette[p+2]

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

def load_gif(file):

    import gif
    reader = gif.Reader()
    reader.feed (file.read())

    if not reader.has_screen_descriptor():
        raise ValueError('Invalid GIF')

    img = make_image(reader.width, reader.height)

    n_colors = len(reader.color_table)
    print('cc', n_colors)

    for block in reader.blocks:
        if not isinstance (block, gif.Image):
            continue

        p = block.get_pixels()
        print(len(p))

    if reader.has_unknown_block():
        raise('Unknown GIF block')

    if not reader.is_complete():
        raise('Missing trailer in GIF')


# Load a fixed palette
palette = make_image(1, 16)
for i, h in enumerate(PALETTE_EGA16_HEX):
    rgb = hex_to_rgb8(h)
    #print(rgb)
    palette[i:i+3] = array.array('B', rgb)

#print(palette)

RESOLUTION_CIF = (352, 288) # ~100k pixels
res = RESOLUTION_CIF
img = make_image(*res)

quant = make_image(*res)

inp = 'IMG_20240626_175314_MP_cifm.gif'
load_gif(open(inp, 'rb'))

print('LOADED')

start = time.ticks_us()
apply_palette(img, quant, palette, rowstride=res[1])

dur = (time.ticks_diff(time.ticks_us(), start) / 1000.0)
print('dur (ms)', dur)

# TODO: complete fixed palette case
# TODO: test performance on ESP32
# TODO: implement dynamic palettes using k-means++

# https://github.com/robert-ancell/pygif
# works with MicroPython ?
# has write-color table

# https://github.com/sedthh/pyxelate/


