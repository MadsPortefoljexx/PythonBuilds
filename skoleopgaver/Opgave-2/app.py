"""Compatibility entrypoint for the existing Streamlit deployment."""

import runpy
import sys
from pathlib import Path

app_directory = Path(__file__).resolve().parents[2] / "101 Data Handling" / "Opgave 2"
sys.path.insert(0, str(app_directory))
runpy.run_path(str(app_directory / "app.py"), run_name="__main__")
