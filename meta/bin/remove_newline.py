#! /usr/bin/env python
'''remove newlines from file names'''
import glob
import os
import sys

if len(sys.argv) > 1:
    os.chdir(sys.argv[1])

for filename in glob.glob('*\r\n*'):
    os.rename(filename, filename.replace('\r\n', ''))

for filename in glob.glob('*\n*'):
    os.rename(filename, filename.replace('\n', ''))
