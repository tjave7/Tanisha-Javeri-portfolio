# Mars Climate & Atmospheric Data Analysis

**Research focus:** What can measured Martian air temperature and pressure tell us about environmental challenges for future human missions?

**Author:** Tanisha Javeri | BA Environmental Studies, Loyola University Chicago

## Dataset and scientific scope

This project uses NASA InSight Mars Weather Service API observations from Elysium Planitia. NASA warns that sensor data can be missing and that the API returns up to seven available sols, not a complete climatology. This project does **not** invent or interpolate missing values. NASA Curiosity REMS provides a larger archival dataset suitable for future seasonal analysis.

## Run

```bash
python -m pip install -r requirements.txt
python analyze_mars.py
```

The script downloads NASA JSON, preserves the raw response, cleans the available temperature and pressure observations, creates two graphs and writes a descriptive findings report under `results/`. Requires internet access and a functioning NASA endpoint. If the API is unavailable, provide an archived NASA JSON response:

```bash
python analyze_mars.py --input data/nasa_insight_raw.json
```

**Note:** The NASA API has historically been intermittent; the code cannot guarantee it will return observations. No measured results have been generated or claimed in the bundled website because the live data could not be retrieved in this build environment.

## Research connections

The separate essay *In the Future, Can Humans Live on Mars?* discusses water, potential past life, and technologies needed for human settlement. This analysis focuses only on measured temperature and pressure. Temperature and pressure alone cannot demonstrate human habitability or prove the existence of liquid water.

## Sources
- NASA Open APIs: https://api.nasa.gov/
- NASA InSight weather: https://mars.nasa.gov/insight/weather/
- NASA PDS Curiosity REMS archive: https://pds-atmospheres.nmsu.edu/data_and_services/atmospheres_data/MARS/curiosity/rems.html
