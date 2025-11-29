# streamlit_Sinewave READEME.md

# Wave Simulation Demo Project

This is a simple demo project showing how to create both wxPython desktop and Streamlit web versions that share the same core logic.
A wxpython prject that runs either localy with WxPython or with streamlit deplayed on web

## Setup

```bash
# Create project structure
mkdir -p demo_project/src/{core,algorithm,gui}
cd demo_project

# Create __init__.py files
touch src/__init__.py
touch src/core/__init__.py
touch src/algorithm/__init__.py
touch src/gui/__init__.py

# Install dependencies
pip install streamlit matplotlib numpy wxPython

# Or use requirements.txt
pip install -r requirements.txt
```

## Running

### Desktop Version (wxPython)
```bash
python -m src.gui.main_window
```

### Web Version (Streamlit)
```bash
streamlit run streamlit_app.py

python -m streamlit run streamlit_app.py
```

## Architecture

Both versions share:
- `src/core/simulation.py` - Simulation core (simulates DLL/SO)
- `src/algorithm/compiler.py` - Parameter compilation and optimization

Each has its own UI layer:
- `src/gui/main_window.py` - wxPython desktop UI
- `streamlit_app.py` - Streamlit web UI

## Key Points

1. **Zero duplication** - Core logic is written once, used by both
2. **Easy migration** - Add web version without touching desktop code
3. **Independent** - Both versions can coexist and evolve separately
4. **Scalable** - Pattern works for complex projects with DLLs
"""