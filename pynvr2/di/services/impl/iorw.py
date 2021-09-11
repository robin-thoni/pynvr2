from pynvr2.di.services.impl.ioro import IORo
import os


class IORw(IORo):

    def remove(self, path: str):
        os.remove(path)
