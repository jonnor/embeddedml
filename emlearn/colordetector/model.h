
    // !!! This file is generated using emlearn !!!

    #include <eml_trees.h>
    

EmlTreesNode simple_rgb_pink_yellow_other_nodes[42] = {
  { 0, 185.5, 1, 6 },
  { 1, 250.0, 2, 3 },
  { 2, 329.5, 3, 4 },
  { -1, 0, -1, -1 },
  { 1, 204.5, 3, 5 },
  { -1, 1, -1, -1 },
  { -1, 2, -1, -1 },
  { 1, 162.0, 8, 9 },
  { 2, 511.5, 3, 6 },
  { 0, 108.5, 10, 3 },
  { 1, 265.5, 5, 3 },
  { 0, 185.0, 12, 6 },
  { 1, 204.5, 3, 13 },
  { 2, 458.0, 14, 3 },
  { 2, 347.0, 3, 5 },
  { 0, 188.0, 16, 6 },
  { 2, 343.5, 3, 17 },
  { 2, 452.0, 5, 3 },
  { 0, 179.5, 19, 6 },
  { 0, 108.0, 20, 3 },
  { 0, 81.0, 3, 21 },
  { 2, 462.5, 22, 3 },
  { 2, 296.0, 3, 5 },
  { 0, 189.0, 24, 6 },
  { 2, 341.5, 3, 25 },
  { 1, 263.5, 5, 3 },
  { 0, 188.0, 27, 6 },
  { 0, 108.0, 28, 3 },
  { 2, 342.0, 3, 5 },
  { 0, 188.0, 30, 6 },
  { 1, 245.5, 31, 3 },
  { 1, 204.5, 3, 32 },
  { 1, 244.5, 5, 33 },
  { 0, 129.0, 5, 3 },
  { 1, 204.5, 35, 36 },
  { 0, 158.0, 3, 6 },
  { 1, 256.0, 37, 3 },
  { 0, 129.5, 5, 3 },
  { 0, 185.5, 39, 6 },
  { 0, 107.5, 40, 3 },
  { 2, 346.5, 3, 41 },
  { 2, 458.0, 5, 3 } 
};

int32_t simple_rgb_pink_yellow_other_tree_roots[10] = { 0, 7, 11, 15, 18, 23, 26, 29, 34, 38 };

EmlTrees simple_rgb_pink_yellow_other = {
        42,
        simple_rgb_pink_yellow_other_nodes,	  
        10,
        simple_rgb_pink_yellow_other_tree_roots,
    };

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_0(const float *features, int32_t features_length) {
          if (features[0] < 185.5) {
              if (features[1] < 250.0) {
                  if (features[2] < 329.5) {
                      return 0;
                  } else {
                      if (features[1] < 204.5) {
                          return 0;
                      } else {
                          return 1;
                      }
                  }
              } else {
                  return 0;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_1(const float *features, int32_t features_length) {
          if (features[1] < 162.0) {
              if (features[2] < 511.5) {
                  return 0;
              } else {
                  return 2;
              }
          } else {
              if (features[0] < 108.5) {
                  if (features[1] < 265.5) {
                      return 1;
                  } else {
                      return 0;
                  }
              } else {
                  return 0;
              }
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_2(const float *features, int32_t features_length) {
          if (features[0] < 185.0) {
              if (features[1] < 204.5) {
                  return 0;
              } else {
                  if (features[2] < 458.0) {
                      if (features[2] < 347.0) {
                          return 0;
                      } else {
                          return 1;
                      }
                  } else {
                      return 0;
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_3(const float *features, int32_t features_length) {
          if (features[0] < 188.0) {
              if (features[2] < 343.5) {
                  return 0;
              } else {
                  if (features[2] < 452.0) {
                      return 1;
                  } else {
                      return 0;
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_4(const float *features, int32_t features_length) {
          if (features[0] < 179.5) {
              if (features[0] < 108.0) {
                  if (features[0] < 81.0) {
                      return 0;
                  } else {
                      if (features[2] < 462.5) {
                          if (features[2] < 296.0) {
                              return 0;
                          } else {
                              return 1;
                          }
                      } else {
                          return 0;
                      }
                  }
              } else {
                  return 0;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_5(const float *features, int32_t features_length) {
          if (features[0] < 189.0) {
              if (features[2] < 341.5) {
                  return 0;
              } else {
                  if (features[1] < 263.5) {
                      return 1;
                  } else {
                      return 0;
                  }
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_6(const float *features, int32_t features_length) {
          if (features[0] < 188.0) {
              if (features[0] < 108.0) {
                  if (features[2] < 342.0) {
                      return 0;
                  } else {
                      return 1;
                  }
              } else {
                  return 0;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_7(const float *features, int32_t features_length) {
          if (features[0] < 188.0) {
              if (features[1] < 245.5) {
                  if (features[1] < 204.5) {
                      return 0;
                  } else {
                      if (features[1] < 244.5) {
                          return 1;
                      } else {
                          if (features[0] < 129.0) {
                              return 1;
                          } else {
                              return 0;
                          }
                      }
                  }
              } else {
                  return 0;
              }
          } else {
              return 2;
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_8(const float *features, int32_t features_length) {
          if (features[1] < 204.5) {
              if (features[0] < 158.0) {
                  return 0;
              } else {
                  return 2;
              }
          } else {
              if (features[1] < 256.0) {
                  if (features[0] < 129.5) {
                      return 1;
                  } else {
                      return 0;
                  }
              } else {
                  return 0;
              }
          }
        }
        

static inline int32_t simple_rgb_pink_yellow_other_predict_tree_9(const float *features, int32_t features_length) {
          if (features[0] < 185.5) {
              if (features[0] < 107.5) {
                  if (features[2] < 346.5) {
                      return 0;
                  } else {
                      if (features[2] < 458.0) {
                          return 1;
                      } else {
                          return 0;
                      }
                  }
              } else {
                  return 0;
              }
          } else {
              return 2;
          }
        }
        

int32_t simple_rgb_pink_yellow_other_predict(const float *features, int32_t features_length) {

        int32_t votes[3] = {0,};
        int32_t _class = -1;

        _class = simple_rgb_pink_yellow_other_predict_tree_0(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_1(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_2(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_3(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_4(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_5(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_6(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_7(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_8(features, features_length); votes[_class] += 1;
    _class = simple_rgb_pink_yellow_other_predict_tree_9(features, features_length); votes[_class] += 1;
    
        int32_t most_voted_class = -1;
        int32_t most_voted_votes = 0;
        for (int32_t i=0; i<3; i++) {

            if (votes[i] > most_voted_votes) {
                most_voted_class = i;
                most_voted_votes = votes[i];
            }
        }
        return most_voted_class;
    }
    