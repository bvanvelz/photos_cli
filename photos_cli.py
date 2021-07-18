import argparse
import os
from lib.photo import Photo, import_photos
import json
from PIL import Image


class PhotosCLI:

    def __init__(self):
        self.args = None
        self.photos = None
        self.duplicates = None

    def _commandline_argument_parser(self):
        """The function parses the command line arguments."""
        # Parse Arguments
        commandline_parser = argparse.ArgumentParser(description='A CLI tool to manage photos.')

        supported_actions = ['duplicates', 'info', 'metadata', 'resize']
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

        commandline_parser.add_argument('--width', '-w',
                                        required=False,
                                        help='Width')

        commandline_parser.add_argument('--height',
                                        required=False,
                                        help='Height')

        # Return Parsesd Arguments
        args = commandline_parser.parse_args()

        if args.action not in supported_actions:
            raise Exception(("Action '{}' is not supported. "
                             "Supported actions: {}.").format(
                                 args.action, supported_actions))

        self.args = args

    def _get_duplicate_photos(self):
        md5s = {}
        for photo in self.photos:
            photo.set_md5()
            if photo.md5 in md5s:
                md5s[photo.md5].append(photo)
            else:
                md5s[photo.md5] = [photo]

        duplicates = []
        for md5 in md5s:
            if len(md5s[md5]) > 1:
                duplicates.append(md5s[md5])

        self.duplicates = duplicates
        return duplicates

    def _delete_duplicates(self):
        deleted_duplicates = []
        for dups in self.duplicates:
            delete_dups = sorted(dups)[1:]
            delete_dups_paths = self._get_paths(delete_dups)
            for path in delete_dups_paths:
                if os.system("rm '{}'".format(path)):
                    raise Exception("Failed to delete duplicate '{}'.".format(path))
                else:
                    print("Deleted duplicate '{}'.".format(path))
            deleted_duplicates.extend(delete_dups)
        return deleted_duplicates

    @staticmethod             
    def _get_paths(photos):
        photos_paths = []
        for photo in photos:
            photos_paths.append(photo.path)
        return photos_paths

    def _get_duplicates_str(self):
        duplicates_str = []
        for dup in self.duplicates:
            duplicates_str.append(self._get_paths(dup))
        return duplicates_str

    def _get_metadata(self):
        metadata = []
        for photo in self.photos:
            photo.set_metadata()
            metadata.append(str(photo))
        return metadata

    def _get_info(self):
        info = []
        for photo in self.photos:
            info.append(str(photo))
        return info

    def _resize_photos(self):
        if not self.args.width and not self.args.height:
            raise Exception("To resize photos, specify either --width or "
                            "--height or both.")

        for photo in self.photos:
            with Image.open(photo.path) as image:
                if self.args.width and self.args.height:
                    image_new = image.resize((int(self.args.width), int(self.args.height)))
                    image_new.save("thumbs/" + photo.path)

                elif self.args.width and not self.args.height:
                    resize_ratio = float(self.args.width) / float(photo.width)
                    height_new = photo.height * resize_ratio
                    image_new = image.resize((int(self.args.width), int(height_new)))
                    image_new.save("thumbs/" + photo.path)

                elif self.args.height and not self.args.width:
                    resize_ratio = float(self.args.height) / float(photo.height)
                    width_new = photo.width * resize_ratio
                    image_new = image.resize((int(width_new), int(self.args.height)))
                    image_new.save("thumbs/" + photo.path)

    # TODO
    def _generate_thumbnails(self):
        # with Image.open(infile) as im:
        #     im.thumbnail(size)
        #     im.save(file + ".thumbnail", "JPEG")
        pass

    def main(self):
        self._commandline_argument_parser()

        self.photos = import_photos(self.args.dir_path)

        results = {"count": len(self.photos)}

        #if args.paths:
        #    results["paths"] = get_paths(photos)

        if self.args.action.lower() in ['duplicates']:
            self._get_duplicate_photos()
            results['duplicates'] = self._get_duplicates_str()
            if self.args.delete:
                deleted_duplicates = self._delete_duplicates()
                results["duplicates_deleted"] = self._get_paths(deleted_duplicates)

        if self.args.action.lower() in ['resize']:
            self._resize_photos()

        if self.args.action.lower() in ['metadata']:
            results["metadata"] = self._get_metadata()

        if self.args.action.lower() in ['info']:
            results["info"] = self._get_info()

        print(json.dumps(results))


if __name__ == "__main__":
    photos_cli = PhotosCLI()
    photos_cli.main()
