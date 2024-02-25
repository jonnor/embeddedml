
#include "dsp/transform_functions.h"
#include "dsp/statistics_functions.h"
#include "dsp/basic_math_functions.h"
#include "dsp/complex_math_functions.h"
#include "dsp/fast_math_functions.h"
#include "dsp/matrix_functions.h"

/* Constants for Q15 implementation */
#define LOG2TOLOG_Q15 0x02C5C860
#define MICRO_Q15 0x00000219
#define SHIFT_MELFILTER_SATURATION_Q15 10


// Based on arm_mfcc_q15 from CMSIS-DSP

void
mel_filters( q15_t *samples, q15_t *tmp, q31_t *mels)
{
    // FIXME: do not forward declare, initialize on spot2
    
    q15_t m;
    uint32_t index;
    uint32_t fftShift=0;
    q31_t logExponent;
    q63_t result;
    uint32_t i;
    uint32_t coefsPos;
    uint32_t filterLimit;

    // FIXME: pass as input struct
    const int fft_length = 128;
    q15_t *window_coefficients;
    const int n_mels = 40;
    const q15_t *mel_filter_starts;
    const q15_t *mel_filter_lengths;
    const q15_t *mel_filter_coeffs;

    arm_rfft_instance_q15 rfft;

    arm_status status = ARM_MATH_SUCCESS;
    
    q15_t *pSrc = samples;

    // q15
    arm_absmax_q15(pSrc, fft_length,&m,&index);

    if ((m != 0) && (m != 0x7FFF))
    {
       q15_t quotient;
       int16_t shift;

       status = arm_divide_q15(0x7FFF,m,&quotient,&shift);
       if (status != ARM_MATH_SUCCESS)
       {
          return(status);
       }
 
       arm_scale_q15(pSrc,quotient,shift,pSrc,fft_length);
    }


    // q15
    arm_mult_q15(pSrc, window_coefficients, pSrc, fft_length);


    /* Compute spectrum magnitude 
    */
    fftShift = 31 - __CLZ(fft_length);

    /* Default RFFT based implementation */
    //const arm_status init_status = arm_rfft_init_128_q15(&rfft, 1, 1);
    arm_rfft_q15(&(rfft),pSrc, tmp);

    filterLimit = 1 + (fft_length >> 1);


    // q15 - fftShift
    arm_cmplx_mag_q15(tmp, pSrc, filterLimit);
    // q14 - fftShift

    /* Apply MEL filters */
    coefsPos = 0;
    for(i=0; i<n_mels; i++)
    {
      arm_dot_prod_q15(pSrc+mel_filter_starts[i],
        &(mel_filter_coeffs[coefsPos]),
        mel_filter_lengths[i],
        &result);

      coefsPos += mel_filter_lengths[i];

      // q34.29 - fftShift
      result += MICRO_Q15;
      result >>= SHIFT_MELFILTER_SATURATION_Q15;
      // q34.29 - fftShift - satShift
      mels[i] = __SSAT(result,31) ;

    }

    if ((m != 0) && (m != 0x7FFF))
    {
      arm_scale_q31(mels,m<<16,0,mels,n_mels);
    }
   
    // q34.29 - fftShift - satShift
    /* Compute the log */
    arm_vlog_q31(mels, mels, n_mels);

    // q5.26
    logExponent = fftShift + 2 + SHIFT_MELFILTER_SATURATION_Q15;
    logExponent = logExponent * LOG2TOLOG_Q15;

    // q8.26
    arm_offset_q31(mels,logExponent,mels,n_mels);
    arm_shift_q31(mels,-19,mels,n_mels);

    return(status);

}
