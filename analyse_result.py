
import json
import statistics

with open("large_area_result.json", "r") as file:
    response = json.load(file)

result = response["data"]["result"]
features = result["map_data"]["features"]
reported = result["stats_data"]["temperature_stats"]

tile_ids = []
temperatures = []
valid_geometries = 0
invalid_geometries = 0

for feature in features:
    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    tile_ids.append(properties.get("tile_id"))

    temperature = properties.get("average_temperature")
    if temperature is not None:
        temperatures.append(temperature)

    coordinates = geometry.get("coordinates", [])

    if (
        geometry.get("type") == "Polygon"
        and coordinates
        and all(len(ring) >= 4 for ring in coordinates)
    ):
        valid_geometries += 1
    else:
        invalid_geometries += 1

print("\n--- STRUCTURAL VALIDATION ---")
print("Total tiles:", len(features))
print("Unique tile IDs:", len(set(tile_ids)))
print("Valid polygon geometries:", valid_geometries)
print("Invalid geometries:", invalid_geometries)
print("Tiles with temperatures:", len(temperatures))

if temperatures:
    calculated = {
        "minimum": min(temperatures),
        "maximum": max(temperatures),
        "mean": statistics.mean(temperatures),
        "standard_deviation": statistics.pstdev(temperatures)
    }

    print("\n--- CALCULATED STATISTICS ---")
    for key, value in calculated.items():
        print(f"{key}: {value:.8f}")

    print("\n--- API REPORTED STATISTICS ---")
    for key, value in reported.items():
        print(f"{key}: {value}")

    print("\n--- DIFFERENCE ---")
    for key, value in calculated.items():
        difference = abs(value - reported[key])
        print(f"{key}: {difference:.10f}")

print("\n--- TILE ID VALIDATION ---")
print("All tile IDs unique:", len(tile_ids) == len(set(tile_ids)))
