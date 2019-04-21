#!/usr/bin/env python3

from src import files

#maps_location = "C:\GOG Games\HoMM 3 Complete\Maps\Test"
maps_location = "/home/user/test/Maps/"
maps_location = "/home/user1/games/Heroes of Might and Magic III/Maps/"
#maps_location = "C:\Games\Heroes of Might and Magic III\Maps"


maps_cataloguer = files.FilesAggregator(maps_location)

for m in maps_cataloguer.prepare():
    # print("file name:", m)
    # print("name:", maps_cataloguer.maps[m].name)
    # print("description:", maps_cataloguer.maps[m].description)
    # print("type:", maps_cataloguer.maps[m].type)
    # print("size:", maps_cataloguer.maps[m].size)
    # print("has dungeon:", maps_cataloguer.maps[m].dungeon)
    # print("difficulty:", maps_cataloguer.maps[m].difficulty)
    # players_dict = maps_cataloguer.maps[m].players
    # for key in players_dict:
    #     #if key != "players":
    #     print(key, players_dict[key])
    # print()
    pass

for m in maps_cataloguer.broken_maps:
    print()
    print(m)

print(len(maps_cataloguer.maps))
