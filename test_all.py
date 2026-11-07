#!/usr/bin/env python3
"""Root test runner delegating to final/run_all.py."""
import sys
from pathlib import Path

final_dir = Path(__file__).resolve().parent / "final"
sys.path.insert(0, str(final_dir))

from run_all import main

if __name__ == "__main__":
    main()
