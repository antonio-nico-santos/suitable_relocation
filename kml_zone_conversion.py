# -*- coding: utf-8 -*-
"""
Created on Mon Feb  2 16:01:29 2026

@author: Nico Antonio (Antonio Augusto Santos)
"""

import geopandas as gpd
import fiona
import os
from config import path_gpkg

# Allowing KML/KMZ files
fiona.drvsupport.supported_drivers['KML'] = 'rw'

def process_kmz(input_path, layer_name):
    # 1. Loading KMZ and reading the first layer
    gdf = gpd.read_file(input_path, driver='KML')
    
    # 2. Converting CRS to EPSG:32632 (WGS 84 / UTM zone 32N)
    gdf = gdf.to_crs(epsg=32632)
    
    # 3. Cleaning data: removing empty columns (NaN)
    gdf = gdf.dropna(axis=1, how='all')
    
    # Removing KML attributes that were not gonna use
    cols_to_drop = ['Description', 'StyleUrl', 'AltitudeMode']
    gdf = gdf.drop(columns=[c for c in cols_to_drop if c in gdf.columns])
    
    return gdf
#Setting files and paths
kmz_torino = os.path.join(path_gpkg,'torino_zone.kmz')
kmz_pinerolo = os.path.join(path_gpkg,'pinerolo_zone.kmz')

torino_gdf = process_kmz(kmz_torino, 'torino')
pinerolo_gdf = process_kmz(kmz_pinerolo, 'pinerolo')

# 4. Saving in a only gpkg in different layers
gpkg_file = "zone_omi.gpkg"
output_path = os.path.join(path_gpkg,gpkg_file)
torino_gdf.to_file(output_path, layer='torino', driver="GPKG")
pinerolo_gdf.to_file(output_path, layer='pinerolo', driver="GPKG")

print(f"File {gpkg_file} sucessfully created, with the layers 'torino' e 'pinerolo'.")