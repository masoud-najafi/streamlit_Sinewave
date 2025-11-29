
# ============================================================================
# File: src/algorithm/compiler.py
# ============================================================================
"""
Compilation and preprocessing logic
This represents your algorithm processing layer
"""

class SimulationCompiler:
    """
    Compiles and validates simulation parameters
    Represents your algorithm/compiler layer
    """
    
    def __init__(self):
        self.compiled_params = None
        print("[SimulationCompiler] Initialized")
    
    def compile(self, raw_config):
        """
        Compile raw configuration into simulation parameters
        
        Args:
            raw_config: dict with user inputs
        
        Returns:
            dict with compiled parameters
        """
        print(f"[SimulationCompiler] Compiling config: {raw_config}")
        
        compiled = {
            'amplitude': raw_config.get('amplitude', 1.0),
            'frequency': raw_config.get('frequency', 1.0),
            'phase': raw_config.get('phase', 0.0),
            'points': raw_config.get('points', 1000)
        }
        
        self.compiled_params = compiled
        print(f"[SimulationCompiler] Compiled successfully")
        return compiled
    
    def validate(self, params):
        """
        Validate parameters
        
        Returns:
            tuple (is_valid, message)
        """
        print(f"[SimulationCompiler] Validating params")
        
        if params['amplitude'] <= 0:
            return False, "Amplitude must be positive"
        
        if params['frequency'] <= 0:
            return False, "Frequency must be positive"
        
        if params['points'] < 100:
            return False, "Points must be at least 100"
        
        print(f"[SimulationCompiler] Validation passed")
        return True, "Valid"
    
    def optimize(self, params):
        """
        Optimize parameters for better performance
        
        Returns:
            dict with optimized parameters
        """
        print(f"[SimulationCompiler] Optimizing params")
        
        optimized = params.copy()
        
        # Simple optimization: round points to nearest hundred
        optimized['points'] = round(params['points'] / 100) * 100
        
        print(f"[SimulationCompiler] Optimized: points {params['points']} -> {optimized['points']}")
        return optimized
