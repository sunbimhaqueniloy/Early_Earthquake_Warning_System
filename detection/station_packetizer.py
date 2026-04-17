import json
import pandas as pd


def detect_p_wave(filepath: str, threshold: float = 0.10) -> dict | None:
    data = pd.read_csv(filepath)

    for i in range(len(data)):
        amplitude = abs(data.loc[i, "amplitude"])
        time_sec = data.loc[i, "time_sec"]

        if amplitude > threshold:
            return {
                "trigger": True,
                "trigger_time_sec": float(time_sec),
                "peak_amplitude": float(amplitude),
                "confidence": 0.85
            }

    return None


def build_station_trigger_packet(station_id: str, detection_result: dict) -> dict:
    return {
        "packet_type": "station_trigger",
        "station_id": station_id,
        "trigger": detection_result["trigger"],
        "trigger_time_sec": detection_result["trigger_time_sec"],
        "peak_amplitude": detection_result["peak_amplitude"],
        "confidence": detection_result["confidence"]
    }


def main() -> None:
    filepath = "data/generated_waveforms/station_ST01.csv"
    station_id = "ST01"

    detection_result = detect_p_wave(filepath, threshold=0.10)

    if detection_result is None:
        print("No trigger found.")
        return

    packet = build_station_trigger_packet(station_id, detection_result)

    output_file = "data/generated_waveforms/station_ST01_trigger.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(packet, f, indent=2)

    print("Station Trigger Packet:")
    print(json.dumps(packet, indent=2))
    print(f"Saved to: {output_file}")


if __name__ == "__main__":
    main()