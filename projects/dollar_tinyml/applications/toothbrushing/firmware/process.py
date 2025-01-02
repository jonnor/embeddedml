
import math
import array
import gc
import time

import npyfile
import emlearn_trees

import timebased
from core import StateMachine

class GravitySplitter():

    def __init__(self, samplerate, lowpass_cutoff=0.5):

        rc = 1.0/(2*3.14*lowpass_cutoff)
        dt = 1.0/samplerate
        self.lowpass_alpha = rc / (rc + dt)

        self.gravity = None
        self.motion = array.array('f', [0, 0, 0])

    def process(self, xyz):
        assert len(xyz) == 3, xyz

        if self.gravity is None:
            # jump straigth to it, to avoid slow ramp-in
            self.gravity = array.array('f', xyz)
        
        a = self.lowpass_alpha
        for i in range(len(xyz)):
            self.gravity[i] = (a * self.gravity[i]) + ((1.0 - a) * xyz[i])
            self.motion[i] = xyz[i] - self.gravity[i]


def empty_array(typecode, length, value=0):
    return array.array(typecode, (value for _ in range(length)))

def mean(arr):
    m = sum(arr) / float(len(arr))
    return m

def magnitude_3d(x, y, z):
    r2 = x**2 + y**2 + z**2
    r = math.sqrt(r2)
    return r

def euclidean(a, b):
    s = 0.0
    assert len(a) == len(b)
    for av, bv in zip(a, b):
        s += (av-bv)**2

    return math.sqrt(s)

def clamp(value, lower, upper) -> float:
    v = value
    v = min(v, upper)
    v = max(v, lower)
    return v

def energy_xyz(xs, ys, zs, orientation):
    assert len(xs) == len(ys)
    assert len(ys) == len(zs)

    xo, yo, zo = orientation
    
    # compute RMS of magnitude, after having removed orientation
    s = 0.0
    for i in range(len(xs)):
        m = magnitude_3d(xs[i]-xo, ys[i]-yo, zs[i]-zo)
        s += m**2

    rms = math.sqrt(s)
    return rms

class DataProcessor():

    def __init__(self):
        # FIXME: proper lookup
        here = __file__
        model_path = './firmware/models/brushing.csv'
        print('load', model_path)
        self.brushing_model = self.load_model(model_path)

        features_typecode = timebased.DATA_TYPECODE
        n_features = timebased.N_FEATURES
        self.features = array.array(features_typecode, (0 for _ in range(n_features)))
    
        self.brushing_outputs = array.array('f', (0 for _ in range(2)))

    def load_model(self, model_path):

        # Load a CSV file with the model
        model = emlearn_trees.new(10, 1000, 10)
        with open(model_path, 'r') as f:
            emlearn_trees.load_model(model, f)

        return model

    def process(self, xs, ys, zs):
        """
        Analyze the accelerometers sensor data, to determine what is happening
        """

        up_direction = [ 0, 1.0, 0.0 ] # the expected gravity vector, when toothbrush is upright (not in use)
        max_distance_from_up = 0.80
        max_motion_energy = 3000
        brushing_energy = 20000

        # find orientation
        orientation_start = time.ticks_ms()
        orientation_xyz = mean(xs), mean(ys), mean(zs)
        mag = magnitude_3d(*orientation_xyz)
        norm_orientation = [ c/mag for c in orientation_xyz ]

        distance_from_up = euclidean(norm_orientation, up_direction)
        energy = energy_xyz(xs, ys, zs, orientation_xyz)    

        # dummy motion classifier
        motion = clamp(energy / max_motion_energy, 0.0, 1.0)

        # dummy brushing classifier
        # assume brushing if
        # a) not perfectly upright (stationary in holder)
        # AND b) relatively high energy
        # TODO: replace with trained ML classifier
        not_upright = clamp(distance_from_up / max_distance_from_up, 0.0, 1.0)
        high_energy = clamp(energy / brushing_energy, 0.0, 1.0)

        dummy_brushing = clamp((not_upright*2) * (high_energy*1.5), 0.0, 1.0)
    
        orientation_duration = time.ticks_ms() - orientation_start

        #norm_orientation, distance_from_up

        # compute features
        features_start = time.ticks_ms()
        ff = timebased.calculate_features_xyz((xs, ys, zs))
        for i, f in enumerate(ff):
            self.features[i] = int(f)
        features_duration = time.ticks_ms() - features_start

        # run model
        predict_start = time.ticks_ms()
        self.brushing_model.predict(self.features, self.brushing_outputs)
        brushing = self.brushing_outputs[1]
        predict_duration = time.ticks_ms() - predict_start

        #print('comp', features_duration, predict_duration)

        return motion, brushing


def read_data_file(path,
        chunk_length,
        n_features=3,
        skip_samples=0,
        limit_samples=None):

    with npyfile.Reader(path) as data:

        # Check that data is expected format: files x timesteps x features, int16
        shape = data.shape
        assert len(shape) == 2, shape
        assert shape[1] == n_features, shape
        assert data.itemsize == 2, data.itemsize
        assert data.typecode == 'h', data.typecode

        # Read one chunk at a time
        sample_count = 0

        chunk_size = n_features*chunk_length
        data_chunks = data.read_data_chunks(chunk_size, offset=n_features*skip_samples)

        for arr in data_chunks:
            yield arr

            sample_count += 1
            if limit_samples is not None and sample_count > limit_samples:
                break


def process_file(path):

    samplerate = 50
    hop_length = 25
    window_length = hop_length

    x_values = empty_array('h', hop_length)
    y_values = empty_array('h', hop_length)
    z_values = empty_array('h', hop_length)

    p = DataProcessor()
    sm = StateMachine(time=0.0)

    n_axes = 3
    sample_no = 0
    for xyz in read_data_file(path, chunk_length=hop_length):
        t = (1.0/samplerate) * sample_no
        n_samples = len(xyz) // n_axes
        for i in range(n_samples):
            x_values[i] = xyz[(i*3)+0]
            y_values[i] = xyz[(i*3)+1]
            z_values[i] = xyz[(i*3)+2]

        motion, brushing = p.process(x_values, y_values, z_values)
        sm.next(t, motion, brushing)
        sample_no += n_samples

        yield t, motion, brushing, sm.state, sm.brushing_time


def test_process_happy():

    # FIXME: select a file with test data for success scenario
    data_path = ''
    for out in process_file(data_path):
        t = out[1]
        state = out[4]
        if state == 'done':
            done_time = t
            break

    expect_done = 300
    assert done_time >= expect_done - 10
    assert done_time <= expect_done + 10

def main():

    import sys

    total_brushing_time = 0.0

    data_path = sys.argv[1]
    for out in process_file(data_path):
        t, motion, brushing, state, brushing_time = out
        print('toothbrush-state-out', out)

        total_brushing_time = max(brushing_time, total_brushing_time)

    print('toothbrush-done', total_brushing_time)

if __name__ == '__main__':
    main()
