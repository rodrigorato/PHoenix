from ast.nodes import *


# FIXME assumption, we're ignoring type hinting
class FunctionDefinitionNode(ChildfulNode):
    def __init__(self, kind, name, arguments, children):
        ChildfulNode.__init__(self, kind, children)
        self.name = name
        self.arguments = arguments  # arguments is a list of VariableNodes
