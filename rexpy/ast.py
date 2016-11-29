from collections import namedtuple

# RE AST Node types
ConcatASTNode = namedtuple('ConcatASTNode', 'nodes')
UnionASTNode = namedtuple('UnionASTNode', 'nodes')
StarASTNode = namedtuple('StarASTNode', 'node')
AtomASTNode = namedtuple('AtomASTNode', 'char')
