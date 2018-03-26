
#include <stdint.h>
#include <math.h>

// TODO: use fixed-point
typedef struct _BayesSummary {
    float mean;
    float std;
} BayesSummary;

typedef struct _BayesModel {
   int32_t n_classes;
   int32_t n_features;
   BayesSummary *summaries;
} BayesModel;

int32_t
embayes_predict(BayesModel *model, float values[], int32_t values_length) {
   //printf("predict(%d), classes=%d features=%d\n",
   //      values_length, model->n_classes, model->n_features);

   const int MAX_CLASSES = 10;
   float class_probabilities[10] = {0.0,};

   for (int class_idx = 0; class_idx<model->n_classes; class_idx++) {

      float p = 0.0;
      for (int value_idx = 0; value_idx<values_length; value_idx++) {
         const int32_t summary_idx = class_idx*model->n_features + value_idx;
         BayesSummary summary = model->summaries[summary_idx];

         const float v = values[value_idx];
         // XXX: seems to be sum of log(p), or product of p
         // TODO: use fixed-point
         const float f = pdf_linear4(v, summary.mean, summary.std);
         p += log(f);
         //printf("v %d=%f s=(%f, %f) : %f\n", value_idx, v, summary.mean, summary.std, f);
      }
      class_probabilities[class_idx] = p;
      //printf("class %d : %f\n", class_idx, p);
   }

   float highest_prob = class_probabilities[0];
   int32_t highest_idx = 0;
   for (int class_idx = 1; class_idx<model->n_classes; class_idx++) {
      const float p = class_probabilities[class_idx]; 
      if (p > highest_prob) {
         highest_prob = p;
         highest_idx = class_idx;
      }
   }
   return highest_idx;
}

