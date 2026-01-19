import numpy as np
from numba import jit, prange

@jit(nopython=True, parallel=True, fastmath=True, cache=True)
def fast_process_v54(img, output, hard_mask, h, w, sigma_threshold, sharpness_ratio):
    """
    JIT-compiled kernel for AWLF-Astro V5.4.
    Implements Laplacian-guided aggressive cosmic ray removal.
    """
    pad = 1  # 3x3 neighborhood
    
    for r in prange(pad, h - pad):
        for c in range(pad, w - pad):
            # 1. Hard Protection (Star Core Preservation)
            if hard_mask[r, c] > 0:
                output[r, c] = img[r, c]
                continue
            
            center = float(img[r, c])
            
            # 2. Local Statistics (Manual sorting for speed optimization)
            # We avoid np.median to reduce overhead in the inner loop
            vals = np.zeros(8, dtype=np.float32)
            idx = 0
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dy == 0 and dx == 0: continue
                    vals[idx] = img[r+dy, c+dx]
                    idx += 1
            
            # Bubble sort (faster for small N=8 than qsort)
            for i in range(8):
                for j in range(i+1, 8):
                    if vals[i] > vals[j]:
                        vals[i], vals[j] = vals[j], vals[i]
            
            local_median = 0.5 * (vals[3] + vals[4])
            
            # 3. Robust Noise Estimation (MAD)
            mad = 0.0
            for k in range(8):
                mad += abs(vals[k] - local_median)
            noise_level = (mad / 8.0) + 1e-6
            
            # 4. Laplacian Sharpness Check
            # 3x3 Cross Kernel
            m1 = float(img[r-1, c])
            m2 = float(img[r+1, c])
            m3 = float(img[r, c-1])
            m4 = float(img[r, c+1])
            laplacian = 4.0 * center - (m1 + m2 + m3 + m4)
            
            # 5. Decision Logic
            snr = (center - local_median) / noise_level
            is_cosmic = False
            
            if snr > sigma_threshold and laplacian > 0:
                contrast = center - local_median
                # Sharpness Ratio Constraint
                if laplacian > sharpness_ratio * contrast:
                    is_cosmic = True
            
            # 6. Repair
            output[r, c] = local_median if is_cosmic else center
