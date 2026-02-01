# -*- coding: utf-8 -*-
"""
Created on Fri Jan 30 18:34:21 2026

@author: Nico Antonio (Antonio Augusto Santos)
"""

import geopandas as gpd
import pandas as pd
import os
from config import path_istat, path_gpkg

# 1. Loading Files that where downloaded from ISTAT
# The names of the files correspond to the original from the site
# https://www.istat.it/notizia/basi-territoriali-e-variabili-censuarie/
shp_path = os.path.join(path_istat, "R01_21_WGS84.shp")
xlsx_path = os.path.join(path_istat, "R01_indicatori_2021_sezioni.xlsx")

gdf_sezioni = gpd.read_file(shp_path)
df_dati = pd.read_excel(xlsx_path)

# 2. Conversion of the field of the Join to string
gdf_sezioni['SEZ21_ID'] = gdf_sezioni['SEZ21_ID'].astype(str)
df_dati['SEZ21_ID'] = df_dati['SEZ21_ID'].astype(str)

# 3. Join of the data
# The field of the join is the 'SEZ21_ID', every census district got a different ID
# It is composed of the code of the district + PROCOM (code of the commune)
gdf_completo = gdf_sezioni.merge(df_dati, on='SEZ21_ID', how= 'left')

# 4. Selecting the data of the communes of interest
# The PRO_COM code values for Torino (1272) and Pinerolo (1191)
# Checking for string or integer
codici_comuni = ['1191', '1272', 1191, 1272]
gdf_final = gdf_completo[gdf_completo['PRO_COM'].isin(codici_comuni)].copy()

# 5. Saving the data to a GeoPackage
output_path = os.path.join(path_gpkg, "census.gpkg")
gdf_final.to_file(output_path, layer='sezioni_censimento', driver="GPKG", mode='w')

print(f" Sucessly saved in {output_path}")