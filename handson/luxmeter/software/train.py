#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, './firmware')

import pandas
import seaborn
import numpy
import matplotlib.pyplot as plt

from analysis import load_files
from luxmeter_core import AS7343_INFO

from sklearn.linear_model import ElasticNet
from sklearn.decomposition import PCA

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_validate, StratifiedKFold, GroupShuffleSplit, GridSearchCV
from sklearn.metrics import make_scorer


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
        scoring=None, random_state=1):
    """Evaluate pipeline using cross_validate"""
    if scoring is None:
        scoring = ['neg_mean_absolute_error', 'r2']

    if features is None:
        features = [ c for c in data.columns if 'ch_F' in c]

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
    plot_gridsearch_results(grid_search, alpha_range)
    plot_sparsity_vs_alpha(grid_search)

    pipeline = grid_search.best_estimator_

    plot_evaluation(pipeline,  X_train, X_test, y_train, y_test)
    # FIXME: feature names not correct when preprocessing like PCA has been used
    plot_model_features(pipeline,  X_train, feature_names=X.columns)


    return pipeline, features


def create_pipeline(n_components=10):
    """Create sklearn pipeline with MinMaxScaler and ElasticNet"""
    pipeline = Pipeline([
        #('scaler', StandardScaler()),
        ('scaler', MinMaxScaler()),
        #('pca', PCA(n_components=n_components, random_state=42)),
        ('regressor', ElasticNet(alpha=0.0001, l1_ratio=0.5, random_state=42, max_iter=100000, positive=True, fit_intercept=True))
        #('regressor', RandomForestRegressor()),
    ])
    return pipeline



def plot_model_features(pipeline, X_train, feature_names=None, figsize=(12, 4)):
    """Plot feature coefficients and regularization analysis"""
    # Get the fitted ElasticNet model
    elasticnet = pipeline.named_steps['regressor']

    # Create subplots
    fig, axes = plt.subplots(1, 3, figsize=figsize)
    fig.suptitle('ElasticNet Model Feature Analysis', fontsize=16, fontweight='bold')

    # 1. Feature coefficients bar plot
    ax1 = axes[0]
    coef_abs = np.abs(elasticnet.coef_)
    colors = ['red' if c < 0 else 'blue' for c in elasticnet.coef_]

    channels = pandas.DataFrame(AS7343_INFO).set_index('channel')

    x = []
    y = []
    names = []
    for i, name in enumerate(feature_names):
        c = elasticnet.coef_[i]
        #name = channels['channel']
        channel = name.removeprefix('ch_')
        try:
            center = channels['peak_wavelength'].loc[channel]
        except KeyError:
            print('Unknown feature', name)
            continue
        y.append(c)
        names.append(channel)
        x.append(center)

    bars = ax1.bar(x, y, color=colors, alpha=0.7, width=5.0)
    ax1.set_xlabel('Features')
    ax1.set_ylabel('Coefficient Value')
    ax1.set_title('Feature Coefficients')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    #if len(names) <= 20:
    #    ax1.set_xticks(x)
    #    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)

    # Annotate each bar near its base (y=0)
    # Alternate y-offsets for labels near y=0
    offsets = [0.0, 0.1]  # Alternate between these values
    import matplotlib.transforms as transforms
    blended_transform = transforms.blended_transform_factory(ax1.transData, ax1.transAxes)
    for i, bar in enumerate(bars):
        x = bar.get_x() + bar.get_width() / 2
        y = offsets[i % 2]  # alternate between 0.3 and 0.6
        ax1.text(
            x, y,
            names[i],
            ha='center', va='bottom',
            transform=blended_transform,
            fontweight='bold', fontsize=12, fontfamily='DejaVu Sans',
        )
        ax1.axvline(x, ls='--', alpha=0.30, color='black')

    ax1.set_xlim(350, 900)

    # Add photopic function as reference
    from luxmeter_core import photopic_interpolated
    wavelengths = numpy.linspace(350, 900, 50)
    photopic_values = numpy.array([photopic_interpolated(wl) for wl in wavelengths])
    ax1.plot(wavelengths, photopic_values,
        label='Photopic (CIE1931)',
        color='black', alpha=0.5, linewidth=1.5, transform=blended_transform)


    # 2. Feature importance (absolute coefficients)
    ax2 = axes[1]
    sorted_idx = np.argsort(coef_abs)[::-1]
    top_features = min(15, len(sorted_idx))  # Show top 15 features

    ax2.barh(range(top_features), coef_abs[sorted_idx[:top_features]], color='steelblue', alpha=0.7)
    ax2.set_xlabel('|Coefficient|')
    ax2.set_ylabel('Features')
    ax2.set_title(f'Top {top_features} Features by Importance')
    ax2.set_yticks(range(top_features))
    ax2.set_yticklabels([feature_names[i] for i in sorted_idx[:top_features]])
    ax2.grid(True, alpha=0.3)

    # 4. Model parameters and sparsity info
    ax4 = axes[2]
    ax4.axis('off')

    # Calculate sparsity metrics
    zero_coef = np.sum(np.abs(elasticnet.coef_) < 1e-10)
    sparsity = zero_coef / len(elasticnet.coef_) * 100

    model_info = f"""
    ElasticNet Parameters:

    Alpha (λ): {elasticnet.alpha:.4f}
    L1 Ratio: {elasticnet.l1_ratio:.4f}

    Model Statistics:

    Total Features: {len(elasticnet.coef_)}
    Zero Coefficients: {zero_coef}
    Sparsity: {sparsity:.1f}%

    Intercept: {elasticnet.intercept_:.4f}

    Coefficient Stats:
    Max: {np.max(elasticnet.coef_):.4f}
    Min: {np.min(elasticnet.coef_):.4f}
    Mean: {np.mean(elasticnet.coef_):.4f}
    Std: {np.std(elasticnet.coef_):.4f}
    """

    ax4.text(0.1, 0.9, model_info, transform=ax4.transAxes, fontsize=11,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.8))

    plt.tight_layout()
    fig.savefig('model_features.png')

    return {
        'coefficients': elasticnet.coef_,
        'intercept': elasticnet.intercept_,
        'feature_importance': coef_abs,
        'sparsity_percent': sparsity,
        'zero_coefficients': zero_coef
    }



def plot_evaluation(pipeline, X_train, X_test, y_train, y_test, figsize=(10, 5), error_threshold=50):
    """Create evaluation plots comparing train and test data"""
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    # Fit pipeline and predict
    pipeline.fit(X_train, y_train)
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)

    # Calculate metrics
    test_mse = mean_squared_error(y_test, y_pred_test)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)

    train_r2 = r2_score(y_train, y_pred_train)
    train_mse = mean_squared_error(y_train, y_pred_train)
    train_mae = mean_absolute_error(y_train, y_pred_train)

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle('Model Evaluation: Train vs Test Comparison', fontsize=16, fontweight='bold')

    # 1. Actual vs Predicted for both train and test
    ax1 = axes[0]

    # Plot training data
    ax1.scatter(y_train, y_pred_train, alpha=0.5, s=30, color='lightblue', 
                label=f'Train (R²={train_r2:.3f})', edgecolors='blue', linewidth=0.5)

    # Plot test data
    ax1.scatter(y_test, y_pred_test, alpha=0.7, s=50, color='orange', 
                label=f'Test (R²={test_r2:.3f})', edgecolors='red', linewidth=0.5)


    # Perfect prediction line
    all_values = np.concatenate([y_train, y_test, y_pred_train, y_pred_test])
    min_val, max_val = all_values.min(), all_values.max()
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, alpha=0.8, label='Perfect Prediction')

    # Reference lines at ±error_threshold
    ax1.plot([min_val, max_val], [min_val + error_threshold, max_val + error_threshold], 'g:', lw=1.5, alpha=0.7, label=f'+{error_threshold} Error')
    ax1.plot([min_val, max_val], [min_val - error_threshold, max_val - error_threshold], 'g:', lw=1.5, alpha=0.7, label=f'-{error_threshold} Error')

    ax1.set_xlabel('Actual Values')
    ax1.set_ylabel('Predicted Values')
    ax1.set_title('Actual vs Predicted')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Residuals plot for both train and test
    ax2 = axes[1]

    train_residuals = y_train - y_pred_train
    test_residuals = y_test - y_pred_test

    ax2.scatter(y_pred_train, train_residuals, alpha=0.5, s=30, color='lightblue', 
                label='Train', edgecolors='blue', linewidth=0.5)
    ax2.scatter(y_pred_test, test_residuals, alpha=0.7, s=50, color='orange', 
                label='Test', edgecolors='red', linewidth=0.5)

    ax2.axhline(y=0, color='r', linestyle='--', lw=2, alpha=0.8)
    ax2.axhline(y=error_threshold, color='g', linestyle=':', lw=1.5, alpha=0.7, label=f'+{error_threshold} Error')
    ax2.axhline(y=-error_threshold, color='g', linestyle=':', lw=1.5, alpha=0.7, label=f'-{error_threshold} Error')

    ax2.set_xlabel('Predicted Values')
    ax2.set_ylabel('Residuals')
    ax2.set_title('Residuals vs Predicted')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    fig.savefig('evaluation.png')

    # Print metrics comparison
    print("\nMetrics Comparison:")
    print(f"{'Metric':<25} {'Train':<12} {'Test':<12} {'Difference':<12}")
    print("-" * 65)
    print(f"{'R² Score':<25} {train_r2:<12.4f} {test_r2:<12.4f} {abs(train_r2-test_r2):<12.4f}")
    print(f"{'RMSE':<25} {np.sqrt(train_mse):<12.4f} {np.sqrt(test_mse):<12.4f} {abs(np.sqrt(train_mse)-np.sqrt(test_mse)):<12.4f}")
    print(f"{'Mean Absolute Error':<25} {mean_absolute_error(y_train, y_pred_train):<12.4f} {test_mae:<12.4f} {abs(mean_absolute_error(y_train, y_pred_train)-test_mae):<12.4f}")
    print(f"{'Sample Size':<25} {len(y_train):<12} {len(y_test):<12}")

    return {
        'train': {'r2': train_r2, 'mae': train_mae, 'rmse': np.sqrt(train_mse)},
        'test': {'r2': test_r2, 'mae': test_mae, 'rmse': np.sqrt(test_mse)}
    }



def plot_gridsearch_results(grid_search, alpha_range, figsize=(10, 5)):
    """Plot grid search results for alpha parameter"""

    # Extract results
    results_df = pd.DataFrame(grid_search.cv_results_)

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle('ElasticNet Alpha Grid Search Results', fontsize=16, fontweight='bold')

    feature = 'rmse'
    mean_train_score = -results_df['mean_train_'+feature]
    mean_test_score = -results_df['mean_test_'+feature]
    param = 'regressor__alpha'

    # 1. Validation curve
    ax1 = axes[0]
    ax1.semilogx(alpha_range, mean_test_score, 'b-', label='CV Score', linewidth=2)
    ax1.fill_between(alpha_range, 
                     mean_test_score - results_df['std_test_'+feature],
                     mean_test_score + results_df['std_test_'+feature],
                     alpha=0.2, color='blue')


    ax1.semilogx(alpha_range, mean_train_score, 'r--', label='Train Score', linewidth=2)
    ax1.axvline(grid_search.best_params_[param], color='green', 
                linestyle=':', linewidth=2, label=f"Best α={grid_search.best_params_[param]:.4f}")

    ax1.set_xlabel('Alpha (log scale)')
    ax1.set_ylabel(feature)
    ax1.set_title('Validation Curve')
    ax1.legend()
    ax1.grid(True, alpha=0.3)


    # 4. Results summary
    ax4 = axes[1]
    ax4.axis('off')

    best_score = grid_search.best_score_
    best_alpha = grid_search.best_params_[param]
    best_std = results_df.loc[results_df['param_'+param] == best_alpha, 'std_test_'+feature].iloc[0]

    
    summary_text = f"""
    Grid Search Results:
    
    Best Alpha: {best_alpha:.6f}
    Best CV Score: {-best_score:.2f} ± {best_std:.2f}
    
    Alpha Range:
    Min: {alpha_range.min():.6f}
    Max: {alpha_range.max():.2f}
    Total Tested: {len(alpha_range)}
    
    Performance at extremes:
    Smallest α: {mean_test_score.iloc[0]:.2f}
    Largest α: {mean_test_score.iloc[-1]:.2f}
    """
    
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    

    plt.tight_layout()
    fig.savefig('gridsearch.png')

    return results_df


def plot_sparsity_vs_alpha(grid_search, figsize=(10, 5)):
    """Plot sparsity metrics using grid search results"""
    
    regressor = grid_search.best_estimator_.named_steps['regressor']
    param = 'regressor__alpha'
    metric = 'rmse'


    # Extract results from grid search cv_results_
    results_df = pd.DataFrame(grid_search.cv_results_)

    alpha_range = results_df['param_'+param].values
    
    # Extract sparsity metrics (note: sparsity scorer returns negative values)
    sparsity_percentages = -results_df['mean_test_sparsity_pct'].values
    num_nonzero_features = results_df['mean_test_num_nonzero'].values
    
    total_features = len(regressor.coef_)
    l1_ratio = regressor.l1_ratio
    
    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(f'Feature Sparsity vs Alpha (from Grid Search)', fontsize=16, fontweight='bold')
    

    # Highlight best alpha from grid search
    best_alpha = grid_search.best_params_[param]
    best_alpha_idx = list(alpha_range).index(best_alpha)
    best_sparsity = sparsity_percentages[best_alpha_idx]
    
    
    # 2. Number of non-zero features vs alpha
    ax2 = axes[0]
    ax2.semilogx(alpha_range, num_nonzero_features, 'g-', linewidth=2, marker='s', markersize=4)
    
    # Highlight best alpha
    best_nonzero = num_nonzero_features[best_alpha_idx]
    ax2.scatter(best_alpha, best_nonzero, color='red', s=100, zorder=5,
                label=f'Best α: {best_nonzero:.0f} features')
    
    ax2.set_xlabel('Alpha (log scale)')
    ax2.set_ylabel('Number of Non-Zero Features')
    ax2.set_title('Active Features vs Alpha')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0, total_features)
    
    # Add reference line for total features
    ax2.axhline(y=total_features, color='gray', linestyle='--', alpha=0.7, 
                label=f'Total features ({total_features})')
    ax2.legend()
    
    # 3. Performance vs Sparsity trade-off
    ax3 = axes[1]
    scores = -results_df['mean_test_'+metric].values
    
    # Create scatter plot of MSE vs Sparsity
    scatter = ax3.scatter(sparsity_percentages, scores, c=np.log10(alpha_range), 
                         cmap='viridis', s=60, alpha=0.7)
    
    # Highlight best alpha
    ax3.scatter(best_sparsity, scores[best_alpha_idx], color='red', s=100, 
                zorder=5, label=f'Best (α={best_alpha:.4f})')
    
    ax3.set_xlabel('Sparsity (%)')
    ax3.set_ylabel(metric)
    ax3.set_title('Performance vs Sparsity Trade-off')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax3)
    cbar.set_label('log₁₀(α)')
    
    plt.tight_layout()
    fig.savefig('sparsity.png')


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

    data = load_files('./data/one')
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

