import hashlib
import os
from PIL import Image, ExifTags

def import_photos(dir, photos=[]):
    if not os.path.isdir(dir):
        raise Exception("Invalid directory '{}'".format(dir))

    files = os.listdir(dir)

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

        self.md5 = None
        self.metadata = None

    def __str__(self):
        return(str(self.__dict__))

    def set_md5(self):
        # TODO: fix
        self.md5 = hashlib.md5(open(self.path,'rb').read()).hexdigest()
        return self.md5

    def set_metadata(self):
        img = Image.open(self.path)
        self.metadata = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
        return self.metadata

    @staticmethod
    def is_photo(path):  # TODO
        return True