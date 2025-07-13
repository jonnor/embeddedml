
import npyfile
import emlearn_linreg
import array

class FeatureScaler():
    """
    Linear transformation of features

    Can be used to do the inference part of
    MinMaxScaler, StandardScaler, et.c. from scikit-learn
    """

    def __init__(self, minimums, scales):
        self.minimums = array.array('f', minimums)
        self.scales = array.array('f', scales)
        n_features = len(self.scales)
        assert len(self.minimums) == n_features, (len(self.minimums), n_features)

    def transform_into(self, inp, out):
        n_features = len(self.scales)
        assert len(inp) == n_features, (len(inp), n_features)
        assert len(out) == n_features, (len(out), n_features)
        for i in range(n_features):
            out[i] = self.minimums[i] + self.scales[i] * inp[i] 

    def transform(self, inp):
        n_features = len(self.scales)
        out = array.array('f', (0.0 for _ in range(n_features)))
        self.transform_into(inp, out)
        return out


def load_pipeline(path, expect_features=None):

    shape, data = npyfile.load(pipeline_path) 

    print(shape)
    assert len(shape) == 2, shape
    assert shape[0] == 4, shape # scale_min, scale_mul, reg_bias, reg_weights
    n_features = shape[1]

    if expect_features is not None:
        assert n_features == expect_features, (n_features, expect_features)

    scaler_minimums = ( data[i] for i in range(0, n_features) )
    scale_multiply = ( data[i] for i in range(n_features, n_features*2) )
    bias = data[n_features*2]
    weights = array.array('f', ( data[i] for i in range(n_features*3, n_features*4) ))

    model = emlearn_linreg.new(n_features, 0, 0, 0)
    model.set_bias(bias)
    model.set_weights(weights)

    scaler = FeatureScaler(scaler_minimums, scale_multiply)

    return scaler, model


pipeline_path = 'notebooks/pipeline.npy'
n_features = 18
scaler, model = load_pipeline(pipeline_path, expect_features=n_features)

data_paths = [
    'data/one/rgb33_100h_156lux.npy',
    'data/one/rgb33_0h_55lux.npy',
    'data/one/rgb1_120h_395lux.npy',
    'data/one/rgb1_180h_714lux.npy',
]
for data_path in data_paths:
    print(data_path)
    shape, data = npyfile.load(data_path)

    assert shape[0] == n_features
    rowstride = 20
    rowstride = 18

    for sample_no in range(0, 3):
        r = sample_no
        offset = rowstride*r
        sample = array.array('f', (data[offset+i] for i in range(n_features)))
        t = scaler.transform(sample)

        out = model.predict(t)
        print(out, data_path)


