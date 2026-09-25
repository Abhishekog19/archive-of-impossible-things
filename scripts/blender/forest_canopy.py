"""Start REF6 with the shared placed-forest production pipeline."""
import runpy
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('forest_approach.py')),init_globals={'DEEP_CANOPY':True})
