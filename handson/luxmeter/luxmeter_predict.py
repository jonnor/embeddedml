
import npyfile
import array

from luxmeter_core import load_pipeline


pipeline_path = 'pipeline.npy'
n_features = 18
scaler, model = load_pipeline(pipeline_path, expect_features=n_features)

data_paths = [
    'data/rgb33_100h_156lux.npy',
    'data/rgb33_0h_55lux.npy',
    'data/rgb1_120h_395lux.npy',
    'data/rgb1_180h_714lux.npy',
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


