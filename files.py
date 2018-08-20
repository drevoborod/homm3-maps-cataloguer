import sys
import os
import gzip
import zlib


class FilesOperations:
    """Find maps in directory."""
    def __init__(self, input_path):
        self.path = input_path

    def move(self):
        """Move file to new place."""
        pass

    def walker(self):
        """Create a list of map files."""
        with os.scandir(self.mappath) as path:
            for element in path:
                if element.is_file():
                    pass

    def makedir(self, path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception:
                sys.exit("Cannot create output directory.")


class MapFile:
    """Unpack map file and return its contents. Write map file to another place if necessary."""
    def __init__(self, filename):
        self.filename = filename

    def check(self):
        """Check if file is a valid HOMM3 map file."""
        pass

    def unpack(self):
        pass
