
#!/usr/bin/env python
# coding: utf-8


"""
Optimizing tree ensembles
===========================


"""

import os.path

import emlearn
import numpy
import pandas
import seaborn
import matplotlib.pyplot as plt

try:
    # When executed as regular .py script
    here = os.path.dirname(__file__)
except NameError:
    # When executed as Jupyter notebook / Sphinx Gallery
    here = os.getcwd()


from quant import Quant, IntervalModel

from sonar import load_sonar_dataset, tidy_sonar_data

# %%
# Load dataset
# ------------------------
#
# The Sonar dataset is a basic binary-classification dataset, included with scikit-learn
# Each instance constains the energy across multiple frequency bands (a spectrum). 

data = load_sonar_dataset()
tidy = tidy_sonar_data(data)
print(tidy.head(3))


# %%
# Visualize data
# ------------------------
#
# Looking at the overall plot, the data looks easily separable by class.
# But plotting each sample shows that there is considerable intra-class variability.


seaborn.relplot(data=tidy, kind='line', x='band', y='energy', hue='label',
        height=3, aspect=3)


seaborn.relplot(data=tidy, kind='line', x='band', y='energy', hue='sample',
            row='label', ci=None, aspect=3, height=3, legend=False);


# %%
# Setup model evaluation and optimization
# ------------------------
#
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import sklearn.model_selection

# custom metrics for model costs
from emlearn.evaluate.trees import model_size_bytes, compute_cost_estimate

from sklearn.feature_selection import SequentialFeatureSelector

def evaluate_classifier(data, n_features, transform, features=None, quant=True):
    spectrum_columns = [c for c in data.columns if c.startswith('b.')]
    
    if features is None:
        features = spectrum_columns
    
    est = RandomForestClassifier(n_estimators=10, n_jobs=1)
    sfs = SequentialFeatureSelector(est, n_features_to_select=n_features, n_jobs=4)

    # minimally prepare dataset        
    X = data[features]
    y = data['label']

    print(X.head())
    if transform == 'interval':
        import torch
        tensor = torch.from_numpy(X.values.reshape(len(X),1,len(X.columns)).astype(numpy.float32))
        X = IntervalModel(input_length=len(X.columns)).fit_transform(tensor, None).numpy()
    else if transform == 'none':
        X = X.values
    else:
        raise ValueError(f'Unknown transform: {transform}')

    print('XX', X.shape)

    X = X.astype('float32')
    y = LabelEncoder().fit_transform(y.astype('str'))
    # split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=1)

    # perform the search
    sfs.fit(X_train, y_train)

    # FIXME: find feature names, return
    selected = sfs.get_support()
    print(selected)

    X_train = X_train[:, selected]
    X_test = X_test[:, selected]

    # summarize
    model = sklearn.base.clone(est)
    model.fit(X_train, y_train)
    y_hat = model.predict(X_test)
    acc = accuracy_score(y_test, y_hat)
    print("Accuracy: %.3f" % acc)

    return acc



# FIXME: test this
n_features = range(3, 6)
transforms = [ 'none', 'interval' ]
index = pandas.MultiIndex.from_product([n_features, transforms], names = ["features", "transforms"])
experiments = pandas.DataFrame(index = index).reset_index()
experiments['accuracy'] = experiments.apply(lamba r: evaluate_classifier(data, transform=r.transform, n_features=r.features))

experiments.to_csv('experiments.csv')




