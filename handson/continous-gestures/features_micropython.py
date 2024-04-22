
def compute_rms(arr):

    pass

def compute_mean(arr):
   
    pass

def compute_scew(arr):

    pass



class TriaxialSpectralFeatures():
    """
    Compute spectral features using FFT and also statistical summaries.

    Inspired by the Spectral Features processing block in Edge Impulse
    https://edge-impulse.gitbook.io/docs/edge-impulse-studio/processing-blocks/spectral-features
    """

    def __init__(self, filter_cutoff):

        # FIXME: load array or compute coefficients using Butterworth directly
        coefficients = array.array('f', [])

        self.fft_length = 64
        self.axes = ['x', 'y', 'z']

        self.filters = { a: emliir.new(coefficients) for a in self.axes }
        self.fft = emlfft.new(fft_length)    
        self.fft_buffer = array.array('f', [0.0]*fft_length)

    def compute_spectral_features(self, signal, output, output_offset):

        length = self.fft_length
        hop = length // 2

        features = array

        # Compute FFT for sub-window
        # aggregated using max response
        while (start + length) < len(signal):
            end = max(start+length)
            start += hop

            # 
            self.fft.run(input, self.fft_buffer)

            feature_index = 0
            for fft_bin in enumerate(output):
                frequency = 

                if frequency <= 0.0 or frequency > self.filter_cutoff:
                    # Not included as features
                    continue

                # compute power, log scale
                

                # max aggregation, write to output
                output_index = output_offset + feature_index
                if value > output[output_index]:
                    output[output_index] = value

                feature_index += 1


    def run(self, input, features):

        feature_index = 0

        for axis in self.axes:
            # select data for this axis only
            offset = # FIXME: compute this
            signal = input[offset:]

            # Apply low-pass filter, reduce high frequency noise
            filter = filters[axis]
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

            output[feature_index] = compute_skew(signal)
            feature_index += 1

            # Compute spectral features using FFT
            feature_index += self.compute_spectral_features(signal, output, output_offset=feature_index)
            

def main():

    # 23 features per axis. 3 statistical summaries, and up to 20 FFT features
    spectral = SpectralFeatures(axes=['x', 'y', 'z'])
    features = array.array('f', [0.0] * 3 * (3 + 6))

    spectral.run(sensor_data, features)


