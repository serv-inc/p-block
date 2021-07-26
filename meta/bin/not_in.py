#! /usr/bin/env python3
"""all files that are in one but not the other directory"""
import glob
import os.path
import sys


def all_in_one(dirname1, dirname2):
    """@return list of all filenames in dirname1 but not in dirname2"""
    one = {os.path.basename(x) for x in glob.glob(dirname1 + "/*")}
    two = {os.path.basename(x) for x in glob.glob(dirname2 + "/*")}
    return list(one - two)


if __name__ == "__main__":
    print("\n".join(all_in_one(sys.argv[1], sys.argv[2])))
