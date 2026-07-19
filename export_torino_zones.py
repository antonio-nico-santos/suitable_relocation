"""
export_torino_zones.py

Costruisce il GeoJSON reale per la mappa interattiva (InteractiveMap.astro),
partendo dai livelli/raster gia' usati per le mappe coropletiche statiche.

Unita' spaziale scelta: zone OMI (poligoni). E' la stessa scelta di
anonimizzazione decisa nello scaffold iniziale ("aggregare per zona OMI
invece di indirizzo esatto") — qui la applichiamo anche ai dati demografici
ISTAT, che nelle mappe statiche erano invece a livello di sezione di
censimento (grana piu' fine delle zone OMI).

LIMITE METODOLOGICO DA DICHIARARE in technical.astro: aggregando i dati
ISTAT (piu' dettagliati) sul poligono OMI (piu' grossolano), la mappa
interattiva mostra la demografia a una risoluzione spaziale INFERIORE
rispetto alle mappe statiche gia' pubblicate. E' una scelta deliberata per
avere un'unica unita' di zona cliccabile con tutti gli attributi insieme,
non un errore — ma va detta esplicitamente, sulla falsariga degli altri
limiti gia' dichiarati nel case study (rete non direzionata, distanza invece
di tempo per i nidi, ecc.).

NOTA: la distanza dal nido NON e' piu' tra gli attributi di zona qui sotto —
e' stata spostata su un layer di contesto a parte (isolinee, risoluzione
piena, nessuna aggregazione per zona). Vedi export_context_layers.py.

Dipendenze (pip):
    pip install geopandas rasterstats pandas --break-system-packages

Adatta i valori nella sezione CONFIG ai tuoi percorsi/nomi di campo reali.
"""
import math
import geopandas as gpd

# ---------------------------------------------------------------------------
# CONFIG — ADATTA QUESTI VALORI AI TUOI DATI REALI
# ---------------------------------------------------------------------------

# Poligoni zone OMI — diventano la geometria e lo zone_name della mappa.
OMI_ZONES_PATH = "C:\\projects\\suitable_relocation\\outputs\\shps\\omi_zones.shp"
OMI_ZONE_NAME_FIELD = "name"          # nome campo reale nel tuo shapefile OMI
OMI_PRICE_FIELD = "affito"    # campo con il canone stimato 80mq gia' calcolato

# Sezioni di censimento ISTAT (grana piu' fine delle zone OMI)
ISTAT_SECTIONS_PATH = "C:\\projects\\suitable_relocation\\outputs\\shps\\istat_sezioni.shp"
ISTAT_UNDER5_FIELD = "p14"          # conteggio assoluto under-5 per sezione
ISTAT_AGE2545_FIELD = "pop25-45"          # conteggio assoluto 25-45 per sezione
ISTAT_POPTOT_FIELD = "p1"          # popolazione totale per sezione

# Raster QNEAT3 gia' prodotto per la mappa statica del commute
COMMUTE_RASTER_PATH = "C:\\projects\\suitable_relocation\\outputs\\soma_min.tif"   # raster commute pesato, in minuti
RASTER_NODATA = -9999

# Zone finite nella shortlist reale — sostituisci con i nomi/zone veri
SHORTLISTED_ZONE_NAMES = ["Adriano Bernini Rivoli, Aeronautica - Lesna, Aurora, Barca Bertolla, Barriera di Milano, Campidoglio Martinetto, Carlo Emanuele, Castello, Cenisia, Collinare Cavoretto, Collinare Superga, Collinare Villa della Regina, Corona Nord, Crimea, Dante, De Gasperi, Duca d'Aosta, Duchessa Jolanda, Filadelfia Traiano, Galileo Ferraris, Garibaldi, Lucento - Vallette, Madonna di Campagna, Michelotti, Mirafiori Nord, Mirafiori Sud, Nizza Millefonte, Parella, Politecnico, Porta Palazzo Maria Ausiliatrice, Pozzo Strada, Rebaudengo - Regio Parco, Rocca, Roma, San Donato, San Paolo, San Salvario, San Secondo, Santa Rita, Solferino, Spina 3 - Euro Torino, Spina 4 - Docks Dora, Stati Uniti, Valentino, Vanchiglia Borgo Rossini, Vanchiglietta, Vinzaglio"]

OUTPUT_PATH = "C:\\projects\\site\\gis-portfolio\\public\\data\\torino-zones-mock.geojson"

# ---------------------------------------------------------------------------
# 1. Zone OMI: geometria + zone_name + omi_class
# ---------------------------------------------------------------------------
zones = gpd.read_file(OMI_ZONES_PATH)
zones = zones.rename(columns={OMI_ZONE_NAME_FIELD: "zone_name"})
 
 
def classify_omi(price):
    # Stesse soglie gia' pubblicate nella choropleth statica — non ricalcolare.
    if price < 664:
        return "<664"
    elif price < 784:
        return "664-784"
    elif price < 1000:
        return "784-1000"
    else:
        return ">1000"
 
 
zones["omi_class"] = zones[OMI_PRICE_FIELD].apply(classify_omi)
 
# ---------------------------------------------------------------------------
# 2. Demografia ISTAT: aggregazione ponderata per area dalle sezioni alle zone OMI
# ---------------------------------------------------------------------------
sections = gpd.read_file(ISTAT_SECTIONS_PATH).to_crs(zones.crs)
sections["sec_area"] = sections.geometry.area
 
joined = gpd.overlay(sections, zones[["zone_name", "geometry"]], how="intersection")
joined["overlap_area"] = joined.geometry.area
joined["weight"] = joined["overlap_area"] / joined["sec_area"]
 
joined["under5_w"] = joined[ISTAT_UNDER5_FIELD] * joined["weight"]
joined["age2545_w"] = joined[ISTAT_AGE2545_FIELD] * joined["weight"]
joined["poptot_w"] = joined[ISTAT_POPTOT_FIELD] * joined["weight"]
 
agg = (
    joined.groupby("zone_name")
    .agg(under5=("under5_w", "sum"), age2545=("age2545_w", "sum"), poptot=("poptot_w", "sum"))
    .reset_index()
)
agg["under5_pct"] = 100 * agg["under5"] / agg["poptot"]
agg["age2545_pct"] = 100 * agg["age2545"] / agg["poptot"]
 
 
def classify_under5(pct):
    # Guardia esplicita: poptot puo' essere 0 per una zona senza sezioni
    # censuarie sovrapposte (o quasi), producendo NaN in under5_pct — senza
    # questo controllo NaN < soglia e' False in Python, quindi il valore
    # scivolava silenziosamente nel ramo piu' alto (il piu' "notato" su una
    # coropleth, il peggior posto per un errore muto).
    #
    # SOGLIE RICALIBRATE (18/07/2026) sui quartili della distribuzione reale
    # a livello di zona OMI (47 zone, vedi diagnosi allegata):
    #   min 2.03, Q1 3.08, mediana 3.34, Q3 3.61, max 4.86
    # Le soglie precedenti (2.2/6.9/22.2) erano quelle della coropleth statica
    # a livello di sezione censuaria — a quella grana il range e' molto piu'
    # ampio; riusate senza modifica sui dati aggregati per zona, comprimevano
    # 46 zone su 47 in un'unica classe. Nota metodologica da riportare in
    # technical.astro: anche con queste soglie, lo scarto assoluto reale tra
    # classe piu' bassa e piu' alta resta ~2.8 punti percentuali — la mappa
    # ora e' leggibile, ma le differenze fra zone restano modeste in valore
    # assoluto, non vanno lette come grandi differenze demografiche.
    if pct is None or not math.isfinite(pct):
        return None
    if pct < 3.1:
        return "<3.1"
    elif pct < 3.4:
        return "3.1-3.4"
    elif pct < 3.6:
        return "3.4-3.6"
    else:
        return ">3.6"
 
 
def classify_age2545(pct):
    # SOGLIE RICALIBRATE (18/07/2026), stesso motivo di classify_under5.
    # Distribuzione reale a livello di zona OMI: min 15.72, Q1 21.39,
    # mediana 23.36, Q3 25.16, max 29.39.
    if pct is None or not math.isfinite(pct):
        return None
    if pct < 21:
        return "<21"
    elif pct < 23:
        return "21-23"
    elif pct < 25:
        return "23-25"
    else:
        return ">25"
 
 
agg["under5_class"] = agg["under5_pct"].apply(classify_under5)
agg["age2545_class"] = agg["age2545_pct"].apply(classify_age2545)
 
# Teniamo anche under5_pct/age2545_pct (non solo le classi) su `zones` —
# servono per il debug (vedi sotto) e altrimenti esistono solo su `agg`,
# che e' una tabella intermedia scartata a fine script.
zones = zones.merge(
    agg[["zone_name", "under5_pct", "age2545_pct", "under5_class", "age2545_class"]],
    on="zone_name",
    how="left",
)
 
# ---------------------------------------------------------------------------
# 3. Commute: media zonale dal raster QNEAT3, riclassificata con soglie gia' pubblicate
# ---------------------------------------------------------------------------
import rasterio
from rasterstats import zonal_stats
 
# IMPORTANTE: non fidarti di un nodata scritto a mano in CONFIG — leggi
# quello dichiarato nel file raster stesso e usa quello. Se il file dice
# un nodata diverso da RASTER_NODATA, e' quasi certamente la causa dei
# valori -inf / enormi che hai visto: i pixel "nodata" del raster reale
# NON venivano riconosciuti come tali (perche' il valore non combaciava
# con -9999), quindi rasterstats li includeva nella media come se fossero
# dati validi. Molti raster QGIS/GDAL usano come sentinella il minimo
# rappresentabile in float32 (-3.4028235e+38) quando non viene impostato
# un nodata esplicito in fase di export — un valore vicino a quello che hai
# visto per Pozzo Strada (-3.644802e+33) e coerente con un overflow numpy
# quando questi valori enormi vengono sommati per calcolare la media.
with rasterio.open(COMMUTE_RASTER_PATH) as src:
    actual_raster_nodata = src.nodata
    print(f"Nodata dichiarato nel file raster: {actual_raster_nodata}")
    print(f"Nodata configurato in RASTER_NODATA: {RASTER_NODATA}")
    if actual_raster_nodata is not None and actual_raster_nodata != RASTER_NODATA:
        print(
            "ATTENZIONE — non coincidono. Uso il valore dichiarato nel file "
            "(piu' affidabile di un numero scritto a mano in CONFIG). "
            "Aggiorna RASTER_NODATA per la prossima esecuzione."
        )
 
effective_nodata = actual_raster_nodata if actual_raster_nodata is not None else RASTER_NODATA
 
commute_stats = zonal_stats(zones.geometry, COMMUTE_RASTER_PATH, stats="mean", nodata=effective_nodata)
zones["commute_mean_min"] = [s["mean"] for s in commute_stats]
 
 
def classify_commute(m):
    # Seconda linea di difesa, indipendente dal fix del nodata sopra: anche
    # se in futuro effective_nodata sbagliasse di nuovo, un valore non
    # finito o fuori da qualunque range plausibile per un commute in minuti
    # (qui: 0-300) non deve MAI diventare silenziosamente "<200" — deve
    # restare esplicitamente mancante (None), cosi' la verifica nella
    # sezione 5 lo segnala invece di nasconderlo.
    if m is None or not math.isfinite(m):
        return None
    if m < 0 or m > 300:
        return None
    if m < 200:
        return "<200"
    elif m < 210:
        return "200-210"
    elif m < 220:
        return "210-220"
    else:
        return ">220"
 
 
zones["commute_class"] = zones["commute_mean_min"].apply(classify_commute)
 
# ---------------------------------------------------------------------------
# 4. Shortlist — manuale, dal tuo elenco reale delle zone rimaste in gioco
# ---------------------------------------------------------------------------
zones["shortlisted"] = zones["zone_name"].isin(SHORTLISTED_ZONE_NAMES)
 
# ---------------------------------------------------------------------------
# 5. Verifica valori nulli prima di esportare (raster con estensione diversa
#    dalle zone OMI puo' lasciare zone senza dato — meglio scoprirlo qui che
#    con una zona invisibile/grigia sulla mappa pubblicata)
# ---------------------------------------------------------------------------
check_cols = ["omi_class", "under5_class", "age2545_class", "commute_class"]
nulls = zones[zones[check_cols].isnull().any(axis=1)]
if len(nulls) > 0:
    print("ATTENZIONE — zone con almeno un valore mancante (controllare prima di pubblicare):")
    print(nulls[["zone_name"] + check_cols])
 
# ---------------------------------------------------------------------------
# 6. Export — riproiezione a WGS84 (EPSG:4326, obbligatorio per MapLibre),
#    solo le colonne che il componente si aspetta
# ---------------------------------------------------------------------------
FINAL_COLUMNS = [
    "zone_name",
    "omi_class",
    "under5_class",
    "age2545_class",
    "commute_class",
    "shortlisted",
    "geometry",
]
 
final = zones[FINAL_COLUMNS].to_crs(epsg=4326)
final.to_file(OUTPUT_PATH, driver="GeoJSON")
 
print(f"\nScritte {len(final)} zone in {OUTPUT_PATH}")
print(final.drop(columns="geometry"))