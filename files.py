import sys
import os
import gzip
import zlib

import parser


class IncorrectMapFileError(Exception): pass


class FilesAggregator:
    """Find maps in directory."""
    def __init__(self, input_path):
        self.path = input_path
        self.maps_dict = []

    def move(self):
        """Move file to new place."""
        pass

    def walker(self):
        """Create a list of directory files."""
        with os.scandir(self.path) as path:
            for element in path:
                if element.is_file():
                    pass

    def makedir(self, path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception:
                sys.exit("Cannot create output directory.")

    def maps_dict_prepare(self):
        files = self.walker()
        for file in files:
            f = MapFile(file)
            f.check()
            file_data = parser.MapObject(f.unpack())
            file_data.parse_map()
            self.maps_dict[file_data.map_name] = file_data.map_contents


class MapFile:
    """Unpack map file and return its contents. Write map file to another place if necessary."""
    def __init__(self, filename):
        self.filename = filename

    def check(self, file):
        """Check if file is a valid HOMM3 map file. If not, raises IncorrectMapFileError."""
        pass

    def unpack(self):
        try:
            f = gzip.open(self.filename, "r")
        except Exception:
            raise IncorrectMapFileError
        else:
            return f
