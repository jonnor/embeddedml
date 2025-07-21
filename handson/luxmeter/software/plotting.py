
"""
Plotting tools
"""

import pandas
import seaborn
import numpy
import matplotlib.pyplot as plt

from analysis import load_files
from luxmeter_core import AS7343_INFO
from preprocessing import IdentityScaler

# annoying convention
pd = pandas
np = numpy


def plot_model_features(pipeline, X_train,
    feature_names=None, figsize=(12, 3),
    wavelength_min=380, wavelength_max=700,
    error_max=None, error_min=None,
    ):
    """Plot feature coefficients and regularization analysis"""
    # Get the fitted ElasticNet model
    elasticnet = pipeline.named_steps['regressor']



    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize, width_ratios=[7, 3])

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
        if c == 0.0:
            continue
        y.append(c)
        names.append(channel)
        x.append(center)

    lollipop_size = 30

    # lollipop style    
    #bars = ax1.bar(x, y, color=colors, alpha=0.7, width=5.0)
    #bars = ax1.stem(x, y)
    ax1.vlines(x, 0, y, colors='gray', linewidth=2.0, ls='--', alpha=0.5)
    ax1.scatter(x, y, s=lollipop_size, c='black', zorder=5)   # Circles

    ax1.set_xlabel('Features')
    ax1.set_ylabel('Coefficient Value')
    ax1.set_title('Feature Coefficients')
    ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    #if len(names) <= 20:
    #    ax1.set_xticks(x)
    #    ax1.set_xticklabels(names, rotation=45, ha='right')

    from matplotlib.ticker import MultipleLocator

    ax1.xaxis.set_major_locator(MultipleLocator(50))
    ax1.yaxis.set_major_locator(MultipleLocator(0.2))

    ax1.grid(True, alpha=0.3)


    # Annotate each bar near its base (y=0)
    # Alternate y-offsets for labels near y=0
    offsets = [-0.05, -0.10]  # Alternate between these values
    import matplotlib.transforms as transforms
    blended_transform = transforms.blended_transform_factory(ax1.transData, ax1.transData)
    for i, xx in enumerate(x):
        if not (xx > wavelength_min and xx < wavelength_max):
            continue
        yy = offsets[i % 2]  # alternate between 0.3 and 0.6
        ax1.text(
            xx, yy,
            names[i],
            ha='center', va='bottom',
            transform=blended_transform,
            fontweight='bold', fontsize=10, fontfamily='DejaVu Sans',
        )
        #ax1.axvline(xx, ls='--', alpha=0.30, color='black')

    ax1.set_xlim(wavelength_min, wavelength_max)


    # Add background color
    color_background_wavelengths(ax1, start=wavelength_min, end=wavelength_max)

    # Add photopic function as reference
    from luxmeter_core import photopic_interpolated
    wavelengths = numpy.linspace(wavelength_min, wavelength_max, 50)
    photopic_values = numpy.array([photopic_interpolated(wl) for wl in wavelengths])
    ax1.plot(wavelengths, photopic_values,
        label='Photopic (CIE1931)',
        color='black', alpha=0.5, linewidth=1.5,
        #transform=blended_transform,
    )


    # 2. Feature importance (absolute coefficients)
    N = 10


    ax2 = axes[1]
    nonzero_coeff_abs = coef_abs
    sorted_idx = np.argsort(coef_abs)[::-1]

    sorted_idx = [i for i in sorted_idx if coef_abs[i] > 0.0 ] # only non-zero

    top_features = min(N, len(sorted_idx))  # Show top 15 features


    feature_weight = coef_abs[sorted_idx[:top_features]]
    feature_n = range(top_features)

    #ax2.barh(range(top_features), coef_abs[sorted_idx[:top_features]], color='steelblue', alpha=0.7)
    # lollipop style
    ax2.hlines(feature_n, 0, feature_weight, color='black', alpha=0.7)
    ax2.scatter(feature_weight, range(top_features), s=lollipop_size, c='black', zorder=5)   # Circles

    ax2.set_xlabel('|Coefficient|')
    ax2.set_ylabel('Features')
    ax2.set_title(f'Top {top_features} Features by Importance')
    ax2.set_yticks(range(top_features))
    ax2.set_yticklabels([feature_names[i] for i in sorted_idx[:top_features]])
    ax2.grid(True, alpha=0.3)

    ax2.set_ylim(-0.5, N-0.5)


    # Calculate sparsity metrics
    zero_coef = np.sum(np.abs(elasticnet.coef_) < 1e-10)
    sparsity = zero_coef / len(elasticnet.coef_) * 100

    plt.tight_layout()

    metrics = {
        'coefficients': elasticnet.coef_,
        'intercept': elasticnet.intercept_,
        'feature_importance': coef_abs,
        'sparsity_percent': sparsity,
        'zero_coefficients': zero_coef
    }

    return fig, metrics


def wavelength_to_rgb_colour(wavelength):
   """Simple wavelength to RGB conversion

   XXX: unverified Claude output
   """
   if 380 <= wavelength < 440:
       R = -(wavelength - 440) / (440 - 380)
       G = 0.0
       B = 1.0
   elif 440 <= wavelength < 490:
       R = 0.0
       G = (wavelength - 440) / (490 - 440)
       B = 1.0
   elif 490 <= wavelength < 510:
       R = 0.0
       G = 1.0
       B = -(wavelength - 510) / (510 - 490)
   elif 510 <= wavelength < 580:
       R = (wavelength - 510) / (580 - 510)
       G = 1.0
       B = 0.0
   elif 580 <= wavelength < 645:
       R = 1.0
       G = -(wavelength - 645) / (645 - 580)
       B = 0.0
   elif 645 <= wavelength <= 780:
       R = 1.0
       G = 0.0
       B = 0.0
   else:
       R = G = B = 0.0
   
   return (R, G, B)


def color_background_wavelengths(ax, start=380, end=800, r=1):

    wl_range = np.arange(start, end, r)
    colors = np.array([wavelength_to_rgb_colour(wl) for wl in wl_range])

    # Create gradient that spans full height regardless of y-limits
    gradient = colors.reshape(1, -1, 3)
    ax.imshow(gradient, aspect='auto', 
              extent=[start, end, 0, 1],  # 0 to 1 in axes coordinates
              transform=ax.get_xaxis_transform(),  # X in data coords, Y in axes coords
              alpha=0.2, zorder=0)


def plot_evaluation(pipeline, X_train, X_test, y_train, y_test, figsize=(12.4, 6),
    error_threshold=20,
    error_min=None, error_max=None,
    scale_predict=1.0):
    """Create evaluation plots comparing train and test data"""
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    if error_max is not None and error_min is None:
        error_min = -error_max

    # Predict
    y_pred_train = pipeline.predict(X_train) * scale_predict
    y_pred_test = pipeline.predict(X_test) * scale_predict

    y_test *= scale_predict
    y_train *= scale_predict

    # Calculate metrics
    test_mse = mean_squared_error(y_test, y_pred_test)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)

    train_r2 = r2_score(y_train, y_pred_train)
    train_mse = mean_squared_error(y_train, y_pred_train)
    train_mae = mean_absolute_error(y_train, y_pred_train)

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize)

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
    ax1.set_aspect('equal', adjustable='box')


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
    if error_max is not None:
        ax2.set_ylim(error_min, error_max)

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

    metrics = {
        'train': {'r2': train_r2, 'mae': train_mae, 'rmse': np.sqrt(train_mse)},
        'test': {'r2': test_r2, 'mae': test_mae, 'rmse': np.sqrt(test_mse)}
    }
    return fig, metrics



def plot_gridsearch_results(grid_search, alpha_range, figsize=(10, 5)):
    """Plot grid search results for alpha parameter"""

    # Extract results
    results_df = pd.DataFrame(grid_search.cv_results_)

    # Create subplots
    fig, axes = plt.subplots(1, 2, figsize=figsize)

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

    return fig, results_df


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

    return fig, results_df

