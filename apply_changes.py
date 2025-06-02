# apply_changes.py

import os
import sys

# 1. Ensure we are running from the project root
script_dir = os.path.abspath(os.path.dirname(__file__))
os.chdir(script_dir)

# 2. Create __init__.py in utils/ and ui/
for folder in ("utils", "ui"):
    init_path = os.path.join(script_dir, folder, "__init__.py")
    if not os.path.exists(init_path):
        with open(init_path, "w", encoding="utf-8") as f:
            f.write("# This file marks the directory as a Python package\n")

# 3. Modify main.py
main_py = os.path.join(script_dir, "main.py")
main_contents = []
with open(main_py, "r", encoding="utf-8") as f:
    for line in f:
        # Replace "from dna_ui import main as run_batch" with "from utils.dna_ui import main as run_batch"
        if line.strip().startswith("from dna_ui import main"):
            main_contents.append("from utils.dna_ui import main as run_batch\n")
        else:
            main_contents.append(line)
with open(main_py, "w", encoding="utf-8") as f:
    f.writelines(main_contents)

# 4. Modify utils/dna_ui.py
dna_ui_py = os.path.join(script_dir, "utils", "dna_ui.py")
dna_ui_lines = []
with open(dna_ui_py, "r", encoding="utf-8") as f:
    for line in f:
        # Change import of DNACalculator
        if line.strip().startswith("from dna_calculator import DNACalculator"):
            dna_ui_lines.append("from utils.dna_calculator import DNACalculator\n")
        # Change project_root calculation to use os.getcwd()
        elif "project_root = os.path.dirname(os.path.abspath(__file__))" in line:
            dna_ui_lines.append("    project_root = os.getcwd()\n")
        else:
            dna_ui_lines.append(line)
with open(dna_ui_py, "w", encoding="utf-8") as f:
    f.writelines(dna_ui_lines)

# 5. Modify setup.py
setup_py = os.path.join(script_dir, "setup.py")
setup_lines = []
with open(setup_py, "r", encoding="utf-8") as f:
    for line in f:
        setup_lines.append(line)
# Check if py_modules already present; if not, insert it after version
found_version = False
new_setup_lines = []
for line in setup_lines:
    new_setup_lines.append(line)
    if line.strip().startswith("version=") and "0.1.0" in line:
        found_version = True
    elif found_version and line.strip().startswith("packages=find_packages()"):
        # Insert py_modules just before this line
        new_setup_lines.insert(len(new_setup_lines) - 1, "    py_modules=[\"main\"],\n")
        found_version = False
# If we never inserted (e.g. different formatting), append at the end of setup()
if not any("py_modules" in l for l in new_setup_lines):
    # find the line with "find_packages()" and insert before it
    out = []
    for line in new_setup_lines:
        if "find_packages()" in line and "packages=" in line:
            out.append("    py_modules=[\"main\"],\n")
            out.append(line)
        else:
            out.append(line)
    new_setup_lines = out

with open(setup_py, "w", encoding="utf-8") as f:
    f.writelines(new_setup_lines)

# 6. Overwrite README.md
readme_md = os.path.join(script_dir, "README.md")
updated_readme = """# SonicDNA

A project for developing a structured data driven approach to audio representation and generative synthesis.

## Project Status: Rule Definition Phase

June 2025 Update:
- All primary variable rules and serialization formats (rules_*.json) are now specified.
- Work on agent scripts audio encoding and the generative engine will continue next.

## Overview

SonicDNA is an experiment in:
- Efficient structured encoding of sound properties
- Data driven generative audio with an emphasis on clear modular rules
- Flexible tools (GUI CLI batch) for analysis and experimentation

## Current State

- [x] Modular folder structure
- [x] Basic PySide6 GUI skeleton
- [x] Audio DNA variable rulesets (rules_*.json)
- [ ] Audio DNA extraction agents planned
- [ ] DNA to audio generative engine planned
- [ ] Rule based validation and dataset building planned
- [ ] Audio compression experiments planned

## Audio DNA Rulesets

All major audio variables are defined in JSON rulesets:
- Volume
- Frequency
- Clarity
- Timbre
- Envelope
- Dynamics
- Emotion
- Macro Intensity
- Perceived Pitch
- Noise Texture
- Wavelength
- Texture Complexity
- Harmonicity
- Transients
- Phase Spatial
- Resonance Damping
- Glide Slur
- Effect Artifact
- Formant Structure

Each JSON file:
- Specifies encoding and decoding structure for a core property
- Documents sub variables ranges padding and serialization
- Will be used by agents for extraction validation and synthesis

## Getting Involved

If you have ideas or feedback please reach out:
- Email: birchstagstudios@gmail.com
- You are welcome to watch fork or experiment with your own designs

## License

MIT or other as specified

## Changelog

2025-06-02
- Refactored imports so that dna_ui and dna_calculator live under utils
- Modified dna_ui to compute project_root using the repository root
- Updated main.py import to point at utils.dna_ui
- Added __init__.py in utils and ui to treat them as packages
- Added py_modules in setup.py so that the console script entry point loads main.py
- Overhauled README.md for clarity and simplicity

Thank you for your interest in this project.
"""
with open(readme_md, "w", encoding="utf-8") as f:
    f.write(updated_readme)

print("All changes applied successfully.")
