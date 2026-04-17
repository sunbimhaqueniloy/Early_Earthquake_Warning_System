import json


def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def get_target_building(filepath: str, target_id: str) -> dict:
    data = load_json(filepath)
    for target in data["targets"]:
        if target["target_id"] == target_id:
            return target
    raise ValueError(f"Target {target_id} not found")


def determine_risk_level(warning_result: dict, target: dict) -> dict:
    warning_time = warning_result["warning_time_sec"]
    distance_km = warning_result["distance_km"]

    # Basic time-based risk
    if warning_time < 1:
        risk_level = "CRITICAL"
    elif warning_time < 3:
        risk_level = "HIGH"
    elif warning_time < 6:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    # Example building adjustment:
    # apartments with gas and elevators can be treated more carefully
    if target["type"] == "apartment" and target["gas_enabled"] and risk_level == "HIGH":
        risk_level = "CRITICAL"

    return {
        "packet_type": "risk_result",
        "target_id": target["target_id"],
        "distance_km": warning_result["distance_km"],
        "warning_time_sec": warning_result["warning_time_sec"],
        "risk_level": risk_level,
        "building_type": target["type"],
        "city": target["city"]
    }


def main():
    warning_result = load_json("data/generated_waveforms/warning_result.json")
    target = get_target_building("configs/building_profiles.json", "HUB01")

    result = determine_risk_level(warning_result, target)

    output_file = "data/generated_waveforms/risk_result.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print("Risk Result:")
    print(json.dumps(result, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()