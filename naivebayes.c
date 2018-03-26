
#include <stdio.h>
#include <stdlib.h>


typedef struct _BayesSummary {
    val_t mean;
    val_t std;
} BayesSummary;

typedef struct _BayesModel {
   int32_t n_classes;
   int32_t n_features;
   BayesSummary *summaries;
} BayesModel;


// TODO: use fixed-point
int32_t
bayes_predict(BayesModel *model, float values[], int32_t values_length) {

   const int MAX_CLASSES = 10;
   float class_probabilities[MAX_CLASSES] = {0.0,};

   for (int class_idx = 0; class_idx<model->n_classes; class_idx++) {

      float p = 0.0;
      for (int value_idx = 0; value_idx<values_length; value_idx++) {
         const int32_t summary_idx = class_idx*model->n_features + value_idx;
         BayesSummary summary = model->summaries[summary_idx];

         float v = values[value_idx];
         // XXX: seems to be sum of log(p), or product of p
         // FIXME: use mean/std
         // TODO: use fixed-point
         p += log(pdf(v, 0.0, 1.0));
      }
      class_probabilities[class_idx] = p;
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

#if 0
int main() {
   volatile int count = 0;
   const int n_repetitions = 1;
   const int samples = 10;
   const float sigma = 3;

   const float mean = 0.0;
   const float std = 1.0;
   for (int r=0; r<n_repetitions; r++) {
      for (int s=0; s<samples; s++) {
         const float x = mean + (std * sigma * (s/(float)(samples-1)));
         const float r = pdf(x, mean, std);
         const float f = pdf_floatfixed(x, mean, std);
         //const float f = pdf_fast(x, mean, std);
         printf("%.2f: P= %.4f% vs %.4f% : E %.4f : %.2f% \n", x, r*100.0, f*100.0, r-f, (1.0-r/f)*100);
      }
      for (int s=0; s<samples; s++) {
         const float x = mean - (std * sigma * (s/(float)(samples-1)));
         const float r = pdf(x, mean, std);
         const float f = pdf_floatfixed(x, mean, std);
         //const float f = pdf_fast(x, mean, std);
         printf("%.2f: P= %.4f% vs %.4f% : E %.4f : %.2f% \n", x, r*100.0, f*100.0, r-f, (1.0-r/f)*100);
      }
      count += 1;
   }
}
#endif
