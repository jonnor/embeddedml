
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
#define VAL_FRACT_BITS 24
#define VAL_ONE (1 << VAL_FRACT_BITS)
#define VAL_FROMINT(x) ((x) << VAL_FRACT_BITS)
#define VAL_FROMFLOAT(x) ((int)((x) * (1 << VAL_FRACT_BITS))) 
#define VAL_TOINT(x) ((x) >> VAL_FRACT_BITS)
#define VAL_TOFLOAT(x) (((float)(x)) / (1 << VAL_FRACT_BITS))
#define VAL_MUL(x, y) ( ((x) >> VAL_FRACT_BITS/2) * ((y)>> VAL_FRACT_BITS/2) )

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



val_t pdf_linear4fp_half(val_t xf) {
    const val_t x0 = VAL_FROMFLOAT(0.36162072933139433);
    const val_t x1 = VAL_FROMFLOAT(1.8155589891884512);
    const val_t x2 = VAL_FROMFLOAT(2.6480578258766743);
    const val_t aaa = VAL_FROMFLOAT(0.0320660290803192);
    const val_t aa = VAL_FROMFLOAT(0.07303982381715937);
    const val_t a = VAL_FROMFLOAT(-0.08126695859921051);
    const val_t b = VAL_FROMFLOAT(-0.030153892551033495);
    const val_t c = VAL_FROMFLOAT(0.21203273553191235);

//    const float y = aaa*fabs(x-x2) + aa*fabs(x-x1) + a*fabs(x-x0) + b*x + c;

    const val_t two = VAL_MUL(aaa, abs(xf-x2));
    const val_t one = VAL_MUL(aa, abs(xf-x1));
    const val_t zero = VAL_MUL(a, abs(xf-x0));
    const val_t bx = VAL_MUL(b, xf);
    const val_t y = two + one + zero + bx + c;
    return y;
}

val_t pdf_linear4fp(val_t x, val_t mean, val_t std) {
   const val_t xm = val_div((x - mean), std);
   const val_t xx = (xm > 0) ? xm : -xm;
   const val_t p = pdf_linear4fp_half(xx);

   val_t pp = val_div(p, std);
   if (pp < 1) {
       pp = 1;
   }
   return pp; 
}

float pdf_floatfixedlinear(float x, float mean, float std) {
   return VAL_TOFLOAT(pdf_linear4fp(VAL_FROMFLOAT(x), VAL_FROMFLOAT(mean), VAL_FROMFLOAT(std)));
}

val_t pdf_loglin4_stdhalf(val_t xf) {

    const val_t x0 = VAL_FROMFLOAT(0.8333333885368039);
    const val_t x1 = VAL_FROMFLOAT(2.0114942763546977);
    const val_t x2 = VAL_FROMFLOAT(3.4195402297818958);
    const val_t aaa = VAL_FROMFLOAT(-1.1193323517431);
    const val_t aa = VAL_FROMFLOAT(-0.9327769306872999);
    const val_t a = VAL_FROMFLOAT(-0.746221586714255);
    const val_t b = VAL_FROMFLOAT(-3.295811966758346);
    const val_t c = VAL_FROMFLOAT(5.042867068181607);

    // const float y = aaa*fabs(x-x2) + aa*fabs(x-x1) + a*fabs(x-x0) + b*x + c;
    const val_t two = VAL_MUL(aaa, abs(xf-x2));
    const val_t one = VAL_MUL(aa, abs(xf-x1));
    const val_t zero = VAL_MUL(a, abs(xf-x0));
    const val_t bx = VAL_MUL(b, xf);
    const val_t y = two + one + zero + bx + c;
    return y;
}

val_t pdf_loglin4(val_t x, val_t mean, val_t std, val_t stdlog2) {
   const val_t xm = val_div((x - mean), std);
   const val_t xx = (xm > 0) ? xm : -xm;
   const val_t p = pdf_loglin4_stdhalf(xx) - stdlog2;
   return p; 
}

float pdf_loglin4_float(float x, float mean, float std, float stdlog2) {
   return VAL_TOFLOAT(pdf_loglin4(VAL_FROMFLOAT(x), VAL_FROMFLOAT(mean), VAL_FROMFLOAT(std), VAL_FROMFLOAT(stdlog2)));
}

#endif // PDF_H
