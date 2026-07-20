# Torino Relocation Suitability — Data Pipeline

Data collection, cleaning, and spatial analysis pipeline behind the **Torino: Relocation Suitability** case study — a personal GIS project used to evaluate neighborhoods, nurseries, and apartments in a city neither my wife nor I had ever visited, ahead of an international relocation.

Full write-up (narrative + methodology) on the live site:
- [Case study overview](https://antonio-nico-santos.github.io/gis-portfolio/en/case-study-torino/)
- [Technical deep dive](https://antonio-nico-santos.github.io/gis-portfolio/en/case-study-torino/technical/)

This repository holds the scripts and database structure behind that write-up. It is not meant to be run end-to-end by others — API keys, database credentials, and raw candidate-apartment records (contact details, exact addresses) have been intentionally excluded; only code and schema are published here.

## 1. Data sources

| Data | Source | CRS |
|---|---|---|
| Services & POIs (nurseries, markets, pharmacies, gyms, playgrounds) | Google Places API | EPSG:4326 |
| Demographics (age brackets, foreign-resident share) | ISTAT, 2021 census | EPSG:32632 |
| Administrative boundaries | ISTAT, 2025 comune limits | EPSG:32632 |
| Road & pedestrian network | OpenStreetMap, via OSMnx | EPSG:32632 |
| Real estate prices | Agenzia delle Entrate — Osservatorio del Mercato Immobiliare (OMI), 2025 H1 | EPSG:32632 |
| Work locations (3 sites) | Manually digitized points | EPSG:32632 |

## 2. Pipeline

**2.1 Data retrieval**
- Services and POIs queried from Google Places, split into sub-areas to stay under its per-query result cap; nursery availability confirmed by directly emailing 100+ locations.
- ISTAT demographic and boundary data downloaded and reprojected to EPSG:32632.
- Road and pedestrian networks extracted with OSMnx (`drive` and `walk` network types), highway attributes cleaned and assigned a `maxspeed` by road classification.
- OMI real-estate zones downloaded as a shapefile; schema extended manually where the published source didn't cover a needed figure.
- Work-site locations digitized by hand as a small point layer (3 locations).

**2.2 Data cleaning**
- All layers loaded into a single PostgreSQL/PostGIS database (schema `torino`) to clean, relate, and query the data consistently across sources.

**2.3 Data processing**
- Commute isochrones from the three work sites: QNEAT3 (QGIS), Iso-Area as Interpolation from Layer, fastest-path strategy, clipped to the comune boundary and combined into a weighted weekly-commute raster.
- Nursery-proximity isochrones: QNEAT3, Iso-Area as Contours/Polygons from Layer, shortest-path strategy over the pedestrian network, multiple sources (nurseries with confirmed availability).
- Demographic and price classification: quantile and Jenks natural breaks tested in parallel per layer.

Full parameter values (exact QNEAT3 settings, classification thresholds, and declared methodological limits) are documented in the [technical deep dive](https://antonio-nico-santos.github.io/gis-portfolio/en/case-study-torino/technical/), not duplicated here.

## 3. Tools

Python (OSMnx, geopandas), QGIS (QNEAT3 plugin, DB Manager), PostgreSQL/PostGIS.

## 4. Data & privacy note

Raw negotiation data for candidate apartments (agent contacts, exact addresses, personal comments) is not included in this repository or in its history. Only anonymized, aggregated outputs derived from that data are published, on the live site.

## 5. Repository structure

- `*_geocoding_*.py` — Google Places retrieval per service type, per city (Torino, Pinerolo)
- `osm_highways_etl.py`, `osm_walkways_download.py` — road and pedestrian network extraction
- `water_forest_download.py`, `water_region.py` — basemap vegetation/water layers (OSMnx)
- `boundaries_comuni.py`, `census_join.py` — administrative boundaries and ISTAT demographic join
- `export_torino_zones.py`, `export_context_layers.py` — GeoJSON export for the interactive map on the live site
- `kml_zone_conversion.py` — zone geometry format conversion
- `*.sql` — schema migrations and derived-column updates
- `*.qgz` — QGIS project files for the analysis layers
