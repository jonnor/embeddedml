#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// Elastic Net regression for embedded systems
// Fixed version with better numerical stability

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

// Coordinate descent update for one feature - FIXED VERSION
static void update_coordinate(elastic_net_model_t* model,
                             const float* X,
                             const float* y,
                             uint16_t n_samples,
                             uint16_t feature_idx) {
    
    // Calculate residuals without the current feature's contribution
    float sum_residual_x = 0.0f;
    float sum_x_squared = 0.0f;
    
    for (uint16_t i = 0; i < n_samples; i++) {
        // Calculate prediction without current feature
        float prediction = model->bias;
        for (uint16_t j = 0; j < model->n_features; j++) {
            if (j != feature_idx) {
                prediction += model->weights[j] * X[i * model->n_features + j];
            }
        }
        
        // Calculate residual
        float residual = y[i] - prediction;
        float x_ij = X[i * model->n_features + feature_idx];
        
        sum_residual_x += residual * x_ij;
        sum_x_squared += x_ij * x_ij;
    }
    
    if (sum_x_squared > 1e-8f) {  // Avoid division by zero
        // Calculate penalties
        float l1_penalty = model->alpha * model->l1_ratio;
        float l2_penalty = model->alpha * (1.0f - model->l1_ratio);
        
        // Coordinate descent update
        float numerator = sum_residual_x;
        float denominator = sum_x_squared + l2_penalty;
        
        // Apply soft thresholding for L1 penalty
        model->weights[feature_idx] = soft_threshold(numerator / denominator, 
                                                   l1_penalty / denominator);
    }
}

// Update bias term
static void update_bias(elastic_net_model_t* model,
                       const float* X,
                       const float* y,
                       uint16_t n_samples) {
    
    float sum_residuals = 0.0f;
    
    for (uint16_t i = 0; i < n_samples; i++) {
        float prediction = 0.0f;
        for (uint16_t j = 0; j < model->n_features; j++) {
            prediction += model->weights[j] * X[i * model->n_features + j];
        }
        sum_residuals += y[i] - prediction;
    }
    
    model->bias = sum_residuals / n_samples;
}

// Single iteration of coordinate descent
void elastic_net_iterate(elastic_net_model_t* model,
                        const float* X,
                        const float* y,
                        uint16_t n_samples) {
    
    // Update each coordinate
    for (uint16_t j = 0; j < model->n_features; j++) {
        update_coordinate(model, X, y, n_samples, j);
    }
    
    // Update bias
    update_bias(model, X, y, n_samples);
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

// Train model using coordinate descent
void elastic_net_train(elastic_net_model_t* model,
                      const float* X,
                      const float* y,
                      uint16_t n_samples,
                      uint16_t max_iterations,
                      float tolerance,
                      int verbose) {
    
    float prev_mse = 1e10f;
    
    if (verbose) {
        printf("Starting training with alpha=%.4f, l1_ratio=%.2f\n", 
               model->alpha, model->l1_ratio);
        printf("Iter    MSE       Change\n");
        printf("----    ----      ------\n");
    }
    
    for (uint16_t iter = 0; iter < max_iterations; iter++) {
        elastic_net_iterate(model, X, y, n_samples);
        
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

// Example usage with debugging
void example_usage() {
    // Static allocation
    static float weights[4];              // 4 features
    static float X_train[20];             // 5 samples x 4 features = 20 elements
    static float y_train[5];              // 5 target values
    
    // Initialize training data with clear relationship
    float training_data[] = {
        1.0f, 2.0f, 3.0f, 4.0f,    // Sample 1
        2.0f, 3.0f, 4.0f, 5.0f,    // Sample 2
        3.0f, 4.0f, 5.0f, 6.0f,    // Sample 3
        4.0f, 5.0f, 6.0f, 7.0f,    // Sample 4
        5.0f, 6.0f, 7.0f, 8.0f     // Sample 5
    };
    
    // Create targets with known relationship: y = 2*x1 + 3*x2 + 1*x3 + 0*x4 + noise
    float targets[] = {
        2*1.0f + 3*2.0f + 1*3.0f + 0.1f,  // 11.1
        2*2.0f + 3*3.0f + 1*4.0f + 0.2f,  // 17.2
        2*3.0f + 3*4.0f + 1*5.0f + 0.1f,  // 23.1
        2*4.0f + 3*5.0f + 1*6.0f + 0.3f,  // 29.3
        2*5.0f + 3*6.0f + 1*7.0f + 0.2f   // 35.2
    };
    
    // Copy to static arrays
    memcpy(X_train, training_data, sizeof(training_data));
    memcpy(y_train, targets, sizeof(targets));
    
    printf("=== Elastic Net Regression Test ===\n\n");
    
    // Print training data
    printf("Training Data (expected relationship: y = 2*x1 + 3*x2 + 1*x3 + 0*x4 + noise):\n");
    for (uint16_t i = 0; i < 5; i++) {
        printf("Sample %d: [%5.2f, %5.2f, %5.2f, %5.2f] -> %6.2f\n", 
               i + 1,
               X_train[i * 4 + 0],
               X_train[i * 4 + 1], 
               X_train[i * 4 + 2],
               X_train[i * 4 + 3],
               y_train[i]);
    }
    printf("\n");
    
    // Test different regularization settings
    float alphas[] = {0.0f, 0.01f, 0.1f};
    float l1_ratios[] = {0.0f, 0.5f, 1.0f};
    
    for (int a = 0; a < 3; a++) {
        for (int l = 0; l < 3; l++) {
            printf("--- Testing alpha=%.2f, l1_ratio=%.1f ---\n", alphas[a], l1_ratios[l]);
            
            // Initialize model
            elastic_net_model_t model;
            elastic_net_init(&model, weights, 4, alphas[a], l1_ratios[l]);
            
            // Train model
            elastic_net_train(&model, X_train, y_train, 5, 1000, 1e-6f, 0);
            
            // Evaluate
            float mse = elastic_net_mse(&model, X_train, y_train, 5);
            uint16_t nonzero = elastic_net_count_nonzero(&model, 1e-6f);
            
            printf("Results:\n");
            printf("  MSE: %.6f\n", mse);
            printf("  Non-zero weights: %d/4\n", nonzero);
            printf("  Weights: [%7.4f, %7.4f, %7.4f, %7.4f]\n",
                   model.weights[0], model.weights[1], model.weights[2], model.weights[3]);
            printf("  Bias: %7.4f\n", model.bias);
            
            // Test prediction
            float test_sample[] = {1.5f, 2.5f, 3.5f, 4.5f};
            float prediction = elastic_net_predict(&model, test_sample);
            float expected = 2*1.5f + 3*2.5f + 1*3.5f;  // True relationship
            
            printf("  Test prediction: %.4f (expected: %.4f, error: %.4f)\n", 
                   prediction, expected, fabsf(prediction - expected));
            printf("\n");
        }
    }
}

int main(void) {

    example_usage();
}

