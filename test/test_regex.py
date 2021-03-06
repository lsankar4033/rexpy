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

    def test_union(self):
        self.assertTrue(match("a*b|c", "aaab"))
        self.assertTrue(match("a*b|c", "c"))
        self.assertFalse(match("a*bc|cd", "d"))

    def test_paren(self):
        self.assertFalse(match("(ab)*", "a"))
        self.assertFalse(match("(ab)*", "abb"))
        self.assertTrue(match("(ab)*", "ab"))
        self.assertTrue(match("(ab)*", "ababab"))

        self.assertFalse(match("(a|bc)d", "acd"))
        self.assertTrue(match("(a|bc)d", "bcd"))
        self.assertTrue(match("(a|bc)d", "ad"))
