"""Reproducible descriptive analysis of published NOAA historic trend summary values."""
import csv
from pathlib import Path
path=Path(__file__).with_name('noaa_city_trends.csv')
with path.open(newline='') as f: data=list(csv.DictReader(f))
for r in sorted(data,key=lambda x:float(x['historic_relative_sea_level_mm_per_year']),reverse=True):
 print(f"{r['city']}: {float(r['historic_relative_sea_level_mm_per_year']):.2f} mm per year")
print('Note: These are historic linear summaries, not projections of city submergence.')
