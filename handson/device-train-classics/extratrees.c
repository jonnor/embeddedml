#include <stdint.h>
#include <stdlib.h>
#include <string.h>

typedef struct _EmlTreesNode {
    int8_t feature;   // -1 for leaf nodes
    int16_t value;    // threshold or class label
    int16_t left;     // left child index
    int16_t right;    // right child index
} EmlTreesNode;

typedef struct _NodeState {
    int16_t node_idx;     // current node being processed
    int16_t start;        // sample range start
    int16_t end;          // sample range end
    int16_t depth;        // current depth
} NodeState;

typedef struct _EmlTreesConfig {
    int16_t max_depth;
    int16_t min_samples_leaf;
    int16_t n_thresholds;
    int16_t subsample_ratio_num;  // numerator of subsample ratio
    int16_t subsample_ratio_den;  // denominator of subsample ratio
    int16_t feature_subsample_ratio_num;
    int16_t feature_subsample_ratio_den;
    uint32_t rng_seed;
} EmlTreesConfig;

typedef struct _EmlTreesModel {
    EmlTreesNode *nodes;          // Pre-allocated node array
    int16_t *tree_starts;         // Start index for each tree
    int16_t max_nodes;            // Maximum nodes available
    int16_t n_nodes_used;         // Current nodes used
    int16_t n_features;           // Number of features
    int16_t n_classes;            // Number of classes
    int16_t n_trees;              // Number of trees
    EmlTreesConfig config;
} EmlTreesModel;

typedef struct _EmlTreesWorkspace {
    int16_t *sample_indices;      // Sample indices for current tree
    int16_t *feature_indices;     // Feature indices for current tree
    int16_t *min_vals;            // Min values per feature [n_features]
    int16_t *max_vals;            // Max values per feature [n_features]
    NodeState *node_stack;        // Stack for tree building
    int16_t *temp_indices;        // Temporary array for partitioning
    uint32_t rng_state;           // Simple RNG state
    int16_t n_samples;            // Number of samples
} EmlTreesWorkspace;

// Simple linear congruential generator
static uint32_t eml_rand(uint32_t *state) {
    *state = *state * 1103515245 + 12345;
    return *state;
}

// Fisher-Yates shuffle for subsampling
static void shuffle_indices(int16_t *indices, int16_t n, uint32_t *rng_state) {
    for (int16_t i = 0; i < n - 1; i++) {
        int16_t j = i + (eml_rand(rng_state) % (n - i));
        int16_t temp = indices[i];
        indices[i] = indices[j];
        indices[j] = temp;
    }
}

// Calculate Gini impurity using floating point
static float calculate_gini_float(const int16_t *labels, const int16_t *indices, 
                                 int16_t start, int16_t end, int16_t n_classes) {
    int16_t counts[256] = {0}; // Assume max 256 classes
    int16_t total = end - start;
    
    if (total == 0) return 0.0f;
    
    for (int16_t i = start; i < end; i++) {
        counts[labels[indices[i]]]++;
    }
    
    float gini = 1.0f;
    for (int16_t i = 0; i < n_classes; i++) {
        if (counts[i] > 0) {
            float prob = (float)counts[i] / (float)total;
            gini -= prob * prob;
        }
    }
    
    return gini;
}

// Find best split for a node using floating point Gini
static int16_t find_best_split(const int16_t *features, const int16_t *labels,
                              EmlTreesModel *model, EmlTreesWorkspace *workspace, 
                              int16_t start, int16_t end, int16_t n_features_subset, 
                              int8_t *best_feature, int16_t *best_threshold) {
    
    float best_improvement = -1.0f; // Best information gain found
    *best_feature = -1;
    *best_threshold = 0;
    
    int16_t total_samples = end - start;
    if (total_samples < 2) return -1;
    
    // Calculate parent impurity
    float parent_gini = calculate_gini_float(labels, workspace->sample_indices, start, end, model->n_classes);
    
    // Try each feature in the subset
    for (int16_t f = 0; f < n_features_subset; f++) {
        int16_t feature_idx = workspace->feature_indices[f];
        int16_t min_val = workspace->min_vals[feature_idx];
        int16_t max_val = workspace->max_vals[feature_idx];
        
        if (min_val >= max_val) continue;
        
        // Try random thresholds
        for (int16_t t = 0; t < model->config.n_thresholds; t++) {
            int16_t threshold = min_val + (eml_rand(&workspace->rng_state) % (max_val - min_val + 1));
            
            // Temporarily partition samples to calculate impurity
            int16_t left_idx = 0, right_idx = 0;
            
            // Count and separate samples
            for (int16_t i = start; i < end; i++) {
                if (features[workspace->sample_indices[i] * model->n_features + feature_idx] <= threshold) {
                    workspace->temp_indices[left_idx++] = workspace->sample_indices[i];
                } else {
                    workspace->temp_indices[total_samples - 1 - right_idx++] = workspace->sample_indices[i];
                }
            }
            
            int16_t left_count = left_idx;
            int16_t right_count = right_idx;
            
            if (left_count == 0 || right_count == 0) continue;
            if (left_count < model->config.min_samples_leaf || right_count < model->config.min_samples_leaf) continue;
            
            // Calculate Gini for left and right partitions
            float left_gini = calculate_gini_float(labels, workspace->temp_indices, 0, left_count, model->n_classes);
            float right_gini = calculate_gini_float(labels, workspace->temp_indices, total_samples - right_count, total_samples, model->n_classes);
            
            // Calculate weighted Gini impurity
            float weighted_gini = ((float)left_count * left_gini + (float)right_count * right_gini) / (float)total_samples;
            
            // Calculate information gain
            float improvement = parent_gini - weighted_gini;
            
            if (improvement > best_improvement) {
                best_improvement = improvement;
                *best_feature = feature_idx;
                *best_threshold = threshold;
            }
        }
    }
    
    return (best_improvement > 0.0f) ? 0 : -1; // Return 0 if good split found, -1 otherwise
}

// Partition samples based on feature threshold
static int16_t partition_samples(const int16_t *features, EmlTreesModel *model, 
                                EmlTreesWorkspace *workspace, int16_t start, int16_t end, 
                                int8_t feature, int16_t threshold) {
    int16_t left = start;
    int16_t right = end - 1;
    
    while (left <= right) {
        // Find element on left that should be on right
        while (left <= right && features[workspace->sample_indices[left] * model->n_features + feature] <= threshold) {
            left++;
        }
        
        // Find element on right that should be on left
        while (left <= right && features[workspace->sample_indices[right] * model->n_features + feature] > threshold) {
            right--;
        }
        
        // Swap if needed
        if (left < right) {
            int16_t temp = workspace->sample_indices[left];
            workspace->sample_indices[left] = workspace->sample_indices[right];
            workspace->sample_indices[right] = temp;
            left++;
            right--;
        }
    }
    
    return left; // Split point
}

// Get majority class in a range
static int16_t get_majority_class(const int16_t *labels, const int16_t *indices,
                                 int16_t start, int16_t end, int16_t n_classes) {
    int16_t counts[256] = {0}; // Assume max 256 classes
    int16_t max_count = 0;
    int16_t majority_class = 0;
    
    for (int16_t i = start; i < end; i++) {
        counts[labels[indices[i]]]++;
    }
    
    for (int16_t i = 0; i < n_classes; i++) {
        if (counts[i] > max_count) {
            max_count = counts[i];
            majority_class = i;
        }
    }
    
    return majority_class;
}

// Build a single tree
static int16_t build_tree(EmlTreesModel *model, EmlTreesWorkspace *workspace,
                         const int16_t *features, const int16_t *labels) {
    
    int16_t tree_start = model->n_nodes_used;
    
    // Subsample features
    int16_t n_features_subset = (model->n_features * model->config.feature_subsample_ratio_num) / 
                               model->config.feature_subsample_ratio_den;
    if (n_features_subset < 1) n_features_subset = 1;
    
    for (int16_t i = 0; i < model->n_features; i++) {
        workspace->feature_indices[i] = i;
    }
    shuffle_indices(workspace->feature_indices, model->n_features, &workspace->rng_state);
    
    // Initialize root node state
    int16_t stack_size = 1;
    workspace->node_stack[0].node_idx = tree_start;
    workspace->node_stack[0].start = 0;
    workspace->node_stack[0].end = workspace->n_samples;
    workspace->node_stack[0].depth = 0;
    
    // Initialize min/max values
    for (int16_t f = 0; f < model->n_features; f++) {
        workspace->min_vals[f] = 32767;
        workspace->max_vals[f] = -32768;
    }
    
    // Calculate initial min/max
    for (int16_t i = 0; i < workspace->n_samples; i++) {
        for (int16_t f = 0; f < model->n_features; f++) {
            int16_t val = features[workspace->sample_indices[i] * model->n_features + f];
            if (val < workspace->min_vals[f]) workspace->min_vals[f] = val;
            if (val > workspace->max_vals[f]) workspace->max_vals[f] = val;
        }
    }
    
    // Process stack
    while (stack_size > 0) {
        NodeState current = workspace->node_stack[--stack_size];
        int16_t node_idx = current.node_idx;
        
        if (node_idx >= model->max_nodes) {
            return -1; // Out of nodes
        }
        
        // Check stopping criteria
        int16_t n_samples_node = current.end - current.start;
        if (current.depth >= model->config.max_depth || 
            n_samples_node < model->config.min_samples_leaf * 2 ||
            n_samples_node <= 0) {
            
            // Create leaf node
            model->nodes[node_idx].feature = -1;
            model->nodes[node_idx].value = get_majority_class(labels, workspace->sample_indices,
                                                            current.start, current.end, model->n_classes);
            model->nodes[node_idx].left = -1;
            model->nodes[node_idx].right = -1;
            if (node_idx >= model->n_nodes_used) {
                model->n_nodes_used = node_idx + 1;
            }
            continue;
        }
        
        // Find best split
        int8_t best_feature;
        int16_t best_threshold;
        int16_t split_result = find_best_split(features, labels, model, workspace, 
                                              current.start, current.end,
                                              n_features_subset, &best_feature, &best_threshold);
        
        if (split_result != 0 || best_feature == -1) {
            // No valid split found, create leaf
            model->nodes[node_idx].feature = -1;
            model->nodes[node_idx].value = get_majority_class(labels, workspace->sample_indices,
                                                            current.start, current.end, model->n_classes);
            model->nodes[node_idx].left = -1;
            model->nodes[node_idx].right = -1;
            if (node_idx >= model->n_nodes_used) {
                model->n_nodes_used = node_idx + 1;
            }
            continue;
        }
        
        // Partition samples
        int16_t split_point = partition_samples(features, model, workspace, current.start, current.end, 
                                               best_feature, best_threshold);
        
        // Check if partition was successful
        if (split_point <= current.start || split_point >= current.end) {
            // Partition failed, create leaf
            model->nodes[node_idx].feature = -1;
            model->nodes[node_idx].value = get_majority_class(labels, workspace->sample_indices,
                                                            current.start, current.end, model->n_classes);
            model->nodes[node_idx].left = -1;
            model->nodes[node_idx].right = -1;
            if (node_idx >= model->n_nodes_used) {
                model->n_nodes_used = node_idx + 1;
            }
            continue;
        }
        
        // Calculate next available node indices
        int16_t next_node = model->n_nodes_used;
        if (next_node + 1 >= model->max_nodes) {
            // Not enough space for children, create leaf
            model->nodes[node_idx].feature = -1;
            model->nodes[node_idx].value = get_majority_class(labels, workspace->sample_indices,
                                                            current.start, current.end, model->n_classes);
            model->nodes[node_idx].left = -1;
            model->nodes[node_idx].right = -1;
            if (node_idx >= model->n_nodes_used) {
                model->n_nodes_used = node_idx + 1;
            }
            continue;
        }
        
        // Create internal node
        model->nodes[node_idx].feature = best_feature;
        model->nodes[node_idx].value = best_threshold;
        model->nodes[node_idx].left = next_node;
        model->nodes[node_idx].right = next_node + 1;
        
        // Update n_nodes_used to reserve space for children
        model->n_nodes_used = next_node + 2;
        if (node_idx >= model->n_nodes_used - 2) {
            model->n_nodes_used = node_idx + 1;
        }
        
        // Add children to stack (right first, then left for correct processing order)
        if (stack_size < 100) { // Reasonable stack limit
            // Right child
            workspace->node_stack[stack_size].node_idx = model->nodes[node_idx].right;
            workspace->node_stack[stack_size].start = split_point;
            workspace->node_stack[stack_size].end = current.end;
            workspace->node_stack[stack_size].depth = current.depth + 1;
            stack_size++;
            
            // Left child
            workspace->node_stack[stack_size].node_idx = model->nodes[node_idx].left;
            workspace->node_stack[stack_size].start = current.start;
            workspace->node_stack[stack_size].end = split_point;
            workspace->node_stack[stack_size].depth = current.depth + 1;
            stack_size++;
        }
    }
    
    return 0;
}

// Main training function
int16_t eml_trees_train(EmlTreesModel *model, EmlTreesWorkspace *workspace,
                       const int16_t *features, const int16_t *labels) {
    
    model->n_nodes_used = 0;
    workspace->rng_state = model->config.rng_seed;
    
    // Calculate subsample size
    int16_t subsample_size = (workspace->n_samples * model->config.subsample_ratio_num) / 
                            model->config.subsample_ratio_den;
    
    // Initialize sample indices
    for (int16_t i = 0; i < workspace->n_samples; i++) {
        workspace->sample_indices[i] = i;
    }
    
    // Build each tree
    for (int16_t tree = 0; tree < model->n_trees; tree++) {
        // Store tree start index
        model->tree_starts[tree] = model->n_nodes_used;
        
        // Subsample without replacement
        shuffle_indices(workspace->sample_indices, workspace->n_samples, &workspace->rng_state);
        
        // Temporarily set n_samples to subsample size for tree building
        int16_t original_n_samples = workspace->n_samples;
        workspace->n_samples = subsample_size;
        
        // Build tree with subsampled data
        int16_t result = build_tree(model, workspace, features, labels);
        
        // Restore original n_samples
        workspace->n_samples = original_n_samples;
        
        if (result != 0) {
            return result;
        }
    }
    
    return 0;
}

// Prediction function that returns probabilities
int16_t eml_trees_predict_proba(const EmlTreesModel *model, const int16_t *features, 
                               float *probabilities, int16_t *votes) {
    
    // Initialize vote counts using model's n_classes
    for (int16_t i = 0; i < model->n_classes; i++) {
        votes[i] = 0;
    }
    
    // Get prediction from each tree
    for (int16_t tree = 0; tree < model->n_trees; tree++) {
        int16_t node_idx = model->tree_starts[tree];
        
        // Traverse tree
        while (model->nodes[node_idx].feature != -1) {
            int8_t feature = model->nodes[node_idx].feature;
            int16_t threshold = model->nodes[node_idx].value;
            
            if (features[feature] <= threshold) {
                node_idx = model->nodes[node_idx].left;
            } else {
                node_idx = model->nodes[node_idx].right;
            }
        }
        
        // Add leaf prediction to votes
        int16_t predicted_class = model->nodes[node_idx].value;
        if (predicted_class >= 0 && predicted_class < model->n_classes) {
            votes[predicted_class]++;
        }
    }
    
    // Convert votes to probabilities
    for (int16_t i = 0; i < model->n_classes; i++) {
        probabilities[i] = (float)votes[i] / (float)model->n_trees;
    }
    
    // Find majority class
    int16_t max_votes = 0;
    int16_t predicted_class = 0;
    for (int16_t i = 0; i < model->n_classes; i++) {
        if (votes[i] > max_votes) {
            max_votes = votes[i];
            predicted_class = i;
        }
    }
    
    return predicted_class;
}
