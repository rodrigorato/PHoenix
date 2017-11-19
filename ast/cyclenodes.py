from ast.nodes import *


class CycleNode(ChildfulNode):
    def __init__(self, kind, children, test):
        ChildfulNode.__init__(self, kind, children)
        self.test = test  # Its an ExpressionNode

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
               'test: ' + pretty_format(self.test) + ',' \
               'children: ' + pretty_format(self.children) + '>'


class WhileNode(CycleNode):
    def __init__(self, kind, children, test):
        CycleNode.__init__(self, kind, children, test)


class DoWhileNode(CycleNode):
    def __init__(self, kind, children, test):
        CycleNode.__init__(self, kind, children, test)


class ForNode(CycleNode):
    def __init__(self, kind, children, test, init, increment):
        CycleNode.__init__(self, kind, children, test)
        self.init = init
        self.increment = increment

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'init: ' + pretty_format(self.init) + ',' \
                'test: ' + pretty_format(self.test) + ',' \
                'increment: ' + pretty_format(self.increment) + ',' + \
                'children: ' + pretty_format(self.children) + '>'
