import json
from pathlib import Path

from actuator_mapper import map_command_to_actuators


def load_json_if_exists(filepath: str) -> dict | None:
    file = Path(filepath)
    if not file.exists():
        return None

    with open(file, "r", encoding="utf-8") as f:
        return json.load(f)


def choose_active_command(online_command: dict | None, fallback_command: dict | None) -> dict:
    """
    Priority:
    1. Online early warning
    2. Offline fallback
    3. Idle mode
    """
    if online_command is not None:
        return online_command

    if fallback_command is not None:
        return fallback_command

    return {
        "packet_type": "device_command",
        "target_id": "HUB01",
        "mode": "IDLE",
        "alarm": False,
        "gas_off": False,
        "main_power_off": False,
        "essential_only": False,
        "lift_stop": False,
        "unlock_exit": False
    }


def main():
    online_command = load_json_if_exists("data/generated_waveforms/device_command.json")
    fallback_command = load_json_if_exists("data/generated_waveforms/fallback_command.json")

    active_command = choose_active_command(online_command, fallback_command)
    hub_state = map_command_to_actuators(active_command)

    output_file = "data/generated_waveforms/hub_status.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(hub_state, f, indent=2)

    print("Hub State:")
    print(json.dumps(hub_state, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()