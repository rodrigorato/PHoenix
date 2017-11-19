from collections import defaultdict

"""
    This class encapsulates knowledge about nodes and their 
    taintness according to a given set of patterns.
    
    The inner reprentation is as follows:
    {
        node_kind_1: {
                        node_name_1: [tainted_by_pattern1, ..., tainted_by_patternN],
                        ...
                     }
        
        node_kind_2: {
                        node_name_1: [tainted_by_pattern1, ..., tainted_by_patternN],
                        ...
                     }
        
        ...
        node_kind_n: ...
    }
    
"""

# Is an abstraction for the inner dicts
class TaintKnowledge:
    def __init__(self):
        self.__nodes_to_patterns = defaultdict(list)

    def get_patterns_for_node(self, node_name):
        return self.__nodes_to_patterns[node_name]

    def __getitem__(self, item):
        return self.__nodes_to_patterns[item]

    def add_pattern_for_node(self, node_name, pattern):
        if pattern not in self.__nodes_to_patterns[node_name]:
            self.__nodes_to_patterns[node_name].append(pattern)

    def remove_pattern_from_node(self, node_name, sanitization_func_name):
        new_patterns = []

        for pattern in self.__nodes_to_patterns[node_name]:
            if sanitization_func_name not in pattern.get_sanitization_functions():
                new_patterns.append(pattern)

        self.__nodes_to_patterns[node_name] = new_patterns

    def get_names(self):
        return self.__nodes_to_patterns.keys()

    def __repr__(self):
        s = '<TAINT-KNOWLEDGE: '
        #s += [str(key) for key in self.__nodes_to_patterns.keys()].__repr__(
        for key in self.__nodes_to_patterns.keys():
            s += '<' + key + ': '
            s += self.__nodes_to_patterns[key].__repr__() + '>, '
        s += '>'
        return s


# FIXME assuming node_kinds and node_names are strings
# FIXME tainted_by_patternI is a Pattern object
# An abstraction for the outer dict
class KindKnowledge:
    def __init__(self):
        self.__kinds = defaultdict(TaintKnowledge)

    def get_kinds(self):
        return self.__kinds.keys()

    def get_taint_knowledge(self, key):
        return self.__kinds[key]

    def __getitem__(self, item):
        return self.__kinds[item]

    def add_pattern_to_kind_node(self, kind, node_name, pattern):
        self[kind].add_pattern_for_node(node_name, pattern)

    def __repr__(self):
        s = '<KIND-KNOWLEDGE: '
        for kind in self.__kinds:
            s += self.__kinds[kind].__repr__()
        s += '>'
        return s

    def remove_pattern_from_kind_node(self, kind_name, node_name, sanitization_function_name):
        self.__kinds[kind_name].remove_pattern_from_node(self, node_name, sanitization_function_name)
