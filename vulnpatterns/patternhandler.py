from .pattern import Pattern


def create_pattern(pattern):
    try:
        return Pattern(pattern[0], 
                       pattern[1].split(','), 
                       pattern[2].split(','), 
                       pattern[3].split(','))
    except ValueError:
        raise ValueError("Pattern Handler-File error: Pattern could not be created.")


def load_patterns():
    patterns_file = "vulnpatterns/patterns.txt"
    patterns = []
    pattern = []

    with open(patterns_file) as file:
        content = file.readlines()

    for line in content:
        if line != "\n":
            pattern += [line.rstrip('\n')]
        if len(pattern) == 4:
            patterns += [create_pattern(pattern)]
            pattern = []

    return patterns
