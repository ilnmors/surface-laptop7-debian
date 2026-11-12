#!/usr/bin/python3
"""Use the shared OEM speaker EQ and lower ceilings of the two chassis revisions."""
from pathlib import Path
from types import SimpleNamespace
from dolby2pipewire import parse, render, summary

folder = Path(__file__).parent
profiles = [parse(path, "music") for path in sorted((folder / "windows-tuning").glob("*.xml"))]
first, second = profiles
if first["eq_db"] != second["eq_db"] or first["isolated"] != second["isolated"]:
    raise ValueError("The supplied Windows revisions do not share the speaker EQ")
for key in ("thr_high_db", "thr_low_db"):
    first[key] = [min(a, b) for a, b in zip(first[key], second[key])]
arguments = SimpleNamespace(margin=0.5, gain_trim=0.0, merge_db=1.0, module_args=False)
configuration = render(first, arguments)
configuration = configuration.replace("Surface Pro 11 speakers:", "Surface Laptop 7 speakers:")
configuration = configuration.replace('node.description = "Internal speakers"', 'node.description = "Surface speakers (Windows EQ)"')
configuration = configuration.replace('media.name = "Internal speakers"', 'media.name = "Surface speakers (Windows EQ)"')
configuration = configuration.replace("surface_pro_11_speakers", "surface_laptop_7_speakers")
configuration = configuration.replace('media.class = "Stream/Output/Audio/Internal"', 'media.class = "Stream/Output/Audio"')
configuration = configuration.replace('node.name = "surface_laptop_7_speakers"\n', 'node.name = "surface_laptop_7_speakers"\n        node.description = "Surface speakers (Windows EQ)"\n')
(folder / "50-surface-speakers.conf").write_text(configuration)
(folder / "tuning-summary.txt").write_text(summary(first) + "\n")
