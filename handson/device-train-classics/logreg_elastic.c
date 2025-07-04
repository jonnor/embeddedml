#include <stdint.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

// Elastic Net Multi-class Logistic Regression for embedded systems
// Fixed version with better numerical stability
// External static allocation for flexibility

typedef struct {
    float* weights;     // n_classes x n_features weight matrix
    float* bias;        // n_classes bias terms
    uint16_t n_features;
    uint16_t n_classes;
    float l1_ratio;     // Mix of L1 vs L2: 0=Ridge, 1=LASSO
    float alpha;        // Overall regularization strength
} elastic_net_multiclass_model_t;

// Numerically stable softmax function
static void softmax(const float* logits, float* probabilities, uint16_t n_classes) {
    // Find maximum for numerical stability
    float max_logit = logits[0];
    for (uint16_t i = 1; i < n_classes; i++) {
        if (logits[i] > max_logit) {
            max_logit = logits[i];
        }
    }
    
    // Compute exp(logit - max) and sum
    float sum_exp = 0.0f;
    for (uint16_t i = 0; i < n_classes; i++) {
        float shifted = logits[i] - max_logit;
        if (shifted < -20.0f) {
            probabilities[i] = 0.0f;
        } else {
            probabilities[i] = expf(shifted);
        }
        sum_exp += probabilities[i];
    }
    
    // Normalize with minimum threshold
    if (sum_exp < 1e-8f) {
        // Fallback to uniform distribution
        for (uint16_t i = 0; i < n_classes; i++) {
            probabilities[i] = 1.0f / n_classes;
        }
    } else {
        for (uint16_t i = 0; i < n_classes; i++) {
            probabilities[i] /= sum_exp;
            // Ensure minimum probability to avoid log(0)
            if (probabilities[i] < 1e-15f) {
                probabilities[i] = 1e-15f;
            }
        }
    }
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
void elastic_net_multiclass_init(elastic_net_multiclass_model_t* model,
                                 float* weights_buffer,    // n_classes x n_features
                                 float* bias_buffer,       // n_classes
                                 uint16_t n_features,
                                 uint16_t n_classes,
                                 float alpha,
                                 float l1_ratio) {
    model->weights = weights_buffer;
    model->bias = bias_buffer;
    model->n_features = n_features;
    model->n_classes = n_classes;
    model->alpha = alpha;
    model->l1_ratio = l1_ratio;
    
    // Initialize weights to small random values for symmetry breaking
    for (uint16_t i = 0; i < n_classes * n_features; i++) {
        weights_buffer[i] = 0.01f * (((float)(i % 7) - 3.0f) / 3.0f);
    }
    
    // Initialize bias to zero
    memset(bias_buffer, 0, n_classes * sizeof(float));
}

// Calculate logits for a sample
static void calculate_logits(const elastic_net_multiclass_model_t* model,
                           const float* features,
                           float* logits) {
    for (uint16_t c = 0; c < model->n_classes; c++) {
        logits[c] = model->bias[c];
        for (uint16_t f = 0; f < model->n_features; f++) {
            logits[c] += model->weights[c * model->n_features + f] * features[f];
        }
    }
}

// Convert integer class label to one-hot encoding
static void class_to_onehot(uint8_t class_label, float* onehot, uint16_t n_classes) {
    for (uint16_t i = 0; i < n_classes; i++) {
        onehot[i] = (i == class_label) ? 1.0f : 0.0f;
    }
}

// Simplified gradient descent update (more stable than coordinate descent for multiclass)
void elastic_net_multiclass_iterate(elastic_net_multiclass_model_t* model,
                                   const float* X,
                                   const uint8_t* y,
                                   uint16_t n_samples,
                                   float learning_rate,
                                   float* temp_logits,
                                   float* temp_probs,
                                   float* temp_onehot) {
    
    // Initialize gradients
    float* weight_gradients = (float*)calloc(model->n_classes * model->n_features, sizeof(float));
    float* bias_gradients = (float*)calloc(model->n_classes, sizeof(float));
    
    if (!weight_gradients || !bias_gradients) {
        // Handle allocation failure - skip this iteration
        if (weight_gradients) free(weight_gradients);
        if (bias_gradients) free(bias_gradients);
        return;
    }
    
    // Calculate gradients
    for (uint16_t i = 0; i < n_samples; i++) {
        // Forward pass
        calculate_logits(model, &X[i * model->n_features], temp_logits);
        softmax(temp_logits, temp_probs, model->n_classes);
        
        // Convert true label to one-hot
        class_to_onehot(y[i], temp_onehot, model->n_classes);
        
        // Calculate error (predicted - true)
        for (uint16_t c = 0; c < model->n_classes; c++) {
            float error = temp_probs[c] - temp_onehot[c];
            
            // Accumulate bias gradient
            bias_gradients[c] += error;
            
            // Accumulate weight gradients
            for (uint16_t f = 0; f < model->n_features; f++) {
                weight_gradients[c * model->n_features + f] += error * X[i * model->n_features + f];
            }
        }
    }
    
    // Update weights with regularization
    for (uint16_t c = 0; c < model->n_classes; c++) {
        for (uint16_t f = 0; f < model->n_features; f++) {
            float gradient = weight_gradients[c * model->n_features + f] / n_samples;
            
            // Add L2 penalty gradient
            float l2_penalty = model->alpha * (1.0f - model->l1_ratio) * model->weights[c * model->n_features + f];
            
            // Update weight
            float new_weight = model->weights[c * model->n_features + f] - learning_rate * (gradient + l2_penalty);
            
            // Apply L1 penalty via soft thresholding
            float l1_penalty = model->alpha * model->l1_ratio * learning_rate;
            model->weights[c * model->n_features + f] = soft_threshold(new_weight, l1_penalty);
        }
        
        // Update bias (no regularization on bias)
        model->bias[c] -= learning_rate * bias_gradients[c] / n_samples;
    }
    
    free(weight_gradients);
    free(bias_gradients);
}

// Calculate cross-entropy loss
static float calculate_cross_entropy_loss(const elastic_net_multiclass_model_t* model,
                                        const float* X,
                                        const uint8_t* y,
                                        uint16_t n_samples,
                                        float* temp_logits,
                                        float* temp_probs) {
    float total_loss = 0.0f;
    
    for (uint16_t i = 0; i < n_samples; i++) {
        calculate_logits(model, &X[i * model->n_features], temp_logits);
        softmax(temp_logits, temp_probs, model->n_classes);
        
        if (y[i] < model->n_classes) {
            float prob = temp_probs[y[i]];
            total_loss -= logf(prob);  // Cross-entropy loss
        }
    }
    
    return total_loss / n_samples;
}

// Train model using gradient descent
void elastic_net_multiclass_train(elastic_net_multiclass_model_t* model,
                                 const float* X,
                                 const uint8_t* y,
                                 uint16_t n_samples,
                                 uint16_t max_iterations,
                                 float learning_rate,
                                 float tolerance,
                                 float* temp_logits,        // n_classes
                                 float* temp_probs,         // n_classes
                                 float* temp_onehot) {      // n_classes
    
    float prev_loss = 1e10f;
    
    for (uint16_t iter = 0; iter < max_iterations; iter++) {
        elastic_net_multiclass_iterate(model, X, y, n_samples, learning_rate,
                                     temp_logits, temp_probs, temp_onehot);
        
        // Check convergence every 10 iterations
        if (iter % 10 == 0) {
            float loss = calculate_cross_entropy_loss(model, X, y, n_samples,
                                                    temp_logits, temp_probs);
            
            // Check for convergence
            if (fabsf(prev_loss - loss) < tolerance) {
                break;
            }
            
            // Check for divergence
            if (loss > prev_loss * 2.0f || !isfinite(loss)) {
                // Reduce learning rate and continue
                learning_rate *= 0.5f;
                if (learning_rate < 1e-6f) {
                    break;  // Learning rate too small
                }
            }
            
            prev_loss = loss;
        }
    }
}

// Predict class probabilities
void elastic_net_multiclass_predict_proba(const elastic_net_multiclass_model_t* model,
                                         const float* features,
                                         float* probabilities,
                                         float* temp_logits) {
    calculate_logits(model, features, temp_logits);
    softmax(temp_logits, probabilities, model->n_classes);
}

// Predict class
uint8_t elastic_net_multiclass_predict(const elastic_net_multiclass_model_t* model,
                                      const float* features,
                                      float* temp_logits,
                                      float* temp_probs) {
    elastic_net_multiclass_predict_proba(model, features, temp_probs, temp_logits);
    
    // Find class with highest probability
    uint8_t best_class = 0;
    float best_prob = temp_probs[0];
    
    for (uint16_t c = 1; c < model->n_classes; c++) {
        if (temp_probs[c] > best_prob) {
            best_prob = temp_probs[c];
            best_class = c;
        }
    }
    
    return best_class;
}

// Calculate accuracy
float elastic_net_multiclass_accuracy(const elastic_net_multiclass_model_t* model,
                                     const float* X,
                                     const uint8_t* y,
                                     uint16_t n_samples,
                                     float* temp_logits,
                                     float* temp_probs) {
    
    uint16_t correct = 0;
    for (uint16_t i = 0; i < n_samples; i++) {
        uint8_t predicted = elastic_net_multiclass_predict(model, &X[i * model->n_features],
                                                         temp_logits, temp_probs);
        if (predicted == y[i]) {
            correct++;
        }
    }
    return (float)correct / n_samples;
}

// Calculate cross-entropy loss on dataset
float elastic_net_multiclass_loss(const elastic_net_multiclass_model_t* model,
                                 const float* X,
                                 const uint8_t* y,
                                 uint16_t n_samples,
                                 float* temp_logits,
                                 float* temp_probs) {
    return calculate_cross_entropy_loss(model, X, y, n_samples, temp_logits, temp_probs);
}

// Count non-zero weights across all classes
uint16_t elastic_net_multiclass_count_nonzero(const elastic_net_multiclass_model_t* model,
                                             float threshold) {
    uint16_t count = 0;
    for (uint16_t c = 0; c < model->n_classes; c++) {
        for (uint16_t f = 0; f < model->n_features; f++) {
            if (fabsf(model->weights[c * model->n_features + f]) > threshold) {
                count++;
            }
        }
    }
    return count;
}

// Example usage with better parameter settings
void example_usage() {
    // Static allocation for 3-class classification with 4 features
    static float weights[12];              // 3 classes x 4 features = 12 elements
    static float bias[3];                  // 3 classes
    static float X_train[20];              // 5 samples x 4 features = 20 elements
    static uint8_t y_train[5];             // 5 class labels (0, 1, or 2)
    
    // Temp arrays for training and prediction
    static float temp_logits[3];           // 3 classes
    static float temp_probs[3];            // 3 classes
    static float temp_onehot[3];           // 3 classes
    
    // Initialize training data with better separation
    float training_data[] = {
        -1.0f, -1.0f, 0.0f, 0.0f,    // Sample 1 -> class 0
        0.0f, 0.0f, 1.0f, 1.0f,      // Sample 2 -> class 1
        1.0f, 1.0f, 2.0f, 2.0f,      // Sample 3 -> class 2
        -0.5f, -0.5f, 0.5f, 0.5f,    // Sample 4 -> class 1
        -1.5f, -1.5f, -0.5f, -0.5f   // Sample 5 -> class 0
    };
    
    uint8_t labels[] = {0, 1, 2, 1, 0};    // Multi-class labels
    
    // Copy to static arrays
    memcpy(X_train, training_data, sizeof(training_data));
    memcpy(y_train, labels, sizeof(labels));
    
    // Initialize model with smaller regularization
    elastic_net_multiclass_model_t model;
    elastic_net_multiclass_init(&model, weights, bias, 4, 3, 0.01f, 0.5f);
    
    // Train model with appropriate learning rate
    elastic_net_multiclass_train(&model, X_train, y_train, 5, 1000, 0.1f, 1e-6f,
                                temp_logits, temp_probs, temp_onehot);
    
    // Evaluate
    float accuracy = elastic_net_multiclass_accuracy(&model, X_train, y_train, 5,
                                                   temp_logits, temp_probs);
    float loss = elastic_net_multiclass_loss(&model, X_train, y_train, 5,
                                            temp_logits, temp_probs);
    uint16_t nonzero_weights = elastic_net_multiclass_count_nonzero(&model, 1e-6f);
    
    // Make predictions
    float test_sample[] = {0.5f, 0.5f, 1.5f, 1.5f};
    uint8_t predicted_class = elastic_net_multiclass_predict(&model, test_sample,
                                                           temp_logits, temp_probs);
    
    // Get class probabilities
    float class_probabilities[3];
    elastic_net_multiclass_predict_proba(&model, test_sample, class_probabilities, temp_logits);
}


int main(void) {

    example_usage();
}

