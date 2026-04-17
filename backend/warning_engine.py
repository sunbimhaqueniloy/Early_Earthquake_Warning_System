import json
import math


VP_KM_S = 6.0
VS_KM_S = 3.5


def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate distance between two lat/lon points in kilometers."""
    r = 6371  # Earth radius in km

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return r * c


def get_target_building(filepath: str, target_id: str) -> dict:
    data = load_json(filepath)
    for target in data["targets"]:
        if target["target_id"] == target_id:
            return target
    raise ValueError(f"Target {target_id} not found")


def calculate_warning(source: dict, target: dict) -> dict:
    distance_km = haversine_km(
        source["origin_lat"],
        source["origin_lon"],
        target["lat"],
        target["lon"]
    )

    p_time = distance_km / VP_KM_S
    s_time = distance_km / VS_KM_S
    warning_time = s_time - p_time

    return {
        "target_id": target["target_id"],
        "distance_km": round(distance_km, 3),
        "p_wave_time_sec": round(p_time, 3),
        "s_wave_time_sec": round(s_time, 3),
        "warning_time_sec": round(warning_time, 3)
    }


def main() -> None:
    source = load_json("data/generated_waveforms/source_estimate.json")
    target = get_target_building("configs/building_profiles.json", "HUB01")

    result = calculate_warning(source, target)

    output_file = "data/generated_waveforms/warning_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Warning Calculation:")
    print(json.dumps(result, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()