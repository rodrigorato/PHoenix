class Node():
    def __init__(self):
        self.kind = None    # This node's kind
        self.children = []  # This node's sub-nodes
        self.name = ""      # This node's name


class ProgramNode(Node):
    def __init__(self, param):
        self.param = param