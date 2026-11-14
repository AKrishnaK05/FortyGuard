import json
import statistics
import math

with open("large_area_result.json", "r", encoding="utf-8") as file:
    response = json.load(file)

result = response["data"]["result"]
features = result["map_data"]["features"]
reported = result["stats_data"]["temperature_stats"]

tile_ids = []
temperatures = []
valid_geometries = 0
invalid_geometries = 0


def valid_polygon_structure(geometry):
    """Check basic GeoJSON Polygon ring structure and coordinate bounds."""
    if geometry.get("type") != "Polygon":
        return False

    rings = geometry.get("coordinates")
    if not isinstance(rings, list) or not rings:
        return False

    for ring in rings:
        if not isinstance(ring, list) or len(ring) < 4:
            return False

        # A linear ring must be closed.
        if ring[0] != ring[-1]:
            return False

        for point in ring:
            if (
                not isinstance(point, (list, tuple))
                or len(point) < 2
            ):
                return False

            longitude, latitude = point[0], point[1]

            if not isinstance(longitude, (int, float)):
                return False
            if not isinstance(latitude, (int, float)):
                return False
            if not math.isfinite(longitude) or not math.isfinite(latitude):
                return False
            if not (-180 <= longitude <= 180):
                return False
            if not (-90 <= latitude <= 90):
                return False

    return True


for feature in features:
    properties = feature.get("properties", {})
    geometry = feature.get("geometry", {})

    tile_ids.append(properties.get("tile_id"))

    temperature = properties.get("average_temperature")
    if isinstance(temperature, (int, float)) and math.isfinite(temperature):
        temperatures.append(temperature)

    if valid_polygon_structure(geometry):
        valid_geometries += 1
    else:
        invalid_geometries += 1

print("\n--- STRUCTURAL VALIDATION ---")
print("Total tiles:", len(features))
print("Unique tile IDs:", len(set(tile_ids)))
print("Valid polygon structures:", valid_geometries)
print("Invalid polygon structures:", invalid_geometries)
print("Tiles with numeric temperatures:", len(temperatures))

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

    print("\n--- ABSOLUTE DIFFERENCE ---")
    for key, value in calculated.items():
        if key in reported:
            difference = abs(value - reported[key])
            print(f"{key}: {difference:.10f}")

print("\n--- TILE ID VALIDATION ---")
print("All tile IDs unique:", len(tile_ids) == len(set(tile_ids)))
print("All tile IDs present:", all(tile_id is not None for tile_id in tile_ids))

# These are structural checks only; they do not prove spatial accuracy
# or validate the physical accuracy of the temperature measurements.
