
import pandas


def rms(x, axis=None):
    from numpy import sqrt, mean
    return sqrt(mean(x**2, axis=axis))

def vector_magnitude(vectors, axis=None):
    """Compute the magnitude of multi-dimensional vectors"""
    # alternative is numpy.linalg.norm(vectors)
    mag = numpy.linalg.norm(vectors, axis=axis)
    return mag

def resample(df, freq='1min', func='mean', group='filename', time='time', numeric_only=True):
    grouped = df.reset_index().set_index(time).groupby(group, observed=True).resample(freq)
    out = grouped.agg(func, numeric_only=numeric_only).reset_index().set_index([group, time])
    return out

def normalize(df, agg='max', group='filename', numeric_only=True):
    df = df.copy()
    grouped = df.groupby(group, as_index=False, observed=True)
    agg_grouped = df.groupby(group, as_index=True, observed=True)
    norm = agg_grouped.agg(agg, numeric_only=numeric_only)
    #print(norm)

    def norm_one(s):
        group = s.name
        s = s.select_dtypes(include='number')
        n = norm.loc[group]
        o = s - n
        return o

    out = grouped.apply(norm_one, include_groups=True)
    # FIXME: avoid hardcoding
    out = out.reset_index().set_index(['filename', 'time'])

    return out
