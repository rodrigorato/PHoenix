#!/usr/bin/env python3

from sys import argv
from inputparser import get_input
from vulnpatterns.patternmanager import PatternManager
from jsonhandler import from_json_to_py


def main(args):

    # Get the patterns to check for
    pattern_manager = PatternManager()
    patterns = pattern_manager.get_patterns()

    # Get the program element from the input file
    program = from_json_to_py(get_input(args))


if __name__ == '__main__':
    main(argv[1:])
