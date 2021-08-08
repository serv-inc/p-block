#! /usr/bin/env python3
"""check files"""
import logging
import os
from PIL import Image

logging.basicConfig(level=logging.INFO)

# https://stackoverflow.com/questions/35859140/
def has_alpha(img):
    """@return has this image an alpha channel?"""
    return img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info
    )


def is_type_ok(image):
    """@return image has ok format"""
    return image.format in ["JPEG", "PNG"]


def path_as_png(path_in):
    """>>> path_as_png('./challenge2018/c273735e93b041a7.jpg')
    ./challenge2018/c273735e93b041a7.png"""
    rest = path_in.split(".")[:-1]
    rest.append("png")
    return ".".join(rest)


if __name__ == "__main__":
    for root, subdirs, files in os.walk("."):
        for file in files:
            path = os.path.join(root, file)
            testme = Image.open(path)
            if has_alpha(testme):
                logging.info("{} has alpha".format(path))

                png = testme.convert("RGBA")
                background = Image.new("RGBA", png.size, (255, 255, 255))

                alpha_composite = Image.alpha_composite(background, png)
                alpha_composite.save(path_as_png(path))
                os.remove(path)
            if not is_type_ok(testme):
                logging.info("%s has wrong type: %s", path, testme.format)
                testme.save(path_as_png(path))
                try:
                    os.remove(path)
                except FileNotFoundError:
                    logging.warning(
                        "path not found for %s in %s with path %s and new path %s",
                        file,
                        root,
                        path,
                        path_as_png(path),
                    )
