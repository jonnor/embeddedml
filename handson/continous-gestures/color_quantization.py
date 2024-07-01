
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
        c0 = vectors[(i*3)+0]
        c1 = vectors[(i*3)+1]
        c2 = vectors[(i*3)+2]

        # perf testing only
        #d = 0

        # euclidean distance
        #d = (v0 - c0)**2 + (v1 - c1)**2 + (v2 - c2)**2

        # euclidean distance written out. Fastest
        d = int(((v0 - c0)*(v0 - c0)) + ((v1 - c1)*(v1 - c1)) + ((v2 - c2)*(v2 - c2)))

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

    print('aa', rows, rowstride)

    for row in range(rows):
        for col in range(rowstride):
            i = 3 * (row*rowstride + col)
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

PALETTE_RAL_CLASSIC = [
'#CDBA88',
'#D0B084',
'#D2AA6D',
'#F9A900',
'#E49E00',
'#CB8F00',
'#E19000',
'#E88C00',
'#AF8050',
'#DDAF28',
'#E3D9C7',
'#DDC49B',
'#E6D2B5',
'#F1DD39',
'#F6A951',
'#FACA31',
'#A48F7A',
'#A08F65',
'#F6B600',
'#F7B500',
'#BA8F4C',
'#FFFF00',
'#A77F0F',
'#FF9C00',
'#E2A300',
'#F99A1D',
'#EB9C52',
'#8F8370',
'#806440',
'#F09200',
'#DA6E00',
'#BA481C',
'#BF3922',
'#F67829',
'#E25304',
'#FF4D08',
'#FFB200',
'#EC6B22',
'#DE5308',
'#D05D29',
'#E26E0F',
'#D5654E',
'#923E25',
'#FC5500',
'#A72920',
'#9B2423',
'#9B2321',
'#861A22',
'#6B1C23',
'#59191F',
'#3E2022',
'#6D342D',
'#782423',
'#C5856D',
'#972E25',
'#CB7375',
'#D8A0A6',
'#A63D30',
'#CA555D',
'#C63F4A',
'#BB1F11',
'#CF6955',
'#FF2D21',
'#FF2A1C',
'#AB273C',
'#CC2C24',
'#A63437',
'#701D24',
'#A53A2E',
'#816183',
'#8D3C4B',
'#C4618C',
'#651E38',
'#76689A',
'#903373',
'#47243C',
'#844C82',
'#9D8692',
'#BB4077',
'#6E6387',
'#6A6B7F',
'#304F6E',
'#0E4C64',
'#00387A',
'#1F3855',
'#191E28',
'#005387',
'#376B8C',
'#2B3A44',
'#215F78',
'#004F7C',
'#1A2B3C',
'#0089B6',
'#193153',
'#637D96',
'#007CAF',
'#005B8C',
'#048B8C',
'#005E83',
'#00414B',
'#007577',
'#222D5A',
'#41698C',
'#6093AC',
'#20697C',
'#0F3052',
'#3C7460',
'#366735',
'#325928',
'#50533C',
'#024442',
'#114232',
'#3C392E',
'#2C3222',
'#36342A',
'#27352A',
'#4D6F39',
'#6B7C59',
'#2F3D3A',
'#7C765A',
'#474135',
'#3D3D36',
'#00694C',
'#587F40',
'#60993B',
'#B9CEAC',
'#37422F',
'#8A9977',
'#3A3327',
'#008351',
'#5E6E3B',
'#005F4E',
'#7EBAB5',
'#315442',
'#006F3D',
'#237F52',
'#45877F',
'#7AADAC',
'#194D25',
'#04574B',
'#008B29',
'#00B51B',
'#B3C43E',
'#7A888E',
'#8C979C',
'#817863',
'#797669',
'#9A9B9B',
'#6B6E6B',
'#766A5E',
'#745F3D',
'#5D6058',
'#585C56',
'#52595D',
'#575D5E',
'#575044',
'#4F5358',
'#383E42',
'#2F3234',
'#4C4A44',
'#808076',
'#45494E',
'#374345',
'#928E85',
'#5B686D',
'#B5B0A1',
'#7F8274',
'#92886F',
'#C5C7C4',
'#979392',
'#7A7B7A',
'#B0B0A9',
'#6B665E',
'#989EA1',
'#8E9291',
'#4F5250',
'#B7B3A8',
'#8D9295',
'#7E868A',
'#C8C8C7',
'#817B73',
'#89693F',
'#9D622B',
'#794D3E',
'#7E4B27',
'#8D4931',
'#70462B',
'#724A25',
'#5A3827',
'#66332B',
'#4A3526',
'#5E2F26',
'#4C2B20',
'#442F29',
'#3D3635',
'#1A1719',
'#A45729',
'#795038',
'#755847',
'#513A2A',
'#7F4031',
'#E9E0D2',
'#D6D5CB',
'#ECECE7',
'#2B2B2C',
'#0E0E10',
'#A1A1A0',
'#868581',
'#F1EDE1',
'#27292B',
'#F8F2E1',
'#F1F1EA',
'#29292A',
'#C8CBC4',
'#858583',
'#787B7A',
]

def hex_to_rgb8(s : str) -> tuple:
    assert s[0] == '#'

    r = int(s[1:3], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return r, g, b

# Load a fixed palette
hh = PALETTE_RAL_CLASSIC
#hh = PALETTE_EGA16_HEX
palette = make_image(1, len(hh))
for i, h in enumerate(hh):
    rgb = hex_to_rgb8(h)
    c = array.array('B', rgb)
    #print(i, rgb, c)
    palette[(i*3):(i*3)+3] = c

#raise Exception()

def quantize_path(inp, outp):
    # https://github.com/jacklinquan/micropython-microbmp
    from microbmp import MicroBMP

    loaded = MicroBMP().load(inp)
    res = (loaded.DIB_w, loaded.DIB_h)
    print('LOADED', res)

    out = MicroBMP(res[0], res[1], 24)

    # Do quantization
    start = time.ticks_us()
    apply_palette(loaded.parray, out.parray, palette, rowstride=res[1])

    dur = (time.ticks_diff(time.ticks_us(), start) / 1000.0)
    print('dur (ms)', dur)

    # Save output
    out.save(outp)

inp = 'IMG_20240626_175314_MP_cifm.bmp'
out = 'quant.bmp'

quantize_path(inp, out)


# TODO: complete fixed palette case
# TODO: test performance on ESP32
# TODO: implement dynamic palettes using k-means++

# https://github.com/robert-ancell/pygif
# works with MicroPython ?
# has write-color table

# https://github.com/sedthh/pyxelate/


