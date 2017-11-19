import pprint

from ast.taintknowledge import KindKnowledge

def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


class Node:
    def __init__(self, kind):
        self.kind = kind      # This node's kind
        self.tainted = False  # FIXME assuming its good until an entry point is found
        self.visited = False  # has this node been visited already?
        self.knowledge = KindKnowledge()

    def __repr__(self):
        return '<kind:' + self.kind + ', taint-knowledge:' + pretty_format(self.is_tainted(self.knowledge)) + '>'

    def is_tainted(self, knowledge):
        # FIXME check if all we need to do is update with the previous knowledge
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)
        return self.knowledge


# This is just a fancy name for an abstraction of a node that has child nodes
# i.e. children somewhere, like inside a body
class ChildfulNode(Node):
    def __init__(self, kind, children):
        Node.__init__(self, kind)
        self.children = children

    def __repr__(self):
        return '<kind:' + self.kind + ', children:' + pretty_format(self.children) + '>'

    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # For this node all we need to do is update our knowledge
        # with the knowledge from all our children
        for child in self.children:
            # FIXME we're doing the check like this to a void cyclic dependencies
            # FIXME this is also an assumption.
            if child.kind == 'function':
                # Store it and don't analyse it yet
                self.knowledge.function_def_nodes[child.name] = child
            else:
                self.knowledge = child.is_tainted(self.knowledge)

        return self.knowledge


class ProgramNode(ChildfulNode):
    def __init__(self, kind, children):
        ChildfulNode.__init__(self, kind, children)

    # Taint analysis bootstraping:
    # The ProgramNode is the first to be analysed and has no previous knowledge.
    def do_static_analysis(self):
        self.knowledge = self.is_tainted(self.knowledge)
        return self.knowledge


"""
# FIXME assumes a node that is actually *nothing* is untainted
class NothingNode(Node):
    def __init__(self):
        Node.__init__(self, 'NOTHING')
        self.tainted = False

    def __bool__(self):
        return False
"""