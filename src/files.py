import sys
import os
import gzip
import binascii

import constants


class MapFileError(Exception): pass
class MapContentsError(Exception): pass


class FilesAggregator:
    """Find maps in directory."""
    def __init__(self, input_path):
        self.path = input_path
        self.maps = {}
        self.broken_maps = []
        #self._prepare()

    def get_files(self):
        """Create a list of files from source directory."""
        files = []
        with os.scandir(self.path) as path:
            for element in path:
                if element.is_file():
                    files.append(element.path)
        return files

    def prepare(self, files=None):
        """Create a list of map files from source directory."""
        if files is None:
            files = self.get_files()
        for path in files:
            try:
                file = MapFile(path)
            except MapFileError:
                pass
            except MapContentsError:
                self.broken_maps.append(path)
            else:
                self.maps[path] = file
                yield file

    @staticmethod
    def _makedir(path):
        if not os.path.exists(path):
            try:
                os.mkdir(path)
            except Exception:
                sys.exit("Cannot create output directory.")

    def move(self):
        """Move file to new place."""
        pass


class MapFile:
    """Unpack map file and return its contents.
    Write map file to another place if necessary."""
    def __init__(self, filename):
        self._filename = filename
        self._mapfile = None
        self.name = None
        self.type = None
        self.size = None
        self.dungeon: bool = None
        self.description = None
        self._difficulty = None
        self._players = None
        self._total_players = None
        self._ai_players = None
        self._human_players = None
        self._offset = 0
        self._parse_main_data()

    def _unpack(self):
        f = gzip.open(self._filename)
        try:
            f.peek(1)
        except OSError as err:
            raise MapFileError(err)
        else:
            self._mapfile = f

    def _read(self, length, offset=None):
        if offset is None:
            offset = self._offset
        self._mapfile.seek(offset)
        return self._mapfile.read(length)

    def _locate_data(self, length, template_dict, offset=None):
        if offset is None:
            offset = self._offset
        prepared_template = {binascii.unhexlify(key): template_dict[key] for key in template_dict}
        data = self._read(length, offset=offset)
        if data not in prepared_template:
            raise MapContentsError(f"Data '{data}' not found in:\n{template_dict}")
        else:
            return prepared_template[data]

    def _bytes_to_dec(self, length, offset=None):
        """Converts bytes to hex, and hex - to decimal integer."""
        if offset is None:
            offset = self._offset
        data = bytearray(self._read(length, offset=offset))
        data.reverse()
        to_hex = binascii.hexlify(data)
        return int(to_hex, 16)

    def _parse_main_data(self):
        self._unpack()
        # Map type:
        self.type = self._locate_data(4, constants.MAP_TYPE)
        # Determine where to start reading next data:
        if self.type == "HotA":
            hero_exists = self._bytes_to_dec(1)
            if hero_exists:
                self._offset = 6
            else:
                self._offset = 4
        # Get map size:
        self._offset += 5
        self.size = self._map_size = self._bytes_to_dec(4)
        # Does map have a dungeon?
        self._offset += 4
        levels = self._bytes_to_dec(1)
        if levels == 0:
            self.dungeon = False
        elif levels == 1:
            self.dungeon = True
        self._offset += 1
        # Get map name:
        length = self._bytes_to_dec(4)
        self._offset += 4
        self.name = self._read(length).decode("cp1251")
        self._offset += length
        # Get map description:
        length = self._bytes_to_dec(4)
        self._offset += 4
        self.description = self._read(length).decode("cp1251")
        self._offset += length

        # # Get map difficulty:
        # self._get_map_difficulty()
        # #Get players:
        # self._get_player_attributes()
        # # Skip heroes parameters:
        # #self.mapfile.read(n)
        # # Get victory conditions:
        # self._get_victory_conditions()
        # # Get loss conditions:
        # self._get_loss_conditions()
        # # Get teams:
        # self._get_teams()

    @property
    def difficulty(self):
        if self._difficulty is None:
            self._difficulty = self._locate_data(1, constants.DIFFICULTY)
        return self._difficulty

    @property
    def players(self):
        ### Works correctly for first player only!
        ### Need to implement determining of actual data length for every player.
        if self._players is None:
            players = dict()
            offset = self._offset + 1
            for player in constants.PLAYERS:
                is_human = self._bytes_to_dec(1, offset=offset + 1)
                is_ai = self._bytes_to_dec(1, offset=offset + 2)
                players[player] = dict()
                players[player]["is_human"] = is_human
                players[player]["is_ai"] = is_ai
                offset += 14
            self._players = players
            self._total_players = len([x for x in players if players[x]["is_human"] or players[x]["is_ai"]])
            self._human_players = len([x for x in players if players[x]["is_human"]])
            self._ai_players = len([x for x in players if players[x]["is_ai"]])
        return {"players": self._players, "total": self._total_players,
                "human": self._human_players, "ai": self._ai_players}

    def _get_victory_conditions(self):
        pass

    def _get_loss_conditions(self):
        pass

    def _get_teams(self):
        pass
