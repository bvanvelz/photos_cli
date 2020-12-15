import argparse
import os
from lib.photo import Photo, import_photos

def commandline_argument_parser():
    """The function parses the command line arguments."""
    # Parse Arguments
    commandline_parser = argparse.ArgumentParser(description='Manage photos')
    commandline_parser.add_argument('--list',
                                    required=False,
                                    metavar='PATH',
                                    help='List all photos')

    commandline_parser.add_argument('--duplicates',
                                    required=False,
                                    metavar='PATH',
                                    help='List all photos')

    # Return Parsed Arguments
    return commandline_parser.parse_args()

def get_duplicate_photos(path):
    photos = import_photos(path)



def generate_list(path):
    if not os.path.isdir(path):
        raise Exception("Invalid directory '{}'".format(path))

    photos = import_photos(path)

    for photo in photos:
        print(photo.path)


def main():
    args = commandline_argument_parser()

    if args.list:
        generate_list(args.list)

    if args.duplicates:
        get_duplicate_photos(args.duplicates)

if __name__ == "__main__":
    main()
