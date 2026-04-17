import json


def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_fallback_command(local_trigger: dict) -> dict | None:
    """
    Create an offline emergency command if local shaking is detected strongly enough.
    """
    if not local_trigger["local_trigger"]:
        return None

    if local_trigger["confidence"] < 0.7:
        return None

    return {
        "packet_type": "device_command",
        "target_id": local_trigger["hub_id"],
        "mode": "OFFLINE_FALLBACK",
        "alarm": True,
        "gas_off": True,
        "main_power_off": False,
        "essential_only": True,
        "lift_stop": True,
        "unlock_exit": True
    }


def main():
    local_trigger = load_json("data/generated_waveforms/local_trigger.json")
    command = build_fallback_command(local_trigger)

    if command is None:
        print("No offline fallback action needed.")
        return

    output_file = "data/generated_waveforms/fallback_command.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(command, f, indent=2)

    print("Fallback Command:")
    print(json.dumps(command, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()