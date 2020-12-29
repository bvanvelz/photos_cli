import argparse
import os
from lib.photo import Photo, import_photos
import json


def commandline_argument_parser():
    """The function parses the command line arguments."""
    # Parse Arguments
    commandline_parser = argparse.ArgumentParser(description='A CLI tool to manage photos.')
    commandline_parser.add_argument('dir_path')
    commandline_parser.add_argument('--paths', '-p',
                                    action='store_true',
                                    required=False,
                                    help='find photos in a directory')

    commandline_parser.add_argument('--duplicates', '-d',
                                    required=False,
                                    action='store_true',
                                    help='find duplicate photos')

    commandline_parser.add_argument('--info',
                                    required=False,
                                    action='store_true',
                                    help='get photos basic info')


    commandline_parser.add_argument('--metadata',
                                    required=False,
                                    action='store_true',
                                    help='get photos metadata') 

    # Return Parsed Arguments
    return commandline_parser.parse_args()


def duplicate_photos(photos):
    duplicates = []
    md5s = {}
    for photo in photos:
        photo.set_md5()
        if photo.md5 in md5s:
            duplicates.append((md5s[photo.md5], photo))
            continue
        else:
            md5s[photo.md5] = photo

    return duplicates


def get_duplicates(photos):
    duplicates = []
    for dup in duplicate_photos(photos):
        duplicates.append((str(dup[0]), str(dup[1])))
    return duplicates


def get_paths(photos):
    paths = []
    for photo in photos:
        paths.append(photo.path)

    return paths

def get_metadata(photos):
    metadata = []
    for photo in photos:
        photo.set_metadata()
        metadata.append(str(photo))
    return metadata

def get_info(photos):
    info = []
    for photo in photos:
        info.append(str(photo))
    return info

def main():
    args = commandline_argument_parser()

    photos = import_photos(args.dir_path)

    results = {"count": len(photos)}

    if args.paths:
        results["paths"] = get_paths(photos)

    if args.duplicates:
        results['duplicates'] = get_duplicates(photos)

    if args.metadata:
        results["metadata"] = get_metadata(photos)

    if args.info:
        results["info"] = get_info(photos)

    print(json.dumps(results))


if __name__ == "__main__":
    main()
