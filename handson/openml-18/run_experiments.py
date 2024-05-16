
import os

from sklearn.metrics import roc_auc_score, make_scorer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

import pandas
import numpy

def linear_quantize(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type, casting='unsafe')
    return new_img

def run_dataset(pipeline, dataset_id,
    n_jobs = 4,
    scoring = 'roc_auc_ovo_weighted',
    ):

    # TODO: support repetitions

    datasets_path = 'data/datasets'
    data = pandas.read_parquet(os.path.join(datasets_path, f'{dataset_id}.parquet'))
    target_column = '__target'
    feature_columns = list(set(data.columns) - set([target_column]))
    Y = data[target_column]
    X = data[feature_columns]

    # FIXME: do quantization as a transformer in the pipeline
    X = linear_quantize(X.values, 0, 255, numpy.uint8)

    out = cross_validate(pipeline, X, Y, cv=10, n_jobs=n_jobs, scoring=scoring)
    df = pandas.DataFrame.from_records(out)
    
    return df

def main():

    # reduce number of features. To <255
    # quantize features to int16

    # reduce number of trees
    # apply

    # FIXME: check for outliers / large feature values
    p = make_pipeline(
        RobustScaler(),
        RandomForestClassifier(n_estimators=100),
    )

    out = run_dataset(p, dataset_id=11)

    print(out['test_score'].mean())


if __name__ == '__main__':
    main()
