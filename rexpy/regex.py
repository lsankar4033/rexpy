import parser

def _add_node(n, current_nodes):
    """Augments current_nodes with n and any other nodes reachable by n with an epsilon transition. Note
    that this method won't add nodes that already exist in current_nodes.
    """
    if n not in current_nodes:
        current_nodes.add(n)

        # Do a DFS on all nodes reachable from n using only epsilon transitions
        frontier = []
        if '' in n.transitions:
            frontier.extend(
                list(filter(lambda n: n not in current_nodes, n.transitions[''])))
        while len(frontier) > 0:
            next_node = frontier.pop()
            current_nodes.add(next_node)

            if '' in next_node.transitions:
                frontier.extend(
                    list(filter(lambda n: n not in current_nodes, next_node.transitions[''])))

# TODO Maybe this should be encapsulated in a class once we add capture variables, etc.
def match(re_str, s):
    nfa = parser.re_string_to_nfa(re_str)

    # add the start node of the NFA to 'current nodes,' then explore any epsilon branches to add to
    # current nodes (do loop detection)
    current_nodes = set()
    _add_node(nfa.start_node, current_nodes)

    # read the next char of s, update all nodes in 'current nodes,' then follow epsilon branches (do loop
    # detection)
    for c in s:
        new_nodes = [new_node
                     for cur_node in current_nodes if c in cur_node.transitions
                     for new_node in cur_node.transitions[c]]
        current_nodes = set()

        for new_node in new_nodes:
            _add_node(new_node, current_nodes)

    # return true if any node is an accept node
    return any(filter(lambda n: n in nfa.accept_nodes, current_nodes))
