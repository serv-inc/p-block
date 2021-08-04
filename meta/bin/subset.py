#! /usr/bin/env python3
"""create a subset of size argv[1] in ./subsets/argv[i]

go to sys.argv[2] if given
"""

import sys
import os
import shutil
from pathlib import Path

size = sys.argv[1]
int(size)  # is number else fail
if len(sys.argv) == 3:
    os.chdir(sys.argv[2])

SUBSET_DIR = "subsets"
Path(os.path.join(SUBSET_DIR, size)).mkdir(parents=True, exist_ok=True)

for root, subdirs, files in os.walk("."):
    if SUBSET_DIR in root:
        continue
    for subdir in subdirs:
        if SUBSET_DIR in subdir:
            continue
        Path(os.path.join(SUBSET_DIR, size, root, subdir)).mkdir(exist_ok=True)
    for filename in files[: int(size)]:
        shutil.copyfile(
            os.path.join(root, filename), os.path.join(SUBSET_DIR, size, root, filename)
        )
