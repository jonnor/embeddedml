
import os
import glob
import uuid

from sklearn.metrics import roc_auc_score, make_scorer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler, FunctionTransformer, OrdinalEncoder
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.cluster import KMeans
from sklearn.base import BaseEstimator, ClassifierMixin
import scipy.special

from emlearn.preprocessing.quantizer import Quantizer
import emlearn
print('emlearn', emlearn.__path__)


import pandas
import numpy
import structlog

log = structlog.get_logger()

def get_tree_estimators(estimator):
    """
    Get the DecisionTree instances from ensembles or single-tree models
    """
    if hasattr(estimator, 'estimators_'):
        trees = [ e for e in estimator.estimators_]
    else:
        trees = [ estimator ]
    return trees

def tree_nodes(model, a=None, b=None):
    """
    Number of nodes total
    """
    model = model.named_steps['customrandomforestclassifier'].estimator

    trees = get_tree_estimators(model)
    nodes = [ len(e.tree_.children_left) for e in trees ]
    return numpy.sum(nodes)

def tree_leaves(model, a=None, b=None):
    """
    """
    model = model.named_steps['customrandomforestclassifier'].estimator

    trees = get_tree_estimators(model)
    leaves = [ numpy.count_nonzero((e.tree_.children_left == -1) & (e.tree_.children_right == -1)) for e in trees ]
    return numpy.sum(leaves)

def unique_leaves(model, a=None, b=None):
    """
    """
    model = model.named_steps['customrandomforestclassifier'].estimator

    trees = get_tree_estimators(model)

    ll = []
    for e in trees:
        l = e.tree_.value[(e.tree_.children_left == -1) & (e.tree_.children_right == -1)]
        ll.append(l)
    leaves = numpy.squeeze(numpy.concatenate(ll))

    return len(numpy.unique(leaves, axis=0))

def leaf_size(model, a=None, b=None):
    """
    Average size of leaves
    """
    model = model.named_steps['customrandomforestclassifier'].estimator

    trees = get_tree_estimators(model)
    sizes = [ e.tree_.value[(e.tree_.children_left == -1) & (e.tree_.children_right == -1)].shape[-1] for e in trees ]
    return numpy.median(sizes)


def quantize_probabilities(p, bits=8):
    assert bits <= 32
    assert bits >= 1
    max = numpy.max(p)
    min = numpy.min(p)
    assert max <= 1.0, max
    assert min >= 0.0, min

    steps = (2**bits)

    quantized = (p * steps).round(0).astype(numpy.uint32)
    out = quantized.astype(float) / steps

    return out

def get_leaves(estimator):

    ll = []
    for e in estimator.estimators_:
        is_leaf = (e.tree_.children_left == -1) & (e.tree_.children_right == -1)
        l = e.tree_.value[is_leaf]
        ll.append(l)

    leaves = numpy.concatenate(ll)
    return leaves

class CustomRandomForestClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, clusters=None, leaf_quantization=None, **kwargs):
        #print('INIT', leaf_quantization)

        self.estimator = RandomForestClassifier(**kwargs)
        self.clusters = clusters
        self.leaf_quantization = leaf_quantization 

    def get_params(self, deep=True):
        params = self.estimator.get_params()
        params['clusters'] = self.clusters
        params['leaf_quantization'] = self.leaf_quantization
        return params

    def set_params(self, **parameters):
        #print("SET", **parameters)
        our_keys = set(['clusters', 'leaf_quantization'])
        our_params = { k: v for k, v in parameters if k in our_keys }
        rf_params = { k: v for k, v in parameters if k not in our_keys }
        ret = self.estimator.set_params(**rf_params)

        for k, v in our_params:
            setattr(self, k, v)

        return ret 

    def predict(self, X):
        return self.estimator.predict(X)

    def predict_proba(self, X):
        return self.estimator.predict_proba(X)

    def fit(self, X, y):
        ret = self.estimator.fit(X, y)
        self.classes_ = self.estimator.classes_

        # Find leaves
        leaves = get_leaves(self.estimator)
        assert leaves.shape[1] == 1, 'only single output supported'
        leaves = numpy.squeeze(leaves)

        n_leaves = len(leaves)
        n_classes = len(numpy.unique(y))
        n_samples = len(y)
        n_unique_leaves = len(numpy.unique(leaves, axis=0))
        if self.clusters is None:
            max_leaves = None
        else:
            max_leaves = max(self.clusters, n_classes)
            max_leaves = min(max_leaves, n_leaves)
            max_leaves = min(max_leaves, n_samples)


        # Quantize leaves

        if self.leaf_quantization is not None:

            for e in self.estimator.estimators_:

                is_leaf = (e.tree_.children_left == -1) & (e.tree_.children_right == -1)
                values = e.tree_.value
                assert values.shape[1] == 1
            
                if self.leaf_quantization == 0:
                    # simple voting. highest probability gets 1.0, rest 0.0
                    # in practice only returning the index of the most probable class
                    voted_class = numpy.argmax(values, axis=-1)

                    quantized = numpy.zeros_like(values)
                    for i, c in enumerate(voted_class):
                        quantized[i, 0, c] = 1.0

                else:
                    quantized = quantize_probabilities(values, bits=self.leaf_quantization)
                assert quantized.shape == values.shape

                for i in range(len(e.tree_.value)):
                    is_leaf = (e.tree_.children_left[i] == -1) and (e.tree_.children_right[i] == -1)
                    if is_leaf:
                        # make sure probabilities still sum to 1.0
                        q = scipy.special.softmax(quantized[i])
                        #print('qq', q.shape, numpy.sum(q))
                        e.tree_.value[i] = q

            leaves = get_leaves(self.estimator)
            assert leaves.shape[1] == 1, 'only single output supported'
            leaves = numpy.squeeze(leaves)
            n_unique_leaves_quantized = len(numpy.unique(leaves, axis=0))
            
            #log.debug('leaf quantized',
            #    bits=self.leaf_quantization,
            #    unique_after=n_unique_leaves_quantized,
            #    unique_before=n_unique_leaves,
            #)
            

        # Cluster leaves
        if self.clusters is None:
            return ret


        print('clusters', max_leaves, n_unique_leaves, n_classes, n_samples, self.clusters)

        if (n_unique_leaves <= n_classes) or (n_unique_leaves <= max_leaves):
            # assume already optimial
            pass

        else:

            cluster = KMeans(n_clusters=max_leaves, tol=1e-4, max_iter=100)
            cluster.fit(leaves)

            # Replace by closest centroid
            for e in self.estimator.estimators_:

                is_leaf = (e.tree_.children_left == -1) & (e.tree_.children_right == -1)
                values = e.tree_.value
                assert values.shape[1] == 1

                # FIXME: fix this collapsing into 1-d. Probably happens for binary classification?
                c_idx = cluster.predict(numpy.squeeze(values))
                centroids = cluster.cluster_centers_[c_idx]
                #print('SS', centroids.shape)
                #print('cc', len(numpy.unique(centroids, axis=0)), len(numpy.unique(c_idx)))
                # XXX: is this correct ??
                v = numpy.where(numpy.expand_dims(is_leaf, -1), centroids, numpy.squeeze(values))
                v = numpy.reshape(v, values.shape)

                for i in range(len(e.tree_.value)):
                    e.tree_.value[i] = v[i]


        return ret        

def setup_data_pipeline(data, quantizer=None):

    target_column = '__target'
    feature_columns = list(set(data.columns) - set([target_column]))
    Y = data[target_column]
    X = data[feature_columns]

    # data preprocessing
    cat_columns = make_column_selector(dtype_include=[object, 'category'])(X)
    num_columns = list(set(feature_columns) - set(cat_columns))

    # ensure that all categories have a well defined mapping, regardless of train/test splits
    categories = OrdinalEncoder().fit(X[cat_columns]).categories_

    log.debug('setup-data-pipeline',
        samples=len(X),
        quantizer=quantizer,
        categorical=len(cat_columns),
        numerical=len(num_columns),
    )

    if quantizer:
        num_transformer = make_pipeline(RobustScaler(), quantizer)
    else:
        num_transformer = make_pipeline(RobustScaler())

    preprocessor = ColumnTransformer(transformers=[
        ('num', num_transformer, num_columns),
        ('cat', OrdinalEncoder(categories=categories), cat_columns)
    ])

    return X, Y, preprocessor

def run_dataset(pipeline, dataset_path, quantizer=None,
    n_jobs = 4,
    repetitions = 1,
    scoring = 'roc_auc_ovo_weighted',
    ):

    data = pandas.read_parquet(dataset_path)
    X, Y, preprocessor = setup_data_pipeline(data, quantizer=quantizer)

    # combine into a pipeline
    pipeline = make_pipeline(
        preprocessor,
        *pipeline,
    )

    scoring = {
        'nodes': tree_nodes,
        'leaves': tree_leaves,
        'leasize': leaf_size,
        'uniqueleaves': unique_leaves,
        'roc_auc': 'roc_auc_ovo_weighted',
    }

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

def run_datasets(pipeline, out_dir, run_id, quantizer=None, kvs={}, dataset_dir=None, **kwargs):

    if dataset_dir is None:
        dataset_dir = 'data/datasets'

    for f in glob.glob('*.parquet', root_dir=dataset_dir):
        dataset_id = os.path.splitext(f)[0]
        dataset_path = os.path.join(dataset_dir, f)

        res = run_dataset(pipeline, dataset_path, quantizer=quantizer, **kwargs)
        res['dataset'] = str(dataset_id)
        for k, v in kvs.items():
            res[k] = v
        res['run'] = run_id

        #o = os.path.join(out_dir, f'dataset={dataset_id}')
        #ensure_dir(o)
        o = os.path.join(out_dir, f'r_{run_id}_ds_{dataset_id}.part')
        assert not os.path.exists(o), o
        res.to_parquet(o)

        score = res['test_roc_auc'].median()
        nodes = res['test_nodes'].median()

        log.info('dataset-run-end', dataset=dataset_id, score=score, **kvs)

def main():

    # optimization steps. To be compared in experiments / ablated
    # reduce number of features. To <255
    # quantize features to int16
    # reduce number of trees
    # try replace nodes with k-means quantized versions

    # TODO: run a hyperparameter search on each dataset.
    # Find appropriate parameters, when no optimizations used
    # for a particular set of trees. 10 is a good starting point?
    # 1. Leaf quantize 8 bit
    # 2. Feature quantize 16 bit
    # 3. Leaf+feature quantize
    #
    # 4. Leaf reduce, in 5-10 levels. Percentage of unique? Maybe in log2 scale 1 / (2,4,8,16,32,64,128)
    # Could also be reported as X times the number of classes?    

    # Research questions
    # A) how well does feature and leaf quantization work?
    # Hypothesis: 16 bit feature is ~lossless. A 8 bit leaf probabilities is ~lossless
    # Results indicate that 16 bit featurs is indeed lossless. Within the margins of error for experiment
    # TODO: merge the int16 support to emlearn
    #
    # TODO: check 8 bit leaf probability quantization on CC-18

    # B) how well does leaf clustering work?
    # Hypothesis: Can reduce leaf size by 2-10 without ~zero loss in performance. Can reduce overall model size by 2-5x
    # Preliminary results do indicate that up to 5x model size reduction is possible with low perf drops
    # however there are a few outliers, where even 0.8 the original size causes drop in performance 

    # C) how does code generation vs data structure compare, wrt size and inference time
    # Hypothesis: datastructure "loadable" is smaller in size, but slower in inference time
    # 

    # D) what are limitating factors for practical models on microcontrollers
    # Hypothesis: Model size is the primary bottleneck/constraint
    # accelerometer. 10 FPS
    # sound. 25 FPS
    # images 1 FPS
    # maybe do a "worst case" analysis of largesr ensembles that fit on a micro. 10kB, 100kB.
    # Execution speed for max depths.
    # Or do a synthetic N deep execution speed test? To get time-per-decision. On common micros
    # Hypothesis: Feature extraction dominates tree execution
    # maybe compare tree execution speed with a simple preprocessing. EX: RMS


    # E) how does emlearn RF compare to other frameworks. m2cgen and micromlgen
    # in terms of size and execution speed. At near 0 error rate 
    

    #q = quantize_probabilities(numpy.array([0, 0.10, 0.25, 0.75, 0.90, 1.0]), bits=8)
    #print(q)

    
    experiments = {
        #'rf10_noclust': dict(clusters=None, n_estimators=10),
        #'rf10_100clust': dict(clusters=100, n_estimators=10),
        #'rf10_30clust': dict(clusters=30, n_estimators=10),
        #'rf10_10clust': dict(clusters=10, n_estimators=10),

       #'rf10_none': dict(dtype=None),
       #'rf10_float': dict(dtype=float, target_max=1000.0),   
       #'rf10_32bit': dict(dtype=numpy.int32, target_max=2**31-1),   
       #'rf10_16bit': dict(dtype=numpy.int16, target_max=2**15-1),
        #'rf10_12bit': dict(dtype=numpy.int16, target_max=2**12-1),
        #'rf10_10bit': dict(dtype=numpy.int16, target_max=2**10-1),
       #'rf10_8bit': dict(dtype=numpy.int8, target_max=127),

       'rf10_majority': dict(leaf_quantization=0),
       'rf10_leaf8bit': dict(leaf_quantization=8),
       'rf10_none': dict(leaf_quantization=None),
       'rf10_leaf16bit': dict(leaf_quantization=16),
       'rf10_leaf4bit': dict(leaf_quantization=8),
    }

    for experiment, config in experiments.items():

        log.info('experiment-start', experiment=experiment, **config)

        p = []

        # feature quantization (optional)
        quantizer = None
        if config.get('dtype'):
            quantizer = Quantizer(dtype=config['dtype'],
                max_quantile=0.001, out_max=config['target_max'])

        # classifier
        rf = CustomRandomForestClassifier(
            n_estimators=config.get('n_estimators', 10), 
            min_samples_leaf=0.01,
            clusters=config.get('clusters', None),
            leaf_quantization=config.get('leaf_quantization', None),
        )
        p.append(rf)

        run_id = uuid.uuid4().hex.upper()[0:6] + f'_{experiment}'

        run_datasets(p, quantizer=quantizer, kvs=dict(experiment=experiment), out_dir='out.parquet', run_id=run_id, repetitions=5)



if __name__ == '__main__':
    main()
