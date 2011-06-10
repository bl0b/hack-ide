import os, sys


all_rc = {}

ide_data_path = '.ide_data/'

class rc_file(object):
    path = property(lambda self: ide_data_path+self.name)
    def __init__(self, name, contents=""):
        if name in all_rc:
            raise NameError("file %s has already been defined"%name)
        all_rc[name] = self
        self.name = name
        self.initial_contents = contents
        if not os.path.exists(ide_data_path):
            os.makedirs(ide_data_path)
        if not os.path.exists(self.path):
            self.reset()
    def reset(self):
        open(self.path, 'w').write(self.initial_contents)

