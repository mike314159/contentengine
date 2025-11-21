

import time

class CodeTimer:

    def __init__(self, name):
        self.name = name
        self.start_time = time.time()

    def elapsed(self):
        return time.time() - self.start_time

    def print_elapsed(self):
        print("%s elapsed time: %0.2f" % (self.name, self.elapsed()))