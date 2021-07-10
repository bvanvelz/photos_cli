import hashlib
import os
from PIL import Image
from PIL.ExifTags import TAGS
import re

def import_photos(dir, photos=[]):
    if not os.path.isdir(dir) and not os.path.isfile(dir):
        raise Exception("Invalid directory '{}'".format(dir))

    if os.path.isdir(dir):
        files = os.listdir(dir)

    else:
        dir = re.sub('./', '', dir)
        files = [dir]
        dir = './'

    for file in files:
        path = os.path.join(dir, file)
        if os.path.isdir(path):
            import_photos(path, photos)
            continue

        if Photo.is_photo(path):
            photos.append(Photo(path=path))

    return photos


class Photo():

    def __init__(self, path):
        if Photo.is_photo(path):
            self.path = path
        else:
            raise Exception("Not a valid photo: '{}'".format(path))
        self.set_create_time()
        self.set_last_modified_time()
        self.set_dimensions()

        self.md5 = None
        self.metadata = None

    def __str__(self):
        # remove null values
        #return str({k: v for k, v in self.__dict__.items() if v is not None})
        return str(self.path)

    def set_md5(self):
        # TODO: fix
        self.md5 = hashlib.md5(open(self.path, 'rb').read()).hexdigest()
        return self.md5

    def set_metadata(self):
        self.metadata = {}

        image = Image.open(self.path)
        exifdata = image.getexif()

        # read the image data using PIL
        for tag_id in exifdata:
            tag = TAGS.get(tag_id, tag_id)
            data = exifdata.get(tag_id)
            if isinstance(data, bytes):
                try:
                    data = data.decode()  # utf-8
                except UnicodeDecodeError:
                    continue
            self.metadata[tag] = data

        return self.metadata

    def set_create_time(self):
        self.create_time = os.path.getctime(self.path)
        return self.create_time

    def set_last_modified_time(self):
        self.last_modified_time = os.path.getmtime(self.path)
        return self.last_modified_time

    def set_dimensions(self):
        im = Image.open(self.path)
        self.width, self.height = im.size
        return self.width, self.height

    @staticmethod
    def is_photo(path):  # TODO
        try:
            im=Image.open(path)
        except IOError:
            return False

        return True
