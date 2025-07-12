#!/usr/bin/env python
# coding: utf-8

import sys
sys.path.insert(0, '../software')

import pandas
import seaborn
import numpy
import matplotlib.pyplot as plt

from analysis import load_files

from sklearn.linear_model import ElasticNet

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import cross_validate, StratifiedKFold, train_test_split, GridSearchCV
import numpy as np


pd = pandas
np = numpy


def evaluate_pipeline(pipeline, X, y, cv=5, test_size=0.30, scoring=None, random_state=1):
    """Evaluate pipeline using cross_validate"""
    if scoring is None:
        scoring = ['neg_mean_absolute_error', 'r2']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    grid_search, alpha_range = gridsearch_alpha(X_train, y_train)

    # Plot grid search results
    grid_results = plot_gridsearch_results(grid_search, alpha_range)
    pipeline = grid_search.best_estimator_

    #scores = cross_validate(pipeline, X_train, y_train, cv=cv, scoring=scoring, return_train_score=True)

    plot_evaluation(pipeline,  X_train, X_test, y_train, y_test)
    plot_model_features(pipeline,  X_train, feature_names=X.columns)

    return pandas.DataFrame(scores)


def create_pipeline():
    """Create sklearn pipeline with MinMaxScaler and ElasticNet"""
    pipeline = Pipeline([
        #('scaler', StandardScaler()),
        #('scaler', MinMaxScaler()),
        ('regressor', ElasticNet(alpha=0.0001, l1_ratio=0.5, random_state=42, max_iter=100000, positive=True))
        #('regressor', RandomForestRegressor()),
    ])
    return pipeline



def plot_model_features(pipeline, X_train, feature_names=None, figsize=(15, 10)):
    """Plot feature coefficients and regularization analysis"""
    # Get the fitted ElasticNet model
    elasticnet = pipeline.named_steps['regressor']

    # Feature names
    if feature_names is None:
        feature_names = [f'Feature_{i}' for i in range(len(elasticnet.coef_))]

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle('ElasticNet Model Feature Analysis', fontsize=16, fontweight='bold')

    # 1. Feature coefficients bar plot
    ax1 = axes[0, 0]
    coef_abs = np.abs(elasticnet.coef_)
    colors = ['red' if c < 0 else 'blue' for c in elasticnet.coef_]
    bars = ax1.bar(range(len(elasticnet.coef_)), elasticnet.coef_, color=colors, alpha=0.7)
    ax1.set_xlabel('Features')
    ax1.set_ylabel('Coefficient Value')
    ax1.set_title('Feature Coefficients')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    if len(feature_names) <= 20:
        ax1.set_xticks(range(len(feature_names)))
        ax1.set_xticklabels(feature_names, rotation=45, ha='right')
    ax1.grid(True, alpha=0.3)

    # 2. Feature importance (absolute coefficients)
    ax2 = axes[0, 1]
    sorted_idx = np.argsort(coef_abs)[::-1]
    top_features = min(15, len(sorted_idx))  # Show top 15 features

    ax2.barh(range(top_features), coef_abs[sorted_idx[:top_features]], color='steelblue', alpha=0.7)
    ax2.set_xlabel('|Coefficient|')
    ax2.set_ylabel('Features')
    ax2.set_title(f'Top {top_features} Features by Importance')
    ax2.set_yticks(range(top_features))
    ax2.set_yticklabels([feature_names[i] for i in sorted_idx[:top_features]])
    ax2.grid(True, alpha=0.3)

    # 3. Coefficient distribution
    ax3 = axes[1, 0]
    ax3.hist(elasticnet.coef_, bins=20, alpha=0.7, color='lightgreen', edgecolor='black')
    ax3.axvline(0, color='red', linestyle='--', lw=2, label='Zero')
    ax3.axvline(np.mean(elasticnet.coef_), color='orange', linestyle='--', lw=2, label=f'Mean: {np.mean(elasticnet.coef_):.3f}')
    ax3.set_xlabel('Coefficient Value')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Distribution of Coefficients')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Model parameters and sparsity info
    ax4 = axes[1, 1]
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
    plt.show()

    return {
        'coefficients': elasticnet.coef_,
        'intercept': elasticnet.intercept_,
        'feature_importance': coef_abs,
        'sparsity_percent': sparsity,
        'zero_coefficients': zero_coef
    }



def plot_evaluation(pipeline, X_train, X_test, y_train, y_test, figsize=(12, 8), error_threshold=50):
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
    plt.show()

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



def plot_gridsearch_results(grid_search, alpha_range, figsize=(12, 8)):
    """Plot grid search results for alpha parameter"""

    # Extract results
    results_df = pd.DataFrame(grid_search.cv_results_)

    # Create subplots
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    fig.suptitle('ElasticNet Alpha Grid Search Results', fontsize=16, fontweight='bold')

    mean_train_score = -results_df['mean_train_score']
    mean_test_score = -results_df['mean_test_score']
    param = 'regressor__alpha'


    # 1. Validation curve
    ax1 = axes[0, 0]
    ax1.semilogx(alpha_range, mean_test_score, 'b-', label='CV Score', linewidth=2)
    ax1.fill_between(alpha_range, 
                     mean_test_score - results_df['std_test_score'],
                     mean_test_score + results_df['std_test_score'],
                     alpha=0.2, color='blue')


    ax1.semilogx(alpha_range, mean_train_score, 'r--', label='Train Score', linewidth=2)
    ax1.axvline(grid_search.best_params_[param], color='green', 
                linestyle=':', linewidth=2, label=f"Best α={grid_search.best_params_[param]:.4f}")

    ax1.set_xlabel('Alpha (log scale)')
    ax1.set_ylabel('Mean Squared Error')
    ax1.set_title('Validation Curve')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # 2. Score vs Alpha (linear scale for detail)
    ax2 = axes[0, 1]
    ax2.plot(alpha_range, mean_test_score, 'bo-', markersize=4, label='CV Score')
    ax2.axvline(grid_search.best_params_[param], color='green', 
                linestyle=':', linewidth=2, label=f"Best α={grid_search.best_params_[param]:.4f}")
    ax2.set_xlabel('Alpha')
    ax2.set_ylabel('Mean Squared Error')
    ax2.set_title('CV Score vs Alpha (Linear Scale)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # 3. Train vs Validation scores
    ax3 = axes[1, 0]
    ax3.semilogx(alpha_range, mean_train_score, 'r-', label='Train', linewidth=2)
    ax3.semilogx(alpha_range, mean_test_score, 'b-', label='Validation', linewidth=2)
    ax3.axvline(grid_search.best_params_[param], color='green', 
                linestyle=':', linewidth=2, label='Best α')
    ax3.set_xlabel('Alpha (log scale)')
    ax3.set_ylabel('Mean Squared Error')
    ax3.set_title('Training vs Validation Score')
    ax3.legend()
    ax3.grid(True, alpha=0.3)

    # 4. Results summary
    ax4 = axes[1, 1]
    ax4.axis('off')

    best_score = grid_search.best_score_
    best_alpha = grid_search.best_params_[param]
    best_std = results_df.loc[results_df['param_'+param] == best_alpha, 'std_test_score'].iloc[0]

    
    summary_text = f"""
    Grid Search Results:
    
    Best Alpha: {best_alpha:.6f}
    Best CV Score: {-best_score:.4f} ± {best_std:.4f}
    
    Alpha Range:
    Min: {alpha_range.min():.6f}
    Max: {alpha_range.max():.2f}
    Total Tested: {len(alpha_range)}
    
    Scoring: {grid_search.scoring}
    CV Folds: {grid_search.cv}
    
    Performance at extremes:
    Smallest α: {mean_test_score.iloc[0]:.4f}
    Largest α: {mean_test_score.iloc[-1]:.4f}
    """
    
    ax4.text(0.1, 0.9, summary_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    

    plt.tight_layout()
    plt.show()

    return results_df


def gridsearch_alpha(X_train, y_train, cv=5, scoring='neg_root_mean_squared_error'):
    """Perform grid search over alpha parameter for ElasticNet"""

    # Create pipeline
    pipeline = create_pipeline()

    # Define alpha range - typical values from very small to large
    alpha_range = np.logspace(-6, 0.5, 25)

    # Alternative ranges you might consider:

    param_grid = {
        'regressor__alpha': alpha_range
    }

    # Perform grid search
    grid_search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=cv, 
        scoring=scoring,
        return_train_score=True,
        n_jobs=-1,
        verbose=1
    )

    grid_search.fit(X_train, y_train)

    return grid_search, alpha_range


def main():

    data = load_files('./data/one')
    #print(data.shape)
    #data.head(5)

    avg = data.groupby(['filename']).agg('median', numeric_only=True)
    print(avg.shape)
    print(avg.head())

    features = [ c for c in data.columns if 'ch_F' in c]
    print(features)
    #sub = avg[avg.colortemp == 2500]
    sub = avg.copy()
    X = sub[features] / 1000.0
    y = sub['lux']

    est = create_pipeline()

    scores = evaluate_pipeline(est, X, y)
    scores


if __name__ == '__main__':
    main()

