

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

# TODO Change the input of this function to be a tree of nodes instead of just an array representing concat.
# Convert a parsed RE to the NFA that recognizes it.
def convert_re_to_nfa(re):
    pass
