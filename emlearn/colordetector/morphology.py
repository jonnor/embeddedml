
"""

"""

import numpy
import pandas
from scipy.ndimage import binary_erosion

def binary_erode_start(series, size):
    """
    Cut the start of 1 value runs. Is shorter by @size steps
    
    @series should be a binary 1d sequence
    """
    if size == 0:
        return series
    if len(series) == 0:
        return series
    
    # Avoid eroding section starting with 1 at leading edge of input
    mask = numpy.ones(len(series))
    mask[0] = 0
    

    v = binary_erosion(series.values, structure=[1, 1], iterations=size, mask=mask)
    out = pandas.Series(v, index=series.index)
    assert len(out) == len(series)
    return out

def binary_erode_end(series, size):
    """
    Cut the end of 1 value runs. Is shorter by @size steps
    
    @series should be a binary 1d sequence
    """
    if size == 0:
        return series

    inv = numpy.flip(series.values)
    # Avoid eroding section ending with 1 at trailing edge of input
    mask = numpy.ones(len(series))
    mask[0] = 0
    v = binary_erosion(inv, structure=numpy.ones(shape=2), iterations=size, mask=mask)
    mm = numpy.flip(v)
    out = pandas.Series(mm, index=series.index)
    assert len(out) == len(series)
    return out

def binary_erode(series, start=0, end=0):
    """
    Erode a binary sequence, by @start timesteps on leading edges and @end timesteps on trailing edges
    """
    
    s = binary_erode_start(series, size=start)
    s = binary_erode_end(s, size=end)
    return s

