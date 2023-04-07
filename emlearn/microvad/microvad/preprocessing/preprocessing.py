
import numpy
import pandas


def compute_windows(arr, frames, pad_value=0.0, overlap=0.5, step=None):
    """
    Extract overlapped time-windows for spectrograms and labels
    """

    if step is None:
        step = int(frames * (1-overlap))
        
    windows = []
    index = []
        
    width, length = arr.shape
    
    for start_idx in range(0, length, step):
        end_idx = min(start_idx + frames, length)

        # create emmpty
        win = numpy.full((width, frames), pad_value, dtype=float)
        # fill with data
        win[:, 0:end_idx-start_idx] = arr[:,start_idx:end_idx]

        windows.append(win)
        index.append(start_idx)

    s = pandas.Series(windows, index=index)
    s.index.name = 'start_index'
    return s


def make_continious_labels(events, length, time_resolution):
    """
    Create a continious vector for the event labels that matches the time format of our spectrogram
    
    Assumes that no annotated event means nothing occurred.
    """

    freq = pandas.Timedelta(seconds=time_resolution)
    
    # Create empty covering entire spectrogram
    duration = length * time_resolution
    ix = pandas.timedelta_range(start=pandas.Timedelta(seconds=0.0),
                    end=pandas.Timedelta(seconds=duration),
                    freq=freq,
                    closed='left',
    )
    ix.name = 'time'
    df = pandas.DataFrame({}, index=ix)
    assert len(df) == length, (len(df), length)
    df["event"] = 0
    
    # fill in event data
    for start, end in zip(events['start'], events['end']):
        s = pandas.Timedelta(start, unit='s')
        e = pandas.Timedelta(end, unit='s')

        
        match = df.loc[s:e]
        df.loc[s:e, "event"] = 1
    
    return df
