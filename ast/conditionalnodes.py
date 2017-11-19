from ast.nodes import *


class IfThenElseNode(ChildfulNode):
    def __init__(self, kind, test, body, alternate=None):
        ChildfulNode.__init__(self, kind, body)
        self.test = test  # An expression
        self.body = body  # A list of Nodes
        self.alternate = alternate  # A IfThenElse node, an ElseNode or None

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
               'children:' + pretty_format(self.children) + ',' \
               + (pretty_format(self.alternate) if self.alternate else '') + '>'


class ElseNode(ChildfulNode):
    def __init__(self, kind, children):
        ChildfulNode.__init__(self, kind, children)


# A SwitchNode's child are its CaseNodes
class SwitchNode(ChildfulNode):
    def __init__(self, kind, test, body):
        ChildfulNode.__init__(self, kind, body)
        self.test = test

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
               'test: ' + pretty_format(self.test) + ',' \
               'body: ' + pretty_format(self.children) + '>'


class CaseNode(ChildfulNode):
    def __init__(self, kind, test, body):
        ChildfulNode.__init__(self, kind, body)
        self.test = test

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
               'test: ' + pretty_format(self.test) + ',' \
               'body: ' + pretty_format(self.children) + '>'
