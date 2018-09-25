import binascii

import constants


class MapContentsError(Exception): pass


class MapObject:
    def __init__(self, mapfile):
        """Prepares full information about map file. Accepts file object of unpacked map file."""
        self.mapfile = mapfile
        self.map_name = ""
        self.map_type = ""
        self.map_size = 0
        self.underground_exists: bool = None
        self.map_description = ""
        self.map_difficulty = ""
        self.total_players = 0
        self.ai_players = 0
        self.human_players = 0

    def parse_map(self):
        self.mapfile.rewind()
        # Get map type:
        self.map_type = self.compare_data(4, constants.MAP_TYPE)
        # Determine where to start reading next data:
        hero_exists = self.bytes_to_dec(1)
        if self.map_type == "HotA":
            if hero_exists:
                self.mapfile.read(6)
            else:
                self.mapfile.read(4)
        # Get map size:
        self.map_size = self.bytes_to_dec(4)
        # Does map have a dungeon?
        levels = self.bytes_to_dec(1)
        if levels == 0:
            self.underground_exists = False
        elif levels == 1:
            self.underground_exists = True
        # Get map name:
        length = self.bytes_to_dec(4)
        self.map_name = self.mapfile.read(length).decode("Ansi")
        # Get map description:
        length = self.bytes_to_dec(4)
        self.map_description = self.mapfile.read(length).decode("Ansi")
        # Get map difficulty:
        self.map_difficulty = self.compare_data(1, constants.DIFFICULTY)
        #Get players:
        self.player_attributes()
        # Skip heroes parameters:
        #self.mapfile.read(n)
        # Get victory conditions:
        self.victory_conditions()
        # Get loss conditions:
        self.loss_conditions()
        # Get teams:
        self.teams()

        print(self.map_size)
        print(self.map_name)
        print(self.map_description)
        print("Has dungeon:", self.underground_exists)
        print(self.map_difficulty)

    def player_attributes(self):
        ### Result should be: how many humans and how many computers exist, and also total number of players.
        pass

    def victory_conditions(self):
        pass

    def loss_conditions(self):
        pass

    def teams(self):
        pass

    def compare_data(self, length, template_dict):
        prepared_template = {binascii.unhexlify(key): template_dict[key] for key in template_dict}
        data = self.mapfile.read(length)
        if data not in prepared_template:
            raise MapContentsError(f"Data '{data}' not found in:\n{template_dict}")
        else:
            return prepared_template[data]

    def bytes_to_dec(self, length):
        """Converts bytes to hex, and hex - to decimal integer."""
        data = bytearray(self.mapfile.read(length))
        data.reverse()
        to_hex = binascii.hexlify(data)
        return int(to_hex, 16)
