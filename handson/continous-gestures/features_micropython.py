
def compute_rms(arr):

    pass

def compute_mean(arr):
    
    pass


class TriaxialSpectralFeatures():
    """
    
    """

    def __init__(self, filter_cutoff):

        # FIXME: load array
        coefficients = array.array('f', [])

        self.fft_length = 64
        self.axes = ['x', 'y', 'z']

        self.filters = { a: emliir.new(coefficients) for a in self.axes }
        self.fft = emlfft.new(fft_length)    
        self.fft_buffer = array.array('f', [0.0]*fft_length)

    def compute_spectral_features(signal, output, output_offset):

        length = self.fft_length
        hop = length // 2

        features = array

        # Compute FFT for sub-window
        # aggregated using max response
        while (start + length) < len(signal):
            end = max(start+length)

            start += hop

            self.fft.run(input, output)

            feature_index
            for fft_bin in enumerate(output):
                frequency = 

                if frequency <= 0.0 or frequency > self.filter_cutoff:
                    # Not included as features
                    continue

                # max aggregation
                index = output_offset + feature_index

                feature_index += 1

            # compute spectral features using FFT
            hop_length = fft_length//2 if fft_overlap else fft_length
            S = numpy.abs(librosa.stft(mean_removed, n_fft=fft_length, hop_length=hop_length, window='hann'))
            S = numpy.log10(S**2 + 1e-12) # log scale
            frequencies = librosa.fft_frequencies(n_fft=fft_length, sr=sr)
            stft = pandas.DataFrame(S.T, columns=frequencies)

            # cut irrelevant FFT columns
            freq_columns = [ f for f in stft.columns if f > 0.0 and f < filter_cutoff ]


            # aggreate FFT sub-windows over time
            spectral = stft.max(axis=0).to_dict()
            for k, v in spectral.items():
                features[k] = v

    def run(self, signal, ):

        # 9 features per axis
        features = array.array('f', [0.0] * 3 * (3 + 6))

        feature_index = 0

        for axis in self.axes:
            filter = filters[axis]

            offset = # FIXME

            axis_data[offset:] 
            signal = 

            # Apply low-pass filter, reduce high frequency noise
            filter.run(data)

            # Remove mean
            signal_mean = compute_mean(data)
            for i in range(len(signal)):
                signal[i] = signal[i] - signal_mean

            # compute statistical features
            output[feature_index] = compute_rms(signal)
            feature_index += 1

            output[feature_index] = compute_kurtosis(signal)
            feature_index += 1

            output[feature_index] = compute_kurtosis(signal)
            feature_index += 1

            # Compute spectral features using FFT
            self.compute_spectral_features(signal, )
