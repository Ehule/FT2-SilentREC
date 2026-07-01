#pragma once

#include <stdint.h>
#include <stdbool.h>
#include "ft2_mix.h" // MIXER_FRAC_BITS

#define SINC_KERNELS 3
#define SINC8_TAPS 8
#define SINC16_TAPS 16

// 256 phases + linear interpolation = near perfect (and low CPU cache usage)
#define SINC_OVERSAMPLING 256

// log2(SINC_OVERSAMPLING)
#define SINC_OVERSAMPLING_BITS 8

// log2(SINC8_TAPS)
#define SINC8_TAPS_BITS 3

// log2(SINC16_TAPS)
#define SINC16_TAPS_BITS 4

#define INTRP_PHASE_SHIFT (MIXER_FRAC_BITS-SINC_OVERSAMPLING_BITS)
#define INTRP_PHASE_SCALE (1L << INTRP_PHASE_SHIFT)
#define INTRP_PHASE_MASK (INTRP_PHASE_SCALE-1)

extern float *fSinc[SINC_KERNELS], *fSinc8[SINC_KERNELS], *fSinc16[SINC_KERNELS];
extern uint64_t sincRatio1, sincRatio2;

bool setupWindowedSincTables(void);
void freeWindowedSincTables(void);
