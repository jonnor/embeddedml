
import os

import numpy
import pandas
from sklearn.preprocessing import FunctionTransformer, RobustScaler
from matplotlib import pyplot as plt
import seaborn
import scipy.stats

from emlearn.preprocessing.quantizer import Quantizer


from run_experiments import setup_data_pipeline

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
