from collections import namedtuple
from rexpy.ast import ConcatASTNode, UnionASTNode, StarASTNode, AtomASTNode

# Each intermediate parse method returns a list of these
ParsedNode = namedtuple('ParsedNode', 'ast_node next_idx')

def parse_regex(re_str, next_idx):
    return parse_union(re_str, next_idx)

def parse_paren(re_str, next_idx):
    if next_idx >= len(re_str):
        return []

    # '('R')'
    if re_str[next_idx] is not '(':
        return []
    next_idx += 1

    parsed_regexes = parse_regex(re_str, next_idx)
    parsed_close_paren = []
    for parsed_regex in parsed_regexes:
        ni = parsed_regex.next_idx
        if ni < len(re_str) and re_str[ni] is ')':
            parsed_close_paren.append(
                parsed_regex._replace(next_idx = ni + 1)
            )

    return parsed_close_paren

def parse_union(re_str, next_idx):
    # C
    parsed_c = parse_concat(re_str, next_idx)

    # C'|'U
    parsed_cu = []
    for parsed_concat in parsed_c:
        ni = parsed_concat.next_idx
        if ni < len(re_str) and re_str[ni] is '|':
            parsed_unions = parse_union(re_str, ni + 1)
            for parsed_union in parsed_unions:
                parsed_cu.append(
                    parsed_union._replace(
                        ast_node = UnionASTNode([parsed_concat.ast_node, parsed_union.ast_node])
                    )
                )

    return parsed_c + parsed_cu

def parse_concat(re_str, next_idx):
    # S
    parsed_s = parse_star(re_str, next_idx)

    # SC
    parsed_sc = []
    for parsed_star in parsed_s:
        parsed_concats = parse_concat(re_str, parsed_star.next_idx)
        for parsed_concat in parsed_concats:
            parsed_sc.append(
                parsed_concat._replace(
                    ast_node = ConcatASTNode([parsed_star.ast_node, parsed_concat.ast_node])
                )
            )

    return parsed_s + parsed_sc

def parse_star(re_str, next_idx):
    # A
    parsed_a = parse_atom(re_str, next_idx)

    # A'*'
    parsed_astar = []
    for parsed_atom in parsed_a:
        ni = parsed_atom.next_idx
        if ni < len(re_str) and re_str[ni] is '*':
            parsed_astar.append(
                ParsedNode(StarASTNode(parsed_atom.ast_node), ni + 1)
            )

    return parsed_a + parsed_astar

# TODO Add escape character support
invalid_atoms = set(['(', '|', '*'])

def parse_atom(re_str, next_idx):
    # P
    parsed_p = parse_paren(re_str, next_idx)

    # \w
    parsed_w = []
    if next_idx < len(re_str) and re_str[next_idx] not in invalid_atoms:
        ast_node = AtomASTNode(re_str[next_idx])
        parsed_w.append(ParsedNode(ast_node, next_idx + 1))

    return parsed_p + parsed_w

def re_string_to_ast(re_str):
    """Uses the following regex grammar to parse the provided string:
    R -> U
    P -> '('R')'
    U -> C | C'|'U
    C -> S | SC
    S -> A | A'*'
    A -> \w | P

    where \w is any non-special character. At some point in the future I'll add proper escape characters.
    """
    parses = parse_regex(re_str, 0)
    finished_parses = [parse for parse in parses if parse.next_idx == len(re_str)]

    return finished_parses[0]
