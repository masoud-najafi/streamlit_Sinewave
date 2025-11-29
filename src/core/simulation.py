
# ============================================================================
# File: src/core/simulation.py
# ============================================================================
"""
Simulates a DLL/SO library with a simple mathematical simulation
In your real project, this would wrap ctypes calls to your actual DLL
"""
import numpy as np
import time

class SimulationCore:
    """
    Mock simulation core that simulates what your DLL would do
    Replace this with actual ctypes wrapper for your DLL
    """
    
    def __init__(self):
        self.version = "1.0.0"
        print(f"[SimulationCore] Initialized version {self.version}")
    
    def run_simulation(self, params):
        """
        Run simulation with given parameters
        
        Args:
            params: dict with 'amplitude', 'frequency', 'phase', 'points'
        
        Returns:
            dict with 'time', 'values', 'statistics'
        """
        print(f"[SimulationCore] Running simulation with params: {params}")
        
        # Simulate some processing time (like a real DLL would take)
        time.sleep(0.5)
        
        # Extract parameters
        amplitude = params.get('amplitude', 1.0)
        frequency = params.get('frequency', 1.0)
        phase = params.get('phase', 0.0)
        points = params.get('points', 1000)
        
        # Generate simulation data (simulates what DLL would compute)
        t = np.linspace(0, 4 * np.pi, points)
        values = amplitude * np.sin(frequency * t + phase)
        
        # Calculate statistics
        stats = {
            'mean': float(np.mean(values)),
            'std': float(np.std(values)),
            'min': float(np.min(values)),
            'max': float(np.max(values))
        }
        
        result = {
            'time': t.tolist(),
            'values': values.tolist(),
            'statistics': stats
        }
        
        print(f"[SimulationCore] Simulation completed: {len(values)} points")
        return result
