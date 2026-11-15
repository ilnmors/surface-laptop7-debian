#!/usr/bin/env python3
from pathlib import Path
import os, sys
os.execv("/bin/bash", ["bash", str(Path(__file__).with_suffix(".sh")), *sys.argv[1:]])
