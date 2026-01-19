import numpy as np
import cv2
from scipy.ndimage import median_filter

def remove_column_noise(image: np.ndarray, window: int = 7) -> np.ndarray:
    """
    Destriping via column-wise median statistics.
    """
    corrected = image.copy().astype(np.float32)
    col_medians = np.median(image, axis=0)
    profile_bg = median_filter(col_medians, size=window * 5)
    stripe_signal = col_medians - profile_bg
    threshold = np.std(stripe_signal) * 0.5
    
    for c in range(image.shape[1]):
        if abs(stripe_signal[c]) > threshold:
            corrected[:, c] -= stripe_signal[c]
            
    return np.maximum(corrected, 0)

def build_soft_mask(image: np.ndarray, blur_sigma: float = 1.4, 
                   p_lo: float = 98.8, p_hi: float = 99.7) -> np.ndarray:
    """
    Generates a soft mask for photometric preservation.
    """
    # Handle NaNs
    img = np.nan_to_num(image, nan=np.nanmedian(image)).astype(np.float32)
    
    # Gaussian blur to suppress single-pixel noise (rays) but keep stars
    blur = cv2.GaussianBlur(img, (0, 0), blur_sigma)
    
    # Morphological opening to remove remaining line structures
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    blur = cv2.morphologyEx(blur, cv2.MORPH_OPEN, kernel)
    
    # Soft thresholding
    lo = np.percentile(blur, p_lo)
    hi = np.percentile(blur, p_hi)
    soft = np.clip((blur - lo) / (hi - lo + 1e-6), 0, 1)
    
    # Dilate to cover halos
    soft = cv2.dilate(soft, kernel, iterations=1)
    
    return soft
