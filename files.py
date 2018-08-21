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
        self.maps_dict = {}
        self.source_dir_files = []

    def move(self):
        """Move file to new place."""
        pass

    def source_walker(self):
        """Create a list of files in source directory."""
        with os.scandir(self.path) as path:
            for element in path:
                if element.is_file():
                    self.source_dir_files.append(element.path)

    def makedir(self, path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception:
                sys.exit("Cannot create output directory.")

    def maps_dict_prepare(self):
        self.source_walker()
        for file in self.source_dir_files:
            f = MapFile(file)
            try:
                f.unpack()
                f.check()
            except IncorrectMapFileError as err:
                pass
                #print(err)
            else:
                self.maps_dict[file] = f.file_object
            # file_data = parser.MapObject(f.unpack())
            # file_data.parse_map()
            # self.maps_dict[file_data.map_name] = file_data.map_contents


class MapFile:
    """Unpack map file and return its contents. Write map file to another place if necessary."""
    def __init__(self, filename):
        self.filename = filename
        self.file_object = None

    def check(self):
        """Check if file is a valid HOMM3 map file. If not, raises IncorrectMapFileError."""
        if not self.file_object:
            raise IncorrectMapFileError("File not opened yet.")
        else:
            pass


    def unpack(self):
        with gzip.open(self.filename, "r") as f:
            try:
                f.peek(1)
            except OSError as err:
                print(err)
                raise IncorrectMapFileError(err)
            else:
                self.file_object = f
