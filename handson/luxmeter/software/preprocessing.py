
from sklearn.base import BaseEstimator, TransformerMixin
import numpy as np

class IdentityScaler(BaseEstimator, TransformerMixin):
    """
    A scaler like StandardScaler / MinMaxScaler that does nothing

    Useful to swap out such a scaler, but keeping the scaling step in a pipeline, for compatibility
    """

    def __init__(self, feature_range=(0, 1), copy=True, clip=False):
        self.feature_range = feature_range
        self.copy = copy
        self.clip = clip
    
    def fit(self, X, y=None):
        X = self._validate_data(X, accept_sparse=False, dtype='numeric')
        
        # Set parameters for identity transformation:
        # X_scaled = X * scale_ + min_
        # For identity: X_scaled = X * 1 + 0
        self.scale_ = np.ones(X.shape[1])   # Multiply by 1
        self.min_ = np.zeros(X.shape[1])    # Add 0
        
        # Store data statistics (like MinMaxScaler)
        self.data_min_ = np.min(X, axis=0)
        self.data_max_ = np.max(X, axis=0)
        self.data_range_ = self.data_max_ - self.data_min_
        self.n_features_in_ = X.shape[1]
        
        return self
    
    def transform(self, X):
        X = self._validate_data(X, accept_sparse=False, dtype='numeric', reset=False)
        
        if self.copy:
            X = X.copy()
        
        # Apply identity transformation
        X *= self.scale_  # X * 1
        X += self.min_    # X + 0
        
        return X
    
    def inverse_transform(self, X):
        return X if not self.copy else X.copy()

