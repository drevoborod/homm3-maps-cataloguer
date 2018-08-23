import files


maps_location = "C:\GOG Games\HoMM 3 Complete\Maps\Test"
#maps_location = "C:\Games\Heroes of Might and Magic III\Maps"
#maps_location = "C:\Windows"

maps_cataloguer = files.FilesAggregator(maps_location)
maps_cataloguer.prepare_maps_dict()
maps_cataloguer.prepare_maps_data()
pass
