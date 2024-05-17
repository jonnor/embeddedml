
import os
import glob
import uuid

from sklearn.metrics import roc_auc_score, make_scorer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler, FunctionTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_validate
from sklearn.cluster import KMeans
from sklearn.base import BaseEstimator, ClassifierMixin

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

class CustomRandomForestClassifier(BaseEstimator, ClassifierMixin):

    def __init__(self, clusters=None, **kwargs):
        #print('INIT', kwargs)

        self.estimator = RandomForestClassifier(**kwargs)
        self.clusters = clusters

    def get_params(self, deep=True):
        return self.estimator.get_params()    

    def set_params(self, **parameters):
        #print("SET", **parameters)
        return self.estimator.set_params(**parameters)

    def predict(self, X):
        return self.estimator.predict(X)

    def predict_proba(self, X):
        return self.estimator.predict_proba(X)

    def fit(self, X, y):
        ret = self.estimator.fit(X, y)

        if self.clusters is not None:

            n_classes = len(numpy.unique(y))
            n_samples = len(y)

            n_clusters = max(self.clusters, n_classes)
            n_clusters = min(n_clusters, n_samples)

            #print('clusters', n_clusters, n_classes, n_samples, self.clusters)

            # Find leaves
            ll = []
            for e in self.estimator.estimators_:
                is_leaf = (e.tree_.children_left == -1) & (e.tree_.children_right == -1)
                l = e.tree_.value[is_leaf]
                ll.append(l)

            leaves = numpy.concatenate(ll)
            assert leaves.shape[1] == 1, 'only single output supported'
            leaves = numpy.squeeze(leaves)

            # Cluster the leaves
            cluster = KMeans(n_clusters=n_clusters, tol=1e-4, max_iter=100)
            cluster.fit(leaves)

            # Replace by closest centroid
            for e in self.estimator.estimators_:

                is_leaf = (e.tree_.children_left == -1) & (e.tree_.children_right == -1)
                values = e.tree_.value
                assert values.shape[1] == 1
                c_idx = cluster.predict(numpy.squeeze(values))
                centroids = cluster.cluster_centers_[c_idx]
                #print('SS', centroids.shape)
                #print('cc', len(numpy.unique(centroids, axis=0)), len(numpy.unique(c_idx)))
                # XXX: is this correct ??
                v = numpy.where(numpy.expand_dims(is_leaf, -1), centroids, numpy.squeeze(values))
                v = numpy.reshape(v, values.shape)

                for i in range(len(e.tree_.value)):
                    e.tree_.value[i] = v[i]


        self.classes_ = self.estimator.classes_

        return ret        



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

    # optimization steps. To be compared in experiments / ablated
    # reduce number of features. To <255
    # quantize features to int16
    # reduce number of trees
    # try replace nodes with k-means quantized versions

    quantizer = FunctionTransformer(linear_quantize,
        kw_args=dict(target_min=0, target_max=255, dtype=numpy.uint8))

    p = make_pipeline(
        RobustScaler(),
        #quantizer,
        CustomRandomForestClassifier(n_estimators=10, max_depth=10, clusters=None),
    )

    run_id = uuid.uuid4().hex.upper()[0:6]

    out = run_datasets(p, kvs=dict(experiment='rf10_noclust'), out_dir='out.parquet', run_id=run_id)



if __name__ == '__main__':
    main()
