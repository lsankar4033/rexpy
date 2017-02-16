import rexpy.ast as ast

# RE Grammar
# One approach is to store the normal precedence rules with paren expressions built on top of that.
# Normal precedence is *, concat, union
#
# Parenthesization can work by creating a new rule for a parenthesized element follwed by each operation (and
# atom)
#
# I can also just look at existing RE grammars online...

# TODO Augment this parser to properly parse according to the full RE grammar
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
