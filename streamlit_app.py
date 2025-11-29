
# ============================================================================
# File: streamlit_app.py
# ============================================================================
"""
Streamlit web version - reuses the same core components
"""
import streamlit as st
import sys
from pathlib import Path
import matplotlib.pyplot as plt

# Add src to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.simulation import SimulationCore
from src.algorithm.compiler import SimulationCompiler


def main():
    st.set_page_config(
        page_title="Wave Simulation Web",
        page_icon="🌊",
        layout="wide"
    )
    
    st.title("🌊 Wave Simulation (Streamlit)")
    st.markdown("*Web version - reuses the same core and algorithm modules*")
    
    # Initialize components (same as wxPython version!)
    if 'sim_core' not in st.session_state:
        st.session_state.sim_core = SimulationCore()
    if 'compiler' not in st.session_state:
        st.session_state.compiler = SimulationCompiler()
    
    # Sidebar parameters
    st.sidebar.header("⚙️ Parameters")
    
    amplitude = st.sidebar.slider(
        "Amplitude",
        min_value=0.1,
        max_value=10.0,
        value=5.0,
        step=0.1
    )
    
    frequency = st.sidebar.slider(
        "Frequency",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1
    )
    
    phase = st.sidebar.slider(
        "Phase",
        min_value=0.0,
        max_value=3.14,
        value=0.0,
        step=0.01
    )
    
    points = st.sidebar.number_input(
        "Points",
        min_value=100,
        max_value=10000,
        value=1000,
        step=100
    )
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Options")
    validate = st.sidebar.checkbox("Validate parameters", value=True)
    optimize = st.sidebar.checkbox("Optimize parameters", value=False)
    
    # Main area
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        run_button = st.button("▶️ Run Simulation", type="primary", use_container_width=True)
    
    if run_button:
        try:
            # Same workflow as wxPython version!
            
            # 1. Create raw config
            raw_config = {
                'amplitude': amplitude,
                'frequency': frequency,
                'phase': phase,
                'points': int(points)
            }
            
            # 2. Compile (REUSE compiler module)
            with st.spinner("Compiling configuration..."):
                params = st.session_state.compiler.compile(raw_config)
                st.success("✅ Compiled")
            
            # 3. Validate if enabled
            if validate:
                with st.spinner("Validating..."):
                    is_valid, msg = st.session_state.compiler.validate(params)
                    if not is_valid:
                        st.error(f"❌ Validation failed: {msg}")
                        st.stop()
                    st.success("✅ Validated")
            
            # 4. Optimize if enabled
            if optimize:
                with st.spinner("Optimizing..."):
                    params = st.session_state.compiler.optimize(params)
                    st.success("✅ Optimized")
            
            # 5. Run simulation (REUSE simulation core)
            with st.spinner("Running simulation..."):
                result = st.session_state.sim_core.run_simulation(params)
                st.session_state.result = result
                st.success("✅ Simulation completed!")
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Results")
            
            stats = result['statistics']
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Points", len(result['values']))
            col2.metric("Mean", f"{stats['mean']:.3f}")
            col3.metric("Min", f"{stats['min']:.3f}")
            col4.metric("Max", f"{stats['max']:.3f}")
            
            # Plot
            st.subheader("📈 Visualization")
            fig, ax = plt.subplots(figsize=(12, 5))
            ax.plot(result['time'], result['values'], linewidth=2)
            ax.set_xlabel('Time')
            ax.set_ylabel('Value')
            ax.set_title('Simulation Results')
            ax.grid(True, alpha=0.3)
            st.pyplot(fig)
            
            # Download
            import io
            buffer = io.StringIO()
            buffer.write("time,value\n")
            for t, v in zip(result['time'], result['values']):
                buffer.write(f"{t},{v}\n")
            
            st.download_button(
                "📥 Download CSV",
                data=buffer.getvalue(),
                file_name="simulation_results.csv",
                mime="text/csv"
            )
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            st.exception(e)
    
    # Footer
    st.markdown("---")
    st.markdown("💡 *This web app uses the exact same simulation core and compiler as the desktop version*")


if __name__ == "__main__":
    main()

