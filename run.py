import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
VENV_PY = ROOT / "venv" / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

if not VENV_PY.exists():
    sys.exit("venv not found. Run this first: python setup.py")

subprocess.run([str(VENV_PY), "main.py"], cwd=ROOT)
