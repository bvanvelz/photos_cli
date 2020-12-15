import hashlib
import os


def import_photos(dir, photos=[]):
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

        self.md5 = self.set_md5()

    def set_md5(self):
        # TODO: fix
        # return hashlib.md5(open(self.path))
        pass

    @staticmethod
    def is_photo(path):  # TODO
        return True