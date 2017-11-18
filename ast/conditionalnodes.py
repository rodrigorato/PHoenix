from ast.nodes import *


class IfThenElseNode(ChildfulNode):
    def __init__(self, kind, test, body, alternate=None):
        ChildfulNode.__init__(self, kind, body)
        self.test = test  # An expression
        self.body = body  # A list of Nodes
        self.alternate = alternate  # A IfThenElse node or None


# A SwitchNode's child are its CaseNodes
class SwitchNode(ChildfulNode):
    def __init__(self, kind, test, body):
        ChildfulNode.__init__(self, kind, body)
        self.test = test


class CaseNode(ChildfulNode):
    def __init__(self, kind, test, body):
        ChildfulNode.__init__(self, kind, body)
        self.test = test


