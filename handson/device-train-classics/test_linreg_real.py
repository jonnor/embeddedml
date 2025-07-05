import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import time
import warnings
warnings.filterwarnings('ignore')

# Import your implementation
try:
    import elastic_net_linear as enl
    CUSTOM_MODEL_AVAILABLE = True
    print("✓ Custom elastic_net_linear module loaded successfully")
except ImportError as e:
    print(f"✗ Failed to import custom module: {e}")
    print("Please ensure elastic_net_linear is compiled and available")
    CUSTOM_MODEL_AVAILABLE = False

def compare_models(X_train, X_test, y_train, y_test, config, dataset_name, scale_features=False):
    """
    Compare sklearn and custom ElasticNet implementations on given dataset.
    
    Parameters:
    - X_train, X_test, y_train, y_test: Training and test data
    - config: Dictionary with alpha, l1_ratio, and name
    - dataset_name: Name of dataset for logging
    - scale_features: Whether to apply StandardScaler to features
    
    Returns:
    - Dictionary with comparison results
    """
    print(f"\n--- {config['name']} (α={config['alpha']}, l1_ratio={config['l1_ratio']}) ---")
    
    # Apply feature scaling if requested
    if scale_features:
        print("Applying feature scaling...")
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        print(f"Feature scaling applied - mean: {X_train_scaled.mean():.6f}, std: {X_train_scaled.std():.6f}")
    else:
        X_train_scaled = X_train
        X_test_scaled = X_test
        print(f"No feature scaling - original data range: [{X_train.min():.2f}, {X_train.max():.2f}]")
    
    # Convert to contiguous float32 arrays for custom implementation
    X_train_f32 = np.ascontiguousarray(X_train_scaled, dtype=np.float32)
    X_test_f32 = np.ascontiguousarray(X_test_scaled, dtype=np.float32)
    y_train_f32 = np.ascontiguousarray(y_train, dtype=np.float32)
    y_test_f32 = np.ascontiguousarray(y_test, dtype=np.float32)
    
    # sklearn ElasticNet
    print("Training sklearn ElasticNet...")
    start_time = time.time()
    sklearn_model = ElasticNet(
        alpha=config['alpha'], 
        l1_ratio=config['l1_ratio'], 
        max_iter=2000,
        random_state=42
    )
    sklearn_model.fit(X_train_scaled, y_train)
    sklearn_time = time.time() - start_time
    
    sklearn_pred = sklearn_model.predict(X_test_scaled)
    sklearn_r2 = r2_score(y_test, sklearn_pred)
    sklearn_mse = mean_squared_error(y_test, sklearn_pred)
    sklearn_mae = mean_absolute_error(y_test, sklearn_pred)
    sklearn_nonzero = np.sum(np.abs(sklearn_model.coef_) > 1e-6)
    
    print(f"sklearn - R²: {sklearn_r2:.6f}, MSE: {sklearn_mse:.6f}, MAE: {sklearn_mae:.6f}")
    print(f"sklearn - Non-zero weights: {sklearn_nonzero}/{len(sklearn_model.coef_)}")
    print(f"sklearn - Training time: {sklearn_time:.3f}s")
    
    result = {
        'config': config['name'],
        'dataset': dataset_name,
        'scaled': scale_features,
        'sklearn_r2': sklearn_r2,
        'sklearn_mse': sklearn_mse,
        'sklearn_mae': sklearn_mae,
        'sklearn_time': sklearn_time,
        'sklearn_nonzero': sklearn_nonzero,
        'n_features': len(sklearn_model.coef_)
    }
    
    # Your implementation
    if CUSTOM_MODEL_AVAILABLE:
        print("Training custom ElasticNet...")
        start_time = time.time()
        custom_model = enl.ElasticNetRegression(
            alpha=config['alpha'],
            l1_ratio=config['l1_ratio'],
            learning_rate=0.01,
            max_iterations=2000,
            tolerance=1e-6,
            verbose=False
        )
        
        try:
            custom_model.fit(X_train_f32, y_train_f32)
            custom_time = time.time() - start_time
            
            custom_pred = custom_model.predict(X_test_f32)
            
            # Debug: Check for NaN/infinite values
            if not np.all(np.isfinite(custom_pred)):
                print(f"⚠ WARNING: Custom model predictions contain NaN or infinite values!")
                print(f"  NaN count: {np.sum(np.isnan(custom_pred))}")
                print(f"  Infinite count: {np.sum(np.isinf(custom_pred))}")
                print(f"  Weights: {custom_model.coef_}")
                print(f"  Bias: {custom_model.intercept_}")
                
                # Skip this configuration
                print("Skipping this configuration due to numerical issues...")
                return result
            
            custom_r2 = custom_model.score(X_test_f32, y_test_f32)
            custom_mse = custom_model.mean_squared_error(X_test_f32, y_test_f32)
            custom_mae = mean_absolute_error(y_test_f32, custom_pred)
            custom_nonzero = custom_model.count_nonzero_weights()
            
            print(f"Custom  - R²: {custom_r2:.6f}, MSE: {custom_mse:.6f}, MAE: {custom_mae:.6f}")
            print(f"Custom  - Non-zero weights: {custom_nonzero}/{custom_model.n_features_}")
            print(f"Custom  - Training time: {custom_time:.3f}s")
            
            # Compare coefficients
            coef_diff = np.mean(np.abs(sklearn_model.coef_ - custom_model.coef_))
            intercept_diff = abs(sklearn_model.intercept_ - custom_model.intercept_)
            
            print(f"Coefficient difference (MAE): {coef_diff:.6f}")
            print(f"Intercept difference: {intercept_diff:.6f}")
            print(f"R² difference: {abs(sklearn_r2 - custom_r2):.6f}")
            
            # Add custom results to result dictionary
            result.update({
                'custom_r2': custom_r2,
                'custom_mse': custom_mse,
                'custom_mae': custom_mae,
                'custom_time': custom_time,
                'custom_nonzero': custom_nonzero,
                'coef_diff': coef_diff,
                'intercept_diff': intercept_diff,
                'r2_diff': abs(sklearn_r2 - custom_r2)
            })
            
        except Exception as e:
            print(f"✗ Error training/testing custom model: {e}")
            print("This indicates a numerical stability issue in your implementation")
            
    else:
        print("Custom model not available - skipping comparison")
        
    return result

def test_california_housing(scale_features=False):
    """Test on California Housing dataset (8 features, 20,640 samples)"""
    print("\n" + "="*60)
    print(f"CALIFORNIA HOUSING DATASET TEST {'(WITH SCALING)' if scale_features else '(WITHOUT SCALING)'}")
    print("="*60)
    
    # Load data
    print("Loading California Housing dataset...")
    data = fetch_california_housing()
    X, y = data.data, data.target
    
    print(f"Dataset shape: {X.shape}")
    print(f"Target range: [{y.min():.2f}, {y.max():.2f}]")
    print(f"Features: {data.feature_names}")
    print(f"Feature ranges:")
    for i, name in enumerate(data.feature_names):
        print(f"  {name}: [{X[:, i].min():.2f}, {X[:, i].max():.2f}]")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    
    # Test different regularization settings
    test_configs = [
        {"alpha": 0.0, "l1_ratio": 0.0, "name": "No Regularization"},
        {"alpha": 0.01, "l1_ratio": 0.0, "name": "Ridge (L2)"},
        {"alpha": 0.01, "l1_ratio": 1.0, "name": "LASSO (L1)"},
        {"alpha": 0.01, "l1_ratio": 0.5, "name": "Elastic Net"},
        {"alpha": 0.1, "l1_ratio": 0.5, "name": "High Regularization"},
        {"alpha": 1.0, "l1_ratio": 0.8, "name": "Very High L1"},
    ]
    
    results = []
    for config in test_configs:
        result = compare_models(X_train, X_test, y_train, y_test, config, "California Housing", scale_features)
        results.append(result)
    
    return results

def test_communities_crime():
    """Test on Communities and Crime dataset (high-dimensional)"""
    print("\n" + "="*60)
    print("COMMUNITIES AND CRIME DATASET TEST")
    print("="*60)
    
    # Load data from UCI repository
    print("Loading Communities and Crime dataset...")
    try:
        # Download and load the dataset
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/communities/communities.data"
        
        # Load data without headers first
        data = pd.read_csv(url, header=None, na_values="?")
        
        print(f"Raw dataset shape: {data.shape}")
        print(f"Missing values: {data.isnull().sum().sum()}")
        
        # The first few columns are categorical (state, community name, etc.)
        # We'll skip the first 5 columns which are non-predictive identifiers
        # Columns 5-127 are the actual features, column 127 is the target
        
        # Skip non-predictive columns (state, community, etc.)
        print("Removing non-predictive identifier columns...")
        data_numeric = data.iloc[:, 5:]  # Skip first 5 columns
        
        print(f"After removing identifiers: {data_numeric.shape}")
        
        # Remove columns with too many missing values
        missing_threshold = 0.5  # Remove columns with >50% missing
        data_clean = data_numeric.loc[:, data_numeric.isnull().mean() < missing_threshold]
        
        print(f"After removing high-missing columns: {data_clean.shape}")
        
        # Remove rows with any missing values
        data_clean = data_clean.dropna()
        
        print(f"After removing rows with missing values: {data_clean.shape}")
        
        # Separate features and target (last column is target)
        X = data_clean.iloc[:, :-1].values
        y = data_clean.iloc[:, -1].values
        
        # Ensure we have numeric data
        try:
            X = X.astype(float)
            y = y.astype(float)
        except ValueError as e:
            print(f"Data conversion error: {e}")
            print("Checking for remaining non-numeric data...")
            
            # Find non-numeric columns
            for i in range(data_clean.shape[1]):
                col_data = data_clean.iloc[:, i]
                try:
                    col_data.astype(float)
                except ValueError:
                    print(f"Column {i} contains non-numeric data: {col_data.dtype}")
                    print(f"Sample values: {col_data.head().tolist()}")
            
            return []
        
        print(f"Final dataset shape: {X.shape}")
        print(f"Target range: [{y.min():.4f}, {y.max():.4f}]")
        print(f"Feature value ranges:")
        print(f"  Min: {X.min():.4f}")
        print(f"  Max: {X.max():.4f}")
        print(f"  Mean: {X.mean():.4f}")
        
    except Exception as e:
        print(f"Failed to load Communities and Crime dataset: {e}")
        return []
    
    # Check if we have enough data
    if X.shape[0] < 100:
        print(f"Warning: Only {X.shape[0]} samples available after cleaning")
        return []
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Standardize features (important for high-dimensional data)
    # Note: We're doing this here explicitly since we always want scaling for this dataset
    print("Applying StandardScaler (required for high-dimensional data)...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    print(f"Training set: {X_train.shape}")
    print(f"Test set: {X_test.shape}")
    print(f"After scaling - mean: {X_train_scaled.mean():.6f}, std: {X_train_scaled.std():.6f}")
    
    # Test configurations for high-dimensional data
    test_configs = [
        {"alpha": 0.001, "l1_ratio": 0.5, "name": "Low Regularization"},
        {"alpha": 0.01, "l1_ratio": 0.7, "name": "Medium L1-heavy"},
        {"alpha": 0.1, "l1_ratio": 0.9, "name": "High L1 (Sparse)"},
        {"alpha": 0.5, "l1_ratio": 0.95, "name": "Very Sparse"},
    ]
    
    results = []
    for config in test_configs:
        result = compare_models(X_train_scaled, X_test_scaled, y_train, y_test, config, "Communities Crime", scale_features=True)
        results.append(result)
    
    return results

def print_summary(california_results, crime_results):
    """Print comprehensive summary of test results"""
    print("\n" + "="*60)
    print("COMPREHENSIVE SUMMARY")
    print("="*60)
    
    if CUSTOM_MODEL_AVAILABLE and california_results:
        print("\nCalifornia Housing Dataset Results:")
        print("-" * 40)
        
        # Extract metrics
        ca_r2_diffs = [r.get('r2_diff', 0) for r in california_results if 'r2_diff' in r]
        ca_coef_diffs = [r.get('coef_diff', 0) for r in california_results if 'coef_diff' in r]
        ca_custom_r2s = [r.get('custom_r2', 0) for r in california_results if 'custom_r2' in r]
        ca_sklearn_r2s = [r.get('sklearn_r2', 0) for r in california_results if 'sklearn_r2' in r]
        
        if ca_r2_diffs:
            print(f"Average R² difference: {np.mean(ca_r2_diffs):.6f}")
            print(f"Maximum R² difference: {np.max(ca_r2_diffs):.6f}")
            print(f"Average coefficient difference: {np.mean(ca_coef_diffs):.6f}")
            print(f"Best custom R²: {np.max(ca_custom_r2s):.6f}")
            print(f"Best sklearn R²: {np.max(ca_sklearn_r2s):.6f}")
            
            # Show sparsity results
            print("\nSparsity Analysis:")
            for r in california_results:
                if 'custom_nonzero' in r:
                    sparsity = (1 - r['custom_nonzero'] / r['n_features']) * 100
                    print(f"  {r['config']}: {sparsity:.1f}% sparse ({r['custom_nonzero']}/{r['n_features']} non-zero)")
    
    if CUSTOM_MODEL_AVAILABLE and crime_results:
        print("\nCommunities & Crime Dataset Results:")
        print("-" * 40)
        
        # Extract metrics
        crime_r2_diffs = [r.get('r2_diff', 0) for r in crime_results if 'r2_diff' in r]
        crime_coef_diffs = [r.get('coef_diff', 0) for r in crime_results if 'coef_diff' in r]
        crime_custom_r2s = [r.get('custom_r2', 0) for r in crime_results if 'custom_r2' in r]
        crime_sklearn_r2s = [r.get('sklearn_r2', 0) for r in crime_results if 'sklearn_r2' in r]
        
        if crime_r2_diffs:
            print(f"Average R² difference: {np.mean(crime_r2_diffs):.6f}")
            print(f"Maximum R² difference: {np.max(crime_r2_diffs):.6f}")
            print(f"Average coefficient difference: {np.mean(crime_coef_diffs):.6f}")
            print(f"Best custom R²: {np.max(crime_custom_r2s):.6f}")
            print(f"Best sklearn R²: {np.max(crime_sklearn_r2s):.6f}")
            
            # Show sparsity results for high-dimensional data
            print("\nSparsity Analysis (High-Dimensional):")
            for r in crime_results:
                if 'custom_nonzero' in r:
                    sparsity = (1 - r['custom_nonzero'] / r['n_features']) * 100
                    print(f"  {r['config']}: {sparsity:.1f}% sparse ({r['custom_nonzero']}/{r['n_features']} non-zero)")
    
    # Overall assessment
    if CUSTOM_MODEL_AVAILABLE:
        print("\nOverall Assessment:")
        print("-" * 20)
        
        all_r2_diffs = []
        all_coef_diffs = []
        
        for results in [california_results, crime_results]:
            for r in results:
                if 'r2_diff' in r:
                    all_r2_diffs.append(r['r2_diff'])
                if 'coef_diff' in r:
                    all_coef_diffs.append(r['coef_diff'])
        
        if all_r2_diffs:
            avg_r2_diff = np.mean(all_r2_diffs)
            max_r2_diff = np.max(all_r2_diffs)
            avg_coef_diff = np.mean(all_coef_diffs)
            
            print(f"Overall average R² difference: {avg_r2_diff:.6f}")
            print(f"Overall maximum R² difference: {max_r2_diff:.6f}")
            print(f"Overall average coefficient difference: {avg_coef_diff:.6f}")
            
            # Performance assessment
            if avg_r2_diff < 0.01:
                print("✓ EXCELLENT: Very close match to sklearn")
            elif avg_r2_diff < 0.05:
                print("✓ GOOD: Acceptable match to sklearn")
            elif avg_r2_diff < 0.1:
                print("⚠ FAIR: Some differences from sklearn")
            else:
                print("✗ POOR: Significant differences from sklearn")

def run_comprehensive_test():
    """Run comprehensive test suite"""
    print("ELASTIC NET LINEAR REGRESSION COMPREHENSIVE TEST")
    print("="*80)
    
    # Test California Housing without scaling first
    print("\n🔸 Testing California Housing WITHOUT feature scaling...")
    # NOTE: unscaled values cause NaN output from our model 
    # Potential gradient explosion due to large values for some features
    #california_results_unscaled = []
    #california_results_unscaled = test_california_housing(scale_features=False)
    
    # Test California Housing with scaling 
    print("\n🔸 Testing California Housing WITH feature scaling...")
    california_results_scaled = test_california_housing(scale_features=True)
    
    # Test Communities and Crime (always scaled due to high dimensionality)
    print("\n🔸 Testing Communities and Crime...")
    crime_results = test_communities_crime()
    
    # Combine results for summary
    all_california_results = california_results_scaled
    
    # Print comprehensive summary
    print_summary(all_california_results, crime_results)
    
    print("\nTest completed!")
    

if __name__ == "__main__":
    run_comprehensive_test()


