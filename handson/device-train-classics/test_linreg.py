

# test_linear_regression.py
import numpy as np
import elastic_net_linear as enl

def test_basic_functionality():
    """Test basic functionality of the Elastic Net Linear Regression"""
    
    # Create sample data with known relationship
    np.random.seed(42)
    n_samples, n_features = 100, 5
    
    # Generate features
    X = np.random.randn(n_samples, n_features).astype(np.float32)
    
    # Create target with known coefficients: y = 2*x0 + 3*x1 + 1*x2 + 0*x3 + 0*x4 + noise
    true_coef = np.array([2.0, 3.0, 1.0, 0.0, 0.0])
    y = X @ true_coef + 0.1 * np.random.randn(n_samples)
    y = y.astype(np.float32)
    
    print("=== Elastic Net Linear Regression Test ===\n")
    print(f"Data shape: X={X.shape}, y={y.shape}")
    print(f"True coefficients: {true_coef}")
    print()
    
    # Test different regularization settings
    test_cases = [
        {"alpha": 0.0, "l1_ratio": 0.0, "name": "No regularization"},
        {"alpha": 0.01, "l1_ratio": 0.0, "name": "Ridge (L2)"},
        {"alpha": 0.01, "l1_ratio": 1.0, "name": "LASSO (L1)"},
        {"alpha": 0.01, "l1_ratio": 0.5, "name": "Elastic Net"},
    ]
    
    for case in test_cases:
        print(f"--- {case['name']} ---")
        
        # Initialize and train model
        model = enl.ElasticNetRegression(alpha=case["alpha"], l1_ratio=case["l1_ratio"])
        print(f"Model: alpha={model.alpha}, l1_ratio={model.l1_ratio}")
        
        # Fit the model
        model.fit(X, y, max_iterations=1000, verbose=False)
        
        # Make predictions
        y_pred = model.predict(X)
        
        # Calculate metrics
        r2_score = model.score(X, y)
        mse = model.mean_squared_error(X, y)
        nonzero_weights = model.count_nonzero_weights()
        
        print(f"R² Score: {r2_score:.6f}")
        print(f"MSE: {mse:.6f}")
        print(f"Non-zero weights: {nonzero_weights}/{model.n_features_}")
        print(f"Learned coefficients: {model.coef_}")
        print(f"Intercept: {model.intercept_:.6f}")
        print(f"Coefficient errors: {np.abs(model.coef_ - true_coef)}")
        print()

def test_sklearn_compatibility():
    """Test sklearn-like interface and compare with sklearn if available"""
    
    print("=== sklearn Compatibility Test ===\n")
    
    try:
        from sklearn.linear_model import ElasticNet
        from sklearn.datasets import make_regression
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score, mean_squared_error
        
        # Generate regression data
        X, y = make_regression(n_samples=200, n_features=10, noise=0.1, 
                              random_state=42, n_informative=5)
        X = X.astype(np.float32)
        y = y.astype(np.float32)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42
        )
        
        # Train our model
        our_model = enl.ElasticNetRegression(alpha=0.1, l1_ratio=0.5)
        our_model.fit(X_train, y_train, verbose=False)
        
        # Train sklearn model
        sklearn_model = ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=1000)
        sklearn_model.fit(X_train, y_train)
        
        # Compare predictions
        our_pred = our_model.predict(X_test)
        sklearn_pred = sklearn_model.predict(X_test)
        
        # Compare metrics
        our_r2 = our_model.score(X_test, y_test)
        sklearn_r2 = r2_score(y_test, sklearn_pred)
        
        our_mse = our_model.mean_squared_error(X_test, y_test)
        sklearn_mse = mean_squared_error(y_test, sklearn_pred)
        
        print("Performance Comparison:")
        print(f"Our R²:      {our_r2:.6f}")
        print(f"sklearn R²:  {sklearn_r2:.6f}")
        print(f"R² diff:     {abs(our_r2 - sklearn_r2):.6f}")
        print()
        print(f"Our MSE:     {our_mse:.6f}")
        print(f"sklearn MSE: {sklearn_mse:.6f}")
        print(f"MSE diff:    {abs(our_mse - sklearn_mse):.6f}")
        print()
        
        # Compare coefficients
        print("Coefficient Comparison:")
        print(f"Our coef:     {our_model.coef_[:5]}")  # First 5 coefficients
        print(f"sklearn coef: {sklearn_model.coef_[:5]}")
        print(f"Coef diff:    {np.abs(our_model.coef_ - sklearn_model.coef_)[:5]}")
        print()
        
        # Compare intercepts
        print(f"Our intercept:     {our_model.intercept_:.6f}")
        print(f"sklearn intercept: {sklearn_model.intercept_:.6f}")
        print(f"Intercept diff:    {abs(our_model.intercept_ - sklearn_model.intercept_):.6f}")
        print()
        
        # Sparsity comparison
        our_nonzero = our_model.count_nonzero_weights()
        sklearn_nonzero = np.sum(np.abs(sklearn_model.coef_) > 1e-6)
        
        print(f"Our non-zero weights:     {our_nonzero}")
        print(f"sklearn non-zero weights: {sklearn_nonzero}")
        
        print("sklearn compatibility test completed!")
        
    except ImportError:
        print("sklearn not available, skipping compatibility test")

def test_edge_cases():
    """Test edge cases and error handling"""
    
    print("=== Edge Cases Test ===\n")
    
    # Test with perfect data (should get exact solution)
    X_perfect = np.array([[1, 2], [2, 3], [3, 4], [4, 5]], dtype=np.float32)
    y_perfect = np.array([5, 8, 11, 14], dtype=np.float32)  # y = 1*x0 + 2*x1 + 1
    
    model = enl.ElasticNetRegression(alpha=0.0, l1_ratio=0.0)
    model.fit(X_perfect, y_perfect, verbose=False)
    
    print("Perfect linear relationship test:")
    print(f"Expected coefficients: [1.0, 2.0]")
    print(f"Learned coefficients:  {model.coef_}")
    print(f"Expected intercept: 1.0")
    print(f"Learned intercept: {model.intercept_:.6f}")
    print(f"MSE: {model.mean_squared_error(X_perfect, y_perfect):.8f}")
    print()
    
    # Test error handling
    try:
        # Test unfitted model
        unfitted_model = enl.ElasticNetRegression()
        unfitted_model.predict(X_perfect)
        print("ERROR: Should have raised exception for unfitted model")
    except RuntimeError as e:
        print(f"✓ Correctly caught unfitted model error: {e}")
    
    try:
        # Test dimension mismatch
        X_wrong = np.array([[1, 2, 3]], dtype=np.float32)
        model.predict(X_wrong)
        print("ERROR: Should have raised exception for dimension mismatch")
    except RuntimeError as e:
        print(f"✓ Correctly caught dimension mismatch: {e}")
    
    print("\nEdge cases test completed!")

if __name__ == "__main__":
    test_basic_functionality()
    print("\n" + "="*60 + "\n")
    test_sklearn_compatibility()
    print("\n" + "="*60 + "\n")
    test_edge_cases()
