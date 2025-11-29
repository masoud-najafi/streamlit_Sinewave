
# ============================================================================
# File: src/gui/main_window.py
# ============================================================================
"""
Original wxPython desktop GUI
This represents your existing GUI code
"""
import wx
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.core.simulation import SimulationCore
from src.algorithm.compiler import SimulationCompiler

try:
    from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
    from matplotlib.figure import Figure
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Warning: matplotlib not available, plots disabled")


class SimulationFrame(wx.Frame):
    """Main wxPython window"""
    
    def __init__(self):
        super().__init__(None, title="Wave Simulation - Desktop", size=(900, 700))
        
        # Initialize core components
        self.sim_core = SimulationCore()
        self.compiler = SimulationCompiler()
        
        # Create UI
        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Title
        title = wx.StaticText(panel, label="🌊 Wave Simulation (wxPython)")
        title_font = title.GetFont()
        title_font.PointSize += 4
        title_font = title_font.Bold()
        title.SetFont(title_font)
        main_sizer.Add(title, 0, wx.ALL | wx.CENTER, 10)
        
        # Parameters section
        params_box = wx.StaticBox(panel, label="Parameters")
        params_sizer = wx.StaticBoxSizer(params_box, wx.VERTICAL)
        
        # Amplitude
        amp_sizer = wx.BoxSizer(wx.HORIZONTAL)
        amp_sizer.Add(wx.StaticText(panel, label="Amplitude:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.amp_slider = wx.Slider(panel, value=50, minValue=1, maxValue=100, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        amp_sizer.Add(self.amp_slider, 1, wx.EXPAND)
        params_sizer.Add(amp_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Frequency
        freq_sizer = wx.BoxSizer(wx.HORIZONTAL)
        freq_sizer.Add(wx.StaticText(panel, label="Frequency:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.freq_slider = wx.Slider(panel, value=10, minValue=1, maxValue=50, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        freq_sizer.Add(self.freq_slider, 1, wx.EXPAND)
        params_sizer.Add(freq_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Phase
        phase_sizer = wx.BoxSizer(wx.HORIZONTAL)
        phase_sizer.Add(wx.StaticText(panel, label="Phase:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.phase_slider = wx.Slider(panel, value=0, minValue=0, maxValue=314, style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        phase_sizer.Add(self.phase_slider, 1, wx.EXPAND)
        params_sizer.Add(phase_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        # Points
        points_sizer = wx.BoxSizer(wx.HORIZONTAL)
        points_sizer.Add(wx.StaticText(panel, label="Points:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        self.points_spinner = wx.SpinCtrl(panel, value="1000", min=100, max=10000)
        points_sizer.Add(self.points_spinner, 0)
        params_sizer.Add(points_sizer, 0, wx.EXPAND | wx.ALL, 5)
        
        main_sizer.Add(params_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Options
        options_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.validate_cb = wx.CheckBox(panel, label="Validate")
        self.validate_cb.SetValue(True)
        self.optimize_cb = wx.CheckBox(panel, label="Optimize")
        options_sizer.Add(self.validate_cb, 0, wx.RIGHT, 10)
        options_sizer.Add(self.optimize_cb, 0)
        main_sizer.Add(options_sizer, 0, wx.ALL, 10)
        
        # Run button
        self.run_button = wx.Button(panel, label="▶️ Run Simulation")
        self.run_button.Bind(wx.EVT_BUTTON, self.on_run)
        main_sizer.Add(self.run_button, 0, wx.ALL | wx.CENTER, 10)
        
        # Results
        results_box = wx.StaticBox(panel, label="Results")
        results_sizer = wx.StaticBoxSizer(results_box, wx.VERTICAL)
        self.results_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(-1, 100))
        results_sizer.Add(self.results_text, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(results_sizer, 0, wx.EXPAND | wx.ALL, 10)
        
        # Plot area
        if MATPLOTLIB_AVAILABLE:
            self.figure = Figure(figsize=(8, 4))
            self.canvas = FigureCanvas(panel, -1, self.figure)
            self.ax = self.figure.add_subplot(111)
            self.ax.set_title("Click 'Run Simulation' to see results")
            main_sizer.Add(self.canvas, 1, wx.EXPAND | wx.ALL, 10)
        
        panel.SetSizer(main_sizer)
        
        self.Centre()
    
    def on_run(self, event):
        """Run simulation button handler"""
        try:
            # Get raw config from UI
            raw_config = {
                'amplitude': self.amp_slider.GetValue() / 10.0,
                'frequency': self.freq_slider.GetValue() / 10.0,
                'phase': self.phase_slider.GetValue() / 100.0,
                'points': self.points_spinner.GetValue()
            }
            
            # Compile
            params = self.compiler.compile(raw_config)
            
            # Validate if enabled
            if self.validate_cb.GetValue():
                is_valid, msg = self.compiler.validate(params)
                if not is_valid:
                    wx.MessageBox(f"Validation failed: {msg}", "Error", wx.OK | wx.ICON_ERROR)
                    return
            
            # Optimize if enabled
            if self.optimize_cb.GetValue():
                params = self.compiler.optimize(params)
            
            # Run simulation (calls the core - simulates DLL)
            self.run_button.Enable(False)
            wx.BeginBusyCursor()
            
            result = self.sim_core.run_simulation(params)
            
            wx.EndBusyCursor()
            self.run_button.Enable(True)
            
            # Display results
            stats = result['statistics']
            results_text = f"Simulation completed successfully!\n\n"
            results_text += f"Points: {len(result['values'])}\n"
            results_text += f"Mean: {stats['mean']:.3f}\n"
            results_text += f"Std Dev: {stats['std']:.3f}\n"
            results_text += f"Min: {stats['min']:.3f}\n"
            results_text += f"Max: {stats['max']:.3f}"
            self.results_text.SetValue(results_text)
            
            # Plot
            if MATPLOTLIB_AVAILABLE:
                self.ax.clear()
                self.ax.plot(result['time'], result['values'])
                self.ax.set_xlabel('Time')
                self.ax.set_ylabel('Value')
                self.ax.set_title('Simulation Results')
                self.ax.grid(True, alpha=0.3)
                self.canvas.draw()
            
        except Exception as e:
            wx.EndBusyCursor()
            self.run_button.Enable(True)
            wx.MessageBox(f"Error: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)


def main():
    """Entry point for desktop version"""
    app = wx.App()
    frame = SimulationFrame()
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()

