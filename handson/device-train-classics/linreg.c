// linreg.c - Corrected implementation
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Elastic Net regression for embedded systems
// Fixed version using proper coordinate descent with residual maintenance

typedef struct {
    float* weights;     // Pointer to externally allocated weights
    float bias;
    uint16_t n_features;
    float l1_ratio;     // Mix of L1 vs L2: 0=Ridge, 1=LASSO
    float alpha;        // Overall regularization strength
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
                     uint16_t n_features,
                     float alpha,
                     float l1_ratio) {
    model->weights = weights_buffer;
    model->n_features = n_features;
    model->alpha = alpha;
    model->l1_ratio = l1_ratio;
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

// CORRECTED: Proper coordinate descent with residual maintenance
static void update_coordinate_fixed(elastic_net_model_t* model,
                                   const float* X,
                                   const float* y,
                                   uint16_t n_samples,
                                   uint16_t feature_idx,
                                   float* residuals) {
    
    // Calculate X^T * residuals and X^T * X for this feature
    float sum_x_residual = 0.0f;
    float sum_x_squared = 0.0f;
    
    for (uint16_t i = 0; i < n_samples; i++) {
        float x_ij = X[i * model->n_features + feature_idx];
        sum_x_residual += x_ij * residuals[i];
        sum_x_squared += x_ij * x_ij;
    }
    
    if (sum_x_squared > 1e-12f) {  // Avoid division by zero
        // Store old weight for residual update
        float old_weight = model->weights[feature_idx];
        
        // Calculate new weight
        float l1_penalty = model->alpha * model->l1_ratio;
        float l2_penalty = model->alpha * (1.0f - model->l1_ratio);
        
        float numerator = sum_x_residual;
        float denominator = sum_x_squared + l2_penalty;
        
        // Apply soft thresholding for L1 penalty
        float new_weight = soft_threshold(numerator / denominator, 
                                        l1_penalty / denominator);
        
        // Update weight
        model->weights[feature_idx] = new_weight;
        
        // Update residuals: r = r - (new_w - old_w) * X[:, j]
        float weight_change = new_weight - old_weight;
        for (uint16_t i = 0; i < n_samples; i++) {
            float x_ij = X[i * model->n_features + feature_idx];
            residuals[i] -= weight_change * x_ij;
        }
    }
}

// Update bias using residuals
static void update_bias_fixed(elastic_net_model_t* model,
                             float* residuals,
                             uint16_t n_samples) {
    
    float sum_residuals = 0.0f;
    for (uint16_t i = 0; i < n_samples; i++) {
        sum_residuals += residuals[i];
    }
    
    float old_bias = model->bias;
    float new_bias = sum_residuals / n_samples;
    
    model->bias = new_bias;
    
    // Update residuals: r = r - (new_bias - old_bias)
    float bias_change = new_bias - old_bias;
    for (uint16_t i = 0; i < n_samples; i++) {
        residuals[i] -= bias_change;
    }
}

// Single iteration of coordinate descent - FIXED VERSION
void elastic_net_iterate(elastic_net_model_t* model,
                        const float* X,
                        const float* y,
                        uint16_t n_samples,
                        float* residuals) {
    
    // Initialize residuals if needed (first iteration)
    // r = y - X*w - bias
    for (uint16_t i = 0; i < n_samples; i++) {
        residuals[i] = y[i] - predict_sample(model, &X[i * model->n_features]);
    }
    
    // Update each coordinate
    for (uint16_t j = 0; j < model->n_features; j++) {
        update_coordinate_fixed(model, X, y, n_samples, j, residuals);
    }
    
    // Update bias
    update_bias_fixed(model, residuals, n_samples);
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

// Train model using coordinate descent - FIXED VERSION
void elastic_net_train(elastic_net_model_t* model,
                      const float* X,
                      const float* y,
                      uint16_t n_samples,
                      uint16_t max_iterations,
                      float tolerance,
                      int verbose) {
    
    // Allocate residuals buffer
    float* residuals = (float*)malloc(n_samples * sizeof(float));
    if (!residuals) {
        if (verbose) printf("Failed to allocate residuals buffer\n");
        return;
    }
    
    float prev_mse = 1e10f;
    
    if (verbose) {
        printf("Starting training with alpha=%.4f, l1_ratio=%.2f\n", 
               model->alpha, model->l1_ratio);
        printf("Iter    MSE       Change\n");
        printf("----    ----      ------\n");
    }
    
    for (uint16_t iter = 0; iter < max_iterations; iter++) {
        elastic_net_iterate(model, X, y, n_samples, residuals);
        
        // Check convergence every 10 iterations
        if (iter % 10 == 0) {
            float mse = elastic_net_mse(model, X, y, n_samples);
            float change = fabsf(prev_mse - mse);
            
            if (verbose) {
                printf("%4d    %.6f  %.6f\n", iter, mse, change);
            }
            
            if (change < tolerance) {
                if (verbose) {
                    printf("Converged at iteration %d\n", iter);
                }
                break;
            }
            prev_mse = mse;
        }
    }
    
    free(residuals);
    
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
    
    printf("=== Testing Fixed Implementation ===\n");
    
    // Test no regularization
    elastic_net_model_t model;
    elastic_net_init(&model, weights, 4, 0.0f, 0.0f);
    
    elastic_net_train(&model, X_train, y_train, 5, 1000, 1e-8f, 1);
    
    printf("Results (expected: [2.0, 3.0, 1.0, 0.0], bias=1.0):\n");
    printf("Learned weights: [%.4f, %.4f, %.4f, %.4f]\n",
           model.weights[0], model.weights[1], model.weights[2], model.weights[3]);
    printf("Learned bias: %.4f\n", model.bias);
    printf("Final MSE: %.8f\n", elastic_net_mse(&model, X_train, y_train, 5));
}
