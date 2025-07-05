import numpy as np
from scipy import stats
from sklearn.base import BaseEstimator, TransformerMixin

class GammaAnomalyTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn style transformer for Gamma distribution-based anomaly scoring.
    
    Parameters
    ----------
    use_log : bool, default=False
        If True, returns -log(1 - CDF) for better separation at extremes
    epsilon : float, default=1e-10
        Small value to avoid log(0) when use_log=True
    """
    
    def __init__(self, use_log=False, epsilon=1e-10):
        self.use_log = use_log
        self.epsilon = epsilon
        
    def fit(self, X, y=None):
        """
        Fit Gamma distribution to the data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples,) or (n_samples, 1)
            Input data
        y : Ignored
            Not used, present for API consistency
            
        Returns
        -------
        self : object
            Returns self
        """
        X = self._validate_input(X)
        
        # Fit Gamma distribution using MLE
        self.shape_, self.loc_, self.scale_ = stats.gamma.fit(X)
        
        # Store goodness of fit
        self.ks_statistic_, self.p_value_ = stats.kstest(
            X, lambda x: stats.gamma.cdf(x, self.shape_, self.loc_, self.scale_)
        )
        
        return self
    
    def transform(self, X):
        """
        Transform data to anomaly scores using fitted Gamma distribution.
        
        Parameters
        ----------
        X : array-like of shape (n_samples,) or (n_samples, 1)
            Input data
            
        Returns
        -------
        X_transformed : ndarray of shape (n_samples,)
            Anomaly scores (higher = more anomalous)
        """
        X = self._validate_input(X)
        
        # Check if fitted
        if not hasattr(self, 'shape_'):
            raise ValueError("This transformer has not been fitted yet.")
        
        # Transform to probabilities using CDF
        probabilities = stats.gamma.cdf(X, self.shape_, self.loc_, self.scale_)
        
        # Convert to anomaly scores (CDF for right-skewed distributions)
        # High CDF values = common, low CDF values = rare/anomalous
        # Use CDF directly since we want high scores for high values (right tail)
        anomaly_scores = probabilities
        
        if self.use_log:
            # For log version, use -log(1 - CDF) to emphasize right tail
            anomaly_scores = -np.log(1 - probabilities + self.epsilon)
            
        return anomaly_scores
    
    def fit_transform(self, X, y=None):
        """
        Fit the transformer and transform the data.
        
        Parameters
        ----------
        X : array-like of shape (n_samples,) or (n_samples, 1)
            Input data
        y : Ignored
            Not used, present for API consistency
            
        Returns
        -------
        X_transformed : ndarray of shape (n_samples,)
            Anomaly scores
        """
        return self.fit(X, y).transform(X)
    
    def _validate_input(self, X):
        """Validate and reshape input data."""
        X = np.asarray(X)
        if X.ndim == 2 and X.shape[1] == 1:
            X = X.ravel()
        elif X.ndim != 1:
            raise ValueError("Input must be 1D array or 2D array with 1 column")
        return X
    
    def get_params_dict(self):
        """Get fitted distribution parameters."""
        if not hasattr(self, 'shape_'):
            raise ValueError("This transformer has not been fitted yet.")
        return {
            'shape': self.shape_,
            'loc': self.loc_,
            'scale': self.scale_,
            'ks_statistic': self.ks_statistic_,
            'p_value': self.p_value_
        }


# Example usage
if __name__ == "__main__":
    from sklearn.model_selection import train_test_split
    
    # Generate sample data
    np.random.seed(42)
    raw_scores = np.random.gamma(2, 2, 1000)
    
    # Split data
    X_train, X_test = train_test_split(raw_scores, test_size=0.3, random_state=42)
    
    # Standard anomaly scoring
    transformer = GammaAnomalyTransformer(use_log=False)
    
    # Fit on training data
    transformer.fit(X_train)
    
    # Transform test data
    anomaly_scores = transformer.transform(X_test)
    
    # Or use fit_transform for training data
    train_anomaly_scores = transformer.fit_transform(X_train)
    
    # Print results
    print("Fitted parameters:", transformer.get_params_dict())
    print(f"Test anomaly scores (first 5): {anomaly_scores[:5]}")
    print(f"Max anomaly score: {anomaly_scores.max():.4f}")
    print(f"Min anomaly score: {anomaly_scores.min():.4f}")
    
    # Example with log transformation
    log_transformer = GammaAnomalyTransformer(use_log=True)
    log_anomaly_scores = log_transformer.fit_transform(X_train)
    
    print(f"\nLog anomaly scores (first 5): {log_anomaly_scores[:5]}")
    print(f"Max log anomaly score: {log_anomaly_scores.max():.4f}")
