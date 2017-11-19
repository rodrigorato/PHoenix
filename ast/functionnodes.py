from ast.nodes import ChildfulNode
from ast.expressionnodes import VariableNode
from ast.taintknowledge import KindKnowledge
import pprint

def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


# FIXME assumption, we're ignoring type hinting
class FunctionDefinitionNode(ChildfulNode):
    def __init__(self, kind, name, arguments, children):
        ChildfulNode.__init__(self, kind, children)
        self.name = name
        self.arguments = arguments  # arguments is a list of VariableNodes

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', name: ' + self.name + ',' \
                'arguments: ' + pretty_format(self.arguments) + ',' \
                'children: ' + pretty_format(self.children) + '>'

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # Handle the body instructions (like a ChildfulNode)
        return_knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        self.knowledge = KindKnowledge()  # Empty its knowledge so that the next call doesn't have values (yet)

        return return_knowledge


# TODO not considering byref arguments
class FunctionDefinitionArgumentsNode(VariableNode):
    def __init__(self, kind, name, value_expr=None):
        VariableNode.__init__(self, kind, name)
        self.value_expr = value_expr

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', name: ' + self.name + ',' \
                'value_expr: ' + pretty_format(self.value_expr) + '>'
