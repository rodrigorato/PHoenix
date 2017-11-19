import pprint


def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


class Node:
    def __init__(self, kind):
        self.kind = kind      # This node's kind
        self.tainted = True   # FIXME assuming its good until an entry point is found
        self.visited = False  # has this node been visited already?

    def __repr__(self):
        return '<kind:' + self.kind + '>'


# This is just a fancy name for an abstraction of a node that has child nodes
# i.e. children somewhere, like inside a body
class ChildfulNode(Node):
    def __init__(self, kind, children):
        Node.__init__(self, kind)
        self.children = children

    def __repr__(self):
        return '<kind:' + self.kind + ', children:' + pretty_format(self.children) + '>'


class ProgramNode(ChildfulNode):
    def __init__(self, kind, children):
        ChildfulNode.__init__(self, kind, children)


"""
# FIXME assumes a node that is actually *nothing* is untainted
class NothingNode(Node):
    def __init__(self):
        Node.__init__(self, 'NOTHING')
        self.tainted = False

    def __bool__(self):
        return False
"""