// Include the header file to get access to the MicroPython API
#include "py/dynruntime.h"

#include <string.h>
#include <stdint.h>

// memset is used by some standard C constructs
#if !defined(__linux__)
void *memcpy(void *dst, const void *src, size_t n) {
    return mp_fun_table.memmove_(dst, src, n);
}
void *memset(void *s, int c, size_t n) {
    return mp_fun_table.memset_(s, c, n);
}
#endif


// Find which vector in @vectors that @v is closes to
uint16_t
compute_euclidean3_argmin_uint8(const uint8_t *vectors, int vectors_length,
            const uint8_t *vv, int channels, uint32_t *out_dist)
{

    uint16_t min_idx = 0;
    uint32_t min_value = UINT32_MAX;
    for (int i=0; i<vectors_length; i++) {

        uint32_t dist = 0;
#if 1
        for (int j; j<channels; j++) {
            uint8_t c = vectors[(i*channels)+j];
            uint8_t v = vectors[j];
            dist += (v - c) * (v - c);
        }
#endif    

        if (dist < min_value) {
            min_value = dist;
            min_idx = i;
        }

    }

    if (out_dist) {
        *out_dist = min_value;
    }

    return min_idx;
}

// MicroPython API
STATIC mp_obj_t
euclidean_argmin(mp_obj_t vectors_obj, mp_obj_t point_obj) {

    // First arg
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(vectors_obj, &bufinfo, MP_BUFFER_RW);
    if (bufinfo.typecode != 'B') {
        mp_raise_ValueError(MP_ERROR_TEXT("expecting B array (uint8)"));
    }
    const uint8_t *values = bufinfo.buf;
    const int values_length = bufinfo.len / sizeof(*values);

    // Second arg
    mp_get_buffer_raise(point_obj, &bufinfo, MP_BUFFER_RW);
    if (bufinfo.typecode != 'B') {
        mp_raise_ValueError(MP_ERROR_TEXT("expecting B array (uint8)"));
    }
    const uint8_t *point = bufinfo.buf;
    const int n_channels = bufinfo.len / sizeof(*values);

    if ((values_length % n_channels) != 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("vectors length must be divisible by @point dimensions"));
    }

    const int vector_length = values_length / n_channels;

    uint32_t min_dist = 0;
    const uint16_t min_index = \
        compute_euclidean3_argmin_uint8(values, vector_length, point, n_channels, &min_dist);

    return mp_obj_new_tuple(2, ((mp_obj_t []) {
        mp_obj_new_int(min_index),
        mp_obj_new_int(min_dist),
    }));
 }
STATIC MP_DEFINE_CONST_FUN_OBJ_2(euclidian_argmin_obj, euclidean_argmin);


// This is the entry point and is called when the module is imported
mp_obj_t mpy_init(mp_obj_fun_bc_t *self, size_t n_args, size_t n_kw, mp_obj_t *args) {
    // This must be first, it sets up the globals dict and other things
    MP_DYNRUNTIME_INIT_ENTRY

    mp_store_global(MP_QSTR_euclidean_argmin, MP_OBJ_FROM_PTR(&euclidian_argmin_obj));

    // This must be last, it restores the globals dict
    MP_DYNRUNTIME_INIT_EXIT
}

