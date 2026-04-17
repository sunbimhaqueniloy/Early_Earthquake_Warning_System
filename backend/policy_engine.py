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


def build_device_command(risk_result: dict, target: dict) -> dict:
    risk = risk_result["risk_level"]

    command = {
        "packet_type": "device_command",
        "target_id": target["target_id"],
        "mode": "ONLINE_EEW",
        "alarm": False,
        "gas_off": False,
        "main_power_off": False,
        "essential_only": False,
        "lift_stop": False,
        "unlock_exit": False
    }

    if risk == "LOW":
        command["alarm"] = True

    elif risk == "MEDIUM":
        command["alarm"] = True
        command["unlock_exit"] = True

    elif risk == "HIGH":
        command["alarm"] = True
        command["gas_off"] = target["gas_enabled"]
        command["lift_stop"] = target["has_elevator"]
        command["unlock_exit"] = True

    elif risk == "CRITICAL":
        command["alarm"] = True
        command["gas_off"] = target["gas_enabled"]
        command["lift_stop"] = target["has_elevator"]
        command["unlock_exit"] = True

        if target["power_policy"] == "essential_only":
            command["essential_only"] = True
        else:
            command["main_power_off"] = True

    return command


def main():
    risk_result = load_json("data/generated_waveforms/risk_result.json")
    target = get_target_building("configs/building_profiles.json", risk_result["target_id"])

    command = build_device_command(risk_result, target)

    output_file = "data/generated_waveforms/device_command.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(command, f, indent=2)

    print("Device Command:")
    print(json.dumps(command, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()