import argparse
import re


class FileType(object):

    patterns = {
        'XLSX': re.compile(r"^.*\.xlsx$"),
    }

    def __init__(self, pattern):
        if pattern not in self.patterns:
            raise KeyError('{} is not a supported file pattern, choose from:'
                           ' {}'.format(pattern, ','.join(self.patterns)))
        self._rules = pattern
        self._pattern = self.patterns[pattern]

    def __call__(self, value):
        if not self._pattern.match(value):
            raise argparse.ArgumentTypeError(
                "'{}' is not a valid file name - does not match {} file".format(value, self._rules))
        return value