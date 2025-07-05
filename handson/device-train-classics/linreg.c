// linreg.c - Simple gradient descent implementation (more reliable than coordinate descent)
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Elastic Net regression for embedded systems
// Using gradient descent instead of coordinate descent for reliability

typedef struct {
    float* weights;           // Pointer to externally allocated weights
    float* weight_gradients;  // Pointer to externally allocated gradient buffer
    float bias;
    uint16_t n_features;
    float l1_ratio;           // Mix of L1 vs L2: 0=Ridge, 1=LASSO
    float alpha;              // Overall regularization strength
    float learning_rate;      // Learning rate for gradient descent
} elastic_net_model_t;

// Soft thresholding function for L1 penalty
static float soft_threshold(float x, float threshold) {
    if (x > threshold) {
        return x - threshold;
    } else if (x < -threshold) {
        return x + threshold;
    } else {
        return 0.0f;
    }
}

// Initialize model with external memory
void elastic_net_init(elastic_net_model_t* model,
                     float* weights_buffer,
                     float* gradients_buffer,
                     uint16_t n_features,
                     float alpha,
                     float l1_ratio,
                     float learning_rate) {
    model->weights = weights_buffer;
    model->weight_gradients = gradients_buffer;
    model->n_features = n_features;
    model->alpha = alpha;
    model->l1_ratio = l1_ratio;
    model->learning_rate = learning_rate;
    model->bias = 0.0f;
    
    // Initialize weights to zero
    memset(weights_buffer, 0, n_features * sizeof(float));
}

// Calculate prediction for a single sample
static float predict_sample(const elastic_net_model_t* model, const float* features) {
    float prediction = model->bias;
    for (uint16_t i = 0; i < model->n_features; i++) {
        prediction += model->weights[i] * features[i];
    }
    return prediction;
}

// Single iteration of gradient descent
void elastic_net_iterate(elastic_net_model_t* model,
                        const float* X,
                        const float* y,
                        uint16_t n_samples) {
    
    // Initialize gradients buffer to zero
    memset(model->weight_gradients, 0, model->n_features * sizeof(float));
    float bias_gradient = 0.0f;
    
    // Forward pass and gradient calculation
    for (uint16_t i = 0; i < n_samples; i++) {
        // Calculate prediction
        float prediction = predict_sample(model, &X[i * model->n_features]);
        
        // Calculate error
        float error = prediction - y[i];  // Note: pred - true for gradient
        
        // Accumulate gradients
        bias_gradient += error;
        for (uint16_t j = 0; j < model->n_features; j++) {
            model->weight_gradients[j] += error * X[i * model->n_features + j];
        }
    }
    
    // Average gradients
    bias_gradient /= n_samples;
    for (uint16_t j = 0; j < model->n_features; j++) {
        model->weight_gradients[j] /= n_samples;
    }
    
    // Update weights with regularization
    for (uint16_t j = 0; j < model->n_features; j++) {
        // Add L2 penalty to gradient
        float l2_penalty = model->alpha * (1.0f - model->l1_ratio) * model->weights[j];
        
        // Update weight
        float new_weight = model->weights[j] - model->learning_rate * (model->weight_gradients[j] + l2_penalty);
        
        // Apply L1 penalty via soft thresholding
        float l1_penalty = model->alpha * model->l1_ratio * model->learning_rate;
        model->weights[j] = soft_threshold(new_weight, l1_penalty);
    }
    
    // Update bias (no regularization on bias)
    model->bias -= model->learning_rate * bias_gradient;
}

// Calculate mean squared error
float elastic_net_mse(const elastic_net_model_t* model,
                     const float* X,
                     const float* y,
                     uint16_t n_samples) {
    
    float mse = 0.0f;
    for (uint16_t i = 0; i < n_samples; i++) {
        float prediction = predict_sample(model, &X[i * model->n_features]);
        float error = y[i] - prediction;
        mse += error * error;
    }
    return mse / n_samples;
}

// Train model using gradient descent
void elastic_net_train(elastic_net_model_t* model,
                      const float* X,
                      const float* y,
                      uint16_t n_samples,
                      uint16_t max_iterations,
                      float tolerance,
                      int verbose,
                      uint16_t check_interval,
                      float divergence_factor) {
    
    float prev_mse = 1e10f;
    
    if (verbose) {
        printf("Starting training with alpha=%.4f, l1_ratio=%.2f, lr=%.4f\n", 
               model->alpha, model->l1_ratio, model->learning_rate);
        printf("Iter    MSE       Change\n");
        printf("----    ----      ------\n");
    }
    
    for (uint16_t iter = 0; iter < max_iterations; iter++) {
        elastic_net_iterate(model, X, y, n_samples);
        
        // Check convergence at specified intervals
        if (iter % check_interval == 0) {
            float mse = elastic_net_mse(model, X, y, n_samples);
            float change = fabsf(prev_mse - mse);
            
            if (verbose) {
                printf("%4d    %.6f  %.6f\n", iter, mse, change);
            }
            
            // Check for convergence
            if (change < tolerance && iter > check_interval * 2) {  // Need at least 2 check intervals
                if (verbose) {
                    printf("Converged at iteration %d\n", iter);
                }
                break;
            }
            
            // Check for divergence
            if (mse > prev_mse * divergence_factor || !isfinite(mse)) {
                if (verbose) {
                    printf("Diverged at iteration %d (MSE: %.6f > %.6f), stopping\n", 
                           iter, mse, prev_mse * divergence_factor);
                }
                break;
            }
            
            prev_mse = mse;
        }
    }
    
    if (verbose) {
        printf("Training completed.\n\n");
    }
}

// Predict using trained model
float elastic_net_predict(const elastic_net_model_t* model, const float* features) {
    return predict_sample(model, features);
}

// Count non-zero weights (sparsity measure)
uint16_t elastic_net_count_nonzero(const elastic_net_model_t* model, float threshold) {
    uint16_t count = 0;
    for (uint16_t i = 0; i < model->n_features; i++) {
        if (fabsf(model->weights[i]) > threshold) {
            count++;
        }
    }
    return count;
}

// Example usage
void example_usage() {
    // Static allocation
    static float weights[4];
    static float weight_gradients[4];     // Working memory for gradients
    static float X_train[20];
    static float y_train[5];
    
    // Simple test case
    float training_data[] = {
        1.0f, 2.0f, 3.0f, 4.0f,
        2.0f, 3.0f, 4.0f, 5.0f,
        3.0f, 4.0f, 5.0f, 6.0f,
        4.0f, 5.0f, 6.0f, 7.0f,
        5.0f, 6.0f, 7.0f, 8.0f
    };
    
    // y = 2*x1 + 3*x2 + 1*x3 + 0*x4 + 1
    float targets[] = {
        2*1.0f + 3*2.0f + 1*3.0f + 1.0f,  // 12
        2*2.0f + 3*3.0f + 1*4.0f + 1.0f,  // 18
        2*3.0f + 3*4.0f + 1*5.0f + 1.0f,  // 24
        2*4.0f + 3*5.0f + 1*6.0f + 1.0f,  // 30
        2*5.0f + 3*6.0f + 1*7.0f + 1.0f   // 36
    };
    
    memcpy(X_train, training_data, sizeof(training_data));
    memcpy(y_train, targets, sizeof(targets));
    
    printf("=== Testing Simple Gradient Descent ===\n");
    
    // Test no regularization
    elastic_net_model_t model;
    elastic_net_init(&model, weights, weight_gradients, 4, 0.0f, 0.0f, 0.01f);
    
    elastic_net_train(&model, X_train, y_train, 5, 2000, 1e-8f, 1, 10, 10.0f);
    
    printf("Results (expected: [2.0, 3.0, 1.0, 0.0], bias=1.0):\n");
    printf("Learned weights: [%.4f, %.4f, %.4f, %.4f]\n",
           model.weights[0], model.weights[1], model.weights[2], model.weights[3]);
    printf("Learned bias: %.4f\n", model.bias);
    printf("Final MSE: %.8f\n", elastic_net_mse(&model, X_train, y_train, 5));
}
