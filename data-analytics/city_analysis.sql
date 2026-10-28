-- Historic NOAA tide gauge trends, not flood projections.
SELECT city, station, historic_relative_sea_level_mm_per_year AS rate_mm_per_year
FROM noaa_city_trends
ORDER BY rate_mm_per_year DESC;

SELECT ROUND(AVG(historic_relative_sea_level_mm_per_year), 2) AS unweighted_sample_mean_mm_per_year
FROM noaa_city_trends;

SELECT city, ROUND(historic_relative_sea_level_mm_per_year * 10, 1) AS historic_linear_mm_per_decade
FROM noaa_city_trends;
