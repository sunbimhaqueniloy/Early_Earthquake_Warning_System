import json
from pathlib import Path


def confirm_event(trigger_file: str) -> tuple[bool, list]:
    """Read trigger packets and confirm if event is real."""
    with open(trigger_file, "r", encoding="utf-8") as f:
        triggers = json.load(f)

    if len(triggers) < 2:
        return False, triggers

    times = [t["trigger_time_sec"] for t in triggers]

    # If all station triggers are close enough in time, confirm event
    if max(times) - min(times) < 2.0:
        return True, triggers

    return False, triggers


def build_confirmed_event_packet(triggers: list) -> dict:
    """Build a confirmed event packet."""
    event_time = min(t["trigger_time_sec"] for t in triggers)
    station_ids = [t["station_id"] for t in triggers]

    return {
        "packet_type": "confirmed_event",
        "event_id": "EQ_0001",
        "confirmed": True,
        "event_time_sec": event_time,
        "triggered_stations": station_ids
    }


def save_confirmed_event(packet: dict, output_file: str) -> None:
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2)


def main() -> None:
    trigger_file = "data/generated_waveforms/all_triggers.json"
    output_file = "data/generated_waveforms/confirmed_event.json"

    is_confirmed, triggers = confirm_event(trigger_file)

    if is_confirmed:
        packet = build_confirmed_event_packet(triggers)
        save_confirmed_event(packet, output_file)
        print("✅ Earthquake CONFIRMED")
        print(json.dumps(packet, indent=2))
    else:
        print("❌ False alarm")


if __name__ == "__main__":
    main()