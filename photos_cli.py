import argparse
import os
from lib.photo import Photo, import_photos
import json


def commandline_argument_parser():
    """The function parses the command line arguments."""
    # Parse Arguments
    commandline_parser = argparse.ArgumentParser(description='A CLI tool to manage photos.')

    supported_actions = ['dedup', 'dedupe', 'deduplicate']
    commandline_parser.add_argument('action',
                                    help="Supported actions: {}".format(
                                        supported_actions))

    commandline_parser.add_argument('dir_path')

    # commandline_parser.add_argument('--paths', '-p',
    #                                 action='store_true',
    #                                 required=False,
    #                                 help='Find photos in a directory')

    commandline_parser.add_argument('--delete', '-d',
                                    required=False,
                                    action='store_true',
                                    help='Delete')

    commandline_parser.add_argument('--info',
                                    required=False,
                                    action='store_true',
                                    help='get photos basic info')

    commandline_parser.add_argument('--metadata',
                                    required=False,
                                    action='store_true',
                                    help='get photos metadata') 

    # Return Parsesd Arguments
    args = commandline_parser.parse_args()

    if args.action not in supported_actions:
        raise Exception(("Action '{}' is not supported. "
                         "Supported actions: {}.").format(
                             args.action, supported_actions))

    return args

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

def delete_duplicates(duplicates):
    for dup in duplicates:
        dup_paths = sorted(get_paths(dup))
        print("dup_paths={}".format(dup_paths))
        delete_paths = dup_paths[1:]
        for path in delete_paths:
            if os.system("rm '{}'".format(path)):
                raise Exception("Failed to delete duplicate '{}'.".format(path))
            else:
                print("Deleted duplicate '{}'.".format(path))
         
def get_paths(photos):
    photos_paths = []
    for photo in photos:
        photos_paths.append(photo.path)
    return photos_paths


def get_duplicates_str(duplicates):
    duplicates_str = []
    for dup in duplicates:
        duplicates_str.append((str(dup[0]), str(dup[1])))
    return duplicates_str


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

    print args

    results = {"count": len(photos)}

    #if args.paths:
    #    results["paths"] = get_paths(photos)

    if args.action.lower() in ['dedup', 'dedupe', 'deduplicate']:
        duplicates = duplicate_photos(photos)
        results['duplicates'] = get_duplicates_str(duplicates)
        if args.delete:
            delete_duplicates(duplicates)

    if args.metadata:
        results["metadata"] = get_metadata(photos)

    if args.info:
        results["info"] = get_info(photos)

    print(json.dumps(results))


if __name__ == "__main__":
    main()
