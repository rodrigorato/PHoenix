from ast.nodes import *


class CycleNode(ChildfulNode):
    def __init__(self, kind, children, test):
        ChildfulNode.__init__(self, kind, children)
        self.test = test  # Its an ExpressionNode


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