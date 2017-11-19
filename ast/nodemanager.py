from ast import *
from vulnpatterns.patternmanager import PatternManager

def is_kind(json, kind_name):
    return json['kind'] == kind_name if 'kind' in json else False

def is_kinds(json, kind_names):
    return json['kind'] in kind_names if 'kind' in json else False


# Build a list with the child nodes of some node
def build_children(children_list):
    children = []
    # TODO check if this works with a null children vector
    for child in children_list:
        # And build their nodes
        children.append(NodeManager.build_node_from_json(child))
    return children

list_of_entry_points = PatternManager().get_unique_patterns_list()

class NodeManager:

    @staticmethod
    def build_node_from_json(node_json):

        # Handles the ProgramNode
        if is_kind(node_json, 'program'):

            # Get it's children (i.e. the whole program)
            children = build_children(node_json['children'])

            return ProgramNode(node_json['kind'],
                               children)

        # FIXME assuming parenthesis is just evaluating the inner part
        elif is_kind(node_json, 'parenthesis'):
            return NodeManager.build_node_from_json(node_json['inner'])

        # TODO FIXME maybe account for arrays one day. no time now.
        elif is_kind(node_json, 'offsetlookup'):
            return NodeManager.build_node_from_json(node_json['what'])

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

        # Handles the AttributionNode
        elif is_kind(node_json, 'assign'):

            return AttributionNode(node_json['kind'],
                                   NodeManager.build_node_from_json(node_json['left']),
                                   NodeManager.build_node_from_json(node_json['right']))

        # Handles the UnaryExpression (with a list of unary expressions)
        # FIXME assuming 'cast' is an unary operation
        elif is_kinds(node_json, ('pre', 'post', 'unary', 'cast')):

            return UnaryExpression(node_json['kind'],
                                   node_json['type'],
                                   NodeManager.build_node_from_json(node_json['what']))

        # Handles the BinaryExpression
        # FIXME assuming all have kind 'bin'
        # FIXME reference: https://github.com/glayzzle/php-parser/blob/master/src/ast/bin.js
        elif is_kind(node_json, 'bin'):

            return BinaryExpression(node_json['kind'],
                                    node_json['type'],
                                    NodeManager.build_node_from_json(node_json['left']),
                                    NodeManager.build_node_from_json(node_json['right']))

        # Handles the TernaryExpression
        elif is_kind(node_json, 'retif'):

            return TernaryExpression(node_json['kind'],
                                     NodeManager.build_node_from_json(node_json['test']),
                                     NodeManager.build_node_from_json(node_json['trueExpr']),
                                     NodeManager.build_node_from_json(node_json['falseExpr']))

        # Handles the VariableNode and the EntryPointNode
        elif is_kind(node_json, 'variable'):

            if ('$' + node_json['name']) in list_of_entry_points:
                return EntryPointNode(node_json['kind'],
                                      node_json['name'])
            else:
                return VariableNode(node_json['kind'],
                                    node_json['name'])

        # Handles FunctionCallNode
        elif is_kind(node_json, 'call'):

            return FunctionCallNode(node_json['kind'],
                                    node_json['what']['name'],
                                    build_children(node_json['arguments']))


        # Handles the ConstantNode
        # FIXME assuming these are the only literal kinds
        elif is_kinds(node_json, ('boolean', 'string', 'number', 'inline', 'magic', 'nowdoc')):

            return ConstantNode(node_json['kind'],
                                node_json['value'])


        # Handles the FunctionDefinitionNode
        elif is_kind(node_json, 'function'):

            return FunctionDefinitionNode(node_json['kind'],
                                          node_json['name'],
                                          build_children(node_json['arguments']),
                                          build_children(node_json['body']['children']))




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
