# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 2026

@author: Nico Antonio (Antonio Augusto Santos)
"""

import geopandas as gpd
import os
from config import path_gpkg 

# 1. Loading File that were downloaded from ISTAT
# The names of the files correspond to the original from the site
# https://www.istat.it/notizia/confini-delle-unita-amministrative-a-fini-statistici-al-1-gennaio-2018-2/
shp_path = os.path.join(path_gpkg, "Com01012025_WGS84.shp")
gdf_communi = gpd.read_file(shp_path)


# 3. Selecting the objects from
# The PRO_COM code values for Torino (1272) and Pinerolo (1191)
# Checking for string or integer
codici_comuni = ['1191', '1272', 1191, 1272]
gdf_final = gdf_communi[gdf_communi['PRO_COM'].isin(codici_comuni)].copy()

# 5. Saving the data to a GeoPackage
output_path = os.path.join(path_gpkg, "boundaries.gpkg")
gdf_final.to_file(output_path, layer='communi', driver="GPKG")

print(f" Sucessly saved in {output_path}")