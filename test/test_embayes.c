
#include <stdio.h>
#include <stdlib.h>

#include "pdf.h"
#include "embayes.h"

int main() {
   volatile int count = 0;
   const int n_repetitions = 1;
   const int samples = 10;
   const float sigma = 3;

   const float mean = 0.0;
   const float std = 10.0;
   for (int r=0; r<n_repetitions; r++) {
      for (int s=0; s<samples; s++) {
         const float x = mean + (std * sigma * (s/(float)(samples-1)));
         const float r = pdf_linear4(x, mean, std);
         //const float f = pdf_floatfixed(x, mean, std);
         const float f = pdf_floatfixedlinear(x, mean, std);
         //const float f = pdf_fast(x, mean, std);
         printf("%.2f: P= %.4f% vs %.4f% : E %.4f : %.2f% \n", x, r*100.0, f*100.0, r-f, (1.0-r/f)*100);
      }

      count += 1;
   }
}

