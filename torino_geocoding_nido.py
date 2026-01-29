# -*- coding: utf-8 -*-
"""
Created on Thu Jan 29 08:21:11 2026

@author: Nico Antonio (Antonio Augusto Santos)
"""

import os
import googlemaps
import geopandas as gpd
from config import API_KEY, path_gpkg
from shapely.geometry import Point

# Initial setup
API_KEY = API_KEY
gmaps = googlemaps.Client(key=API_KEY)
data_list = []

# Parameters for query
query = "Asilo Nido Torino"

# Search 
places_result = gmaps.places(query=query)

for place in places_result['results']:
    place_id = place.get('place_id')
    
    details = gmaps.place(place_id=place_id, fields=[
              'website', 'formatted_phone_number']).get('result', {})
    
    lat = place['geometry']['location']['lat']
    lng = place['geometry']['location']['lng']
    
    data_list.append({
        'name': place.get('name'),
        'address': place.get('formatted_address'),
        'website': details.get('website'),
        'phone': details.get('formatted_phone_number'),
        'rating_note': place.get('rating', 0),
        'num_reviews': place.get('user_ratings_total', 0),
        'city': "Torino",
        'geometry': Point(lng, lat)
    })
    
#defining gdf    
gdf = gpd.GeoDataFrame(data_list, crs="EPSG:4326")    
# To add the data to a GeoPackage:
gpkg_file = "torino_locations.gpkg"
gpkg = os.path.join(path_gpkg,gpkg_file)
gdf.to_file(
    gpkg, 
    layer='asili_nido', 
    driver="GPKG", 
    mode='w'
    )



