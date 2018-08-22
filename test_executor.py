import files


maps_location = "C:\Games\Heroes of Might and Magic III\Maps"
#maps_location = "C:\Windows"

maps_cataloguer = files.FilesAggregator(maps_location)
maps_cataloguer.prepare_maps_dict()
pass
