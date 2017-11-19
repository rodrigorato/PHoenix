from ast.nodes import Node
from ast.taintknowledge import KindKnowledge
import pprint


def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


class ExpressionNode(Node):
    def __init__(self, kind):
        Node.__init__(self, kind)


class AttributionNode(ExpressionNode):
    def __init__(self, kind, left_expr, right_expr):
        ExpressionNode.__init__(self, kind)
        self.left_expr = left_expr
        self.right_expr = right_expr

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'left_expr: ' + pretty_format(self.left_expr) + ',' \
                'right_expr: ' + pretty_format(self.right_expr) + '>'


class UnaryExpression(ExpressionNode):
    def __init__(self, kind, type, expr):
        ExpressionNode.__init__(self, kind)
        self.type = type    # The Unary operator, like '!' and '++'
        self.expr = expr    # Every Unary expression has an expression associated with it

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'type: ' + pretty_format(self.type) + ',' \
                'expr: ' + pretty_format(self.expr) + '>'


class BinaryExpression(ExpressionNode):
    def __init__(self, kind, type, left_expr, right_expr):
        ExpressionNode.__init__(self, kind)
        self.type = type                # The operator, like '+' or '*'
        self.left_expr = left_expr      # Every binary expression has a left expr and a..
        self.right_expr = right_expr    # right expression!

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'type: ' + pretty_format(self.type) + ',' \
                'left_expr: ' + pretty_format(self.left_expr) + ',' \
                'right_expr: ' + pretty_format(self.right_expr) + '>'


class TernaryExpression(ExpressionNode):
    def __init__(self, kind, test, true_expr, false_expr):
        ExpressionNode.__init__(self, kind)
        self.test = test
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'test: ' + pretty_format(self.test) + ',' \
                'true_expr: ' + pretty_format(self.true_expr) + ',' \
                'false_expr: ' + pretty_format(self.false_expr) + '>'


# FIXME assumption - an indexation is a variable
# so $a[1] is a variable node
class VariableNode(ExpressionNode):
    def __init__(self, kind, name):
        ExpressionNode.__init__(self, kind)
        self.name = name

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'name: ' + self.name + '>'


# FIXME assumption - we're not handling indexation calls
# so $a[1]("ha"); isn't handled
class FunctionCallNode(ExpressionNode):
    def __init__(self, kind, name, arguments):
        ExpressionNode.__init__(self, kind)
        self.name = name
        self.arguments = arguments  # arguments is a list of ExpressionNodes

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'name: ' + self.name + ',' \
                'arguments: ' + pretty_format(self.arguments) + '>'

    # FIXME assuming that a function call to a function not defined here is safe
    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # We have the function definition
        if self.name in self.knowledge.function_def_nodes:
            func_def_node = self.knowledge.function_def_nodes[self.name]

            knowledge_for_func_call = self.knowledge

            # Match the arguments from this func call to the func def
            for arg_index in range(len(func_def_node.arguments)):
                func_def_node.arguments[arg_index].name = self.arguments[arg_index]


            func_def_node.is_tainted()

        # The function isnt defined here
        # FIXME we're assuming it is safe
        else:

            # Evaluate the current arguments as they are expressions
            for argument in self.arguments:
                self.knowledge = argument.is_tainted(self.knowledge)

            return self.knowledge

# Stuff like $_GET and $_POST
class EntryPointNode(VariableNode):
    def __init__(self, kind, name):
        VariableNode.__init__(self, kind, name)
        self.tainted = True
        self.visited = True

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'name: ' + self.name + '>'


class ConstantNode(ExpressionNode):
    def __init__(self, kind, value):
        ExpressionNode.__init__(self, kind)
        self.value = value
        self.tainted = False

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'value: ' + pretty_format(self.value) + '>'


class EncapsedStringNode(ExpressionNode):
    def __init__(self, kind, value, type):
        ExpressionNode.__init__(self, kind)
        self.value = value  # Value is a list of ExpressionNodes
        self.type = type  # FIXME assuming only string is possible


class SinkCallNode(FunctionCallNode):
    def __init__(self, kind, name, arguments, patterns_list):
        FunctionCallNode.__init__(self, kind, name, arguments)
        self.patterns_list = patterns_list


class SanitizationCallNode(FunctionCallNode):
    def __init__(self, kind, name, arguments, patterns_list):
        FunctionCallNode.__init__(self, kind, name, arguments)
        self.patterns_list = patterns_list
