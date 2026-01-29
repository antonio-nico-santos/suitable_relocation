# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 08:21:11 2026

@author: Nico Antonio (Antonio Augusto Santos)
"""

import time
import os
import googlemaps
import geopandas as gpd
from config import API_KEY, path_gpkg
from shapely.geometry import Point

# Initial setup
API_KEY = API_KEY
gmaps = googlemaps.Client(key=API_KEY)
data_list = []
next_page_token = None

# Parameters for query
query = "Stazione Torino"

# Search 
while True:
    # At first, there is no token.
    if next_page_token:
        # Wait 3 seconds for a new request
        time.sleep(3)
        places_result = gmaps.places(query=query, page_token=next_page_token)
    else:
        places_result = gmaps.places(query=query)


    for place in places_result['results']:
        place_id = place.get('place_id')
          
        lat = place['geometry']['location']['lat']
        lng = place['geometry']['location']['lng']
        
        data_list.append({
            'name': place.get('name'),
            'address': place.get('formatted_address'),
            #converting list to concatenated string
            'class' : ", ".join(place.get('types', [])),
            'city': "Torino",
            'geometry': Point(lng, lat)
        })
        
    #If there is no other token, the loop is closed
    if not next_page_token:
        break
    
#defining gdf    
gdf = gpd.GeoDataFrame(data_list, crs="EPSG:4326")    
# To add the data to a GeoPackage:
gpkg_file = "torino_locations.gpkg"
gpkg = os.path.join(path_gpkg,gpkg_file)
gdf.to_file(
    gpkg, 
    layer='stazione', 
    driver="GPKG", 
    mode='w'
    )



