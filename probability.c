
// Iplementations and approximations of
// Gaussian Probability Densify Function
// aka normpdf
// for use in Gaussian Naive Bayes classifier
// in very constrained systems

#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Reference implementation
float pdf(float x, float mean, float std) {
    const float exponent = -((x - mean)*(x - mean) / (2 * std*std));
    const float div = sqrt(2*M_PI) * std;
    //printf("ref %f\n", exponent); 
    return (exp(exponent) / div);
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


typedef int32_t val_t;
// Typically Q15
#define VAL_FRACT_BITS 16
#define VAL_FRACT_BITS_D2 8
#define VAL_ONE (1 << VAL_FRACT_BITS)
#define VAL_FROMINT(x) ((x) << VAL_FRACT_BITS)
#define VAL_FROMFLOAT(x) ((int)((x) * (1 << VAL_FRACT_BITS))) 
#define VAL_TOINT(x) ((x) >> VAL_FRACT_BITS)
#define VAL_TOFLOAT(x) (((float)(x)) / (1 << VAL_FRACT_BITS))
#define VAL_MUL(x, y) ( ((x) >> VAL_FRACT_BITS_D2) * ((y)>> VAL_FRACT_BITS_D2) )

val_t val_div(val_t a, val_t b)
{
    int64_t temp = (int64_t)a << VAL_FRACT_BITS;
    if((temp >= 0 && b >= 0) || (temp < 0 && b < 0)) {   
        temp += b / 2;
    } else {
        temp -= b / 2;
    }
    return (int32_t)(temp / b);
}

#define base VAL_FRACT_BITS

// From https://gist.github.com/Madsy/1088393 has fp_exp(), but it gave errors

const val_t VAL_SQRT_2PI = VAL_FROMFLOAT(sqrt(2*M_PI));

typedef int32_t fixed_prob; // 0.0 - 1.0
#define PROB_SHIFT 15 // TODO: use something more suitable


// https://codingforspeed.com/using-faster-exponential-approximation/
// Only valid for x < 5
double exp_mul8(double o) {
  double x = 1.0 + o / 256.0;
  //printf("FEXP: %f %f %d\n", o, x, VAL_FROMFLOAT(x));

  x *= x;
  x *= x;
  x *= x;
  x *= x;

  x *= x;
  x *= x;
  x *= x;
  x *= x;
  return x;
}

double exp_mul10(double x) {
  x = 1.0 + x / 1024;
  x *= x; x *= x; x *= x; x *= x;
  x *= x; x *= x; x *= x; x *= x;
  x *= x; x *= x;
  return x;
}

float pdf_fast(float x, float mean, float std) {
    const float exponent = -((x - mean)*(x - mean) / (2 * std*std));
    const float div = sqrt(2*M_PI) * std;
    //printf("ref %f\n", exponent); 
    return (exp_mul10(exponent) / div);
}


// TODO: make work with 10 multiplications, in floatingpoint has error < 10% until 5 sigma
#define FIXED_MUL(fracs, x, y) ( ((x) >> (fracs/2)) * ((y)>> (fracs/2)) )
val_t exp_fpmul(val_t v) {
  // implicit division by 256 = 2**8
  const int q = 16+8;
  int32_t x = v;
  x += 1<<q;

  //printf("FXP: %f %f %d\n", VAL_TOFLOAT(v), VAL_TOFLOAT(x >> 8), x>>8);
  x = FIXED_MUL(q, x, x);
  x = FIXED_MUL(q, x, x);
  x = FIXED_MUL(q, x, x);
  x = FIXED_MUL(q, x, x);

  x = FIXED_MUL(q, x, x);
  x = FIXED_MUL(q, x, x);
  x = FIXED_MUL(q, x, x);
  x = FIXED_MUL(q, x, x);

  const val_t vv = (x >> q-16);
  return vv;
}

val_t val_exp(val_t ex) {
    VAL_FROMFLOAT(exp_mul10(VAL_TOFLOAT(ex)));
    return exp_fpmul(ex);
}

val_t pdf_fixed(val_t x, val_t mean, val_t std) {
    const val_t std2 = VAL_MUL(std, std);
    const val_t xm2 = VAL_MUL(x - mean, x - mean);
    const val_t div = VAL_MUL(VAL_SQRT_2PI, std);
    const val_t exponent = -val_div(xm2, 2*std2);    
    val_t p = val_div(val_exp(exponent), div);

    // Check if outside valid domain, clamp to min
    if (exponent < VAL_FROMFLOAT(-9.0)) {
        p = VAL_FROMFLOAT(0.0001);
    }
    return p;
}

typedef struct _BayesSummary {
    val_t mean;
    val_t std;
} BayesSummary;

int main() {
   volatile int count = 0;
   const int n_repetitions = 1;
   const int samples = 30;

   const float mean = 0.0;
   const float std = 1.0;
   for (int r=0; r<n_repetitions; r++) {
      for (int s=0; s<samples; s++) {
         const float x = mean - (std * 6 * (s/(float)(samples-1)));
         const float r = pdf(x, mean, std);
         const float f = VAL_TOFLOAT(pdf_fixed(VAL_FROMFLOAT(x), VAL_FROMFLOAT(mean), VAL_FROMFLOAT(std)));
         //const float f = pdf_fast(x, mean, std);
         printf("%.2f: %.4f vs %.4f : %.4f : %.2f% \n", x, r, f, r-f, (1.0-r/f)*100);
      }
      count += 1;
   }
}
