import numpy as np
import time
from .core import fast_process_v54
from .filters import remove_column_noise, build_soft_mask

class AstroRestorer:
    def __init__(self, sigma_threshold=4.0, sharpness_ratio=0.5):
        self.sigma = sigma_threshold
        self.ratio = sharpness_ratio
        self._warmed_up = False
        
    def warmup(self):
        """Trigger JIT compilation."""
        dummy = np.zeros((10, 10), dtype=np.float32)
        fast_process_v54(dummy, dummy, dummy.astype(np.uint8), 10, 10, 4.0, 0.5)
        self._warmed_up = True

    def process(self, image: np.ndarray) -> np.ndarray:
        """
        Main inference pipeline.
        Args:
            image: 2D numpy array (float32)
        Returns:
            Cleaned image
        """
        if not self._warmed_up:
            self.warmup()
            
        # 1. Destriping
        destriped = remove_column_noise(image)
        
        # 2. Mask Generation
        soft_mask = build_soft_mask(destriped)
        hard_mask = (soft_mask > 0.2).astype(np.uint8)
        
        # 3. Core Restoration
        h, w = destriped.shape
        output = np.zeros_like(destriped)
        fast_process_v54(destriped, output, hard_mask, h, w, self.sigma, self.ratio)
        
        # 4. Photometric Recovery (Soft Blend)
        final = output * (1.0 - soft_mask) + destriped * soft_mask
        
        return final
