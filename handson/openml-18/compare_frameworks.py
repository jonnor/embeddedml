
from run_experiments import run_datasets, setup_data_pipeline

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import pandas


import emlearn
import m2cgen
import micromlgen

def export_emlearn(estimator, **kwargs):

    c = emlearn.convert(estimator, **kwargs)
    code = c.save(name='model')    

    return code

def export_m2cgen(estimator, **kwargs):

    code = m2cgen.export_to_c(estimator)

    return code

def export_micromlgen(estimator, **kwargs):

    code = micromlgen.port(estimator)

    return code

def main():

    dataset_path = 'data/datasets/151.parquet'
    data = pandas.read_parquet(dataset_path)
    X, Y, preprocessor = setup_data_pipeline(data)

    # combine into a pipeline
    pipeline = make_pipeline(
        preprocessor,
        RandomForestClassifier(n_estimators=10, max_depth=10),
    )

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.30)
    pipeline.fit(X_train, Y_train)

    m = pipeline.named_steps['randomforestclassifier']
    ce = export_emlearn(m)
    c2 = export_m2cgen(m)
    cu = export_micromlgen(m)

    print(len(ce)/1000, len(c2)/1000, len(cu)/1000)


if __name__ == '__main__':
    main()
