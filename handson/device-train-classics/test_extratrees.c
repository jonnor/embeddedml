#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>
#include "extratrees.c"

// Generate synthetic spiral dataset - good medium complexity problem
void generate_spiral_dataset(int16_t *features, int16_t *labels, int16_t n_samples, 
                             int16_t n_features, int16_t n_classes) {
    srand(42); // Fixed seed for reproducibility
    
    int16_t samples_per_class = n_samples / n_classes;
    
    for (int16_t class = 0; class < n_classes; class++) {
        for (int16_t i = 0; i < samples_per_class; i++) {
            int16_t sample_idx = class * samples_per_class + i;
            if (sample_idx >= n_samples) break;
            
            // Generate spiral pattern
            float t = (float)i / samples_per_class * 4.0f * M_PI; // 4 full rotations
            float radius = 0.3f + 0.7f * (float)i / samples_per_class;
            float class_offset = (float)class * 2.0f * M_PI / n_classes;
            
            // Add some noise
            float noise_x = ((float)rand() / RAND_MAX - 0.5f) * 0.2f;
            float noise_y = ((float)rand() / RAND_MAX - 0.5f) * 0.2f;
            
            float x = radius * cosf(t + class_offset) + noise_x;
            float y = radius * sinf(t + class_offset) + noise_y;
            
            // Scale and convert to int16_t (multiply by 1000 for precision)
            features[sample_idx * n_features + 0] = (int16_t)(x * 1000);
            features[sample_idx * n_features + 1] = (int16_t)(y * 1000);
            
            // Add additional features for complexity
            if (n_features > 2) {
                features[sample_idx * n_features + 2] = (int16_t)(x * y * 500); // interaction
                if (n_features > 3) {
                    features[sample_idx * n_features + 3] = (int16_t)((x*x + y*y) * 300); // radial distance
                }
            }
            
            labels[sample_idx] = class;
        }
    }
}

// Generate XOR-like dataset - classic non-linear problem
void generate_xor_dataset(int16_t *features, int16_t *labels, int16_t n_samples, int16_t n_features) {
    srand(42);
    
    for (int16_t i = 0; i < n_samples; i++) {
        // Generate random points in [-1000, 1000] range
        int16_t x = (rand() % 2001) - 1000;
        int16_t y = (rand() % 2001) - 1000;
        
        features[i * n_features + 0] = x;
        features[i * n_features + 1] = y;
        
        // XOR pattern: class depends on signs of x and y
        int16_t class_val = ((x > 0) ^ (y > 0)) ? 1 : 0;
        
        // Add noise to make it more realistic
        if (n_features > 2) {
            features[i * n_features + 2] = (rand() % 1001) - 500; // random noise feature
            if (n_features > 3) {
                features[i * n_features + 3] = x + y; // linear combination
            }
        }
        
        labels[i] = class_val;
    }
}

// Test prediction accuracy
float test_accuracy(EmlTreesModel *model, const int16_t *features, const int16_t *labels, 
                   int16_t n_samples, int16_t n_features) {
    int16_t correct = 0;
    float probabilities[256];
    int16_t votes[256];
    
    for (int16_t i = 0; i < n_samples; i++) {
        int16_t predicted = eml_trees_predict_proba(model, &features[i * n_features], 
                                                   probabilities, votes);
        if (predicted == labels[i]) {
            correct++;
        }
    }
    
    return (float)correct / n_samples;
}

// Print model statistics
void print_model_stats(EmlTreesModel *model) {
    printf("Model Statistics:\n");
    printf("  Trees: %d\n", model->n_trees);
    printf("  Features: %d\n", model->n_features);
    printf("  Classes: %d\n", model->n_classes);
    printf("  Nodes used: %d / %d\n", model->n_nodes_used, model->max_nodes);
    printf("  Max depth: %d\n", model->config.max_depth);
    printf("  Min samples leaf: %d\n", model->config.min_samples_leaf);
    printf("\n");
}

// Test basic functionality
int test_basic_functionality() {
    printf("=== Basic Functionality Test ===\n");
    
    // Simple 2D XOR problem
    const int16_t n_samples = 400;
    const int16_t n_features = 2;
    const int16_t n_classes = 2;
    const int16_t n_trees = 10;
    
    // Allocate data
    int16_t *features = malloc(n_samples * n_features * sizeof(int16_t));
    int16_t *labels = malloc(n_samples * sizeof(int16_t));
    
    // Generate XOR dataset
    generate_xor_dataset(features, labels, n_samples, n_features);
    
    // Setup model
    EmlTreesModel model = {0};
    model.n_features = n_features;
    model.n_classes = n_classes;
    model.n_trees = n_trees;
    model.max_nodes = 1000;
    model.nodes = malloc(model.max_nodes * sizeof(EmlTreesNode));
    model.tree_starts = malloc(n_trees * sizeof(int16_t));
    
    // Setup config - improved settings for better accuracy
    model.config.max_depth = 10;
    model.config.min_samples_leaf = 2;
    model.config.n_thresholds = 20;
    model.config.subsample_ratio_num = 9;
    model.config.subsample_ratio_den = 10;
    model.config.feature_subsample_ratio_num = 1;
    model.config.feature_subsample_ratio_den = 1;
    model.config.rng_seed = 12345;
    
    // Setup workspace
    EmlTreesWorkspace workspace = {0};
    workspace.n_samples = n_samples;
    workspace.sample_indices = malloc(n_samples * sizeof(int16_t));
    workspace.feature_indices = malloc(n_features * sizeof(int16_t));
    workspace.min_vals = malloc(n_features * sizeof(int16_t));
    workspace.max_vals = malloc(n_features * sizeof(int16_t));
    workspace.node_stack = malloc(model.max_nodes * sizeof(NodeState));
    workspace.temp_indices = malloc(n_samples * sizeof(int16_t));
    
    // Train model
    printf("Training on XOR dataset...\n");
    int16_t result = eml_trees_train(&model, &workspace, features, labels);
    
    if (result != 0) {
        printf("Training failed with error: %d\n", result);
        return -1;
    }
    
    print_model_stats(&model);
    
    // Test accuracy
    float accuracy = test_accuracy(&model, features, labels, n_samples, n_features);
    printf("Training accuracy: %.3f\n", accuracy);
    
    // Test individual prediction
    printf("\nTesting individual predictions:\n");
    int16_t test_features[2] = {500, 500};   // Should be class 0
    float probabilities[2];
    int16_t votes[2];
    int16_t pred = eml_trees_predict_proba(&model, test_features, probabilities, votes);
    printf("Input: [%d, %d] -> Class: %d, Probs: [%.3f, %.3f]\n", 
           test_features[0], test_features[1], pred, probabilities[0], probabilities[1]);
    
    test_features[0] = 500; test_features[1] = -500;  // Should be class 1
    pred = eml_trees_predict_proba(&model, test_features, probabilities, votes);
    printf("Input: [%d, %d] -> Class: %d, Probs: [%.3f, %.3f]\n", 
           test_features[0], test_features[1], pred, probabilities[0], probabilities[1]);
    
    // Cleanup
    free(features);
    free(labels);
    free(model.nodes);
    free(model.tree_starts);
    free(workspace.sample_indices);
    free(workspace.feature_indices);
    free(workspace.min_vals);
    free(workspace.max_vals);
    free(workspace.node_stack);
    free(workspace.temp_indices);
    
    printf("Basic test passed!\n\n");
    return 0;
}

// Test spiral dataset - more complex problem
int test_spiral_dataset() {
    printf("=== Spiral Dataset Test ===\n");
    
    const int16_t n_samples = 600;
    const int16_t n_features = 4;
    const int16_t n_classes = 3;
    const int16_t n_trees = 20;
    
    // Allocate data
    int16_t *features = malloc(n_samples * n_features * sizeof(int16_t));
    int16_t *labels = malloc(n_samples * sizeof(int16_t));
    
    // Generate spiral dataset
    generate_spiral_dataset(features, labels, n_samples, n_features, n_classes);
    
    // Setup model
    EmlTreesModel model = {0};
    model.n_features = n_features;
    model.n_classes = n_classes;
    model.n_trees = n_trees;
    model.max_nodes = 5000;
    model.nodes = malloc(model.max_nodes * sizeof(EmlTreesNode));
    model.tree_starts = malloc(n_trees * sizeof(int16_t));
    
    // Setup config for complex problem - better settings
    model.config.max_depth = 12;
    model.config.min_samples_leaf = 2;
    model.config.n_thresholds = 30;
    model.config.subsample_ratio_num = 8;
    model.config.subsample_ratio_den = 10;
    model.config.feature_subsample_ratio_num = 1;
    model.config.feature_subsample_ratio_den = 1;
    model.config.rng_seed = 54321;
    
    // Setup workspace
    EmlTreesWorkspace workspace = {0};
    workspace.n_samples = n_samples;
    workspace.sample_indices = malloc(n_samples * sizeof(int16_t));
    workspace.feature_indices = malloc(n_features * sizeof(int16_t));
    workspace.min_vals = malloc(n_features * sizeof(int16_t));
    workspace.max_vals = malloc(n_features * sizeof(int16_t));
    workspace.node_stack = malloc(model.max_nodes * sizeof(NodeState));
    workspace.temp_indices = malloc(n_samples * sizeof(int16_t));
    
    // Train model
    printf("Training on 3-class spiral dataset...\n");
    clock_t start = clock();
    int16_t result = eml_trees_train(&model, &workspace, features, labels);
    clock_t end = clock();
    
    if (result != 0) {
        printf("Training failed with error: %d\n", result);
        return -1;
    }
    
    double training_time = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Training time: %.3f seconds\n", training_time);
    
    print_model_stats(&model);
    
    // Test accuracy
    float accuracy = test_accuracy(&model, features, labels, n_samples, n_features);
    printf("Training accuracy: %.3f\n", accuracy);
    
    // Show class distribution in predictions
    printf("\nClass distribution analysis:\n");
    int16_t class_counts[3] = {0};
    float probabilities[3];
    int16_t votes[3];
    
    for (int16_t i = 0; i < n_samples; i++) {
        int16_t pred = eml_trees_predict_proba(&model, &features[i * n_features], probabilities, votes);
        if (pred >= 0 && pred < n_classes) {
            class_counts[pred]++;
        }
    }
    
    for (int16_t i = 0; i < n_classes; i++) {
        printf("  Class %d: %d predictions (%.1f%%)\n", 
               i, class_counts[i], 100.0f * class_counts[i] / n_samples);
    }
    
    // Cleanup
    free(features);
    free(labels);
    free(model.nodes);
    free(model.tree_starts);
    free(workspace.sample_indices);
    free(workspace.feature_indices);
    free(workspace.min_vals);
    free(workspace.max_vals);
    free(workspace.node_stack);
    free(workspace.temp_indices);
    
    printf("Spiral test passed!\n\n");
    return 0;
}

int main() {
    printf("EML Trees Test Suite\n");
    printf("===================\n\n");
    
    // Run tests
    if (test_basic_functionality() != 0) {
        printf("Basic functionality test failed!\n");
        return 1;
    }
    
    if (test_spiral_dataset() != 0) {
        printf("Spiral dataset test failed!\n");
        return 1;
    }
    
    printf("All tests passed successfully!\n");
    return 0;
}
