#! /usr/bin/env python3
"""downloads images from smutty.com"""
from dataclasses import dataclass
import os
import logging
import sys

import requests
from bs4 import BeautifulSoup

BASE = "smutty.com"

os.environ["NO_PROXY"] = BASE


@dataclass
class TagPage:
    """>>> t = TagPage.from_tag('female')"""

    tag: str
    dom: BeautifulSoup

    @staticmethod
    def from_tag(tag: str):
        """load tag search page from tag name"""
        response = requests.get("http://" + BASE + "/h/" + tag)
        dom = BeautifulSoup(response.content, "html.parser")
        return TagPage(tag, dom)

    def all_image_a_tags(self):
        """@return all image tags on this tag page"""
        out = []
        for anchor in self.dom.findAll("a"):
            img = anchor.find("img")
            if img and img.get("src") and "javascript" not in img.get("src"):
                out.append(anchor)
        return out

    def next_page(self):
        """@return next page of topic"""
        nexturl = self.dom.find("a", {"class": "next"})
        logging.info("next url: %s", nexturl.get("href"))
        response = requests.get("http://" + BASE + nexturl.get("href"))
        return TagPage(self.tag, BeautifulSoup(response.content, "html.parser"))

    def download_all(self):
        """download all images on page"""
        for tag in self.all_image_a_tags():
            if logging.getLogger().level <= logging.INFO:
                print(".", end="", flush=True)
            try:
                ImagePage.from_a_tag(tag).download()
            except AttributeError:
                logging.warning("no download for %s", str(tag))


@dataclass
class ImagePage:
    """ >>> a = t.all_image_a_tags()
    >>> i = ImagePage.from_a_tag(a[15])
    >>> i.download() """

    id_: str
    dom: BeautifulSoup

    @staticmethod
    def from_a_tag(tag):
        """load ImagePage from tag name"""
        response = requests.get("http://" + BASE + tag.get("href"))
        dom = BeautifulSoup(response.content, "html.parser")
        if "Bad gateway" in dom.find("title").text:
            raise Exception("failed to retrieve " + tag.get("href"))
        return ImagePage(tag.find("img").get("alt"), dom)

    @property
    def image_url(self):
        """its image URL"""
        return self.dom.find("img", {"class": "image_perma_img"}).get("src")

    @property
    def tags(self):
        """its tags"""
        return [
            x
            for x in self.dom.find("img", {"class": "image_perma_img"})
            .get("alt")
            .split("#")
            if x
        ]

    def download(self, filename=None):
        """download image to filename or URL path plus tags"""
        if not filename:
            filename = self.image_url.split("/")[-1]
            parts = filename.split(".")
            nuparts = [parts[0]]
            nuparts.extend(self.tags)
            filename = ".".join(nuparts).replace(" ", "")
            filename += "." + parts[1]
        if os.path.exists(filename):
            logging.info("file %s already exists, skipping", filename)
        with open(filename, "wb") as outfile:
            outfile.write(requests.get("http:" + self.image_url).content)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        subject = sys.argv[1]
    except:
        subject = "female"
    logging.info("downloading for %s", subject)
    t = TagPage.from_tag(subject)
    for _ in range(100):
        t.download_all()
        t = t.next_page()
