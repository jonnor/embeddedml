#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <vector>
#include <memory>
#include <stdexcept>
#include <cstring>
#include <cmath>
#include <cstdlib>

namespace py = pybind11;


#include "logreg_elastic.c"

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


// Python wrapper class
class ElasticNetMulticlass {
private:
    elastic_net_multiclass_model_t model;
    std::vector<float> weights_buffer;
    std::vector<float> bias_buffer;
    std::vector<float> temp_logits;
    std::vector<float> temp_probs;
    std::vector<float> temp_onehot;
    bool is_fitted;

public:
    ElasticNetMulticlass(double alpha = 0.01, double l1_ratio = 0.5) 
        : is_fitted(false) {
        model.alpha = static_cast<float>(alpha);
        model.l1_ratio = static_cast<float>(l1_ratio);
    }
    
    void fit(py::array_t<float> X, py::array_t<uint8_t> y, 
             int max_iterations = 1000, double learning_rate = 0.1, 
             double tolerance = 1e-6, bool verbose = true) {
        
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
        
        // Find number of classes
        py::buffer_info y_buf = y.request();
        uint8_t* y_ptr = static_cast<uint8_t*>(y_buf.ptr);
        uint8_t n_classes = 0;
        for (py::ssize_t i = 0; i < y.shape(0); i++) {
            if (y_ptr[i] > n_classes) {
                n_classes = y_ptr[i];
            }
        }
        n_classes += 1;  // Convert from max index to count
        
        // Initialize model
        model.n_features = n_features;
        model.n_classes = n_classes;
        
        // Allocate memory
        weights_buffer.resize(n_classes * n_features);
        bias_buffer.resize(n_classes);
        temp_logits.resize(n_classes);
        temp_probs.resize(n_classes);
        temp_onehot.resize(n_classes);
        
        // Initialize model
        elastic_net_multiclass_init(&model, weights_buffer.data(), bias_buffer.data(),
                                   n_features, n_classes, model.alpha, model.l1_ratio);
        
        // Get data pointers
        py::buffer_info X_buf = X.request();
        py::buffer_info y_buf_train = y.request();
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        uint8_t* y_ptr_train = static_cast<uint8_t*>(y_buf_train.ptr);
        
        // Copy data to contiguous arrays if needed
        std::vector<float> X_flat;
        std::vector<uint8_t> y_flat;
        
        // Check if arrays are contiguous
        if (X_buf.strides[0] == sizeof(float) * n_features && X_buf.strides[1] == sizeof(float)) {
            // X is already contiguous
        } else {
            // Copy to contiguous array
            X_flat.resize(n_samples * n_features);
            auto X_unchecked = X.unchecked<2>();
            for (py::ssize_t i = 0; i < n_samples; i++) {
                for (py::ssize_t j = 0; j < n_features; j++) {
                    X_flat[i * n_features + j] = X_unchecked(i, j);
                }
            }
            X_ptr = X_flat.data();
        }
        
        if (y_buf_train.strides[0] == sizeof(uint8_t)) {
            // y is already contiguous
        } else {
            // Copy to contiguous array
            y_flat.resize(n_samples);
            auto y_unchecked = y.unchecked<1>();
            for (py::ssize_t i = 0; i < n_samples; i++) {
                y_flat[i] = y_unchecked(i);
            }
            y_ptr_train = y_flat.data();
        }
        
        // Train model
        if (verbose) {
            printf("Starting training with learning rate: %.4f\n", learning_rate);
            printf("Iter     Loss      Accuracy   LR\n");
            printf("----     ----      --------   --\n");
        }
        
        float prev_loss = 1e10f;
        float current_lr = static_cast<float>(learning_rate);
        
        for (int iter = 0; iter < max_iterations; iter++) {
            elastic_net_multiclass_iterate(&model, X_ptr, y_ptr_train, n_samples, current_lr,
                                         temp_logits.data(), temp_probs.data(), temp_onehot.data());
            
            // Check convergence every 10 iterations
            if (iter % 10 == 0) {
                float loss = calculate_cross_entropy_loss(&model, X_ptr, y_ptr_train, n_samples,
                                                        temp_logits.data(), temp_probs.data());
                
                if (verbose) {
                    float accuracy = elastic_net_multiclass_accuracy(&model, X_ptr, y_ptr_train, n_samples,
                                                                   temp_logits.data(), temp_probs.data());
                    printf("%4d     %.4f    %.4f     %.6f\n", iter, loss, accuracy, current_lr);
                }
                
                // Check for convergence
                if (fabsf(prev_loss - loss) < tolerance) {
                    if (verbose) {
                        printf("Converged at iteration %d (loss change: %.6f)\n", 
                               iter, fabsf(prev_loss - loss));
                    }
                    break;
                }
                
                // Check for divergence
                if (loss > prev_loss * 2.0f || !std::isfinite(loss)) {
                    current_lr *= 0.5f;
                    if (verbose) {
                        printf("Reducing learning rate to %.6f (loss: %.4f)\n", current_lr, loss);
                    }
                    
                    if (current_lr < 1e-6f) {
                        if (verbose) {
                            printf("Learning rate too small, stopping training\n");
                        }
                        break;
                    }
                }
                
                prev_loss = loss;
            }
        }
        
        if (verbose) {
            printf("Training completed.\n\n");
        }
        
        is_fitted = true;
    }
    
    py::array_t<uint8_t> predict(py::array_t<float> X) {
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
        auto result = py::array_t<uint8_t>(n_samples);
        py::buffer_info result_buf = result.request();
        uint8_t* result_ptr = static_cast<uint8_t*>(result_buf.ptr);
        
        py::buffer_info X_buf = X.request();
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        
        std::vector<float> sample(model.n_features);
        
        for (py::ssize_t i = 0; i < n_samples; i++) {
            // Copy sample
            for (uint16_t j = 0; j < model.n_features; j++) {
                sample[j] = X_ptr[i * model.n_features + j];
            }
            
            // Predict
            result_ptr[i] = elastic_net_multiclass_predict(&model, sample.data(),
                                                         temp_logits.data(), temp_probs.data());
        }
        
        return result;
    }
    
    py::array_t<float> predict_proba(py::array_t<float> X) {
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
        
        // Create 2D array with proper shape
        std::vector<py::ssize_t> shape = {n_samples, model.n_classes};
        auto result = py::array_t<float>(shape);
        py::buffer_info result_buf = result.request();
        float* result_ptr = static_cast<float*>(result_buf.ptr);
        
        py::buffer_info X_buf = X.request();
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        
        std::vector<float> sample(model.n_features);
        std::vector<float> probabilities(model.n_classes);
        
        for (py::ssize_t i = 0; i < n_samples; i++) {
            // Copy sample
            for (uint16_t j = 0; j < model.n_features; j++) {
                sample[j] = X_ptr[i * model.n_features + j];
            }
            
            // Predict probabilities
            elastic_net_multiclass_predict_proba(&model, sample.data(), 
                                               probabilities.data(), temp_logits.data());
            
            // Copy to result
            for (uint16_t j = 0; j < model.n_classes; j++) {
                result_ptr[i * model.n_classes + j] = probabilities[j];
            }
        }
        
        return result;
    }
    
    double score(py::array_t<float> X, py::array_t<uint8_t> y) {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted before scoring");
        }
        
        if (X.shape(0) != y.shape(0)) {
            throw std::runtime_error("X and y must have the same number of samples");
        }
        
        uint16_t n_samples = static_cast<uint16_t>(X.shape(0));
        
        py::buffer_info X_buf = X.request();
        py::buffer_info y_buf = y.request();
        float* X_ptr = static_cast<float*>(X_buf.ptr);
        uint8_t* y_ptr = static_cast<uint8_t*>(y_buf.ptr);
        
        return elastic_net_multiclass_accuracy(&model, X_ptr, y_ptr, n_samples, 
                                             temp_logits.data(), temp_probs.data());
    }
    
    // Property getters
    py::array_t<float> get_weights() const {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted first");
        }
        
        // Create 2D array with proper shape
        std::vector<py::ssize_t> shape = {model.n_classes, model.n_features};
        auto result = py::array_t<float>(shape);
        py::buffer_info result_buf = result.request();
        float* result_ptr = static_cast<float*>(result_buf.ptr);
        
        for (uint16_t c = 0; c < model.n_classes; c++) {
            for (uint16_t f = 0; f < model.n_features; f++) {
                result_ptr[c * model.n_features + f] = model.weights[c * model.n_features + f];
            }
        }
        
        return result;
    }
    
    py::array_t<float> get_bias() const {
        if (!is_fitted) {
            throw std::runtime_error("Model must be fitted first");
        }
        
        auto result = py::array_t<float>(model.n_classes);
        py::buffer_info result_buf = result.request();
        float* result_ptr = static_cast<float*>(result_buf.ptr);
        
        for (uint16_t c = 0; c < model.n_classes; c++) {
            result_ptr[c] = model.bias[c];
        }
        
        return result;
    }
    
    int get_n_features() const { return model.n_features; }
    int get_n_classes() const { return model.n_classes; }
    double get_alpha() const { return model.alpha; }
    double get_l1_ratio() const { return model.l1_ratio; }
    bool get_is_fitted() const { return is_fitted; }
};

PYBIND11_MODULE(elastic_net_multiclass, m) {
    m.doc() = "Elastic Net Multi-class Logistic Regression";
    
    py::class_<ElasticNetMulticlass>(m, "ElasticNetMulticlass")
        .def(py::init<double, double>(), 
             py::arg("alpha") = 0.01, py::arg("l1_ratio") = 0.5,
             "Initialize Elastic Net Multi-class classifier")
        .def("fit", &ElasticNetMulticlass::fit,
             py::arg("X"), py::arg("y"), 
             py::arg("max_iterations") = 1000,
             py::arg("learning_rate") = 0.1,
             py::arg("tolerance") = 1e-6,
             py::arg("verbose") = true,
             "Fit the model to training data")
        .def("predict", &ElasticNetMulticlass::predict,
             py::arg("X"),
             "Predict class labels for samples in X")
        .def("predict_proba", &ElasticNetMulticlass::predict_proba,
             py::arg("X"),
             "Predict class probabilities for samples in X")
        .def("score", &ElasticNetMulticlass::score,
             py::arg("X"), py::arg("y"),
             "Return the mean accuracy on the given test data and labels")
        .def_property_readonly("weights_", &ElasticNetMulticlass::get_weights,
                              "Learned weights matrix")
        .def_property_readonly("bias_", &ElasticNetMulticlass::get_bias,
                              "Learned bias terms")
        .def_property_readonly("n_features_", &ElasticNetMulticlass::get_n_features,
                              "Number of features")
        .def_property_readonly("n_classes_", &ElasticNetMulticlass::get_n_classes,
                              "Number of classes")
        .def_property_readonly("alpha", &ElasticNetMulticlass::get_alpha,
                              "Regularization strength")
        .def_property_readonly("l1_ratio", &ElasticNetMulticlass::get_l1_ratio,
                              "L1 vs L2 regularization ratio")
        .def_property_readonly("is_fitted_", &ElasticNetMulticlass::get_is_fitted,
                              "Whether the model has been fitted");
}
