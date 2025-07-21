
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



class FixedScaler(BaseEstimator, TransformerMixin):
    """
    A scaler that applies fixed scaling and shift parameters specified as a pandas DataFrame.
    
    Parameters:
    -----------
    params_df : pandas.DataFrame
        DataFrame with feature names as index and columns for scale/shift values
    scale_col : str, default='scale'
        Column name for scaling factors (multiply)
    shift_col : str, default='shift'
        Column name for shift values (add after scaling)
    """

    def __init__(self, params_df, scale_col='scale', shift_col='shift'):
        self.params_df = params_df.copy()  # Store a copy to avoid external modifications
        self.scale_col = scale_col
        self.shift_col = shift_col

    def fit(self, X, y=None):
        X = self._validate_data(X, accept_sparse=False, dtype='numeric')
        
        # Convert to DataFrame if numpy array
        if isinstance(X, np.ndarray):
            if hasattr(self, 'feature_names_in_'):
                feature_names = self.feature_names_in_
            else:
                feature_names = [f'feature_{i}' for i in range(X.shape[1])]
            X_df = pd.DataFrame(X, columns=feature_names)
        else:
            X_df = X
            feature_names = X_df.columns.tolist()

        self.feature_names_in_ = feature_names
        self.n_features_in_ = len(feature_names)

        # Initialize with identity transformation (compatible with StandardScaler/MinMaxScaler)
        self.scale_ = np.ones(self.n_features_in_)
        self.min_ = np.zeros(self.n_features_in_)

        # Validate column names exist
        if self.scale_col not in self.params_df.columns:
            raise ValueError(f"Scale column '{self.scale_col}' not found in params_df columns: {list(self.params_df.columns)}")
        if self.shift_col not in self.params_df.columns:
            raise ValueError(f"Shift column '{self.shift_col}' not found in params_df columns: {list(self.params_df.columns)}")

        # Map parameters from DataFrame (index = features)
        scale_dict = self.params_df[self.scale_col].to_dict()
        shift_dict = self.params_df[self.shift_col].to_dict()
        
        for i, feature in enumerate(feature_names):
            if feature in scale_dict:
                self.scale_[i] = scale_dict[feature]
            if feature in shift_dict:
                self.min_[i] = shift_dict[feature]

        # Store data statistics (like MinMaxScaler/StandardScaler)
        if isinstance(X, np.ndarray):
            X_for_stats = X
        else:
            X_for_stats = X.values

        self.data_min_ = np.min(X_for_stats, axis=0)
        self.data_max_ = np.max(X_for_stats, axis=0)
        self.data_range_ = self.data_max_ - self.data_min_

        return self
    
    def transform(self, X):
        X = self._validate_data(X, accept_sparse=False, dtype='numeric', reset=False)
        X = X.copy()  # Always copy to avoid modifying original
        
        # Apply transformation: X_scaled = X * scale_ + min_ (compatible with StandardScaler/MinMaxScaler)
        X *= self.scale_
        X += self.min_
        
        return X
    
    def inverse_transform(self, X):
        X = self._validate_data(X, accept_sparse=False, dtype='numeric', reset=False)
        X = X.copy()  # Always copy to avoid modifying original
        
        # Reverse transformation: X_original = (X_scaled - min_) / scale_
        X -= self.min_
        X /= self.scale_
        
        return X

