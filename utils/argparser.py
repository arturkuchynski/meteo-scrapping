from pathlib import Path
from .argtypes import FileType
import argparse
import sys


def parse_file(pattern):
    """
    Parse file path if corresponding argument was given
    :param pattern: custom file type keyword for argument parser
    :return: file path if file exists else NoneType
    """
    ap = argparse.ArgumentParser()

    ap.add_argument("-p", "--path", required=False, type=FileType(pattern),
                    help="path to .xlsx file where the weather data will be stored")
    args = vars(ap.parse_args())

    file = Path(args["path"]).absolute() if args["path"] else None

    if file and not file.exists():
        print('File not found.\nPlease check if the file path was set correctly.')
        sys.exit(1)

    return file
