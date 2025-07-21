#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, './firmware')

import pandas
import seaborn
import numpy
import matplotlib.pyplot as plt


from sklearn.linear_model import ElasticNet
from sklearn.decomposition import PCA

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestRegressor

from sklearn.linear_model import ElasticNet
from sklearn.linear_model import QuantileRegressor
#from sklearn.linear_model import SGDRegressor

from sklearn.model_selection import cross_validate, GroupShuffleSplit, GridSearchCV
from sklearn.metrics import make_scorer

from analysis import load_files
from luxmeter_core import AS7343_INFO
from preprocessing import IdentityScaler
from plotting import plot_gridsearch_results, plot_sparsity_vs_alpha, plot_evaluation, plot_model_features

# annoying convention
pd = pandas
np = numpy


def sparsity_percentage_scorer(estimator, X=None, y=None):
    """Custom scorer for sparsity percentage"""
    model = estimator.named_steps['regressor']
    zero_coef = np.sum(np.abs(model.coef_) < 1e-10)
    return (zero_coef / len(model.coef_)) * 100

def num_nonzero_features_scorer(estimator, X=None, y=None):
    """Custom scorer for number of non-zero features"""
    model = estimator.named_steps['regressor']
    return np.sum(np.abs(model.coef_) >= 1e-10)


def evaluate_pipeline(pipeline, data,
        group='colortemp', target='lux',
        features=None, cv=5, test_size=0.30,
        scoring=None, random_state=1,
        scale_predict=1.0,
        error_threshold=20,
        ):
    """Evaluate pipeline using cross_validate"""
    if scoring is None:
        scoring = ['neg_mean_absolute_error', 'r2']

    if features is None:
        features = [ c for c in data.columns if 'ch_F' in c]

    data = data.reset_index()
    X = data[features]
    y = data[target]
    groups = data[group]

    # Split respecting groups
    train_inds, test_inds = next(GroupShuffleSplit(n_splits=1, test_size=test_size).split(X, y, groups))
    X_train, X_test = X.iloc[train_inds], X.iloc[test_inds]
    y_train, y_test = y.iloc[train_inds], y.iloc[test_inds]
    groups_train = groups.iloc[train_inds]
    
    splitter = GroupShuffleSplit(n_splits=cv)
    grid_search, alpha_range = gridsearch_alpha(X_train, y_train, cv=splitter, groups=groups_train)

    # Plot grid search results
    gridsearch_fig, _ = plot_gridsearch_results(grid_search, alpha_range)
    sparsity_fig, _ = plot_sparsity_vs_alpha(grid_search)

    # Fit on entire training data
    pipeline = grid_search.best_estimator_
    pipeline.fit(X_train, y_train)

    predictions_fig, _ = plot_evaluation(pipeline,  X_train, X_test, y_train, y_test,
        scale_predict=scale_predict, error_threshold=error_threshold)
    features_fig, _ = plot_model_features(pipeline,  X_train, feature_names=X.columns)

    # Error analysis
    results = data.copy()
    results.loc[train_inds, 'split'] = 'train'
    results.loc[test_inds, 'split'] = 'test'
    results['out'] = pipeline.predict(results[features]) * scale_predict
    results['error'] = results['out'] - (results[target] * scale_predict)

    figures = {
        'gridsearch': gridsearch_fig,
        'sparsity': sparsity_fig,
        'features': features_fig,
        'predictions': predictions_fig,
    }

    return pipeline, features, results, figures





def create_pipeline(n_components=10, positive=True, fit_intercept=True, scaler=MinMaxScaler):
    """Create sklearn pipeline with MinMaxScaler and ElasticNet"""

    pipeline = Pipeline([
        #('scaler', StandardScaler()),
        ('scaler', scaler()),
        #('regressor', ElasticNet(alpha=0.0001, l1_ratio=0.5, random_state=42, max_iter=100000, positive=positive, fit_intercept=fit_intercept))

        # QuantileRegressor is more robust, has ability to reject some outliers in training data
        ('regressor', QuantileRegressor(quantile=0.5, alpha=0.01, solver='highs', fit_intercept=fit_intercept)),
        #('regressor', SGDRegressor(loss='huber', penalty='elasticnet', l1_ratio=0.5, alpha=0.01, epsilon=1.35)),
        #('regressor', SGDRegressor(loss='epsilon_insensitive', penalty='elasticnet', l1_ratio=0.5, alpha=0.01, epsilon=0.1)),
    ])
    return pipeline


def gridsearch_alpha(X_train, y_train, cv=5, groups=None):
    """Perform grid search over alpha parameter for ElasticNet"""

    # Create pipeline
    pipeline = create_pipeline()

    # Define alpha range - typical values from very small to large
    alpha_range = np.logspace(-4, 0.5, 25)

    param_grid = {
        'regressor__alpha': alpha_range
    }

    # Create custom scorers
    sparsity_scorer = sparsity_percentage_scorer
    nonzero_scorer = num_nonzero_features_scorer
    

    scoring = {
        'rmse': 'neg_root_mean_squared_error',
        'mae': 'neg_mean_absolute_error',
        'r2': 'r2',
        'sparsity_pct': sparsity_scorer,
        'num_nonzero': nonzero_scorer
    }

    # Perform grid search
    grid_search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=cv, 
        scoring=scoring,
        return_train_score=True,
        refit='rmse',
        n_jobs=4,
        verbose=1
    )

    grid_search.fit(X_train, y_train, groups=groups)

    return grid_search, alpha_range


def main():

    data = load_files('./data/one', fixup_shape=True)
    #print(data.shape)
    #data.head(5)

    sampled = data.groupby('filename', group_keys=False).apply(lambda df: df.head(7).tail(1))

    avg = sampled.groupby(['filename']).agg('median', numeric_only=True)
    print(avg.shape)
    print(avg.head())

    est = create_pipeline()

    scores = evaluate_pipeline(est, avg)


if __name__ == '__main__':
    main()

