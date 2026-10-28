"""Reproduce the published coral reef heat-stress extent comparison.
This is a secondary analysis of NOAA summary values, not independent satellite processing.
"""
import csv
from pathlib import Path
import matplotlib.pyplot as plt
ROOT = Path(__file__).resolve().parent
with (ROOT / "coral_heat_stress_comparison.csv").open(newline="") as f:
    rows = list(csv.DictReader(f))
values = [float(r["percent_global_reef_area_exposed_to_bleaching_level_heat_stress"]) for r in rows]
change_pp = values[1] - values[0]
print(f"Change in exposed reef area: {change_pp:.1f} percentage points")
print(f"Relative increase in reported exposure: {100 * change_pp / values[0]:.1f}%")
fig, ax = plt.subplots(figsize=(9, 5))
ax.bar(["Third event\n2014–2017", "Fourth event\n2023–2025"], values, color=["#379aab", "#ee9268"])
ax.set_ylabel("Global reef area exposed to bleaching-level heat stress (%)")
ax.set_ylim(0, 100)
for i, v in enumerate(values): ax.text(i, v + 2, f"{v:.1f}%", ha="center", fontsize=12)
ax.set_title("Reported exposure during two global coral bleaching events")
fig.text(0.5, 0.01, "Source: NOAA Coral Reef Watch (2026). Event-wide exposure, not coral mortality.", ha="center", fontsize=9)
fig.tight_layout(rect=[0, .05, 1, 1])
fig.savefig(ROOT / "coral_bleaching_comparison.png", dpi=180)
