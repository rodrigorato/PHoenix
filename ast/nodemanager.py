from ast.nodes import *


def is_kind(json, kind_name):
    return json['kind'] == kind_name


class NodeManager:

    @staticmethod
    def build_node_from_json(node_json):

        if is_kind(node_json, 'program'):

            children = []
            for child in node_json['children']:
                children.append(NodeManager.build_node_from_json(child))

            return ProgramNode(node_json['kind'],
                               children)

        else:
            s = "NODE NOT IMPLEMENTED: " + node_json['kind']
            print(s)
            return Node(s)
