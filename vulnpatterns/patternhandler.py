#from sys import exit
#from os import listdir
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


"""
def load_pattern(fd):
    pattern = []
    for _ in range(4):
        line = fd.readline().rstrip('\n')
        if line:
            pattern.append(line)
        else:
            # TODO throw exception, maybe
            break
    return create_pattern(pattern)


def load_patterns():
    input_dir_path = "./vulnpatterns/patterns/"  # FIXME
    file_ind = "pattern"
    patterns = []
    for filename in listdir(input_dir_path):
        if filename.startswith(file_ind):
            try:
                file = open(input_dir_path + filename, 'r')
            except FileNotFoundError:
                exit("Pattern Handler-File error: File could not be found.")
            else:

                while file:
                    patterns.append(load_pattern(file))
                    if file.readline() not in ['\n', '\r\n']:
                        break  # TODO throw exception, maybe
                file.close()
    return patterns
    """
