import osmnx as ox
from config import path_gpkg
import os


output_net = os.path.join(path_gpkg, "nature.gpkg")

# bbox: (west, south, east, north) — copre Torino e Pinerolo insieme,
# non tutto il Piemonte
bbox = (7.25, 44.80, 7.75, 45.15)

water_tags = {
    "natural": "water",
    "waterway": True,
}
vegetation_tags = {
    "natural": "wood",
    "landuse": ["forest", "meadow", "grass"],
    "leisure": "park",
}


water = ox.features.features_from_bbox(bbox=bbox, tags=water_tags)
vegetation = ox.features.features_from_bbox(bbox=bbox, tags=vegetation_tags)

water = water.to_crs("EPSG:32632")
vegetation = vegetation.to_crs("EPSG:32632")

water.to_file(output_net, layer="water", driver="GPKG")
vegetation.to_file(output_net, layer="vegetation", driver="GPKG")