"""Explore and validate the daylight data. Not part of the app. Run with:  python analysis/explore.py

Fetches all cities through api.py, checks the API against an astronomical formula
(scikit-learn metrics), prints the key numbers and saves three figures to docs/figures/.
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save figures to files, no window
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from sklearn.metrics import mean_absolute_error, r2_score

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from api import get_year_of_daylight  # noqa: E402
from cities import CITIES  # noqa: E402

YEAR = 2026
FIGURES = ROOT / "docs" / "figures"


def formula_hours(lat, dates):
    """Day length from the sunrise equation (NOAA solar declination; -0.833° for refraction + sun radius)."""
    g = 2 * np.pi / 365 * (dates.dt.dayofyear - 1)
    decl = (0.006918 - 0.399912 * np.cos(g) + 0.070257 * np.sin(g) - 0.006758 * np.cos(2 * g)
            + 0.000907 * np.sin(2 * g) - 0.002697 * np.cos(3 * g) + 0.00148 * np.sin(3 * g))
    phi = np.radians(lat)
    cos_h = (np.sin(np.radians(-0.833)) - np.sin(phi) * np.sin(decl)) / (np.cos(phi) * np.cos(decl))
    return 2 * np.degrees(np.arccos(np.clip(cos_h, -1, 1))) / 15  # clip = polar night (0 h) / midnight sun (24 h)


data = pd.concat(
    [get_year_of_daylight(city, YEAR).assign(city=city, lat=lat) for city, (lat, _) in CITIES.items()],
    ignore_index=True,
)
data["formula"] = formula_hours(data["lat"], data["date"])

# 1. Can we trust the API?
mae = mean_absolute_error(data["hours"], data["formula"]) * 60
r2 = r2_score(data["hours"], data["formula"])
print(f"API vs astronomical formula ({len(data):,} city-days): MAE {mae:.1f} min, R² {r2:.4f}\n")

# 2. Shortest day, longest day and yearly average per city
print(data.groupby("city", sort=False)["hours"].agg(shortest="min", longest="max", yearly_average="mean").round(2), "\n")

# 3. The story numbers: every city compared with Aalborg on 21 December and over the whole year
wide = data.pivot(index="date", columns="city", values="hours")
gap = wide.rsub(wide["Aalborg, Denmark"], axis=0)  # Aalborg minus each city, per day
print("Aalborg minus each city: gap on 21 Dec and summed over the year (hours)")
print(pd.DataFrame({"21 Dec": gap.loc[f"{YEAR}-12-21"], "whole year": gap.sum()}).round(2))

# Figures
FIGURES.mkdir(parents=True, exist_ok=True)
sns.set_theme(style="whitegrid")
north_south = LinearSegmentedColormap.from_list("", ["#e34948", "#a3a19b", "#2a78d6"])  # south, equator, north

ax = sns.lineplot(data=data, x="date", y="hours", hue="lat", palette=north_south, hue_norm=(-70, 70), linewidth=2, errorbar=None)
ax.set(title=f"Daylight per day, {YEAR}: every city gets ~12 h at the equinoxes", xlabel="", ylabel="Hours of daylight", ylim=(0, 24))
ax.legend(title="Latitude", loc="upper left", bbox_to_anchor=(1, 1))
plt.savefig(FIGURES / "fig1_all_cities.png", dpi=150, bbox_inches="tight")
plt.close()

monthly = data.pivot_table(index="city", columns=data["date"].dt.month, values="hours", sort=False)
monthly.columns = [pd.Timestamp(YEAR, m, 1).strftime("%b") for m in monthly.columns]
plt.figure(figsize=(10, 5))
ax = sns.heatmap(monthly, cmap="Blues", vmin=0, vmax=24, annot=True, fmt=".1f", cbar_kws={"label": "Hours"})
ax.set(title="Average daylight per day by month (north → south)", ylabel="")
plt.savefig(FIGURES / "fig2_monthly_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()

plt.figure(figsize=(6, 6))
ax = sns.scatterplot(data=data, x="formula", y="hours", s=8, linewidth=0, alpha=0.5)
ax.plot([0, 24], [0, 24], color="gray", linewidth=1)
ax.set(title=f"API vs astronomy: MAE {mae:.1f} min, R² {r2:.4f}", xlabel="Formula (h)", ylabel="Sunrise-Sunset API (h)")
plt.savefig(FIGURES / "fig3_api_vs_formula.png", dpi=150, bbox_inches="tight")
plt.close()
print(f"\nFigures saved to {FIGURES}")
