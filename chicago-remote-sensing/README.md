# Chicago Satellite Remote Sensing — Landsat NDVI

**Research question:** How did vegetation greenness change across a selected Chicago area between two comparable dates?

**Data:** Real Landsat 8/9 Collection 2 Level-2 Surface Reflectance, USGS EarthExplorer (no fabricated imagery).

1. Download two cloud-free growing-season scenes from the same footprint, with similar seasonal timing, from https://earthexplorer.usgs.gov/ .
2. Extract `_SR_B4.TIF` (red) and `_SR_B5.TIF` (near-infrared) for each date. Apply `QA_PIXEL` cloud, shadow, snow masking in GIS before drawing conclusions; this sample script only handles fill pixels.
3. Ensure all four rasters are aligned to identical CRS, pixel grid, and extent (e.g. clip/reproject in QGIS).
4. `pip install -r requirements.txt`
5. `python analyze_ndvi.py --early-red early_SR_B4.TIF --early-nir early_SR_B5.TIF --late-red late_SR_B4.TIF --late-nir late_SR_B5.TIF`

Outputs include GeoTIFF NDVI maps, a change image, and measured summary statistics.

**Status:** Code complete, observational comparison pending selection/download of suitable imagery and QA masking. No claims of actual Chicago vegetation change have been made.
