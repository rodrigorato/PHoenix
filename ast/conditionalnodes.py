from ast.nodes import ChildfulNode
from ast.taintknowledge import KindKnowledge
import pprint


def pretty_format(obj):
    return pprint.PrettyPrinter(indent=4).pformat(obj)


class IfThenElseNode(ChildfulNode):
    def __init__(self, kind, test, body, alternate=None):
        ChildfulNode.__init__(self, kind, body)
        self.test = test  # An expression
        self.body = body  # A list of Nodes
        self.alternate = alternate  # A IfThenElse node, an ElseNode or None

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', children:' + pretty_format(self.children) + ',' \
               + (pretty_format(self.alternate) if self.alternate else '') + '>'

    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # Update our knowledge with the test, its mandatory
        self.knowledge = self.test.is_tainted(self.knowledge)

        # Branch into 2 possible cases
        # The If body and The Else body
        knowledge_if_body, knowledge_else_body = self.knowledge, self.knowledge
        for child in self.body:
            knowledge_if_body = child.is_tainted(self.knowledge)

        if self.alternate:
            knowledge_else_body = self.alternate.is_tainted(self.knowledge)

        self.knowledge = KindKnowledge.union(knowledge_if_body, knowledge_else_body)

        return self.knowledge


class ElseNode(ChildfulNode):
    def __init__(self, kind, children):
        ChildfulNode.__init__(self, kind, children)

    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # The children are handled by the ChildfulNode
        self.knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        return self.knowledge


# A SwitchNode's child are its CaseNodes
class SwitchNode(ChildfulNode):
    def __init__(self, kind, test, body):
        ChildfulNode.__init__(self, kind, body)
        self.test = test

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', test: ' + pretty_format(self.test) + ',' \
               'body: ' + pretty_format(self.children) + '>'

    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # Update our knowledge with the test, its mandatory
        self.knowledge = self.test.is_tainted(self.knowledge)

        # The children are handled by the ChildfulNode
        self.knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        return self.knowledge


class CaseNode(ChildfulNode):
    def __init__(self, kind, test, body):
        ChildfulNode.__init__(self, kind, body)
        self.test = test

    def __repr__(self):
        return '<kind:' + self.kind + ', id:' + str(self.id) + ', test: ' + pretty_format(self.test) + ',' \
               'body: ' + pretty_format(self.children) + '>'

    def is_tainted(self, knowledge):
        self.knowledge = KindKnowledge.union(self.knowledge, knowledge)

        # Update our knowledge with the test, its mandatory
        # we're assuming the case's test is only constants
        self.knowledge = self.test.is_tainted(self.knowledge)

        # The children are handled by the ChildfulNode
        self.knowledge = ChildfulNode.is_tainted(self, self.knowledge)

        return self.knowledge
