"""Original educational scenario model, not measured flood observations."""
import csv
from pathlib import Path
import matplotlib.pyplot as plt
HERE = Path(__file__).resolve().parent
with (HERE / 'assumptions.csv').open(newline='') as f:
    areas = [(row['illustrative_area'], float(row['assumed_ground_elevation_m'])) for row in csv.DictReader(f)]
scenarios = [0, .3, .6, 1, 1.5, 2, 3]
with (HERE / 'scenario_results.csv').open('w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['scenario_rise_m','illustrative_area','assumed_ground_elevation_m','water_above_ground_m','potentially_inundated_boolean'])
    for rise in scenarios:
        for name, elev in areas:
            writer.writerow([rise,name,elev,round(max(0,rise-elev),2),int(rise>elev)])
counts = [sum(rise > elev for _, elev in areas) for rise in scenarios]
plt.figure(figsize=(8,4.5))
plt.step(scenarios,counts,where='post',linewidth=2)
plt.scatter(scenarios,counts)
plt.ylim(-.2,len(areas)+.4)
plt.yticks(range(len(areas)+1))
plt.xlabel('Hypothetical sea-level rise (m)')
plt.ylabel('Illustrative locations below water level')
plt.title('Exposure under assumed elevations (not a real flood map)')
plt.grid(alpha=.2)
plt.tight_layout()
plt.savefig(HERE/'scenario_chart.png',dpi=160)
print('Created scenario_results.csv and scenario_chart.png')
