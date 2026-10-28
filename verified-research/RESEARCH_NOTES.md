# Independent analysis — verified source excerpt

Data transcription: 24 monthly global GISTEMP anomalies Oct 2024–Sep 2026 as published in the Green Decades tracker citing NASA GISS/GISTEMP. This is a **small excerpt** and NOT a complete NASA climate record. Source: https://www.greendecades.org/tracker/temperature-anomaly-global ; original: https://data.giss.nasa.gov/gistemp/ (accessed 2026-10-27).

## Earth climate
- 2025 mean of 12 anomalies: 1.185 °C relative to 1951–1980.
- Jan–Sep 2026 mean: 1.234 °C (NOT directly comparable to a full calendar-year mean).
- Linear slope within the short 24-month excerpt: -0.011 °C/year. **Not a long-term climate trend.**

## ML demonstration
- Ridge regression with three previous months as features, time-ordered train/test split; six-month holdout Apr–Sep 2026.
- Ridge MAE 0.094 °C; previous-month baseline MAE 0.083 °C. Small sample, not robust forecasting evidence.

## Mars reference comparison
- NASA planetary means: Mars -65 °C; Earth +15 °C (80 °C difference). Source https://science.nasa.gov/resource/solar-system-temperatures/
- NASA Mars pressure range 6–10 mbar; Earth sea-level ~1 bar. Source https://science.nasa.gov/resource/wind-flow/
- Mars pressure about 0.59%–0.99% of Earth reference (1013.25 mbar).
- This is an **original comparison of published reference values**, not new rover time-series analysis, and NOT a validated habitability index.

## Chicago satellite research
- The Chicago vegetation project is a fully specified reproducible workflow, but **no original imagery or tract-level observations were available for execution**. No measured NDVI changes are claimed. ChiVes provides tract-level NDVI and canopy fields: https://chichives.com/data . The site is not falsely described as a completed empirical study.

No invented NASA measurements. Charts and code generated locally. The original Mars essay is unaltered.
