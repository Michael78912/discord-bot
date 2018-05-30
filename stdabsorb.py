import sys

class StdAbsorber:
    def __init__(self, file):
        self.file = file
        self.str = ''

    def set_file(self):
        self.old = getattr(sys, self.file)
        exec('sys.' + self.file + ' = self')

    def reset(self):
        exec('sys.' + self.file + ' = self.old')

    def write(self, item):
        self.str += item

    def flush(self):
        pass

    def close(self):
        pass

    def read(self):
        return self.str
    
