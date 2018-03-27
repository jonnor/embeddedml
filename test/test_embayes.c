
#include <stdio.h>
#include <stdlib.h>

#include "embayes.h"
#include "cancer.h"

int main() {
   volatile int count = 0;
   const int n_repetitions = 1;
   const int samples = 10;
   const float sigma = 3;

   val_t values[samples];

   const float mean = 0.0;
   const float std = 10.0;
   for (int r=0; r<n_repetitions; r++) {
      for (int s=0; s<samples; s++) {
         const float x = mean + (std * sigma * (s/(float)(samples-1)));
         values[s] = VAL_FROMFLOAT(x);
      }

      const int32_t p = embayes_predict(&cancer_model, values, samples);
      printf("p: %d\n", p);

      count += 1;
   }
}

