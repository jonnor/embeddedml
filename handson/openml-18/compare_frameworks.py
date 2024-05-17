
from run_experiments import run_datasets, setup_data_pipeline

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
import pandas


import emlearn
import m2cgen
import micromlgen

def export_emlearn(estimator, inference='loadable', dtype='int16_t', **kwargs):

    c = emlearn.convert(estimator, dtype=dtype, **kwargs)
    code = c.save(name='model', inference=inference)    

    return code

def export_m2cgen(estimator, **kwargs):

    code = m2cgen.export_to_c(estimator)

    return code

def export_micromlgen(estimator, **kwargs):

    code = micromlgen.port(estimator)

    return code

from emlearn.evaluate.size import get_program_size, check_build_tools

def generate_test_program(model_code, features):

    # XXX: the cast to float is wrong. Will crash horribly during execution
    # Only works for size estimation

    # FIXME: implement inference for all types. emlearn, m2cgen, micromlgen

    model_code += f"""
    int {model_name}_predict(const {dtype} *f, int l) {{
        return eml_trees_predict(&{model_name}, (float *)f, l);
    }}"""


    test_program = \
    f"""
    #include <stdint.h>

    #if {model_enabled}
    {model_code}

    static {dtype} features[{features_length}] = {{0, }};
    #endif

    int main()
    {{
        uint8_t pred = 0;
        #if {model_enabled}
        pred = {model_name}_predict(features, {features_length});
        #endif
        int out = pred;
        return out;
    }}
    """


def main():

    platforms = pandas.DataFrame.from_records([
        ('arm', 'Cortex-M0'),
        ('arm', 'Cortex-M4F'),
    ], columns=['platform', 'cpu'])

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

    data = get_program_size(test_program, platform=platform, mcu=mcu)

    return pandas.Series(data)



if __name__ == '__main__':
    main()
