import unittest
from rexpy.regex import *

class TestRegex(unittest.TestCase):

    def test_unit(self):
        self.assertTrue(match("a", "a"))
        self.assertFalse(match("a", "b"))

    def test_star(self):
        self.assertTrue(match("a*", ""))
        self.assertTrue(match("a*", "a"))
        self.assertTrue(match("a*", "aa"))
        self.assertTrue(match("a*", "aaaa"))
        self.assertFalse(match("a*", "aab"))

    def test_concat(self):
        self.assertFalse(match("a*b", "aaa"))
        self.assertTrue(match("a*b*", "aaa"))
