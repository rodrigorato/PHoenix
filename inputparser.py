from argparse import ArgumentParser
import os


def validate_input(file_name):
    # TODO
    return file_name


def is_valid_file(parser, file_path):
    input_dir_path = './input/'
    file_path = validate_input(file_path)
    if os.path.isfile(file_path) in os.scandir(input_dir_path):
        parser.error("File {} does not exist.".format(file_path))
    else:
        return input_dir_path + file_path


def get_input(argv):
    parser = ArgumentParser(description='Analyses PHP code slices for vulnerabilities.')
    parser.add_argument(dest="filename",
                        help="input file name with json PHP code",
                        metavar="FILE",
                        type=lambda x: is_valid_file(parser, x))
    # add more options, if needed
    args = parser.parse_args(argv)
    return args.filename
