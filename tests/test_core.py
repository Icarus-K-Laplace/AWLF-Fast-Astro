import unittest
import numpy as np
from awlf_astro.pipeline import AstroRestorer

class TestAstroRestorer(unittest.TestCase):
    
    def setUp(self):
        self.engine = AstroRestorer()
        
    def test_cosmic_ray_removal(self):
        """Test if a simple spike is removed."""
        img = np.zeros((20, 20), dtype=np.float32)
        img[:] = 100.0
        # Add a spike
        img[10, 10] = 10000.0
        
        res = self.engine.process(img)
        
        # The spike should be gone (replaced by median ~100)
        self.assertLess(res[10, 10], 200.0, "Cosmic ray was not removed")
        
    def test_star_preservation(self):
        """Test if a 'fat' star is preserved."""
        img = np.zeros((20, 20), dtype=np.float32)
        img[:] = 100.0
        # Add a 3x3 star
        img[8:11, 8:11] = 5000.0
        
        res = self.engine.process(img)
        
        # The center should still be bright
        self.assertGreater(res[9, 9], 4000.0, "Star was wrongly removed")
        
    def test_destriping(self):
        """Test if a hot column is corrected."""
        img = np.zeros((50, 50), dtype=np.float32)
        img[:] = 100.0
        # Add a hot column
        img[:, 25] = 150.0
        
        res = self.engine.process(img)
        
        # The column median should be close to background
        col_median = np.median(res[:, 25])
        self.assertLess(abs(col_median - 100.0), 5.0, "Stripe was not removed")

if __name__ == '__main__':
    unittest.main()
