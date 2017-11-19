from ast.nodes import ChildfulNode
from ast.taintknowledge import KindKnowledge
import pprint

def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


class CycleNode(ChildfulNode):
    def __init__(self, kind, children, test):
        ChildfulNode.__init__(self, kind, children)
        self.test = test  # Its an ExpressionNode

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
               'test: ' + pretty_format(self.test) + ',' \
               'children: ' + pretty_format(self.children) + '>'

    # FIXME assuming when a cycle is ran the test runs first
    # FIXME assuming cycles are ran once after the test
    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # The test must be handled first
        self.knowledge = self.test.is_tainted(self.knowledge)

        # The children are handled by the ChildfulNode
        self.knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        return self.knowledge


class WhileNode(CycleNode):
    def __init__(self, kind, children, test):
        CycleNode.__init__(self, kind, children, test)

    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # The While is just like a cycle therefore we have the same assumptions
        # FIXME check the CycleNode assumptions because they're the same here
        self.knowledge = CycleNode.is_tainted(self, self.knowledge)

        return self.knowledge


class DoWhileNode(CycleNode):
    def __init__(self, kind, children, test):
        CycleNode.__init__(self, kind, children, test)

    # FIXME assuming when a cycle is ran the test runs before
    # FIXME assuming cycles are ran once before the test
    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # The children are handled by the ChildfulNode
        self.knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        # The test must be handled last
        self.knowledge = self.test.is_tainted(self.knowledge)

        return self.knowledge


class ForNode(CycleNode):
    def __init__(self, kind, children, test, init, increment):
        CycleNode.__init__(self, kind, children, test)
        self.init = init  # Its a list of ExpressionNodes
        self.increment = increment  # Its a list of ExpressionNodes

    def __repr__(self):
        return '<kind:' + self.kind + ',' \
                'init: ' + pretty_format(self.init) + ',' \
                'test: ' + pretty_format(self.test) + ',' \
                'increment: ' + pretty_format(self.increment) + ',' + \
                'children: ' + pretty_format(self.children) + '>'

    # FIXME assuming the order of execution for a for cycle is:
    # FIXME init -> test -> children -> increment
    # FIXME and everything is only ran once
    # FIXME also assuming the test is a list (only for the ForNode)
    def is_tainted(self, knowledge):

        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # Handle the init block (its a list)
        for init_instruction in self.init:
            self.knowledge = init_instruction.is_tainted(self.knowledge)

        # Handle the test instructions (check assumptions, its a list)
        for test_instruction in self.test:
            self.knowledge = test_instruction.is_tainted(self.knowledge)

        # Handle the body instructions (like a ChildfulNode)
        self.knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        # Handle the increment instructions (check assumptions, its a list)
        for increment_instructions in self.increment:
            self.knowledge = increment_instructions.is_tainted(self.knowledge)

        return self.knowledge

