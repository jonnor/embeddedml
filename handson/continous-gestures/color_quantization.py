
"""
Color quantization
"""

import array
import time
import os

#print('os', os.uname())

from distance import euclidean_argmin
print('ff0', euclidean_argmin)

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

    print('aa', rows, rowstride)

    for row in range(rows):
        for col in range(rowstride):
            i = 3 * (row*rowstride + col)
            rgb = array.array('B', img[i:i+3])

            # find closest value in palette
            #print('p', palette)
            #print('p', rgb)
            assert len(rgb) == 3
            palette_idx, distance = euclidean_argmin(palette, rgb)

            #palette_idx, distance = 0, 0
    
            # copy the palette value
            p = palette_idx*3

            #print(palette_idx, distance, p, (r,g,b), tuple(palette[p:p+3]))

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


def sample_pixels(img, samples, n, channels=3):
    import random

    assert (len(samples) // channels) >= n, len(samples)
    elements = len(img) // channels

    for i in range(n):
        e = random.randint(0, elements)
        samples[i*channels:(i+1)*channels] = img[e*channels:(e+1)*channels]

@micropython.native
def kmeans_cluster(values, centroids, channels=3, max_iter=10, stop_changes=0):
    """
    Perform K-Means clustering of @values

    Uses the @centroid as initial values.
    NOTE: will mutate @centroids
    """

    # https://reasonabledeviations.com/2019/10/02/k-means-in-cpp/

    n_clusters = len(centroids) // channels
    n_samples = len(values) // channels

    assert channels == 3, 'only support 3 channels for now'

    assert channels < 255, channels
    assert n_clusters < 255, n_clusters
    assert n_samples < 65535, n_samples

    assignments = array.array('B', (255 for _ in range(n_samples)))
    cluster_sums = array.array('L', (0 for _ in range(n_clusters*channels)))
    cluster_counts = array.array('H', (0 for _ in range(n_clusters)))

    for i in range(max_iter):

        ## update sample assignments
        changes = 0
        for s in range(n_samples):
            v = values[(s*channels)+0:(s*channels)+3]
            #v0 = values[(s*channels)+0]
            #v1 = values[(s*channels)+1]
            #v2 = values[(s*channels)+2]

            idx, dist = euclidean_argmin(centroids, v)
            #idx, dist = 0, 0

            if idx != assignments[s]:
                changes += 1            
            assignments[s] = idx

        print('iter', i, changes)
        if changes <= stop_changes:
            break

        ## update cluster centroids
        # reset old values
        for c in range(n_clusters*channels):
            cluster_sums[c] = 0
        for c in range(n_clusters):
            cluster_counts[c] = 0

        # evaluate samples
        for s in range(n_samples):
            c = assignments[s]
            v0 = values[(s*channels)+0]
            v1 = values[(s*channels)+1]
            v2 = values[(s*channels)+2]            

            cluster_sums[(c*channels)+0] += v0
            cluster_sums[(c*channels)+1] += v1
            cluster_sums[(c*channels)+2] += v2
            cluster_counts[c] += 1

        # set new centroid means
        for c in range(n_clusters):
            count = cluster_counts[c]
            if count == 0:
                continue

            centroids[(c*channels)+0] = cluster_sums[(c*channels)+0] // count
            centroids[(c*channels)+1] = cluster_sums[(c*channels)+1] // count
            centroids[(c*channels)+2] = cluster_sums[(c*channels)+2] // count

        #yield assignments
        # TODO: make this into a generator? so other work can be done in between
        

    return assignments


def quantize_path(inp, outp, palette):
    # https://github.com/jacklinquan/micropython-microbmp
    from microbmp import MicroBMP

    loaded = MicroBMP().load(inp)
    res = (loaded.DIB_w, loaded.DIB_h)
    print('LOADED', res)

    out = MicroBMP(res[0], res[1], 24)

    # Sample some pixels
    n_samples = 100
    samples = make_image(1, n_samples)

    start = time.ticks_us()
    sample_pixels(loaded.parray, samples, n=n_samples)
    dur = (time.ticks_diff(time.ticks_us(), start) / 1000.0)
    print('sample duration (ms)', dur)

    # Learn a palette
    start = time.ticks_us()
    kmeans_cluster(samples, palette, max_iter=20)
    dur = (time.ticks_diff(time.ticks_us(), start) / 1000.0)
    print('cluster duration (ms)', dur)

    for i in range(len(palette)//3):
        print(palette[(i*3):(i*3)+3])

    # Apply palette
    start = time.ticks_us()
    apply_palette(loaded.parray, out.parray, palette, rowstride=res[1])

    dur = (time.ticks_diff(time.ticks_us(), start) / 1000.0)
    print('apply palette duration (ms)', dur)

    # Save output
    out.save(outp)

#import machine
#machine.freq(240000000)

inp = 'IMG_20240626_175314_MP_cifm.bmp'
out = 'quant.bmp'

# Load a fixed palette
#hh = PALETTE_RAL_CLASSIC
hh = PALETTE_EGA16_HEX
palette = make_image(1, len(hh))
for i, h in enumerate(hh):
    rgb = hex_to_rgb8(h)
    c = array.array('B', rgb)
    #print(i, rgb, c)
    palette[(i*3):(i*3)+3] = c

quantize_path(inp, out, palette)

# TODO: implement dynamic palettes using k-means++

# https://github.com/robert-ancell/pygif
# works with MicroPython ?
# has write-color table

# https://github.com/sedthh/pyxelate/


