import binascii

import constants


class MapContentsError(Exception): pass


class MapObject:
    def __init__(self, mapfile):
        """Prepares full information about map file. Accepts file object of unpacked map file."""
        self.mapfile = mapfile
        self.map_name = None
        self.map_type = None
        self.map_size = None
        self.has_dungeon = None
        self.map_description = None

    def parse_map(self):
        self.mapfile.rewind()
        # Get map type:
        self.map_type = self.compare_data(4, constants.MAP_TYPE)
        #### Insert check of 01/00: if 00, read +5, else +6
        #### Also check how it will be for non-HotA maps!

        # Get map size:
        if self.map_type == "HotA":
            self.mapfile.read(7)
        else:
            self.mapfile.read(1)

        ### Refactor to correct usage of all 4 bytes!
        self.map_size = self.compare_data(1, constants.MAP_SIZE)
        self.mapfile.read(3)
        # Does map have a dungeon?
        levels = self.bytes_to_dec(self.mapfile.read(1))
        if levels == 0:
            self.has_dungeon = False
        elif levels == 1:
            self.has_dungeon = True
        # Get map name:
        length = self.bytes_to_dec(self.mapfile.read(4))
        self.map_name = self.mapfile.read(length).decode("Ansi")
        # Get map description:
        length = self.bytes_to_dec(self.mapfile.read(4))
        self.map_description = self.mapfile.read(length).decode("Ansi")

    def compare_data(self, length, template_dict):
        prepared_template = {binascii.unhexlify(key): template_dict[key] for key in template_dict}
        data = self.mapfile.read(length)
        if data not in prepared_template:
            raise MapContentsError(f"Data '{data}' not found in:\n{template_dict}")
        else:
            return prepared_template[data]

    def bytes_to_dec(self, data):
        """Converts bytes to hex, and hex - to decimal integer."""
        data_prepared = bytearray(data)
        data_prepared.reverse()
        to_hex = binascii.hexlify(data_prepared)
        return int(to_hex, 16)
