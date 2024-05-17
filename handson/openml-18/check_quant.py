
import os

import numpy
import pandas
from sklearn.preprocessing import FunctionTransformer, RobustScaler
from matplotlib import pyplot as plt
import seaborn
import scipy.stats



import numpy
from sklearn.base import BaseEstimator, TransformerMixin

class Quantizer(BaseEstimator, TransformerMixin):

    """
    Scales the features to fit a target range, usually a signed integer.
    Quantization is applied uniformly to all features.
    Scaling done using a linear multiplication, without any offset.

    If different features have very different scales,
    it is recommended to use a feature standardization transformation before this step.
    Examples: StandardScaler, RobustScaler, MinMaxScaler

    If the feature values have a very large range, or the range is very assymetrical,
    a non-linear pre-transformation may also be useful.
    """

    def __init__(self,
            max_quantile=0.01,
            max_value=None,
            out_max=None, # automatically from dtype
            dtype='int16'):
        self.max_quantile = max_quantile
        self.max_value = max_value
        self.dtype = numpy.dtype(dtype)
        self.out_max = out_max

    def _get_out_max(self):
        if self.out_max is not None:
            return self.out_max

        info = None
        try:
            info = numpy.iinfo(self.dtype)
        except ValueError:
            info = numpy.finfo(self.dtype)
        if info is None:
            raise ValueError(f"Unsupported dtype {self.dtype}")

        out_max = info.max
        return out_max

    def fit(self, X, y=None):
        # TODO: normalize and check X,y using sklearn helpers
        out_max = self._get_out_max()

        if self.max_value is None:
            # learn the value from data
            high = 1.0-self.max_quantile
            low = self.max_quantile
            min_value = numpy.quantile(X, q=low, axis=None)
            max_value = numpy.quantile(X, q=high, axis=None)
            largest = max(max_value, -min_value)
            #print('mm', min_value, max_value, largest)
        else:
            largest = self.max_value            
    
        self.scale_ = out_max / largest
        #print('ss', self.scale_, out_max)
        return self

    def transform(self, X, y=None):

        # scale
        out = X * self.scale_

        # clip out-of-range values
        out_max = self._get_out_max()
        out = numpy.clip(out, -out_max, out_max)

        # quantize / convert dtype
        out = out.astype(self.dtype)

        # check post-conditions
        assert out.shape == X.shape
        assert out.dtype == self.dtype

        if y is None:
            return out

        return out, y
        
    def inverse_transform(self, X, y=None):

        # ensure workig with floats, not fixed-size integers
        out = X.astype(float)

        # apply scale
        out = out / self.scale_

        # clip out-of-range values
        out_max = self._get_out_max()
        out = numpy.clip(out, -out_max, out_max)

        assert out.shape == X.shape

        if y is None:
            return out

        return out, y



from run_experiments import setup_data_pipeline, linear_quantize

def main():

    experiments = {
       'rf10_none': dict(dtype=None),
       'rf10_float': dict(dtype=float, target_min=-10.0, target_max=10.0),   
       'rf10_32bit': dict(dtype=numpy.int32, target_min=-2**30, target_max=2**30),   
       'rf10_16bit': dict(dtype=numpy.int16, target_min=-2**14, target_max=2**14),
        #'rf10_12bit': dict(dtype=numpy.int16, target_min=-2**12, target_max=2**12),
        #'rf10_10bit': dict(dtype=numpy.int16, target_min=-2**10, target_max=2**10),
        'rf10_8bit': dict(dtype=numpy.int8, target_min=-127, target_max=127),
    }


    # badly performing
    datasets = [
        '1478', 
        #'40983',
        #'40984',
        #'1494',
        #'40982', '1486', '4134', '44', '151', '1050', '1487', '458', '37', '1475', '1510'
    ]

    datasets_path = 'data/datasets'

    config  = experiments['rf10_float']
    quantizer = FunctionTransformer(linear_quantize, kw_args=dict(\
        target_min=config['target_min'],
        target_max=config['target_max'],
        dtype=config['dtype'],
    ))

    for dataset_id in datasets:
        d = os.path.join(datasets_path, f'{dataset_id}.parquet')
        data = pandas.read_parquet(d)

        X, Y, preprocessor = setup_data_pipeline(data, quantizer)

        print(X.shape)
        print(X.dtypes)
        print(X.describe())
        print(X.nunique())

        #if 'short.line.density.5' in X.columns:
        #    print(X['short.line.density.2'].unique())

        #fig, ax = plt.subplots(1, figsize=(20, 5))
        #for c in X.columns:
        #    seaborn.kdeplot(ax=ax, data=X, x=c)
        #ax.figure.savefig('pp.png')

        s = pandas.DataFrame(RobustScaler().fit_transform(X), columns=X.columns)

        q = Quantizer(dtype=float, out_max=1e6, max_quantile=0.001)
        s = q.fit_transform(s.values)
        s = pandas.DataFrame(q.inverse_transform(s), columns=X.columns)

        d = s.describe(percentiles=[0.01, 0.1, 0.9, 0.99]).T
        print(d)
        print(d.sort_values('max', ascending=False)[['max', '99%', '90%']].head(20))
        print(d.sort_values('min', ascending=True)[['min', '1%', '10%']].head(20))

    
        #mad = scipy.stats.median_abs_deviation(X, axis=0)
        #print(mad.shape)
        #print(mad)

if __name__ == '__main__':
    main()
