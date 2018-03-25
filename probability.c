
// Iplementations and approximations of
// Gaussian Probability Densify Function
// aka normpdf
// for use in Gaussian Naive Bayes classifier
// in very constrained systems

#include <math.h>

// Reference implementation
float pdf(float x, float mean, float std) {
    const float exponent = exp(- ((x - mean)*(x - mean) / (2 * std*std)));
    return (exponent / (sqrt(2 * M_PI) * std));
}

// Linear 
float pdf_lin2_half(float x) {
   const float x0 = 0.34247959;
   const float x1 = 2.00265729;
   const float aa = 0.0951662;
   const float a = -0.07833795;
   const float b = -0.03716455;
   const float c = 0.23640959;

   const float y = aa*fabs(x-x1) + a*fabs(x-x0) + b*x + c;
   return y;
}

float pdf_lin2(float x, float mean, float std) {
   const float xm = (x - mean) / std;
   const float xx = (xm > 0) ? xm : -xm; 
   return pdf_lin2_half(xx);
}

// NOTE: branchless trick for integers conditional sign-flip
// https://stackoverflow.com/questions/4866187/how-to-flip-the-sign-of-an-integer-value-using-some-constant-and-operators-wit
// const int32_t flip = xm-1;
// int32_t xx = (x ^ flip) - flip;



int main() {
   volatile int count = 0;
   const int n_repetitions = 1;
   const int samples = 10;

   for (int r=0; r<n_repetitions; r++) {
      for (int s=0; s<samples; s++) {
         const float x = 3.14 * (s/(float)(samples-1));
         const float f = pdf_lin2(x, 0.0, 1.0);
         printf("%.2f: %.4f\n", x, f);
      }
      count += 1;
   }
}
