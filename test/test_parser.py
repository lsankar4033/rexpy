import unittest
import rexpy.ast as ast
from rexpy.parser import *

class TestParser(unittest.TestCase):

    def test_unit(self):
        self.assertEqual(re_string_to_ast("a"), ast.AtomASTNode("a"))

    def test_star(self):
        self.assertEqual(re_string_to_ast("a*"),
                         ast.StarASTNode(ast.AtomASTNode("a")))

    def test_concat(self):
        self.assertEqual(re_string_to_ast("ab"),
                         ast.ConcatASTNode(
                             [ast.AtomASTNode("a"),
                              ast.AtomASTNode("b")]))

    def test_union(self):
        self.assertEqual(re_string_to_ast("a|b"),
                         ast.UnionASTNode(
                             [ast.AtomASTNode("a"),
                              ast.AtomASTNode("b")]))

    def test_combination(self):
        self.assertEqual(re_string_to_ast("a*b|cd*"),
                         ast.UnionASTNode(
                             [ast.ConcatASTNode(
                                 [ast.StarASTNode(ast.AtomASTNode("a")),
                                  ast.AtomASTNode("b")]),
                              ast.ConcatASTNode(
                                  [ast.AtomASTNode("c"),
                                   ast.StarASTNode(ast.AtomASTNode("d"))])]))

    def test_paren(self):
        self.assertEqual(re_string_to_ast("(a|b)*c"),
                         ast.ConcatASTNode(
                             [ast.StarASTNode(
                                 ast.UnionASTNode(
                                     [ast.AtomASTNode("a"),
                                      ast.AtomASTNode("b")])),
                              ast.AtomASTNode("c")]))

        # NOTE: Maybe we want to collapse the nesting of Concats/Unions as seen here in the future
        self.assertEqual(re_string_to_ast("(a(b(c|d)))"),
                         ast.ConcatASTNode(
                             [ast.AtomASTNode("a"),
                              ast.ConcatASTNode(
                                  [ast.AtomASTNode("b"),
                                   ast.UnionASTNode(
                                       [ast.AtomASTNode("c"),
                                        ast.AtomASTNode("d")])])]))
