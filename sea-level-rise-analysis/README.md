# Sea Level Rise and Coastal Flood Exposure

**Author:** Tanisha Javeri | BA Environmental Studies, Loyola University Chicago

## Research question
How does increasing water level change exposure for hypothetical coastal sites at different elevations?

## Method
This original educational model assigns five **fictional** coastal locations ground elevations of 0.25, 0.75, 1.2, 2.1 and 3.4 meters. For scenarios of 0, 0.3, 0.6, 1, 1.5, 2 and 3 meters, a location is counted as potentially inundated when scenario rise exceeds assumed ground elevation. Water above ground is `max(0, rise - elevation)`. The code produces a CSV and chart.

## Results
At +1.0 m, 2 of 5 hypothetical sites are below the modeled waterline. At +3.0 m, 4 of 5 are below it. These results depend entirely on fictional assumptions, not observations.

## Limitations
Not a real-world flood forecast, geographic map, or projection for Chicago, Paris or any city. No tides, waves, storm surge, subsidence, land topography, flood defenses, drainage, or time horizon. Rising sea level is a real global concern, but this model does not estimate the pace of future change.

## Reproduce
`pip install matplotlib` then `python analyze.py`.

## Background reading
NASA Sea Level Change: https://sealevel.nasa.gov/
NOAA Sea Level Rise Viewer: https://coast.noaa.gov/slr/
