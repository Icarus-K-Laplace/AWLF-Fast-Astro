
import sys
import os
import cv2
import numpy as np
# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from awlf_astro.pipeline import AstroRestorer

def main():
    # Load sample
    data_path = os.path.join("data", "sample_astro.npy")
    if not os.path.exists(data_path):
        print("Sample data not found.")
        return

    raw = np.load(data_path)
    
    # Run
    engine = AstroRestorer()
    print("Processing...")
    start = cv2.getTickCount()
    result = engine.process(raw)
    end = cv2.getTickCount()
    
    t = (end - start) / cv2.getTickFrequency()
    print(f"Done in {t:.4f}s")
    
    # Visualize
    # ... (Add your normalization and imwrite code here) ...

if __name__ == "__main__":
    main()
