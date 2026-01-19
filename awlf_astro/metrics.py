import numpy as np
import cv2

def calculate_metrics(noisy: np.ndarray, denoised: np.ndarray, soft_mask: np.ndarray) -> dict:
    """
    Calculate robust metrics for astronomical image restoration.
    
    Args:
        noisy: Original input image
        denoised: Restored output image
        soft_mask: Star probability map (0-1)
        
    Returns:
        Dictionary containing CR Rejection Rate, Star Flux Loss, and Background NRR.
    """
    metrics = {}
    
    # 1. Background Noise Reduction (NRR)
    # Only consider background pixels (low star probability)
    mask_bg = soft_mask < 0.1
    if np.sum(mask_bg) > 0:
        std_in = np.std(noisy[mask_bg])
        std_out = np.std(denoised[mask_bg])
        metrics['Background_NRR_dB'] = 20 * np.log10(std_in / (std_out + 1e-9))
    else:
        metrics['Background_NRR_dB'] = 0.0

    # 2. Cosmic Ray Rejection Rate (CRRR)
    # Define CR as > 5 sigma outlier in original, but cleaned in output
    med = np.median(noisy)
    mad = np.median(np.abs(noisy - med))
    sigma = 1.4826 * mad
    
    cr_in = (noisy - med) > 5 * sigma
    cr_out = (denoised - med) > 5 * sigma
    
    count_in = np.sum(cr_in)
    count_out = np.sum(cr_out)
    
    if count_in > 0:
        metrics['CR_Rejection_Rate'] = (1 - count_out / count_in) * 100
    else:
        metrics['CR_Rejection_Rate'] = 0.0

    # 3. Star Flux Loss
    # Evaluate only in high-probability star regions
    mask_star = soft_mask > 0.2
    if np.sum(mask_star) > 0:
        flux_in = np.sum(noisy[mask_star])
        flux_out = np.sum(denoised[mask_star])
        metrics['Star_Flux_Loss'] = (1 - flux_out / (flux_in + 1e-9)) * 100
    else:
        metrics['Star_Flux_Loss'] = 0.0
        
    return metrics
