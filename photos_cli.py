import argparse
import os
from lib.photo import Photo, import_photos
import json


def commandline_argument_parser():
    """The function parses the command line arguments."""
    # Parse Arguments
    commandline_parser = argparse.ArgumentParser(description='Manage photos')
    commandline_parser.add_argument('--list',
                                    required=False,
                                    metavar='DIR_PATH',
                                    help='Find photos in a directory')

    commandline_parser.add_argument('--duplicates',
                                    required=False,
                                    metavar='DIR_PATH',
                                    help='Find duplicate photos')

    # Return Parsed Arguments
    return commandline_parser.parse_args()


def get_duplicate_photos(path):
    photos = import_photos(path)
    duplicates = []
    md5s = set()
    for photo in photos:
        photo.set_md5()
        if photo.md5 in md5s:
            duplicates.append(str(photo))
            continue
        else:
            md5s.add(photo.md5)

    return duplicates

def generate_list(path):
    photos = []
    for photo in import_photos(path):
        photos.append(str(photo))

    return photos

def main():
    args = commandline_argument_parser()

    if args.list:
        results = {"list": generate_list(args.list)}
        print(json.dumps(results))
        

    if args.duplicates:
        results = {'duplicates': str(get_duplicate_photos(args.duplicates))}
        print(json.dumps(results))

if __name__ == "__main__":
    main()
