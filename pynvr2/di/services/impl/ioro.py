from pynvr2.di.services.io import IO
import glob


class IORo(IO):
    def remove(self, path: str):
        print('DELETING {}'.format(path))

    def glob(self, pattern: str):
        return glob.glob(pattern)
