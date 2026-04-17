import json


def load_station_config(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_confirmed_event(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def estimate_source(station_config: dict, confirmed_event: dict) -> dict:
    triggered_ids = confirmed_event["triggered_stations"]
    stations = station_config["stations"]

    matched = [s for s in stations if s["id"] in triggered_ids]

    avg_lat = sum(s["lat"] for s in matched) / len(matched)
    avg_lon = sum(s["lon"] for s in matched) / len(matched)

    return {
        "origin_lat": round(avg_lat, 6),
        "origin_lon": round(avg_lon, 6)
    }


def main():
    station_config = load_station_config("configs/station_config.json")
    confirmed_event = load_confirmed_event("data/generated_waveforms/confirmed_event.json")

    source = estimate_source(station_config, confirmed_event)

    output_file = "data/generated_waveforms/source_estimate.json"

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(source, f, indent=2)

    print("Estimated Source:")
    print(json.dumps(source, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()