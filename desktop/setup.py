#!/usr/bin/env python3
"""Python entry point for this component's shared shell implementation."""
from pathlib import Path
import os,sys
os.execv('/bin/bash',['bash',str(Path(__file__).with_suffix('.sh')),*sys.argv[1:]])
