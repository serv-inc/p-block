import os
import filecmp

SUBSET_DIR = set(["subsets"])  # duplicate

old = "/store/storage/p-block/images/"
new = os.path.expanduser("~/repo/p-block/images/plaintext/images")

dirs = set(os.listdir(old)) - SUBSET_DIR

assert dirs == set(os.listdir(new)) - SUBSET_DIR, "sub directories differ"

for a_dir in dirs:
    print(a_dir)
    dold = os.path.join(old, a_dir)
    dnew = os.path.join(new, a_dir)
    cmp = filecmp.dircmp(dold, dnew)
    print("old only: {}".format(len(cmp.left_only)))
    print("new only {}".format(len(cmp.right_only)))
