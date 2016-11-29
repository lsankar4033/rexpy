class NFA:
    """The NFA class represents an entire NFA representing an RE. Each NFA consists of a start_node and
    accept_nodes. The transition function is implicit as each node has its own transition map.
    """
    def __init__(self, start_node, accept_nodes):
        self.start_node = start_node
        self.accept_nodes = accept_nodes

    def __str__(self):
        """Human readable format used just for debugging.
        """

        # Use 'id(x)' to label each node
        edges = []

        # Do a DFS through the graph, keeping track of each edge
        frontier = [self.start_node]
        visited = set()
        node_dict = {} # used to re-index nodes to a more human readable format
        cur_node_ind = 0
        while len(frontier) > 0:
            next_node = frontier.pop()
            node_dict[id(next_node)] = cur_node_ind
            cur_node_ind += 1

            for edge, nodes in next_node.transitions.items():
                for node in nodes:
                    edges.append((id(next_node), edge, id(node)))

                    if node not in visited:
                        frontier.append(node)

            visited.add(next_node)

        lines = [str(node_dict[s]) + " -> '" + str(t) + "' -> " + str(node_dict[e]) for s,t,e in edges]
        lines_str = "Edges: \n" + "\n".join(lines)

        start_str = "Start node: " + str(node_dict[id(self.start_node)])
        accept_str = "Accept nodes: " + str([node_dict[id(n)] for n in self.accept_nodes])

        return "\n".join([start_str, accept_str, lines_str])

class Node:
    """The Node class represents a single State of the NFA as well as any transitions out of it. Nodes are
    represented this way to facilitate BFS through the NFA.

    transitions is a map from char -> [Node]
    """
    def __init__(self):
        self.transitions = {}

    def add_transition(self, trans_char, node):
        if trans_char in self.transitions:
            self.transitions[trans_char].append(node)
        else:
            self.transitions[trans_char] = [node]

def build_single_char_nfa(char):
    """Given a single character, creates an NFA with one transition from start node to end node using
    that character."""
    start = Node()
    accept = Node()
    start.add_transition(char, accept)
    return NFA(start, set([accept]))

def build_star_nfa(nfa):
    """Given a NFA nfa, create a new NFA representing (nfa)*."""
    new_start = Node()
    new_start.add_transition("", nfa.start_node)

    new_accept = Node()
    for old_accept in nfa.accept_nodes:
        old_accept.add_transition("", new_accept)

    new_accept.add_transition("", new_start)
    new_start.add_transition("", new_accept)

    return NFA(new_start, set([new_accept]))

def build_concat_nfa(nfas):
    """Given a sequence of NodeGroups, create a NodeGroup representing their (in order) concatenation."""
    for i in range(1, len(nfas)):
        for inner_accept in nfas[i-1].accept_nodes:
            inner_accept.add_transition("", nfas[i].start_node)

    new_start = Node()
    new_accept = Node()

    new_start.add_transition("", nfas[0].start_node)
    for end_accept in nfas[-1].accept_nodes:
        end_accept.add_transition("", new_accept)

    return NFA(new_start, set([new_accept]))
