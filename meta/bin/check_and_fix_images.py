"""check files"""
import os
from PIL import Image


def file_has_alpha(image_filename):
    """@return true if file contains alpha channel"""
    return has_alpha(Image.open(image_filename))


def has_alpha(image):
    """@return has this image an alpha channel?"""
    return image.mode == "RGBA"


# use image.save('newpath.png') to save to valid format
def is_type_ok(image):
    """@return image has ok format"""
    return image.format in ["JPEG", "PNG"]


def path_as_png(path):
    """>>> path_as_png('./challenge2018/c273735e93b041a7.jpg')
    ./challenge2018/c273735e93b041a7.png"""
    rest = path.split(".")[:-1]
    rest.append("png")
    return ".".join(rest)


if __name__ == "__main__":
    for root, subdirs, files in os.walk("."):
        for file in files:
            path = os.path.join(root, file)
            testme = Image.open(path)
            if has_alpha(testme):
                print("{} has alpha".format(path))
            if not is_type_ok(testme):
                testme.save(path_as_png(path))
                os.remove(path)
