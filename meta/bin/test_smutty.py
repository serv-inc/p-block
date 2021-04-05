#! /usr/bin/env python3
'''testing smutty.py'''
import unittest

from smutty import TagPage


class TestSmuttyLoads(unittest.TestCase):
    '''check that loads'''
    def test_get(self):
        '''get and parse page'''
        page = TagPage.from_tag("female")
        self.assertEqual(page.tag, "female")


if __name__ == "__main__":
    unittest.main()
