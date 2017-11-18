from sys import exit
from json import load, dump


def from_json_to_py(filename):
    try:
        file = open(filename, 'r')
    except FileNotFoundError:
        exit("Json Handler-File error: File could not be found.")
    else:
        data = load(file)
        file.close()
        return data


def from_py_to_json(data, filename):
    try:
        file = open(filename, 'w')
    except FileNotFoundError:
        exit("Json Handler-File error: File could not be found.")
    else:
        dump(data, file)
        file.close()
