from argparse import ArgumentParser


def validate_input(file_name):
    # TODO
    return file_name


def get_input(argv):
    parser = ArgumentParser(description='Analyses PHP code slices for vulnerabilities.')
    parser.add_argument(dest="filename",
                        help="input file name with json PHP code",
                        metavar="FILE")
    # add more options, if needed
    args = parser.parse_args(argv)
    return args.filename
