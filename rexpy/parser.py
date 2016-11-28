import nfa

# TODO When the grammar is augmented to have more than just '*' and 'concat,' change this to properly parse a
# CFG and return a tree.
# Convert a RE string to a parsed RE. Returns a list of terminals (should be a tree in the future).
def parse_re_string(re_str):
    re_terminals = []

    prev_char = None
    for char in re_str:
        new_terminal = char
        if prev_char is None and char is "*":
            raise ValueError("Regex string %s has leading '*' character!" % re_str)

        elif prev_char is "*" and char is "*":
            raise ValueError("Regex string %s has consecutive '*' characters!" % re_str)

        elif prev_char is not "*" and char is "*":
            re_terminals.pop()
            new_terminal = prev_char + char

        re_terminals.append(new_terminal)
        prev_char = char

    return re_terminals

# This method is a temporary approach to converting a terminal string (i.e. a or a*) to a node group. Once I
# update the parsed form of an RE to include the full derivation tree, this method should no longer be
# necessary.
def term_str_to_node_group(term_str):
    if len(term_str) is 1:
        return nfa.build_single_char_node_group(term_str[0])
    elif len(term_str) is 2 and term_str[1] is "*":
        base = nfa.build_single_char_node_group(term_str[0])
        return nfa.build_star_node_group(base)
    else:
        raise ValueError("Term string %s isn't of the form 'a' or 'a*'" % term_str)

# TODO Change the input of this function to be a tree of nodes instead of just an array representing concat.
# Convert a parsed RE to the NFA that recognizes it.
def convert_re_to_nfa(parsed_re):
    to_concat = [term_str_to_node_group(t) for t in parsed_re]
    concat_node_group = nfa.build_concat_node_group(to_concat)

    return nfa.NFA(concat_node_group.start_node, set([concat_node_group.end_node]))

def re_string_to_nfa(re_str):
    return convert_re_to_nfa(parse_re_string(re_str))
