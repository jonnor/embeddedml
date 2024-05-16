
import os
import glob
import uuid

from sklearn.metrics import roc_auc_score, make_scorer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate

import pandas
import numpy
import structlog

log = structlog.get_logger()

def linear_quantize(img, target_min, target_max, dtype):
    imin = img.min()
    imax = img.max()

    a = (target_max - target_min) / (imax - imin)
    b = target_max - a * imax
    new_img = (a * img + b).astype(dtype, casting='unsafe')
    return new_img


def run_dataset(pipeline, dataset_path,
    n_jobs = 4,
    repetitions = 1,
    scoring = 'roc_auc_ovo_weighted',
    ):

    data = pandas.read_parquet(dataset_path)
    target_column = '__target'
    feature_columns = list(set(data.columns) - set([target_column]))
    Y = data[target_column]
    X = data[feature_columns]

    dfs = []

    for repetition in range(repetitions):
        out = cross_validate(pipeline, X, Y, cv=10, n_jobs=n_jobs, scoring=scoring)
        df = pandas.DataFrame.from_records(out)        
        df['repetition'] = repetition
        dfs.append(df)
    
    out = pandas.concat(dfs)
    return out

def ensure_dir(p):
    if not os.path.exists(p):
        os.makedirs(p)

def run_datasets(pipeline, out_dir, run_id, kvs={}, dataset_dir=None, **kwargs):

    if dataset_dir is None:
        dataset_dir = 'data/datasets'

    for f in glob.glob('*.parquet', root_dir=dataset_dir):
        dataset_id = os.path.splitext(f)[0]
        dataset_path = os.path.join(dataset_dir, f)

        res = run_dataset(pipeline, dataset_path, **kwargs)
        res['dataset'] = str(dataset_id)
        for k, v in kvs.items():
            res[k] = v
        res['run'] = run_id

        #o = os.path.join(out_dir, f'dataset={dataset_id}')
        #ensure_dir(o)
        res.to_parquet(os.path.join(out_dir, f'r_{run_id}_ds_{dataset_id}.part'))

        print(res)

        log.info('dataset-run-end', dataset=dataset_id)

def main():

    # reduce number of features. To <255
    # quantize features to int16

    # reduce number of trees
    # apply

    quantizer = FunctionTransformer(linear_quantize,
        kw_args=dict(target_min=0, target_max=255, dtype=numpy.uint8))

    p = make_pipeline(
        RobustScaler(),
        quantizer,
        RandomForestClassifier(n_estimators=10),
    )

    run_id = uuid.uuid4().hex.upper()[0:6]

    out = run_datasets(p, kvs=dict(experiment='rf10_8bit'), out_dir='out.parquet', run_id=run_id)



if __name__ == '__main__':
    main()
