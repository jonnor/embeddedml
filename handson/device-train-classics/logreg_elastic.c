#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdio.h>

// Elastic Net Logistic Regression for embedded systems
// Combines L1 (LASSO) and L2 (Ridge) regularization with logistic regression
// Uses coordinate descent with logistic loss

typedef struct {
    float* weights;     // Pointer to externally allocated weights
    float bias;
    uint16_t n_features;
    float l1_ratio;     // Mix of L1 vs L2: 0=Ridge, 1=LASSO
    float alpha;        // Overall regularization strength
} elastic_net_logistic_model_t;

// Sigmoid function with overflow protection
static float sigmoid(float x) {
    if (x > 20.0f) return 1.0f;
    if (x < -20.0f) return 0.0f;
    return 1.0f / (1.0f + expf(-x));
}

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
void elastic_net_logistic_init(elastic_net_logistic_model_t* model,
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

// Calculate linear prediction (before sigmoid)
static float linear_predict(const elastic_net_logistic_model_t* model, const float* features) {
    float prediction = model->bias;
    for (uint16_t i = 0; i < model->n_features; i++) {
        prediction += model->weights[i] * features[i];
    }
    return prediction;
}

// Calculate working weights and response for IRLS (Iterative Reweighted Least Squares)
static void calculate_working_values(const elastic_net_logistic_model_t* model,
                                   const float* X,
                                   const float* y,
                                   uint16_t n_samples,
                                   float* working_weights,
                                   float* working_response) {
    
    for (uint16_t i = 0; i < n_samples; i++) {
        float linear_pred = linear_predict(model, &X[i * model->n_features]);
        float prob = sigmoid(linear_pred);
        
        // Working weight: p(1-p)
        working_weights[i] = prob * (1.0f - prob);
        if (working_weights[i] < 1e-8f) {
            working_weights[i] = 1e-8f;  // Avoid division by zero
        }
        
        // Working response: z = linear_pred + (y - p) / w
        working_response[i] = linear_pred + (y[i] - prob) / working_weights[i];
    }
}

// Coordinate descent update for one feature (weighted least squares)
static void update_coordinate_logistic(elastic_net_logistic_model_t* model,
                                      const float* X,
                                      const float* working_response,
                                      const float* working_weights,
                                      uint16_t n_samples,
                                      uint16_t feature_idx) {
    
    float weighted_sum_x_r = 0.0f;
    float weighted_sum_x_x = 0.0f;
    
    // Calculate weighted sums
    for (uint16_t i = 0; i < n_samples; i++) {
        float x_ij = X[i * model->n_features + feature_idx];
        float w_i = working_weights[i];
        
        // Subtract current contribution
        float residual = working_response[i] - model->weights[feature_idx] * x_ij;
        
        weighted_sum_x_r += w_i * x_ij * residual;
        weighted_sum_x_x += w_i * x_ij * x_ij;
    }
    
    if (weighted_sum_x_x > 1e-8f) {
        // Calculate penalties
        float l1_penalty = model->alpha * model->l1_ratio;
        float l2_penalty = model->alpha * (1.0f - model->l1_ratio);
        
        // Coordinate descent update with elastic net penalty
        float numerator = weighted_sum_x_r;
        float denominator = weighted_sum_x_x + l2_penalty;
        
        // Apply soft thresholding for L1 penalty
        model->weights[feature_idx] = soft_threshold(numerator / denominator, 
                                                   l1_penalty / denominator);
    }
}

// Update bias term
static void update_bias_logistic(elastic_net_logistic_model_t* model,
                                const float* working_response,
                                const float* working_weights,
                                uint16_t n_samples) {
    
    float weighted_sum_r = 0.0f;
    float sum_weights = 0.0f;
    
    for (uint16_t i = 0; i < n_samples; i++) {
        // Subtract current bias contribution
        float residual = working_response[i] - model->bias;
        
        weighted_sum_r += working_weights[i] * residual;
        sum_weights += working_weights[i];
    }
    
    if (sum_weights > 1e-8f) {
        model->bias = weighted_sum_r / sum_weights;
    }
}

// Single IRLS iteration
void elastic_net_logistic_iterate(elastic_net_logistic_model_t* model,
                                 const float* X,
                                 const float* y,
                                 uint16_t n_samples,
                                 float* working_weights,
                                 float* working_response) {
    
    // Calculate working weights and response
    calculate_working_values(model, X, y, n_samples, working_weights, working_response);
    
    // Update each coordinate
    for (uint16_t j = 0; j < model->n_features; j++) {
        update_coordinate_logistic(model, X, working_response, working_weights, 
                                 n_samples, j);
    }
    
    // Update bias
    update_bias_logistic(model, working_response, working_weights, n_samples);
}

// Calculate log-likelihood
static float calculate_log_likelihood(const elastic_net_logistic_model_t* model,
                                    const float* X,
                                    const float* y,
                                    uint16_t n_samples) {
    float log_likelihood = 0.0f;
    
    for (uint16_t i = 0; i < n_samples; i++) {
        float linear_pred = linear_predict(model, &X[i * model->n_features]);
        
        if (y[i] > 0.5f) {  // Positive class
            log_likelihood += linear_pred - logf(1.0f + expf(linear_pred));
        } else {  // Negative class
            log_likelihood += -logf(1.0f + expf(linear_pred));
        }
    }
    
    return log_likelihood;
}

// Train model using coordinate descent with IRLS
void elastic_net_logistic_train(elastic_net_logistic_model_t* model,
                               const float* X,
                               const float* y,
                               uint16_t n_samples,
                               uint16_t max_iterations,
                               float tolerance,
                               float* working_weights,
                               float* working_response) {
    
    float prev_log_likelihood = -1e10f;
    
    for (uint16_t iter = 0; iter < max_iterations; iter++) {
        elastic_net_logistic_iterate(model, X, y, n_samples, 
                                   working_weights, working_response);
        
        // Check convergence every 10 iterations (expensive to compute)
        if (iter % 10 == 0) {
            float log_likelihood = calculate_log_likelihood(model, X, y, n_samples);

            printf("iter loss=%f\n", log_likelihood);
            
            if (fabsf(log_likelihood - prev_log_likelihood) < tolerance) {
                break;  // Converged
            }
            prev_log_likelihood = log_likelihood;

        }
    }
}

// Predict probability
float elastic_net_logistic_predict_proba(const elastic_net_logistic_model_t* model, 
                                        const float* features) {
    float linear_pred = linear_predict(model, features);
    return sigmoid(linear_pred);
}

// Predict class (0 or 1)
uint8_t elastic_net_logistic_predict(const elastic_net_logistic_model_t* model, 
                                    const float* features) {
    return elastic_net_logistic_predict_proba(model, features) > 0.5f ? 1 : 0;
}

// Calculate accuracy on dataset
float elastic_net_logistic_accuracy(const elastic_net_logistic_model_t* model,
                                   const float* X,
                                   const float* y,
                                   uint16_t n_samples) {
    
    uint16_t correct = 0;
    for (uint16_t i = 0; i < n_samples; i++) {
        uint8_t predicted = elastic_net_logistic_predict(model, &X[i * model->n_features]);
        uint8_t actual = (y[i] > 0.5f) ? 1 : 0;
        if (predicted == actual) {
            correct++;
        }
    }
    return (float)correct / n_samples;
}

// Calculate log-loss on dataset
float elastic_net_logistic_log_loss(const elastic_net_logistic_model_t* model,
                                   const float* X,
                                   const float* y,
                                   uint16_t n_samples) {
    
    float total_loss = 0.0f;
    for (uint16_t i = 0; i < n_samples; i++) {
        float prob = elastic_net_logistic_predict_proba(model, &X[i * model->n_features]);
        
        // Clip probabilities to avoid log(0)
        if (prob < 1e-15f) prob = 1e-15f;
        if (prob > 1.0f - 1e-15f) prob = 1.0f - 1e-15f;
        
        if (y[i] > 0.5f) {
            total_loss -= logf(prob);
        } else {
            total_loss -= logf(1.0f - prob);
        }
    }
    return total_loss / n_samples;
}

// Count non-zero weights
uint16_t elastic_net_logistic_count_nonzero(const elastic_net_logistic_model_t* model, 
                                           float threshold) {
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
    static float weights[4];              // 4 features
    static float X_train[20];             // 5 samples x 4 features = 20 elements
    static float y_train[5];              // 5 binary labels
    static float working_weights[5];      // Working weights buffer
    static float working_response[5];     // Working response buffer
    
    // Initialize training data (binary classification)
    float training_data[] = {
        1.0f, 2.0f, 3.0f, 4.0f,    // Sample 1
        2.0f, 3.0f, 4.0f, 5.0f,    // Sample 2
        3.0f, 4.0f, 5.0f, 6.0f,    // Sample 3
        1.5f, 2.5f, 3.5f, 4.5f,    // Sample 4
        0.5f, 1.5f, 2.5f, 3.5f     // Sample 5
    };
    
    float labels[] = {0.0f, 1.0f, 1.0f, 1.0f, 0.0f};  // Binary labels
    
    // Copy to static arrays
    memcpy(X_train, training_data, sizeof(training_data));
    memcpy(y_train, labels, sizeof(labels));
    
    // Initialize model
    elastic_net_logistic_model_t model;
    elastic_net_logistic_init(&model, weights, 4, 0.1f, 0.5f);  // alpha=0.1, l1_ratio=0.5
    
    // Train model
    elastic_net_logistic_train(&model, X_train, y_train, 5, 1000, 1e-7f,
                              working_weights, working_response);
    
    // Evaluate
    float accuracy = elastic_net_logistic_accuracy(&model, X_train, y_train, 5);
    float log_loss = elastic_net_logistic_log_loss(&model, X_train, y_train, 5);
    uint16_t nonzero_weights = elastic_net_logistic_count_nonzero(&model, 1e-6f);
    
    // Make predictions
    float test_sample[] = {1.8f, 2.8f, 3.8f, 4.8f};
    float probability = elastic_net_logistic_predict_proba(&model, test_sample);
    uint8_t prediction = elastic_net_logistic_predict(&model, test_sample);

    printf("out p=%f c=%d\n", probability, prediction);
}

int main(void) {

    example_usage();

}
