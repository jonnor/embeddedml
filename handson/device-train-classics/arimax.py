import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')


class ARIMAXAnomalyDetector:
    """
    ARIMAX-based anomaly detection using linear regression with time-series features.
    
    This implementation builds ARIMAX components manually:
    - AR (AutoRegressive): Lagged values of the target variable
    - I (Integrated): Differencing to achieve stationarity
    - MA (Moving Average): Lagged residuals/errors
    - X (eXogenous): External variables that influence the target
    """
    
    def __init__(self, ar_order=2, ma_order=2, diff_order=1, 
                 seasonal_ar=0, seasonal_ma=0, seasonal_period=24,
                 time_features=['hour', 'weekday', 'weekend', 'month'],
                 regression_model=None,
                 anomaly_threshold=3.0,
                 ar_penalty=1.0, ma_penalty=1.0, time_penalty=1.0):
        """
        Initialize ARIMAX anomaly detector.
        
        Parameters:
        - ar_order: Number of autoregressive terms
        - ma_order: Number of moving average terms  
        - diff_order: Number of differencing operations
        - seasonal_ar: Number of seasonal AR terms
        - seasonal_ma: Number of seasonal MA terms
        - seasonal_period: Seasonal period (e.g., 24 for hourly data)
        - anomaly_threshold: Threshold for anomaly detection (std deviations)
        - ar_penalty: Penalty factor for AR terms (< 1.0 reduces influence)
        - ma_penalty: Penalty factor for MA terms (< 1.0 reduces influence)
        - time_penalty: Penalty factor for time features (< 1.0 reduces influence)
        """
        self.ar_order = ar_order
        self.ma_order = ma_order
        self.diff_order = diff_order
        self.seasonal_ar = seasonal_ar
        self.seasonal_ma = seasonal_ma
        self.seasonal_period = seasonal_period
        self.anomaly_threshold = anomaly_threshold
        self.time_features = set(time_features)
        
        # Feature penalties
        self.ar_penalty = ar_penalty
        self.ma_penalty = ma_penalty
        self.time_penalty = time_penalty
        
        if regression_model is None:
            self.model = LinearRegression()
        else:
            self.model = regression_model

        # Create preprocessing pipeline
        self.scaler = StandardScaler()
        self.is_fitted = False

    def _apply_penalties_and_scaling(self, X, fit=False):
        """Apply scaling and penalties manually for better control."""
        if fit:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = self.scaler.transform(X)
        
        # Apply penalties after scaling
        X_penalized = X_scaled.copy()
        feature_names = X.columns
        
        for i, feature_name in enumerate(feature_names):
            if feature_name.startswith('ar_'):
                X_penalized[:, i] *= self.ar_penalty
            elif feature_name.startswith('ma_'):
                X_penalized[:, i] *= self.ma_penalty
            elif feature_name.startswith('t_'):
                X_penalized[:, i] *= self.time_penalty
        
        return X_penalized
        
        
    def _create_lags(self, series, max_lag):
        """Create lagged features for AR terms."""
        lagged_features = []
        for lag in range(1, max_lag + 1):
            lagged = series.shift(lag)
            lagged_features.append(lagged)
        return pd.concat(lagged_features, axis=1)
    
    def _create_seasonal_lags(self, series, seasonal_lags):
        """Create seasonal lagged features."""
        seasonal_features = []
        for lag in seasonal_lags:
            seasonal_lag = lag * self.seasonal_period
            lagged = series.shift(seasonal_lag)
            seasonal_features.append(lagged)
        return pd.concat(seasonal_features, axis=1)
    
    def _create_ma_terms(self, residuals, ma_order):
        """Create moving average terms from residuals."""
        ma_features = []
        for lag in range(1, ma_order + 1):
            ma_term = residuals.shift(lag)
            ma_features.append(ma_term)
        return pd.concat(ma_features, axis=1)
    
    def _difference_series(self, series, order):
        """Apply differencing to achieve stationarity."""
        diff_series = series.copy()
        self.original_values = [series.iloc[:order]]
        
        for i in range(order):
            diff_series = diff_series.diff()
            
        return diff_series
    
    def _inverse_difference(self, diff_series, original_values, order):
        """Reverse differencing operation."""
        series = diff_series.copy()
        
        for i in range(order):
            # Add back the differenced values
            series = series.cumsum()
            if i < len(original_values):
                series.iloc[0] = original_values[i].iloc[-1]
                
        return series
    
    def _create_time_features(self, timestamps):
        """Create time-based features."""
        time_features = pd.DataFrame(index=timestamps)
        
        if 'hour' in self.time_features:
            # Hour of day
            time_features['t_hour'] = timestamps.hour
            time_features['t_hour_sin'] = np.sin(2 * np.pi * timestamps.hour / 24)
            time_features['t_hour_cos'] = np.cos(2 * np.pi * timestamps.hour / 24)

        if 'weekday' in self.time_features:
            # Day of week
            time_features['t_dow'] = timestamps.dayofweek
            time_features['t_dow_sin'] = np.sin(2 * np.pi * timestamps.dayofweek / 7)
            time_features['t_dow_cos'] = np.cos(2 * np.pi * timestamps.dayofweek / 7)
        
        # Month
        if 'month' in self.time_features:
            time_features['t_month'] = timestamps.month
            time_features['t_month_sin'] = np.sin(2 * np.pi * timestamps.month / 12)
            time_features['t_month_cos'] = np.cos(2 * np.pi * timestamps.month / 12)
        
        # Is weekend
        if 'weekend' in self.time_features:
            time_features['t_is_weekend'] = (timestamps.dayofweek >= 5).astype(int)
        
        return time_features
    
    def prepare_features(self, y, X=None, timestamps=None):
        """
        Prepare all features for ARIMAX model.
        
        Parameters:
        - y: Target time series
        - X: Exogenous variables (optional)
        - timestamps: DatetimeIndex for time features
        """
        features = pd.DataFrame(index=y.index)
        
        # Apply differencing if specified
        if self.diff_order > 0:
            y_diff = self._difference_series(y, self.diff_order)
        else:
            y_diff = y.copy()
            
        # AR terms - lagged values of the (differenced) target
        if self.ar_order > 0:
            ar_features = self._create_lags(y_diff, self.ar_order)
            ar_features.columns = [f'ar_lag_{i+1}' for i in range(self.ar_order)]
            features = pd.concat([features, ar_features], axis=1)
        
        # Seasonal AR terms
        if self.seasonal_ar > 0:
            seasonal_lags = list(range(1, self.seasonal_ar + 1))
            seasonal_features = self._create_seasonal_lags(y_diff, seasonal_lags)
            seasonal_features.columns = [f'sar_lag_{i+1}' for i in range(self.seasonal_ar)]
            features = pd.concat([features, seasonal_features], axis=1)
        
        # Exogenous variables
        if X is not None:
            if isinstance(X, pd.DataFrame):
                features = pd.concat([features, X], axis=1)
            else:
                X_df = pd.DataFrame(X, index=y.index)
                features = pd.concat([features, X_df], axis=1)
        
        # Time-based features
        if timestamps is not None:
            time_features = self._create_time_features(timestamps)
            features = pd.concat([features, time_features], axis=1)
        
        return features, y_diff
    
    def fit(self, y, X=None, timestamps=None):
        """
        Fit the ARIMAX model.
        
        Parameters:
        - y: Target time series (pandas Series)
        - X: Exogenous variables (pandas DataFrame or numpy array)
        - timestamps: DatetimeIndex for time features
        """
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
            
        if timestamps is None and hasattr(y.index, 'to_pydatetime'):
            timestamps = y.index
        
        # Prepare features
        features, y_diff = self.prepare_features(y, X, timestamps)
        
        # Initialize residuals for MA terms (start with zeros)
        residuals = pd.Series(0, index=y.index)
        
        # Iterative fitting for MA terms
        for iteration in range(3):  # A few iterations to estimate MA terms
            # Add MA terms if specified
            if self.ma_order > 0:
                ma_features = self._create_ma_terms(residuals, self.ma_order)
                ma_features.columns = [f'ma_lag_{i+1}' for i in range(self.ma_order)]
                features_with_ma = pd.concat([features, ma_features], axis=1)
            else:
                features_with_ma = features
            
            # Remove rows with NaN values
            valid_idx = features_with_ma.dropna().index
            X_clean = features_with_ma.loc[valid_idx]
            y_clean = y_diff.loc[valid_idx]
            
            # Apply penalties and scaling
            X_scaled = np.ascontiguousarray(self._apply_penalties_and_scaling(X_clean, fit=True))
            
            # Fit linear regression
            self.model.fit(X_scaled, np.ascontiguousarray(y_clean))
            
            # Calculate residuals for next iteration
            predictions = self.model.predict(X_scaled)
            residuals.loc[valid_idx] = y_clean - predictions
        
        # Store training information
        self.features_ = features
        self.y_diff_ = y_diff
        self.residuals_ = residuals
        self.valid_idx_ = valid_idx
        self.feature_names_ = features_with_ma.columns.tolist()
        
        # Calculate prediction errors for anomaly detection
        train_errors = residuals.loc[valid_idx]
        self.error_mean_ = train_errors.mean()
        self.error_std_ = train_errors.std()
        
        self.is_fitted = True
        return self
    
    def predict(self, steps=1, X=None, timestamps=None):
        """
        Make predictions for the next 'steps' time periods.
        
        Parameters:
        - steps: Number of steps to predict
        - X: Future exogenous variables
        - timestamps: Future timestamps
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        predictions = []
        current_residuals = self.residuals_.copy()
        
        for step in range(steps):
            # Prepare features for this step
            # This is a simplified version - in practice, you'd need to handle
            # the recursive nature of multi-step predictions more carefully
            if X is not None:
                if isinstance(X, pd.DataFrame):
                    current_X = X.iloc[step:step+1]
                else:
                    current_X = X[step:step+1]
            else:
                current_X = None
            
            # For simplicity, we'll use the last known features
            # In practice, you'd build the feature vector recursively
            last_features = self.features_.iloc[-1:].copy()
            
            # Add MA terms
            if self.ma_order > 0:
                ma_features = self._create_ma_terms(current_residuals, self.ma_order)
                ma_features.columns = [f'ma_lag_{i+1}' for i in range(self.ma_order)]
                last_features = pd.concat([last_features, ma_features.iloc[-1:]], axis=1)
            
            # Apply penalties and scaling
            X_scaled = np.ascontiguousarray(self._apply_penalties_and_scaling(last_features, fit=False))
            pred = self.model.predict(X_scaled)[0]
            predictions.append(pred)
        
        return np.array(predictions)
    
    def detect_anomalies(self, y, X=None, timestamps=None):
        """
        Detect anomalies in the time series.
        
        Parameters:
        - y: Time series to analyze
        - X: Exogenous variables
        - timestamps: DatetimeIndex
        
        Returns:
        - anomaly_scores: Standardized residuals
        - anomalies: Boolean mask indicating anomalies
        - predictions: Model predictions
        """
        if not isinstance(y, pd.Series):
            y = pd.Series(y)
            
        if timestamps is None and hasattr(y.index, 'to_pydatetime'):
            timestamps = y.index
        
        # Prepare features
        features, y_diff = self.prepare_features(y, X, timestamps)
        
        # Initialize residuals for MA terms
        residuals = pd.Series(0, index=y.index)
        
        # Iterative process to estimate MA terms for new data
        for iteration in range(2):  # Fewer iterations for inference
            if self.ma_order > 0:
                ma_features = self._create_ma_terms(residuals, self.ma_order)
                ma_features.columns = [f'ma_lag_{i+1}' for i in range(self.ma_order)]
                features_with_ma = pd.concat([features, ma_features], axis=1)
            else:
                features_with_ma = features
            
            # Get valid indices
            valid_idx = features_with_ma.dropna().index
            if len(valid_idx) == 0:
                # If no valid data, return empty results
                empty_series = pd.Series(np.nan, index=y.index)
                empty_bool = pd.Series(False, index=y.index)
                return empty_series, empty_bool, empty_series
            
            X_clean = features_with_ma.loc[valid_idx]
            y_clean = y_diff.loc[valid_idx]
            
            # Apply penalties and scaling
            X_scaled = np.ascontiguousarray(self._apply_penalties_and_scaling(X_clean, fit=False))
            
            # Make predictions on differenced data
            predictions_diff = self.model.predict(X_scaled)
            
            # Update residuals for next iteration
            residuals.loc[valid_idx] = np.ascontiguousarray(y_clean) - predictions_diff
        
        # Convert predictions back to original scale
        predictions_original = predictions_diff.copy()
        if self.diff_order > 0:
            # Simple inverse differencing approximation
            predictions_original = pd.Series(predictions_diff, index=valid_idx)
            
            # Add back the last known value to approximate inverse differencing
            if len(valid_idx) > 0:
                start_val = y.loc[valid_idx[0]] if valid_idx[0] in y.index else y.iloc[0]
                predictions_original = start_val + predictions_original.cumsum()
        
        # Calculate residuals on original scale for anomaly detection
        final_residuals = y.loc[valid_idx] - predictions_original
        anomaly_scores = (final_residuals - self.error_mean_) / self.error_std_
        
        # Detect anomalies
        anomalies = np.abs(anomaly_scores) > self.anomaly_threshold
        
        # Create full-length results
        full_anomaly_scores = pd.Series(np.nan, index=y.index)
        full_anomaly_scores.loc[valid_idx] = anomaly_scores
        
        full_anomalies = pd.Series(False, index=y.index)
        full_anomalies.loc[valid_idx] = anomalies
        
        full_predictions = pd.Series(np.nan, index=y.index)
        full_predictions.loc[valid_idx] = predictions_original
        
        return full_anomaly_scores, full_anomalies, full_predictions
    


