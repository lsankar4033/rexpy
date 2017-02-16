from collections import namedtuple

# TODO Change import to import specific node types
import rexpy.ast as ast

# RE Grammar
# One approach is to store the normal precedence rules with paren expressions built on top of that.
# Normal precedence is *, concat, union
#
# One possible grammar (quotes used to indicate character instead of symbol):
#
# R -> U | P
# P -> '('R')'
# U -> C | C'|'U | P | P'|'U
# C -> S | SC | P | PC
# S -> A | A'*' | P | P'*'
# A -> \w | P
#
# Note that this grammar is NOT LL(1) because each level has multiple derivations starting with '('

# Each intermediate parse method returns a list of these
ParsedNode = namedtuple('ParsedNode', 'ast_node next_idx')

def parse_regex(re_str, next_idx):
    union_attempts = parse_union(re_str, next_idx)
    if len(union_attempts) > 0:
        return union_attempts
    else:
        return parse_paren(re_str, next_idx)

def parse_paren(re_str, next_idx):
    if re_str[next_idx] is not '(':
        return []
    next_idx += 1

    parsed_regexes = parse_regex(re_str, next_idx)

    # TODO generalize this filtering mechanism. This would clean up below methods as well
    parsed_close_paren = []
    for parsed_regex in parsed_regexes:
        ni = parsed_regex.next_idx
        if re_str[ni] is ')':
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
        if re_str[ni] is '|':
            parsed_unions = parse_union(re_str, ni + 1)
            for parsed_union in parsed_unions:
                parsed_cu.append(
                    parsed_union._replace(
                        ast_node = ast.UnionASTNode([parsed_concat.ast_node, parsed_union.ast_node])
                    )
                )

    # P
    parsed_p = parse_paren(re_str, next_idx)

    # P'|'U
    parsed_pu = []
    for parsed_paren in parsed_p:
        ni = parsed_paren.next_idx
        if re_str[ni] is '|':
            parsed_unions = parse_union(re_str, ni + 1)
            for parsed_union in parsed_unions:
                parsed_pu.append(
                    parsed_union._replace(
                        ast_node = ast.UnionASTNode([parsed_paren.ast_node, parsed_union.ast_node])
                    )
                )

    return parsed_c + parsed_cu + parsed_p + parsed_pu

def parse_concat(re_str, i):
    return []

def parse_star(re_str, i):
    return []

def parse_atom(re_str, i):
    return []

# TODO Augment this parser to properly parse according to the full RE grammar. Will involve hardcoding an LR
# parser
def re_string_to_ast(re_str):
    """This simplified version of regexes allows for only expressions with a non-recursive tree structure and
    no parens. What this means is that each of the '|', concat, and '*' operators occur at a single depth of
    the derivation tree each and only in the order [|, concat, *]
    """
    return build_union_node(re_str)

def build_union_node(re_str):
    union_strs = re_str.split("|")
    if union_strs[0] is "" or union_strs[-1] is "":
        raise ValueError("Regex substring %s has leading or trailing '|' character" % re_str)

    nodes_to_union = [build_concat_node(s) for s in union_strs]
    if len(nodes_to_union) is 1:
        return nodes_to_union[0]
    else:
        return ast.UnionASTNode(nodes_to_union)

def build_concat_node(re_str):
    nodes_to_concat = []

    prev_char = None
    for char in re_str:
        if prev_char is None and char is "*":
            raise ValueError("Regex string %s has leading '*' character!" % re_str)

        elif prev_char is "*" and char is "*":
            raise ValueError("Regex string %s has consecutive '*' characters!" % re_str)

        elif prev_char is not "*" and char is "*":
            prev_node = nodes_to_concat.pop()
            nodes_to_concat.append(ast.StarASTNode(prev_node))

        else:
            nodes_to_concat.append(ast.AtomASTNode(char))

        prev_char = char

    if len(nodes_to_concat) is 1:
        return nodes_to_concat[0]
    else:
        return ast.ConcatASTNode(nodes_to_concat)
