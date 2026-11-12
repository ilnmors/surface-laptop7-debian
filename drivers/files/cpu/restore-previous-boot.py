#!/usr/bin/env python3
import os,sys
from pathlib import Path
os.execv("/bin/bash",["bash",str(Path(__file__).with_suffix(".sh")),*sys.argv[1:]])
