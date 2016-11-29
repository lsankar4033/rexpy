import rexpy.ast as ast
import rexpy.nfa as nfa

def re_string_to_ast(re_str):
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

    return ast.ConcatASTNode(nodes_to_concat)
