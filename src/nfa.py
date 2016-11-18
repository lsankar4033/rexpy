class Node:
    """The Node class represents a single State of the NFA as well as any transitions out of it. Nodes are
    represented this way to facilitate BFS through the NFA.

    transitions is a map from char -> [Node]
    """
    def __init__(self):
        self.transitions = {}
        self.is_accept = False

    def add_transition(self, trans_char, node):
        if self.transitions.has_key(trans_char):
            self.transitions[trans_char].append(node)
        else:
            self.transitions[trans_char] = [node]

class NodeGroup:
    """A NodeGroup represents a single grouping from the RE derivation tree. Each NodeGroup must have both a
    start Node and an end Node so that it can be composed with other groups properly.
    """
    def __init__(self, start_node, end_node):
        self.start_node = start_node
        self.end_node = end_node

def build_star_node_group(input_group):
    """Given an NodeGroup input_group, create a new NodeGroup representing (input_group)*."""
    new_start = Node()
    new_start.add_transition("", input_group.start_node)

    new_end = Node()
    input_group.end_node.add_transition("", new_end)

    return NodeGroup(new_start, new_end)

def build_concat_node_group(*input_groups):
    """Given a sequence of NodeGroups, create a NodeGroup representing their (in order) concatenation."""
    for i in range(1, len(input_groups)):
        input_groups[i-1].end_node.add_transition("", input_groups[i].start_node)

    new_start = Node()
    new_end = Node()

    new_start.add_transition("", input_groups[0].start_node)
    input_groups[-1].add_transition("", new_end)

    return NodeGroup(new_start, new_end)
