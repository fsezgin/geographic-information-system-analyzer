import geopandas as gpd
import matplotlib.pyplot as plt
import json
from shapely.geometry import Point, Polygon

# Harbiye poligon koordinatları (OSM'den alabilirsin)
harbiye_coords = [
    (28.987, 41.060),
    (28.995, 41.060),
    (28.995, 41.070),
    (28.987, 41.070),
]  # Örnek bounding box, gerçek poligon OSM’den alınmalı
harbiye_poly = Polygon(harbiye_coords)

# JSON dosyasını oku
with open(r"/data/processed/harbiye_mahalle_all_poi_20251013_155643.json", "r", encoding="utf-8") as f:
    data = json.load(f)["data"]

points = [Point(d["lon"], d["lat"]) for d in data]

# Plot
plt.figure(figsize=(6,6))
x,y = harbiye_poly.exterior.xy
plt.plot(x, y, color="blue", label="Harbiye Poligon")
plt.scatter([p.x for p in points], [p.y for p in points], color="red", s=20, alpha=0.6, label="POI")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.legend()
plt.show()
