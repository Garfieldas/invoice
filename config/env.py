import environ
from pathlib import Path
import sys

env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "apps"))