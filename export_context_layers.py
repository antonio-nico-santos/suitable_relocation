"""
export_context_layers.py

Esporta i due layer di contesto (non cliccabili) della mappa interattiva:
fiumi e isolinee di distanza dai nidi. A differenza di export_torino_zones.py,
qui non c'e' nessuna aggregazione per zona OMI — entrambi i layer mantengono
la risoluzione nativa gia' usata nelle mappe statiche.

Dipendenze (pip):
    pip install geopandas osmnx --break-system-packages

Adatta i valori in CONFIG ai tuoi percorsi/nomi di campo reali.
"""

import geopandas as gpd
import osmnx as ox

# ---------------------------------------------------------------------------
# CONFIG — ADATTA QUESTI VALORI AI TUOI DATI REALI
# ---------------------------------------------------------------------------

# Area di interesse per l'estrazione OSMnx — stessa AOI gia' usata per
# l'hero e la mappa di contesto del commute. Puoi passare un bbox
# (nord, sud, est, ovest) o un nome di luogo, secondo quale hai gia' usato.
AOI_PLACE = "Torino, Piemonte, Italia"
  # (north, south, east, west) — esempio, sostituisci col tuo

WATER_TAGS = {"natural": "water", "waterway": True}

RIVERS_LINES_OUTPUT = "C:\\projects\\site\\gis-portfolio\\public\\data\\torino-rivers-lines-mock.geojson"
RIVERS_POLYGONS_OUTPUT = "C:\\projects\\site\\gis-portfolio\\public\\data\\torino-rivers-polygons-mock.geojson"

# Layer vettoriale isolinee QNEAT3 gia' usato per lo Step 4 statico
# ("Iso-Area as Contours from Layer") — NON il PNG renderizzato. Se lo hai
# ancora nel progetto QGIS, esportalo da li' (Save Features As -> GeoJSON,
# EPSG:4326) e salta questa sezione; questo script assume che tu parta da
# uno shapefile/geopackage gia' esportato da QGIS.
NIDO_CONTOURS_SOURCE = "C:\\projects\\suitable_relocation\\outputs\\shps\\nido_isolines.shp"
NIDO_VALUE_FIELD = "cost_level"  # campo con il valore esatto della isolinea (200/400/600/800/1000)
NIDO_CONTOURS_OUTPUT = "C:\\projects\\site\\gis-portfolio\\public\\data\\torino-nido-contours-mock.geojson"

# ---------------------------------------------------------------------------
# 1. Fiumi — stessa estrazione OSMnx gia' usata per l'hero/basemap custom
# ---------------------------------------------------------------------------
water = ox.features_from_place(AOI_PLACE, tags=WATER_TAGS)

rivers_lines = water[water.geometry.type == "LineString"].copy()
rivers_polygons = water[water.geometry.type.isin(["Polygon", "MultiPolygon"])].copy()

# Nessuna proprieta' richiesta dal componente: teniamo solo la geometria
# (piu' eventualmente 'name' se vuoi un domani aggiungere tooltip).
rivers_lines = rivers_lines[["geometry"]].to_crs(epsg=4326)
rivers_polygons = rivers_polygons[["geometry"]].to_crs(epsg=4326)

rivers_lines.to_file(RIVERS_LINES_OUTPUT, driver="GeoJSON")
rivers_polygons.to_file(RIVERS_POLYGONS_OUTPUT, driver="GeoJSON")

print(f"Fiumi: {len(rivers_lines)} linee -> {RIVERS_LINES_OUTPUT}")
print(f"Fiumi: {len(rivers_polygons)} poligoni -> {RIVERS_POLYGONS_OUTPUT}")

# ---------------------------------------------------------------------------
# 2. Isolinee distanza nido — riuso diretto del layer QNEAT3 gia' prodotto,
#    solo riproiezione e pulizia delle colonne
# ---------------------------------------------------------------------------
nido = gpd.read_file(NIDO_CONTOURS_SOURCE)
nido = nido.rename(columns={NIDO_VALUE_FIELD: "value"})

# Verifica che i valori siano esattamente quelli attesi dal componente
expected_values = {200, 400, 600, 800, 1000}
actual_values = set(nido["value"].unique())
if not actual_values.issubset(expected_values):
    print(f"ATTENZIONE — valori isolinea inattesi: {actual_values - expected_values}")
    print("Il componente ha un colore di fallback per valori non riconosciuti,")
    print("ma meglio allineare qui i valori esatti (200/400/600/800/1000).")

nido = nido[["value", "geometry"]].to_crs(epsg=4326)
nido.to_file(NIDO_CONTOURS_OUTPUT, driver="GeoJSON")

print(f"Isolinee nido: {len(nido)} linee -> {NIDO_CONTOURS_OUTPUT}")
