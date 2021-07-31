#! /usr/bin/env python3
"""finds files in current dir that are neither jpeg nor png"""
import os
import subprocess

a = os.listdir(".")
for line in a:
    b = subprocess.run(["file", line], capture_output=True, check=True)
    if "PNG" not in str(b.stdout) and "JPEG" not in str(b.stdout):
        print(line + " is not PNG/jpg")
