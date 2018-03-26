
// Iplementations and approximations of
// Gaussian Probability Densify Function
// aka normpdf
// for use in Gaussian Naive Bayes classifier
// in very constrained systems

#ifndef PDF_H
#define PDF_H

#include <math.h>
#include <stdint.h>

// Reference implementation
float pdf(float x, float mean, float std) {
    const float exponent = -((x - mean)*(x - mean) / (2 * std*std));
    const float div = sqrt(2*M_PI) * std;
    //printf("ref %f\n", exponent); 
    return (exp(exponent) / div);
}

// Linear approximation
float pdf_linear4_half(float x) {
    const float x0 = 0.36162072933139433;
    const float x1 = 1.8155589891884512;
    const float x2 = 2.6480578258766743;
    const float aaa = 0.0320660290803192;
    const float aa = 0.07303982381715937;
    const float a = -0.08126695859921051;
    const float b = -0.030153892551033495;
    const float c = 0.21203273553191235;

    const float y = aaa*fabs(x-x2) + aa*fabs(x-x1) + a*fabs(x-x0) + b*x + c;
    return y;
}

float pdf_linear4(float x, float mean, float std) {
   const float xm = (x - mean) / std;
   const float xx = (xm > 0) ? xm : -xm; 
   const float p = pdf_linear4_half(xx) / std;
   return p;
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
    return (exp_mul8(exponent) / div);
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

  const val_t vv = (x >> (q-16));
  return vv;
}

val_t val_exp(val_t ex) {
    return exp_fpmul(ex);
}

val_t pdf_fixed(val_t x, val_t mean, val_t std) {
    const val_t std2 = VAL_MUL(std, std);
    const val_t xm2 = VAL_MUL(x - mean, x - mean);
    val_t div = VAL_MUL(VAL_SQRT_2PI, std);
    val_t stddiv = VAL_MUL(VAL_FROMINT(2), std2);
    if (stddiv == 0) {
      stddiv = 1; // avoid division-by-zero
    }
    if (div == 0) {
      div = 1; // avoid division-by-zero
    }
    const val_t exponent = -val_div(xm2, stddiv);    
    val_t p = val_div(val_exp(exponent), div);

    // Check if outside valid domain, clamp to min
    if (exponent < VAL_FROMFLOAT(-9.0)) {
        p = VAL_FROMFLOAT(0.0001);
    }
    return p;
}

float pdf_floatfixed(float x, float mean, float std) {
   return VAL_TOFLOAT(pdf_fixed(VAL_FROMFLOAT(x), VAL_FROMFLOAT(mean), VAL_FROMFLOAT(std)));
}

val_t pdf_linear4fp_half(val_t xf) {
    const float x0 = 0.36162072933139433;
    const float x1 = 1.8155589891884512;
    const float x2 = 2.6480578258766743;
    const float aaa = 0.0320660290803192;
    const float aa = 0.07303982381715937;
    const float a = -0.08126695859921051;
    const float b = -0.030153892551033495;
    const float c = 0.21203273553191235;

//    const float y = aaa*fabs(x-x2) + aa*fabs(x-x1) + a*fabs(x-x0) + b*x + c;

    const float x = VAL_TOFLOAT(xf);
    const float y = aaa*fabs(x-x2) + aa*fabs(x-x1) + a*fabs(x-x0) + b*x + c;
    
    return VAL_FROMFLOAT(y);
}

val_t pdf_linear4fp(val_t x, val_t mean, val_t std) {
   const val_t xm = val_div((x - mean), std);
   const val_t xx = (xm > 0) ? xm : -xm;
   const val_t p = pdf_linear4fp_half(xx);
   return val_div(p, std);
}

float pdf_floatfixedlinear(float x, float mean, float std) {
   return VAL_TOFLOAT(pdf_linear4fp(VAL_FROMFLOAT(x), VAL_FROMFLOAT(mean), VAL_FROMFLOAT(std)));
}

#endif // PDF_H
