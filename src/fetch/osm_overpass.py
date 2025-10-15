import overpy
import json
from pathlib import Path
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import time

def fetch_and_save_harbiye_poi(folder: str):
    """
    Fetch all POI nodes within Harbiye Mahallesi polygon,
    save to JSON with 'tag' field, and visualize.
    """
    api = overpy.Overpass(url="https://lz4.overpass-api.de/api/interpreter")

    query = """
    [out:json][timeout:50];
    area["name"="Harbiye Mahallesi"]["admin_level"="8"]->.a;
    node(area.a);
    out center;
    """

    # Retry mekanizması
    for attempt in range(5):
        try:
            print(f"Fetching all POI in Harbiye Mahallesi... (attempt {attempt+1})")
            result = api.query(query)
            break
        except (overpy.exception.OverpassGatewayTimeout,
                overpy.exception.OverpassTooManyRequests,
                overpy.exception.OverpassUnknownHTTPStatusCode) as e:
            wait_time = 10 * (attempt + 1)
            print(f"Sunucu yoğun veya hata: {e}, {wait_time} saniye bekleyip tekrar deniyorum...")
            time.sleep(wait_time)
    else:
        print("Veri alınamadı.")
        return None

    # POI verilerini kaydet
    data = []
    for node in result.nodes:
        tag_key = next(iter(node.tags), None)
        data.append({
            "id": node.id,
            "name": node.tags.get("name"),
            "tags": node.tags,
            "lat": float(node.lat),
            "lon": float(node.lon),
            "tag": tag_key  # artık json'da 'tag' var
        })

    Path(folder).mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = Path(folder) / f"harbiye_mahalle_all_poi_{timestamp}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"area": "Harbiye Mahallesi", "count": len(data), "data": data},
                  f, ensure_ascii=False, indent=2)

    print(f"Saved {len(data)} POI to {file_path}")

    # --- DataFrame ve analiz ---
    df = pd.json_normalize({"data": data}, record_path=["data"])
    print("\nİlk 5 POI:")
    print(df.head())

    print("\nTag dağılımı:")
    tag_counts = df["tag"].value_counts()
    print(tag_counts)

    # Bar chart
    plt.figure(figsize=(8,5))
    tag_counts.plot(kind="bar", color="skyblue")
    plt.title("Harbiye Mahallesi POI Tag Dağılımı")
    plt.ylabel("Adet")
    plt.xlabel("Tag")
    plt.show()

    # Scatter plot koordinat bazlı
    plt.figure(figsize=(6,6))
    plt.scatter(df["lon"], df["lat"], c="red", alpha=0.6, s=20)
    plt.title("Harbiye Mahallesi POI Noktaları")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.show()

    return df, file_path

if __name__ == "__main__":
    folder = r"C:/Users/lunaf/Desktop/Projects/geographic-information-system-analyzer/data/raw"
    fetch_and_save_harbiye_poi(folder)
