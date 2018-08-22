import sys
import os
import gzip
import zlib
import binascii

import map_parser
import constants


class MapFileError(Exception): pass


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

    def prepare_maps_dict(self):
        self.source_walker()
        for file in self.source_dir_files:
            f = MapFile(file)
            try:
                f.unpack()
                f.check()
            except MapFileError:
                pass
            else:
                self.maps_dict[file] = f.file_object

    def prepare_maps_data(self):
        for key in self.maps_dict:
            file_data = map_parser.MapObject(self.maps_dict[key])
            print()
            print(key)
            file_data.parse_map()
            self.maps_dict[key].close()
            self.maps_dict[key] = file_data


class MapFile:
    """Unpack map file and return its contents. Write map file to another place if necessary."""
    def __init__(self, filename):
        self.filename = filename
        self.file_object = None

    def check(self):
        """Check if file is a valid HOMM3 map file. If not, raises IncorrectMapFileError."""
        if not self.file_object:
            raise MapFileError("File not opened yet.")
        else:
            map_type = self.file_object.read(4)
            if map_type not in map(binascii.unhexlify, constants.MAP_TYPE):
                raise MapFileError("Incorrect Heroes 3 map type.")

    def unpack(self):
        f = gzip.open(self.filename, "r")
        try:
            f.peek(1)
        except OSError as err:
            raise MapFileError(err)
        else:
            self.file_object = f
