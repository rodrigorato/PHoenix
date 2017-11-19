from ast.nodes import Node
from ast.taintknowledge import KindKnowledge
import pprint


def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


class ExpressionNode(Node):
    def __init__(self, kind):
        Node.__init__(self, kind)


# FIXME assume left_expr is only a variable
# FIXME not considering indexations
class AttributionNode(ExpressionNode):
    def __init__(self, kind, left_expr, right_expr):
        ExpressionNode.__init__(self, kind)
        self.left_expr = left_expr
        self.right_expr = right_expr

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', left_expr: ' + pretty_format(self.left_expr) + ',' \
                'right_expr: ' + pretty_format(self.right_expr) + '>'

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # Evaluate the right expression
        self.knowledge = self.right_expr.is_tainted(self.knowledge)

        # Evaluate the left expression FIXME check if necessary
        self.knowledge = self.left_expr.is_tainted(self.knowledge)

        # Give the right expression's patterns to the left one
        self.knowledge.kinds[self.left_expr.kind].nodes[self.left_expr.name] = \
            self.knowledge.kinds[self.right_expr.kind].nodes[self.right_expr.id]

        # Record that we learned this (un)taintness and return it out
        return self.knowledge



class UnaryExpression(ExpressionNode):
    def __init__(self, kind, type, expr):
        ExpressionNode.__init__(self, kind)
        self.type = type    # The Unary operator, like '!' and '++'
        self.expr = expr    # Every Unary expression has an expression associated with it

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', type: ' + pretty_format(self.type) + ',' \
                'expr: ' + pretty_format(self.expr) + '>'

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        self.knowledge = self.expr.is_tainted(self.knowledge)

        return self.knowledge


class BinaryExpression(ExpressionNode):
    def __init__(self, kind, type, left_expr, right_expr):
        ExpressionNode.__init__(self, kind)
        self.type = type                # The operator, like '+' or '*'
        self.left_expr = left_expr      # Every binary expression has a left expr and a..
        self.right_expr = right_expr    # right expression!

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', type: ' + pretty_format(self.type) + ',' \
                'left_expr: ' + pretty_format(self.left_expr) + ',' \
                'right_expr: ' + pretty_format(self.right_expr) + '>'

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        self.knowledge = self.left_expr.is_tainted(self.knowledge)
        self.knowledge = self.right_expr.is_tainted(self.knowledge)

        return self.knowledge


class TernaryExpression(ExpressionNode):
    def __init__(self, kind, test, true_expr, false_expr):
        ExpressionNode.__init__(self, kind)
        self.test = test
        self.true_expr = true_expr
        self.false_expr = false_expr

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', test: ' + pretty_format(self.test) + ',' \
                'true_expr: ' + pretty_format(self.true_expr) + ',' \
                'false_expr: ' + pretty_format(self.false_expr) + '>'

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        self.knowledge = self.test.is_tainted(self.knowledge)
        self.knowledge = self.true_expr.is_tainted(self.knowledge)
        self.knowledge = self.false_expr.is_tainted(self.knowledge)

        return self.knowledge


# FIXME assumption - an indexation is a variable
# so $a[1] is a variable node
class VariableNode(ExpressionNode):
    def __init__(self, kind, name):
        ExpressionNode.__init__(self, kind)
        self.name = name

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', name: ' + self.name + '>'

    # TODO check if nothing is needed here as we kind of assumed it

# FIXME assumption - we're not handling indexation calls
# so $a[1]("ha"); isn't handled
class FunctionCallNode(ExpressionNode):
    def __init__(self, kind, name, arguments):
        ExpressionNode.__init__(self, kind)
        self.name = name
        self.arguments = arguments  # arguments is a list of ExpressionNodes

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', name: ' + self.name + ',' \
                'arguments: ' + pretty_format(self.arguments) + '>'

    # FIXME assuming that a function call to a function not defined here is safe
    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # We have the function definition
        if self.name in self.knowledge.function_def_nodes:
            # TODO
            # TODO
            # TODO Function definition case
            # TODO
            # TODO
            # TODO

            func_def_node = self.knowledge.function_def_nodes[self.name]

            knowledge_for_func_call = self.knowledge

            # Match the arguments from this func call to the func def
            for arg_index in range(len(func_def_node.arguments)):
                func_def_node.arguments[arg_index].name = self.arguments[arg_index]


            func_def_node.is_tainted()

        # The function isn't defined here
        # FIXME we're assuming it is safe
        else:

            # Evaluate the current arguments as they are expressions
            for argument in self.arguments:
                self.knowledge = argument.is_tainted(self.knowledge)

            return self.knowledge


# Stuff like $_GET and $_POST
class EntryPointNode(VariableNode):
    def __init__(self, kind, name, patterns):
        VariableNode.__init__(self, kind, name)
        self.tainted = True
        self.visited = True
        self.patterns = patterns  # A list of patterns vulnerable to these entry points

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', name: ' + self.name + ', ' \
                'patterns: ' + self.patterns.__repr__() + '>'

    # This node bad, load its tainted patterns
    def is_tainted(self, knowledge):

        indexation_name_or_id = ""
        if hasattr(self, 'name'):
            indexation_name_or_id = self.name
        else:
            indexation_name_or_id = self.id

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        self.knowledge.kinds[self.kind].nodes[indexation_name_or_id].append(self.patterns)

        return self.knowledge


class ConstantNode(ExpressionNode):
    def __init__(self, kind, value):
        ExpressionNode.__init__(self, kind)
        self.value = value
        self.tainted = False

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', value: ' + pretty_format(self.value) + '>'

    # This node is always safe, clear its tainted patterns
    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        knowledge.kinds[self.kind].nodes[self.id] = []

        return self.knowledge


class EncapsedStringNode(ExpressionNode):
    def __init__(self, kind, value, type):
        ExpressionNode.__init__(self, kind)
        self.value = value  # Value is a list of ExpressionNodes
        self.type = type  # FIXME assuming only string is possible

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)
        #print("encapsed")
        # Evaluate all the expressions
        for exp in self.value:

            indexation_name_or_id = ""
            if hasattr(exp, 'name'):
                indexation_name_or_id = exp.name
            else:
                indexation_name_or_id = exp.id

            self.knowledge = exp.is_tainted(self.knowledge)
            #print("EXPRESSION", exp)
            #print("COISAS MAS", self.knowledge.kinds[exp.kind].nodes[indexation_name_or_id])
            # Give each expr's patterns to the encapsed one
            self.knowledge.kinds[self.kind].nodes[self.id]\
                .append(self.knowledge.kinds[exp.kind].nodes[indexation_name_or_id])

        return self.knowledge


# FIXME assuming all arguments in a sink are sensitive
class SinkCallNode(FunctionCallNode):
    def __init__(self, kind, name, arguments, patterns_list):
        FunctionCallNode.__init__(self, kind, name, arguments)
        self.patterns_list = patterns_list

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        for arg in self.arguments:
            self.knowledge = arg.is_tainted(self.knowledge)

        for arg in self.arguments:

            indexation_name_or_id = ""
            if hasattr(arg, 'name'):
                indexation_name_or_id = arg.name
            else:
                indexation_name_or_id = arg.id

            patterns_lists = self.knowledge.kinds[arg.kind].nodes[indexation_name_or_id]

            for patterns_list in patterns_lists:
                for pattern in patterns_list:
                    #print("AAAAAAAAAAAAAAAAAAAAAAAAAA", pattern.__repr__())
                    sinks_list = pattern.get_sinks()
                    #print(sinks_list.__repr__())
                    #print(self.name)
                    if self.name in sinks_list:
                        print("====================================================================")
                        print("                           VULNERABILITY                            ")
                        print("                               FOUND                                ")
                        print("                                                                    ")
                        print("Vulnerability Name: " + pattern.get_vulnerability_name().__repr__())
                        print("Possible sanitizations: " + pattern.get_sanitization_functions().__repr__())
                        print("====================================================================")

            #print("acabei")
        return self.knowledge


class SanitizationCallNode(FunctionCallNode):
    def __init__(self, kind, name, arguments, patterns_list):
        FunctionCallNode.__init__(self, kind, name, arguments)
        self.patterns_list = patterns_list

    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        for arg in self.arguments:

            indexation_name_or_id = ""
            if hasattr(arg, 'name'):
                indexation_name_or_id = arg.name
            else:
                indexation_name_or_id = arg.id

            new_patterns_lists = []
            patterns_lists = self.knowledge.kinds[arg.kind].nodes[indexation_name_or_id]
            for patterns_list in patterns_lists:

                new_patterns_list = []
                for pattern in patterns_list:
                    sanits_list = pattern.get_sanitization_functions()

                    if self.name not in sanits_list:
                        new_patterns_list.append(pattern)

                new_patterns_lists.append(new_patterns_list)

            self.knowledge.kinds[arg.kind].nodes[indexation_name_or_id] = new_patterns_lists

        return self.knowledge
