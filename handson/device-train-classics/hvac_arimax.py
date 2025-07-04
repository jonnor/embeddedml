import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
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
                 anomaly_threshold=3.0):
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
        """
        self.ar_order = ar_order
        self.ma_order = ma_order
        self.diff_order = diff_order
        self.seasonal_ar = seasonal_ar
        self.seasonal_ma = seasonal_ma
        self.seasonal_period = seasonal_period
        self.anomaly_threshold = anomaly_threshold
        
        self.model = LinearRegression()
        self.scaler = StandardScaler()
        self.is_fitted = False
        
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
        
        # Hour of day
        time_features['hour'] = timestamps.hour
        time_features['hour_sin'] = np.sin(2 * np.pi * timestamps.hour / 24)
        time_features['hour_cos'] = np.cos(2 * np.pi * timestamps.hour / 24)
        
        # Day of week
        time_features['dow'] = timestamps.dayofweek
        time_features['dow_sin'] = np.sin(2 * np.pi * timestamps.dayofweek / 7)
        time_features['dow_cos'] = np.cos(2 * np.pi * timestamps.dayofweek / 7)
        
        # Month
        time_features['month'] = timestamps.month
        time_features['month_sin'] = np.sin(2 * np.pi * timestamps.month / 12)
        time_features['month_cos'] = np.cos(2 * np.pi * timestamps.month / 12)
        
        # Is weekend
        time_features['is_weekend'] = (timestamps.dayofweek >= 5).astype(int)
        
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
            
            # Scale features
            X_scaled = self.scaler.fit_transform(X_clean)
            
            # Fit linear regression
            self.model.fit(X_scaled, y_clean)
            
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
            
            # Scale and predict
            X_scaled = self.scaler.transform(last_features)
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
            
            # Scale features
            X_scaled = self.scaler.transform(X_clean)
            
            # Make predictions
            predictions = self.model.predict(X_scaled)
            
            # Update residuals for next iteration
            residuals.loc[valid_idx] = y_clean - predictions
        
        # Calculate anomaly scores (standardized residuals)
        final_residuals = y_clean - predictions
        anomaly_scores = (final_residuals - self.error_mean_) / self.error_std_
        
        # Detect anomalies
        anomalies = np.abs(anomaly_scores) > self.anomaly_threshold
        
        # Create full-length results
        full_anomaly_scores = pd.Series(np.nan, index=y.index)
        full_anomaly_scores.loc[valid_idx] = anomaly_scores
        
        full_anomalies = pd.Series(False, index=y.index)
        full_anomalies.loc[valid_idx] = anomalies
        
        full_predictions = pd.Series(np.nan, index=y.index)
        full_predictions.loc[valid_idx] = predictions
        
        return full_anomaly_scores, full_anomalies, full_predictions
    
    def plot_results(self, y, anomaly_scores, anomalies, predictions, title="ARIMAX Anomaly Detection"):
        """Plot the results of anomaly detection."""
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        
        # Plot 1: Original time series with anomalies
        axes[0].plot(y.index, y.values, 'b-', label='Original Data', alpha=0.7)
        axes[0].plot(y.index, predictions, 'r-', label='ARIMAX Predictions', alpha=0.8)
        anomaly_points = y[anomalies]
        axes[0].scatter(anomaly_points.index, anomaly_points.values, 
                       color='red', s=50, label='Anomalies', zorder=5)
        axes[0].set_title(f'{title} - Time Series with Anomalies')
        axes[0].set_ylabel('Value')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Plot 2: Residuals
        residuals = y - predictions
        axes[1].plot(residuals.index, residuals.values, 'g-', label='Residuals', alpha=0.7)
        axes[1].axhline(y=0, color='k', linestyle='--', alpha=0.5)
        axes[1].axhline(y=self.anomaly_threshold * self.error_std_, 
                       color='r', linestyle='--', alpha=0.5, label='Anomaly Threshold')
        axes[1].axhline(y=-self.anomaly_threshold * self.error_std_, 
                       color='r', linestyle='--', alpha=0.5)
        axes[1].set_title('Residuals')
        axes[1].set_ylabel('Residual')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        # Plot 3: Anomaly scores
        axes[2].plot(anomaly_scores.index, anomaly_scores.values, 'purple', 
                    label='Anomaly Scores', alpha=0.7)
        axes[2].axhline(y=self.anomaly_threshold, color='r', linestyle='--', 
                       alpha=0.5, label='Threshold')
        axes[2].axhline(y=-self.anomaly_threshold, color='r', linestyle='--', alpha=0.5)
        axes[2].scatter(anomaly_scores[anomalies].index, anomaly_scores[anomalies].values,
                       color='red', s=30, label='Anomalies', zorder=5)
        axes[2].set_title('Standardized Anomaly Scores')
        axes[2].set_ylabel('Score')
        axes[2].set_xlabel('Time')
        axes[2].legend()
        axes[2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


# Example usage with synthetic HVAC data
def generate_hvac_data(n_points=1000):
    """Generate synthetic HVAC data with anomalies."""
    np.random.seed(42)
    
    # Create datetime index
    timestamps = pd.date_range('2023-01-01', periods=n_points, freq='H')
    
    # Base temperature pattern with daily and weekly cycles
    hours = np.arange(n_points)
    base_temp = (20 + 5 * np.sin(2 * np.pi * hours / 24) +  # Daily cycle
                 3 * np.sin(2 * np.pi * hours / (24 * 7)) +  # Weekly cycle
                 2 * np.sin(2 * np.pi * hours / (24 * 365)))  # Yearly cycle
    
    # Add some noise
    noise = np.random.normal(0, 0.5, n_points)
    
    # Create exogenous variables (outdoor temperature, occupancy)
    outdoor_temp = base_temp + np.random.normal(0, 2, n_points)
    occupancy = np.random.poisson(10, n_points)  # People count
    
    # Target variable (indoor temperature) influenced by outdoor temp and occupancy
    indoor_temp = (base_temp + 
                   0.3 * outdoor_temp + 
                   0.1 * occupancy + 
                   noise)
    
    # Inject anomalies
    anomaly_indices = np.random.choice(n_points, size=20, replace=False)
    indoor_temp[anomaly_indices] += np.random.normal(0, 5, 20)  # Temperature spikes
    
    # Create DataFrame
    data = pd.DataFrame({
        'indoor_temp': indoor_temp,
        'outdoor_temp': outdoor_temp,
        'occupancy': occupancy
    }, index=timestamps)
    
    return data, anomaly_indices

def example():

    # Generate example data
    print("Generating synthetic HVAC data...")
    data, true_anomalies = generate_hvac_data(1000)

    # Prepare data
    y = data['indoor_temp']
    X = data[['outdoor_temp', 'occupancy']]
    timestamps = data.index

    # Split into train/test
    train_size = int(0.8 * len(data))
    y_train = y[:train_size]
    X_train = X[:train_size]
    timestamps_train = timestamps[:train_size]

    y_test = y[train_size:]
    X_test = X[train_size:]
    timestamps_test = timestamps[train_size:]

    print(f"Training data: {len(y_train)} points")
    print(f"Testing data: {len(y_test)} points")

    # Create and fit ARIMAX model
    print("\nFitting ARIMAX model...")
    arimax_detector = ARIMAXAnomalyDetector(
        ar_order=2,           # Use 2 autoregressive terms
        ma_order=2,           # Use 2 moving average terms
        diff_order=1,         # First differencing
        seasonal_ar=1,        # 1 seasonal AR term
        seasonal_ma=0,        # No seasonal MA terms
        seasonal_period=24,   # 24-hour seasonality
        anomaly_threshold=2.5 # 2.5 standard deviations
    )

    arimax_detector.fit(y_train, X_train, timestamps_train)

    # Detect anomalies on test data
    print("Detecting anomalies...")
    anomaly_scores, anomalies, predictions = arimax_detector.detect_anomalies(
        y_test, X_test, timestamps_test
    )

    # Print results
    n_anomalies = anomalies.sum()
    print(f"\nDetected {n_anomalies} anomalies out of {len(y_test)} points")
    print(f"Anomaly rate: {n_anomalies/len(y_test)*100:.2f}%")

    # Print feature importance (coefficients)
    print("\nModel coefficients:")
    for i, coef in enumerate(arimax_detector.model.coef_):
        if i < len(arimax_detector.feature_names_):
            print(f"{arimax_detector.feature_names_[i]}: {coef:.4f}")

    # Calculate performance metrics on aligned data
    valid_mask = ~(y_test.isna() | predictions.isna())
    y_test_aligned = y_test[valid_mask]
    predictions_aligned = predictions[valid_mask]

    if len(y_test_aligned) > 0:
        test_mse = mean_squared_error(y_test_aligned, predictions_aligned)
        test_mae = mean_absolute_error(y_test_aligned, predictions_aligned)
        print(f"\nTest MSE: {test_mse:.4f}")
        print(f"Test MAE: {test_mae:.4f}")
        print(f"Evaluated on {len(y_test_aligned)} valid points")
    else:
        print("\nNo valid predictions to evaluate")

    # Plot results
    arimax_detector.plot_results(y_test, anomaly_scores, anomalies, predictions)

    print("\nKey features of this ARIMAX implementation:")
    print("1. AR terms: Lagged values of the target variable")
    print("2. MA terms: Lagged residuals from previous predictions")
    print("3. I (Integration): Differencing to achieve stationarity")
    print("4. X (Exogenous): External variables (outdoor temp, occupancy)")
    print("5. Seasonal terms: Handle daily/weekly patterns")
    print("6. Time features: Hour, day of week, month patterns")
    print("7. Anomaly detection: Based on standardized residuals")


