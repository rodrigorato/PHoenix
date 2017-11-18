from ast import *


def is_kind(json, kind_name):
    return json['kind'] == kind_name if 'kind' in json else False


# Build a list with the child nodes of some node
def build_children(children_list):
    children = []
    # TODO check if this works with a null children vector
    for child in children_list:
        # And build their nodes
        children.append(NodeManager.build_node_from_json(child))
    return children


class NodeManager:

    @staticmethod
    def build_node_from_json(node_json):

        # Handles the ProgramNode
        if is_kind(node_json, 'program'):

            # Get it's children (i.e. the whole program)
            children = build_children(node_json['children'])

            return ProgramNode(node_json['kind'],
                               children)

        # Handles the IfThenElseNode
        elif is_kind(node_json, 'if'):

            # Build it's children nodes as a list
            children = build_children(node_json['body']['children'])

            # Check for alternate (i.e. the else)
            alternate_node = None
            if 'alternate' in node_json and node_json['alternate']:
                alternate_node = NodeManager.build_node_from_json(node_json['alternate'])

            return IfThenElseNode(node_json['kind'],
                                  NodeManager.build_node_from_json(node_json['test']),
                                  children,
                                  alternate_node)

        # Handles the SwitchNode
        elif is_kind(node_json, 'switch'):

            # Build it's children nodes as a list
            children = build_children(node_json['body'])

            return SwitchNode(node_json['kind'],
                              NodeManager.build_node_from_json(node_json['test']),
                              children)

        # Handles the CaseNode
        elif is_kind(node_json, 'case'):

            return CaseNode(node_json['kind'],
                            NodeManager.build_node_from_json(node_json['test']),
                            build_children(node_json['body']['children']))

        # Handles the WhileNode
        elif is_kind(node_json, 'while'):

            return WhileNode(node_json['kind'],
                             build_children(node_json['body']['children']),
                             NodeManager.build_node_from_json(node_json['test']))

        # Handles the DoWhileNode
        elif is_kind(node_json, 'do'):

            return DoWhileNode(node_json['kind'],
                               build_children(node_json['body']['children']),
                               NodeManager.build_node_from_json(node_json['test']))

        # Handles the ForNode
        elif is_kind(node_json, 'for'):

            return ForNode(node_json['kind'],
                           build_children(node_json['body']['children']),
                           NodeManager.build_node_from_json(node_json['test']),
                           build_children(node_json['init']),
                           build_children(node_json['increment']))
        


        # ATTENTION - Leave this to catch any node with children that we did not consider
        elif 'body' in node_json and 'children' in node_json['body']:

            children = build_children(node_json['body']['children'])

            s = "childfull node not implement: " + node_json['kind']
            print(s)
            return ChildfulNode(s, children)

        # ATTENTION - Leave this to catch any other node that we did not consider
        else:
            s = "NODE NOT IMPLEMENTED: " + node_json['kind']
            print(s)
            return Node(s)
