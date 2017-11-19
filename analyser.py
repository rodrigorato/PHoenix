#!/usr/bin/env python3

from sys import argv
from inputparser import get_input
from vulnpatterns.patternmanager import PatternManager
from jsonhandler import from_json_to_py
import pprint

from ast.nodemanager import NodeManager
from ast import *


def pretty(obj):
    pprint.PrettyPrinter(indent=4).pprint(obj)


def main(args):

    # Get the patterns to check for
    pattern_manager = PatternManager()
    patterns = pattern_manager.get_patterns()

    # Get the program element from the input file
    program = from_json_to_py(get_input(args))

    program_node = NodeManager.build_node_from_json(program)

    program_repr = program_node.__repr__()
    print("YARRR OUR PROGRAM BE:", program_repr)
    print("\n\n")
    print("AND ITS ANALYSIS BE:", program_node.do_static_analysis())


if __name__ == '__main__':
    main(argv[1:])
