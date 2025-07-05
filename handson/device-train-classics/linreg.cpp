
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include <memory>
#include <stdexcept>
#include <cstring>
#include <cmath>
#include <cstdlib>
#include <cstdint>
#include <cstdio>

namespace py = pybind11;

// Include the C implementation
extern "C" {
    #include "linreg.c"
}

// Python wrapper class for Elastic Net Linear Regression
class ElasticNetRegression {
private:
    elastic_net_model_t model;
    std::vector<float> weights_buffer;
    std::vector<float> gradients_buffer;  // Working memory for gradients
    bool is_fitted;

public:
    ElasticNetRegression(double alpha = 0.01, double l1_ratio = 0.5, double learning_rate = 0.01) 
        : is_fitted(false) {
        model.alpha = static_cast<float>(alpha);
        model.l1_ratio = static_cast<float>(l1_ratio);
        model.learning_rate = static_cast<float>(learning_rate);
    }
    
    void fit(py::array_t<float> X, py::array_t<float> y, 
             int max_iterations = 1000, double tolerance = 1e-6, 
             bool verbose = true, int check_interval = 10, double divergence_factor = 10.0) {
        
        // Validate input shapes
        if (X.ndim() != 2) {
            throw std::runtime_error("X must be a 2D array");
        }
        if (y.ndim() != 1) {
            throw std::runtime_error("y must be a 1D array");
        }
        if (X.shape(0) != y.shape(0)) {
            throw std::runtime_error("X and y must have the same number of samples");
        }
        
        uint16_t n_samples = static_cast<uint16_t>(X.shape(0));
        uint16_t n_features = static_cast<uint16_t>(X.shape(1));
        
        // Initialize model
        model.n_features = n_features;
        
        // Allocate memory for weights and gradients
        weights_buffer.resize(n_features);
        gradients_buffer.resize(n_features);  // Working memory for gradients
        
        // Initialize model
        elastic_net_init(&model, weights_buffer.data(), gradients_buffer.data(), 
                        n_features, model.alpha, model.l1_ratio, model.learning_rate);
        
        // Get data pointers and check for contiguous arrays
        py::buffer_info X_buf = X.request();
        py::buffer_info y_buf = y.request();
        
        // Check if X is C-contiguous
        if (X_buf.strides[0] != sizeof(float) * n_features || 
            X_buf.strides[1] != sizeof(float)) {
            throw std::runtime_error("X must be C-contiguous. Use np.ascontiguousarray(X) if needed.");
        }
        
        // Check if y is C-contiguous
        if (y_buf.strides[0] != sizeof(float)) {
            throw std::runtime_error("y must be C-contiguous. Use np.ascontiguousarray(y) if needed.");
        }
        
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        float* y_ptr = static_cast<float*>(y_buf.ptr);
        
        // Train model
        elastic_net_train(&model, X_ptr, y_ptr, n_samples, 
                         max_iterations, static_cast<float>(tolerance), 
                         verbose ? 1 : 0, static_cast<uint16_t>(check_interval),
                         static_cast<float>(divergence_factor));
        
        is_fitted = true;
    }
    
    py::array_t<float> predict(py::array_t<float> X) {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted before making predictions");
        }
        
        if (X.ndim() != 2) {
            throw std::runtime_error("X must be a 2D array");
        }
        if (X.shape(1) != model.n_features) {
            throw std::runtime_error("X must have " + std::to_string(model.n_features) + " features");
        }
        
        py::ssize_t n_samples = X.shape(0);
        auto result = py::array_t<float>(n_samples);
        py::buffer_info result_buf = result.request();
        float* result_ptr = static_cast<float*>(result_buf.ptr);
        
        py::buffer_info X_buf = X.request();
        
        // Check if X is C-contiguous
        if (X_buf.strides[0] != sizeof(float) * model.n_features || 
            X_buf.strides[1] != sizeof(float)) {
            throw std::runtime_error("X must be C-contiguous. Use np.ascontiguousarray(X) if needed.");
        }
        
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        
        // Make predictions
        for (py::ssize_t i = 0; i < n_samples; i++) {
            result_ptr[i] = elastic_net_predict(&model, &X_ptr[i * model.n_features]);
        }
        
        return result;
    }
    
    double score(py::array_t<float> X, py::array_t<float> y) {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted before scoring");
        }
        
        if (X.shape(0) != y.shape(0)) {
            throw std::runtime_error("X and y must have the same number of samples");
        }
        
        uint16_t n_samples = static_cast<uint16_t>(X.shape(0));
        
        py::buffer_info X_buf = X.request();
        py::buffer_info y_buf = y.request();
        
        // Check if arrays are C-contiguous
        if (X_buf.strides[0] != sizeof(float) * model.n_features || 
            X_buf.strides[1] != sizeof(float)) {
            throw std::runtime_error("X must be C-contiguous. Use np.ascontiguousarray(X) if needed.");
        }
        
        if (y_buf.strides[0] != sizeof(float)) {
            throw std::runtime_error("y must be C-contiguous. Use np.ascontiguousarray(y) if needed.");
        }
        
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        float* y_ptr = static_cast<float*>(y_buf.ptr);
        
        // Calculate R² score
        float mse = elastic_net_mse(&model, X_ptr, y_ptr, n_samples);
        
        // Calculate total sum of squares for R²
        float y_mean = 0.0f;
        for (uint16_t i = 0; i < n_samples; i++) {
            y_mean += y_ptr[i];
        }
        y_mean /= n_samples;
        
        float tss = 0.0f;
        for (uint16_t i = 0; i < n_samples; i++) {
            float diff = y_ptr[i] - y_mean;
            tss += diff * diff;
        }
        
        // R² = 1 - (RSS/TSS) = 1 - (MSE*n/TSS)
        if (tss > 1e-8f) {
            return 1.0 - (mse * n_samples) / tss;
        } else {
            return 0.0;  // Perfect fit or constant target
        }
    }
    
    double mean_squared_error(py::array_t<float> X, py::array_t<float> y) {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted before calculating MSE");
        }
        
        if (X.shape(0) != y.shape(0)) {
            throw std::runtime_error("X and y must have the same number of samples");
        }
        
        uint16_t n_samples = static_cast<uint16_t>(X.shape(0));
        
        py::buffer_info X_buf = X.request();
        py::buffer_info y_buf = y.request();
        
        // Check if arrays are C-contiguous
        if (X_buf.strides[0] != sizeof(float) * model.n_features || 
            X_buf.strides[1] != sizeof(float)) {
            throw std::runtime_error("X must be C-contiguous. Use np.ascontiguousarray(X) if needed.");
        }
        
        if (y_buf.strides[0] != sizeof(float)) {
            throw std::runtime_error("y must be C-contiguous. Use np.ascontiguousarray(y) if needed.");
        }
        
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        float* y_ptr = static_cast<float*>(y_buf.ptr);
        
        return elastic_net_mse(&model, X_ptr, y_ptr, n_samples);
    }
    
    // Property getters
    py::array_t<float> get_weights() const {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted first");
        }
        
        auto result = py::array_t<float>(model.n_features);
        py::buffer_info result_buf = result.request();
        float* result_ptr = static_cast<float*>(result_buf.ptr);
        
        for (uint16_t f = 0; f < model.n_features; f++) {
            result_ptr[f] = model.weights[f];
        }
        
        return result;
    }
    
    float get_bias() const {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted first");
        }
        return model.bias;
    }
    
    int get_n_features() const { return model.n_features; }
    double get_alpha() const { return model.alpha; }
    double get_l1_ratio() const { return model.l1_ratio; }
    bool get_is_fitted() const { return is_fitted; }    
    double get_learning_rate() const { return model.learning_rate; }

    int count_nonzero_weights(double threshold = 1e-6) const {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted first");
        }
        return elastic_net_count_nonzero(&model, static_cast<float>(threshold));
    }
};

PYBIND11_MODULE(elastic_net_linear, m) {
    m.doc() = "Elastic Net Linear Regression";
    
    py::class_<ElasticNetRegression>(m, "ElasticNetRegression")
        .def(py::init<double, double, double>(), 
             py::arg("alpha") = 0.01, py::arg("l1_ratio") = 0.5, py::arg("learning_rate") = 0.01,
             "Initialize Elastic Net Linear Regression\n\n"
             "Parameters:\n"
             "  alpha: Regularization strength (default: 0.01)\n"
             "  l1_ratio: L1 vs L2 mix, 0=Ridge, 1=LASSO (default: 0.5)\n"
             "  learning_rate: Learning rate for gradient descent (default: 0.01)")
        .def("fit", &ElasticNetRegression::fit,
             py::arg("X"), py::arg("y"), 
             py::arg("max_iterations") = 1000,
             py::arg("tolerance") = 1e-6,
             py::arg("verbose") = true,
             py::arg("check_interval") = 10,
             py::arg("divergence_factor") = 10.0,
             "Fit the model to training data\n\n"
             "Parameters:\n"
             "  X: Training features (n_samples, n_features)\n"
             "  y: Training targets (n_samples,)\n"
             "  max_iterations: Maximum number of iterations (default: 1000)\n"
             "  tolerance: Convergence tolerance (default: 1e-6)\n"
             "  verbose: Print training progress (default: True)\n"
             "  check_interval: Iterations between convergence checks (default: 10)\n"
             "  divergence_factor: Factor for divergence detection (default: 10.0)")
        .def("predict", &ElasticNetRegression::predict,
             py::arg("X"),
             "Predict target values for samples in X\n\n"
             "Parameters:\n"
             "  X: Input features (n_samples, n_features)\n"
             "Returns:\n"
             "  Predicted values (n_samples,)")
        .def("score", &ElasticNetRegression::score,
             py::arg("X"), py::arg("y"),
             "Return the R² score on the given test data\n\n"
             "Parameters:\n"
             "  X: Test features (n_samples, n_features)\n"
             "  y: True target values (n_samples,)\n"
             "Returns:\n"
             "  R² score (coefficient of determination)")
        .def("mean_squared_error", &ElasticNetRegression::mean_squared_error,
             py::arg("X"), py::arg("y"),
             "Return the mean squared error on the given test data\n\n"
             "Parameters:\n"
             "  X: Test features (n_samples, n_features)\n"
             "  y: True target values (n_samples,)\n"
             "Returns:\n"
             "  Mean squared error")
        .def("count_nonzero_weights", &ElasticNetRegression::count_nonzero_weights,
             py::arg("threshold") = 1e-6,
             "Count non-zero weights (sparsity measure)\n\n"
             "Parameters:\n"
             "  threshold: Minimum absolute value to consider non-zero\n"
             "Returns:\n"
             "  Number of non-zero weights")
        .def_property_readonly("coef_", &ElasticNetRegression::get_weights,
                              "Learned coefficients/weights")
        .def_property_readonly("intercept_", &ElasticNetRegression::get_bias,
                              "Learned intercept/bias term")
        .def_property_readonly("n_features_", &ElasticNetRegression::get_n_features,
                              "Number of features")
        .def_property_readonly("alpha", &ElasticNetRegression::get_alpha,
                              "Regularization strength")
        .def_property_readonly("l1_ratio", &ElasticNetRegression::get_l1_ratio,
                              "L1 vs L2 regularization ratio")
        .def_property_readonly("learning_rate", &ElasticNetRegression::get_learning_rate,
                              "Learning rate for gradient descent")
        .def_property_readonly("is_fitted_", &ElasticNetRegression::get_is_fitted,
                              "Whether the model has been fitted");
}
