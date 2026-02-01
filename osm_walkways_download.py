# -*- coding: utf-8 -*-
"""
Created on Sun Feb  1  2026

@author: Nico Antonio (Antonio Augusto Santos)
"""

import osmnx as ox
import geopandas as gpd
import os
from config import path_gpkg

# 1. Using comune GeoPackage boundaries as Mask
gpkg_path = os.path.join(path_gpkg, "boundaries.gpkg")
gdf_confini = gpd.read_file(gpkg_path, layer='comuni')

# Covering CRS to 4326
gdf_confini = gdf_confini.to_crs(epsg=4326)

# Setting the output path 
output_net = os.path.join(path_gpkg, "walkways.gpkg")

# 2. Cicle for downloading and saving the data
for index, row in gdf_confini.iterrows():
    try:
        nome_comune = str(row['COMUNE'])
        print(f"--- Preparing: {nome_comune} ---")
        
        #Reparing geometry
        geom_pulita = row['geometry'].buffer(0)
        
        if geom_pulita.is_empty:
            print(f"{nome_comune}: empy geometry.")
            continue

        # Scaricamento della rete pedonale
        print(f"Downloading walkways of {nome_comune} from OSM...")
        G = ox.graph_from_polygon(geom_pulita, network_type='walk')
        
        # Conversio to GeoDataFrame 
        _, edges = ox.graph_to_gdfs(G)
        
        # Conversio to a metric CRS
        edges_metric = edges.to_crs(epsg=32632)
        
        # Layer name (lowcase and with underscore)
        layer_name = f"vie_{nome_comune.lower().replace(' ', '_')}"
        
        # Saving in he GeoPackage
        print(f"Saved the layer: {layer_name}")
        edges_metric[['name', 'highway', 'geometry']].to_file(
            output_net, 
            layer=layer_name, 
            driver="GPKG",
            mode='w'
        )
        
    except Exception as e:
        print(f"Error during execution of {row.get('COMUNE', 'Sconosciuto')}: {e}")

print(f"\nSuccess! File is ready in: {output_net}")