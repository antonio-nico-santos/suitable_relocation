# -*- coding: utf-8 -*-
"""
Created on Thu Feb  5 07:56:09 2026

@author: Nico Antonio (Antonio Augusto Santos)
"""
import osmnx as ox
import geopandas as gpd
import pandas as pd
import numpy as np
from config import path_gpkg

def process_osm_data():
    # 1. Carico ROI e scarico dati
    roi = gpd.read_file(f"{path_gpkg}/highways.gpkg", layer="roi_highways")
    polygon = roi.geometry.union_all() 

    cf = '["highway"~"motorway|trunk|primary|secondary|tertiary|residential"]'
    print("Downloading data from OSM")
    # Download con velocità di default per i buchi
    G = ox.graph_from_polygon(polygon, custom_filter=cf, retain_all=True)
    
    hwy_speeds = {
        "motorway": 130, "trunk": 110, "primary": 90, 
        "secondary": 70, "tertiary": 50, "residential": 30
    }
    G = ox.add_edge_speeds(G, hwy_speeds=hwy_speeds)
    
    # Trasformazione in GeoDataFrame (edges=True mantiene le linee)
    gdf = ox.graph_to_gdfs(G, nodes=False, edges=True)

    # 2. & 3. Pulizia e Unificazione Velocità
    print("Cleaning and adjusting speed values")
    speed_cols = [c for c in gdf.columns if 'speed' in c.lower() and 'type' not in c.lower()]
    
    def to_int(val):
        if isinstance(val, (list, np.ndarray)):
            val = val[0] if len(val) > 0 else 0
        try:
            return int(float(val))
        except:
            return 0

    for col in speed_cols:
        gdf[col] = gdf[col].apply(to_int)

    if 'speed' in gdf.columns:
        speed_cols.append('speed')

    gdf['maxspeed_finale'] = gdf[speed_cols].max(axis=1).fillna(0).astype(int)
    
    # --- PUNTO CRITICO: Mantenere 'geometry' ---
    keep_cols = ['highway', 'lanes', 'surface', 'maxspeed_finale', 'geometry']
    # Filtriamo solo le colonne che esistono davvero, ma geometry DEVE esserci
    print("Cleaning unused columns")
    existing_keep = [c for c in keep_cols if c in gdf.columns]
    gdf = gdf[existing_keep].copy()

    # Reset index per avere un FID pulito e rimuovere l'indice multi-livello di OSMnx
    gdf = gdf.reset_index(drop=True)

    # 4. Conversione CRS
    print("Converting CRS to 32632")
    gdf = gdf.to_crs(epsg=32632)

    # 5. & 6. Salvataggio
    # Pulizia nomi highway (se sono liste)
    print("Saving in GeoPackage")
    gdf['highway'] = gdf['highway'].apply(lambda x: x[0] if isinstance(x, list) else x)
    
    output_path = f"{path_gpkg}/highways.gpkg"
    
    # Merged layer
    gdf.to_file(output_path, layer="all_highways_merged", driver="GPKG")
    
    # Layer separati
    for h_type, group in gdf.groupby('highway'):
        group.to_file(output_path, layer=f"highway_{h_type}", driver="GPKG")

    print(f"File salvato con successo in: {output_path}")

if __name__ == "__main__":
    process_osm_data()