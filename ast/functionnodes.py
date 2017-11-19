from ast.nodes import *
from ast.expressionnodes import *


# FIXME assumption, we're ignoring type hinting
class FunctionDefinitionNode(ChildfulNode):
    def __init__(self, kind, name, arguments, children):
        ChildfulNode.__init__(self, kind, children)
        self.name = name
        self.arguments = arguments  # arguments is a list of VariableNodes


# TODO not considering byref arguments
class FunctionDefinitionArgumentsNode(VariableNode):
    def __init__(self, kind, name, value_expr=None):
        VariableNode.__init__(self, kind, name)
        self.value_expr = value_expr
