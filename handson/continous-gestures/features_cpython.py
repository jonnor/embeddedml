
import librosa
import scipy.stats
import scipy.signal
import numpy
import pandas

def spectral_features(window,
        data_columns=['accX', 'accY', 'accZ'],
        sr=62.5,
        filter_type='low',
        filter_order=6,
        filter_cutoff=8.0,
        fft_length=64,
        fft_overlap=True,
        #fft_log=True,
    ):
    """
    Implementation of Spectral Features

    As defined in https://edge-impulse.gitbook.io/docs/edge-impulse-studio/processing-blocks/spectral-features
    """

    features = {}

    filter_sos = scipy.signal.butter(filter_order, filter_cutoff, btype=filter_type, analog=False, output='sos', fs=sr)
    
    for column in data_columns:
        data = window[column]

        # Apply filter
        filtered = scipy.signal.sosfilt(filter_sos, data)

        # Remove mean
        mean_removed = (filtered - filtered.mean())

        # compute statistical features
        features[column+' RMS']= numpy.sqrt(numpy.mean((mean_removed)**2))
        features[column+' Kurtosis']= scipy.stats.kurtosis(mean_removed)
        features[column+' Skew']= scipy.stats.skew(mean_removed)

        # compute spectral features using FFT
        hop_length = fft_length//2 if fft_overlap else fft_length
        S = numpy.abs(librosa.stft(mean_removed, n_fft=fft_length, hop_length=hop_length, window='hann'))
        S = numpy.log10(S**2 + 1e-12) # log scale
        frequencies = librosa.fft_frequencies(n_fft=fft_length, sr=sr)
        stft = pandas.DataFrame(S.T, columns=frequencies)

        # cut irrelevant FFT columns
        freq_columns = [ f for f in stft.columns if f > 0.0 and f < filter_cutoff ]
        stft = stft[freq_columns]

        # make nice feature names
        stft = stft.rename(columns=lambda f: f'{column} Spectral Power {f:.2f} Hz')

        # aggreate FFT sub-windows over time
        spectral = stft.max(axis=0).to_dict()
        for k, v in spectral.items():
            features[k] = v
    
    s = pandas.Series(features)
    return s
