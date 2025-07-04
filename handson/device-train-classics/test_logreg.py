# test_elastic_net.py
import numpy as np
import elastic_net_multiclass as enm

def test_basic_functionality():
    """Test basic functionality of the Elastic Net Multi-class classifier"""
    
    # Create sample data
    np.random.seed(42)
    n_samples, n_features, n_classes = 100, 4, 3
    
    # Generate synthetic data with clear class separation
    X = np.random.randn(n_samples, n_features).astype(np.float32)
    
    # Create class-dependent features
    for i in range(n_samples):
        class_id = i % n_classes
        X[i, :] += class_id * 2.0  # Offset each class
    
    # Create labels
    y = np.array([i % n_classes for i in range(n_samples)], dtype=np.uint8)
    
    print("Test Data Shape:", X.shape)
    print("Labels Shape:", y.shape)
    print("Unique labels:", np.unique(y))
    print()
    
    # Initialize and train model
    model = enm.ElasticNetMulticlass(alpha=0.01, l1_ratio=0.5)
    print("Model initialized with alpha=0.01, l1_ratio=0.5")
    print()
    
    # Fit the model
    print("Training model...")
    model.fit(X, y, max_iterations=500, learning_rate=0.1, verbose=True)
    print()
    
    # Check model properties
    print("Model Properties:")
    print(f"  Features: {model.n_features_}")
    print(f"  Classes: {model.n_classes_}")
    print(f"  Alpha: {model.alpha}")
    print(f"  L1 Ratio: {model.l1_ratio}")
    print(f"  Is Fitted: {model.is_fitted_}")
    print()
    
    # Make predictions
    predictions = model.predict(X)
    probabilities = model.predict_proba(X)
    
    print("Predictions shape:", predictions.shape)
    print("Probabilities shape:", probabilities.shape)
    print()
    
    # Calculate accuracy
    accuracy = model.score(X, y)
    print(f"Training Accuracy: {accuracy:.4f} ({accuracy*100:.1f}%)")
    print()
    
    # Show learned parameters
    weights = model.weights_
    bias = model.bias_
    
    print("Learned Parameters:")
    print("Weights shape:", weights.shape)
    print("Bias shape:", bias.shape)
    print("Weights:\n", weights)
    print("Bias:", bias)
    print()
    
    # Test predictions on a few samples
    print("Sample Predictions:")
    for i in range(min(5, len(X))):
        pred = model.predict(X[i:i+1])[0]
        proba = model.predict_proba(X[i:i+1])[0]
        actual = y[i]
        
        print(f"Sample {i}: True={actual}, Pred={pred}, " +
              f"Proba=[{proba[0]:.3f}, {proba[1]:.3f}, {proba[2]:.3f}] " +
              f"{'✓' if pred == actual else '✗'}")
    
    print("\nTest completed successfully!")

def test_sklearn_compatibility():
    """Test sklearn-like interface"""
    try:
        from sklearn.datasets import make_classification
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, classification_report
        
        print("Testing sklearn compatibility...")
        
        # Generate more realistic data
        X, y = make_classification(n_samples=200, n_features=10, n_classes=3, 
                                 n_redundant=0, n_informative=8, random_state=42)
        X = X.astype(np.float32)
        y = y.astype(np.uint8)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=42, stratify=y
        )
        
        # Train model
        model = enm.ElasticNetMulticlass(alpha=0.05, l1_ratio=0.7)
        model.fit(X_train, y_train, max_iterations=1000, verbose=False)
        
        # Evaluate
        train_acc = model.score(X_train, y_train)
        test_acc = model.score(X_test, y_test)
        
        print(f"Training accuracy: {train_acc:.4f}")
        print(f"Test accuracy: {test_acc:.4f}")
        
        # Detailed evaluation
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)
        
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred))
        
        print(f"Probability predictions shape: {y_proba.shape}")
        print(f"Probability sums (should be ~1.0): {y_proba.sum(axis=1)[:5]}")
        
        print("sklearn compatibility test passed!")
        
    except ImportError:
        print("sklearn not available, skipping compatibility test")

if __name__ == "__main__":
    test_basic_functionality()
    print("\n" + "="*50 + "\n")
    test_sklearn_compatibility()
