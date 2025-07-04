#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdio.h>

// Elastic Net regression for embedded systems
// Combines L1 (LASSO) and L2 (Ridge) regularization
// Uses external static allocation for flexibility

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

// Coordinate descent update for one feature
static void update_coordinate(elastic_net_model_t* model,
                             const float* X,
                             const float* y,
                             uint16_t n_samples,
                             uint16_t feature_idx,
                             float* residuals) {
    
    float sum_x_r = 0.0f;
    float sum_x_x = 0.0f;
    
    // Calculate sums for coordinate update
    for (uint16_t i = 0; i < n_samples; i++) {
        float x_ij = X[i * model->n_features + feature_idx];
        sum_x_r += x_ij * residuals[i];
        sum_x_x += x_ij * x_ij;
    }
    
    // Add back contribution of current weight to residuals
    float old_weight = model->weights[feature_idx];
    for (uint16_t i = 0; i < n_samples; i++) {
        float x_ij = X[i * model->n_features + feature_idx];
        residuals[i] += old_weight * x_ij;
        sum_x_r += x_ij * residuals[i];
    }
    
    if (sum_x_x > 1e-8f) {  // Avoid division by zero
        // Calculate L1 and L2 penalties
        float l1_penalty = model->alpha * model->l1_ratio;
        float l2_penalty = model->alpha * (1.0f - model->l1_ratio);
        
        // Coordinate descent update with elastic net penalty
        float numerator = sum_x_r;
        float denominator = sum_x_x + l2_penalty;
        
        // Apply soft thresholding for L1 penalty
        float new_weight = soft_threshold(numerator / denominator, l1_penalty / denominator);
        
        // Update residuals with new weight
        float weight_diff = new_weight - old_weight;
        for (uint16_t i = 0; i < n_samples; i++) {
            float x_ij = X[i * model->n_features + feature_idx];
            residuals[i] -= weight_diff * x_ij;
        }
        
        model->weights[feature_idx] = new_weight;
    }
}

// Single iteration of coordinate descent
void elastic_net_iterate(elastic_net_model_t* model,
                        const float* X,
                        const float* y,
                        uint16_t n_samples,
                        float* residuals_buffer) {
    
    // Initialize residuals
    for (uint16_t i = 0; i < n_samples; i++) {
        float prediction = model->bias;
        for (uint16_t j = 0; j < model->n_features; j++) {
            prediction += model->weights[j] * X[i * model->n_features + j];
        }
        residuals_buffer[i] = y[i] - prediction;
    }
    
    // Update each coordinate
    for (uint16_t j = 0; j < model->n_features; j++) {
        update_coordinate(model, X, y, n_samples, j, residuals_buffer);
    }
    
    // Update bias
    float sum_residuals = 0.0f;
    for (uint16_t i = 0; i < n_samples; i++) {
        sum_residuals += residuals_buffer[i];
    }
    model->bias += sum_residuals / n_samples;
}

// Train model using coordinate descent
void elastic_net_train(elastic_net_model_t* model,
                      const float* X,
                      const float* y,
                      uint16_t n_samples,
                      uint16_t max_iterations,
                      float tolerance,
                      float* residuals_buffer) {
    
    float prev_loss = 1e10f;
    
    for (uint16_t iter = 0; iter < max_iterations; iter++) {
        elastic_net_iterate(model, X, y, n_samples, residuals_buffer);
        
        // Check convergence
        float loss = 0.0f;
        for (uint16_t i = 0; i < n_samples; i++) {
            loss += residuals_buffer[i] * residuals_buffer[i];
        }
        loss /= n_samples;
        
        printf("iter loss=%f \n");
        if (fabsf(prev_loss - loss) < tolerance) {
            break;  // Converged
        }
        prev_loss = loss;
    }
}

// Predict using trained model
float elastic_net_predict(const elastic_net_model_t* model, const float* features) {
    float prediction = model->bias;
    for (uint16_t i = 0; i < model->n_features; i++) {
        prediction += model->weights[i] * features[i];
    }
    return prediction;
}

// Calculate mean squared error on dataset
float elastic_net_evaluate(const elastic_net_model_t* model,
                          const float* X,
                          const float* y,
                          uint16_t n_samples) {
    
    float mse = 0.0f;
    for (uint16_t i = 0; i < n_samples; i++) {
        const float* sample = &X[i * model->n_features];
        float pred = elastic_net_predict(model, sample);
        float error = y[i] - pred;
        mse += error * error;
    }
    return mse / n_samples;
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
    // Static allocation outside the functions
    static float weights[5];              // 5 features
    static float X_train[20];             // 4 samples x 5 features = 20 elements
    static float y_train[4];              // 4 target values
    static float residuals[4];            // Temporary buffer for training
    
    // Initialize training data
    float training_data[] = {
        1.0f, 2.0f, 3.0f, 4.0f, 5.0f,    // Sample 1
        1.5f, 2.5f, 3.5f, 4.5f, 5.5f,    // Sample 2
        2.0f, 3.0f, 4.0f, 5.0f, 6.0f,    // Sample 3
        1.2f, 2.2f, 3.2f, 4.2f, 5.2f     // Sample 4
    };
    
    float targets[] = {15.0f, 17.5f, 20.0f, 15.8f};
    
    // Copy to static arrays
    memcpy(X_train, training_data, sizeof(training_data));
    memcpy(y_train, targets, sizeof(targets));
    
    // Initialize model
    elastic_net_model_t model;
    elastic_net_init(&model, weights, 5, 0.1f, 0.5f);  // alpha=0.1, l1_ratio=0.5
    
    // Train model
    elastic_net_train(&model, X_train, y_train, 4, 20, 1e-6f, residuals);
    
    // Evaluate
    float mse = elastic_net_evaluate(&model, X_train, y_train, 4);
    uint16_t nonzero_weights = elastic_net_count_nonzero(&model, 1e-6f);
    
    // Make prediction on new data
    float test_sample[] = {1.3f, 2.3f, 3.3f, 4.3f, 5.3f};
    float prediction = elastic_net_predict(&model, test_sample);

    printf("out=%f\n", prediction);
}

int main(void) {

    example_usage();
}

