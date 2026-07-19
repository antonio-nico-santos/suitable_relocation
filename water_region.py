import osmnx as ox
from config import path_gpkg
import os


output_net = os.path.join(path_gpkg, "water_region.gpkg")

# bbox: (west, south, east, north) — copre Torino e Pinerolo insieme,
# non tutto il Piemonte
bbox = (7.15, 44.75, 7.75, 45.85)

water_tags = {
    "natural": "water",
    "waterway": True,
}


water = ox.features.features_from_bbox(bbox=bbox, tags=water_tags)


water = water.to_crs("EPSG:32632")


water.to_file(output_net, layer="water", driver="GPKG")
