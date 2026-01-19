import sys
import os
import time
import numpy as np

# Add parent dir to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from awlf_astro.pipeline import AstroRestorer

def run_benchmark():
    print("="*60)
    print("AWLF-Astro Performance Benchmark")
    print("="*60)
    
    # 1. Create synthetic 2K image (2048x2048) similar to modern sensors
    H, W = 2048, 2048
    print(f"Creating synthetic data ({W}x{H}, float32)...")
    data = np.random.normal(100, 10, (H, W)).astype(np.float32)
    # Add fake stars and rays
    data[1000, 1000] = 50000  # Star
    data[500:600, 500] = 20000 # Ray
    
    # 2. Initialize
    engine = AstroRestorer()
    print("Warming up JIT compiler...")
    engine.warmup()
    
    # 3. Loop
    num_frames = 50
    print(f"Running {num_frames} iterations...")
    
    start_time = time.time()
    for i in range(num_frames):
        _ = engine.process(data)
        print(f"Processed frame {i+1}/{num_frames}", end='\r')
        
    total_time = time.time() - start_time
    avg_time = total_time / num_frames
    fps = 1.0 / avg_time
    
    print(f"\n\nResults:")
    print(f"  Total Time: {total_time:.4f} s")
    print(f"  Avg Latency: {avg_time*1000:.2f} ms")
    print(f"  Throughput:  {fps:.2f} FPS")
    print("-" * 60)
    
    if fps > 10:
        print("✅ Status: High-Throughput Ready (Suitable for Pipelines)")
    else:
        print("⚠️ Status: Optimization Recommended")

if __name__ == "__main__":
    run_benchmark()
