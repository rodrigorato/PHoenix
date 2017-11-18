class Node:
    def __init__(self, kind):
        self.kind = kind  # This node's kind

    def __repr__(self):
        return '<kind:' + self.kind + '>'


# This is just a fancy name for an abstraction of a node that has child nodes
class ChildfulNode(Node):
    def __init__(self, kind, children):
        Node.__init__(self, kind)
        self.children = children

    def __repr__(self):
        return '<kind:' + self.kind + ', children:' + self.children.__repr__() + '>'


class ProgramNode(ChildfulNode):
    def __init__(self, kind, children):
        ChildfulNode.__init__(self, kind, children)

