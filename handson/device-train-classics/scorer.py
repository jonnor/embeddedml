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
    severity_factor : float, default=1.0
        Adjusts scoring severity. >1 makes extreme values more severe,
        <1 makes them less severe
    epsilon : float, default=1e-10
        Small value to avoid log(0) when use_log=True
    """
    
    def __init__(self, use_log=False, severity_factor=1.0, epsilon=1e-10):
        self.use_log = use_log
        self.severity_factor = severity_factor
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
        
        # Adjust parameters for severity
        # Decreasing shape makes tail heavier (more severe scoring)
        # Increasing scale spreads distribution (less severe scoring)
        self.adjusted_shape_ = self.shape_ / self.severity_factor
        self.adjusted_scale_ = self.scale_ * self.severity_factor
        self.adjusted_loc_ = self.loc_  # Keep location fixed
        
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
        
        # Transform to probabilities using adjusted parameters
        probabilities = stats.gamma.cdf(X, self.adjusted_shape_, self.adjusted_loc_, self.adjusted_scale_)
        
        # Convert to anomaly scores (CDF for right-skewed distributions)
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
            'original_shape': self.shape_,
            'original_loc': self.loc_,
            'original_scale': self.scale_,
            'adjusted_shape': self.adjusted_shape_,
            'adjusted_loc': self.adjusted_loc_,
            'adjusted_scale': self.adjusted_scale_,
            'severity_factor': self.severity_factor,
            'ks_statistic': self.ks_statistic_,
            'p_value': self.p_value_
        }


class HalfNormAnomalyTransformer(BaseEstimator, TransformerMixin):
    """
    Scikit-learn style transformer for Half-Normal distribution-based anomaly scoring.
    
    Parameters
    ----------
    use_log : bool, default=False
        If True, returns -log(1 - CDF) for better separation at extremes
    severity_factor : float, default=1.0
        Adjusts scoring severity. >1 makes extreme values more severe,
        <1 makes them less severe
    epsilon : float, default=1e-10
        Small value to avoid log(0) when use_log=True
    """
    
    def __init__(self, use_log=False, severity_factor=1.0, epsilon=1e-10):
        self.use_log = use_log
        self.severity_factor = severity_factor
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
        
        # Fit Half-Normal distribution using MLE
        self.loc_, self.scale_ = stats.halfnorm.fit(X)
        
        # Adjust parameters for severity
        # Increasing scale makes distribution wider (less severe scoring)
        # Decreasing scale makes distribution narrower (more severe scoring)
        self.adjusted_scale_ = self.scale_ / self.severity_factor
        self.adjusted_loc_ = self.loc_  # Keep location fixed
        
        # Store goodness of fit
        self.ks_statistic_, self.p_value_ = stats.kstest(
            X, lambda x: stats.halfnorm.cdf(x, self.adjusted_loc_, self.adjusted_scale_)
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
        if not hasattr(self, 'scale_'):
            raise ValueError("This transformer has not been fitted yet.")
        
        # Transform to probabilities using adjusted parameters
        probabilities = stats.halfnorm.cdf(X, self.adjusted_loc_, self.adjusted_scale_)
        
        # Convert to anomaly scores (CDF for right-skewed distributions)
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
        if not hasattr(self, 'scale_'):
            raise ValueError("This transformer has not been fitted yet.")
        return {
            'original_loc': self.loc_,
            'original_scale': self.scale_,
            'adjusted_loc': self.adjusted_loc_,
            'adjusted_scale': self.adjusted_scale_,
            'severity_factor': self.severity_factor,
            'ks_statistic': self.ks_statistic_,
            'p_value': self.p_value_
        }


