# Earth Climate Change Analysis

**Question:** How has global mean surface temperature changed since 1880?

**Source:** NASA GISTEMP v4 annual global land-ocean temperature anomaly (1951–1980 reference).

## Run
`pip install -r requirements.txt` then `python analyze_earth.py`.
The script downloads the original NASA CSV on first run, excludes incomplete 2026, and produces a cleaned CSV, plot and findings in `results/`. If offline, manually save NASA's `GLB.Ts+dSST.csv` to `data/NASA_GISTEMP_GLB.csv` and rerun.

**Status:** Reproducible analysis implemented; results are not claimed until real NASA CSV has been processed.
