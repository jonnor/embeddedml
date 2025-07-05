
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
            if feature_name.startswith('ar_') or feature_name.startswith('sar_'):
                X_penalized[:, i] *= self.ar_penalty
            elif feature_name.startswith('ma_') or feature_name.startswith('sma_'):
                X_penalized[:, i] *= self.ma_penalty
            elif feature_name.startswith('t_'):
                X_penalized[:, i] *= self.time_penalty
        
        return X_penalized

        
    def _create_ma_terms(self, residuals, ma_order):
            """Create moving average terms from residuals."""
            ma_features = []
            for lag in range(1, ma_order + 1):
                ma_term = residuals.shift(lag)
                ma_features.append(ma_term)
            return pd.concat(ma_features, axis=1)

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
    
    def _create_seasonal_ma_terms(self, residuals, seasonal_ma_order):
        """Create seasonal moving average terms from residuals."""
        seasonal_ma_features = []
        for lag in range(1, seasonal_ma_order + 1):
            seasonal_lag = lag * self.seasonal_period
            seasonal_ma_term = residuals.shift(seasonal_lag)
            seasonal_ma_features.append(seasonal_ma_term)
        return pd.concat(seasonal_ma_features, axis=1)
    
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
            
            # Add seasonal MA terms if specified
            if self.seasonal_ma > 0:
                seasonal_ma_features = self._create_seasonal_ma_terms(residuals, self.seasonal_ma)
                seasonal_ma_features.columns = [f'sma_lag_{i+1}' for i in range(self.seasonal_ma)]
                features_with_ma = pd.concat([features_with_ma, seasonal_ma_features], axis=1)

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


    def predict(self, steps=1, X=None, timestamps=None, start_index=None):
        """
        Make predictions for future time periods.
        
        Parameters:
        - steps: Number of future steps to predict
        - X: Future exogenous variables (pandas DataFrame or numpy array)
        - timestamps: Future timestamps (DatetimeIndex)
        - start_index: Starting index for predictions (if None, continues from training data)
        
        Returns:
        - predictions: Series with future predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        # Determine prediction index
        if start_index is not None:
            pred_index = pd.RangeIndex(start=start_index, stop=start_index + steps)
        elif timestamps is not None:
            if len(timestamps) != steps:
                raise ValueError(f"Length of timestamps ({len(timestamps)}) must match steps ({steps})")
            pred_index = timestamps
        else:
            # Continue from last training index
            last_idx = self.valid_idx_[-1] if len(self.valid_idx_) > 0 else 0
            pred_index = pd.RangeIndex(start=last_idx + 1, stop=last_idx + 1 + steps)
        
        # Initialize prediction containers
        predictions = pd.Series(np.nan, index=pred_index)
        
        # Get the last known values for AR terms
        last_y_values = self.y_diff_.iloc[-max(self.ar_order, self.seasonal_ar * self.seasonal_period):]
        
        # Get residuals history for MA terms
        residuals_history = self.residuals_.copy()
        
        # Make predictions step by step
        for i, pred_idx in enumerate(pred_index):
            # Prepare features for this prediction step
            features_row = {}
            
            # AR terms - use last known values and previous predictions
            if self.ar_order > 0:
                for lag in range(1, self.ar_order + 1):
                    if i >= lag:
                        # Use previous prediction
                        features_row[f'ar_lag_{lag}'] = predictions.iloc[i - lag]
                    else:
                        # Use last known training value
                        if len(last_y_values) >= lag:
                            features_row[f'ar_lag_{lag}'] = last_y_values.iloc[-(lag - i)]
                        else:
                            features_row[f'ar_lag_{lag}'] = 0
            
            # Seasonal AR terms
            if self.seasonal_ar > 0:
                for lag in range(1, self.seasonal_ar + 1):
                    seasonal_lag = lag * self.seasonal_period
                    if i >= seasonal_lag:
                        # Use previous prediction
                        features_row[f'sar_lag_{lag}'] = predictions.iloc[i - seasonal_lag]
                    else:
                        # Use last known training value
                        if len(last_y_values) >= seasonal_lag - i:
                            features_row[f'sar_lag_{lag}'] = last_y_values.iloc[-(seasonal_lag - i)]
                        else:
                            features_row[f'sar_lag_{lag}'] = 0
            
            # MA terms - use residuals history
            if self.ma_order > 0:
                for lag in range(1, self.ma_order + 1):
                    if len(residuals_history) >= lag:
                        features_row[f'ma_lag_{lag}'] = residuals_history.iloc[-lag]
                    else:
                        features_row[f'ma_lag_{lag}'] = self.error_mean_
            
            # Seasonal MA terms
            if self.seasonal_ma > 0:
                for lag in range(1, self.seasonal_ma + 1):
                    seasonal_lag = lag * self.seasonal_period
                    if len(residuals_history) >= seasonal_lag:
                        features_row[f'sma_lag_{lag}'] = residuals_history.iloc[-seasonal_lag]
                    else:
                        features_row[f'sma_lag_{lag}'] = self.error_mean_
            
            # Exogenous variables
            if X is not None:
                if isinstance(X, pd.DataFrame):
                    if i < len(X):
                        for col in X.columns:
                            features_row[col] = X.iloc[i][col]
                    else:
                        # Fill with last known values or zeros
                        for col in X.columns:
                            features_row[col] = X.iloc[-1][col] if len(X) > 0 else 0
                else:
                    if i < len(X):
                        for j in range(X.shape[1]):
                            features_row[f'X_{j}'] = X[i, j]
                    else:
                        for j in range(X.shape[1]):
                            features_row[f'X_{j}'] = X[-1, j] if len(X) > 0 else 0
            
            # Time features
            if timestamps is not None:
                current_timestamp = timestamps[i] if i < len(timestamps) else timestamps[-1]
                time_features = self._create_time_features(pd.DatetimeIndex([current_timestamp]))
                for col in time_features.columns:
                    features_row[col] = time_features.iloc[0][col]
            
            # Create feature vector
            feature_vector = pd.DataFrame([features_row])
            
            # Ensure all training features are present
            for col in self.feature_names_:
                if col not in feature_vector.columns:
                    feature_vector[col] = 0
            
            # Reorder to match training
            feature_vector = feature_vector[self.feature_names_]
            
            # Apply scaling and penalties
            X_scaled = self._apply_penalties_and_scaling(feature_vector, fit=False)
            
            # Make prediction
            pred_diff = self.model.predict(X_scaled)[0]
            
            # Store prediction
            predictions.iloc[i] = pred_diff
            
            # Update residuals history (assume prediction error is close to training mean)
            new_residual = self.error_mean_
            residuals_history = pd.concat([residuals_history, pd.Series([new_residual])])
        
        # Reverse differencing if applied
        if self.diff_order > 0:
            # For out-of-sample prediction, we need to connect to the last training value
            if hasattr(self, 'original_values') and len(self.original_values) > 0:
                # Use the last actual value from training as reference
                last_original = self.original_values[0].iloc[-1]  # Last undifferenced value
                
                # Create a series that starts with the last original value
                extended_series = pd.Series([last_original] + predictions.tolist())
                
                # Apply inverse differencing
                predictions_original = self._inverse_difference(
                    extended_series, self.original_values, self.diff_order
                )[1:]  # Remove the reference value
                
                # Restore original index
                predictions_original.index = predictions.index
            else:
                predictions_original = predictions
        else:
            predictions_original = predictions
        
        return predictions_original

