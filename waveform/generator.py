import json
import csv
from pathlib import Path

import numpy as np


def load_scenario(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_waveform(scenario: dict) -> tuple[np.ndarray, np.ndarray]:
    duration = scenario["duration_sec"]
    sample_rate = scenario["sample_rate_hz"]
    noise_level = scenario["noise_level"]

    total_samples = duration * sample_rate
    time = np.linspace(0, duration, total_samples, endpoint=False)

    signal = np.random.normal(0, noise_level, total_samples)

    p = scenario["p_wave"]
    p_mask = (time >= p["start_sec"]) & (time < p["start_sec"] + p["duration_sec"])
    signal[p_mask] += p["amplitude"] * np.sin(2 * np.pi * p["frequency_hz"] * time[p_mask])

    s = scenario["s_wave"]
    s_mask = (time >= s["start_sec"]) & (time < s["start_sec"] + s["duration_sec"])
    signal[s_mask] += s["amplitude"] * np.sin(2 * np.pi * s["frequency_hz"] * time[s_mask])

    return time, signal


def save_waveform_csv(output_path: str, time: np.ndarray, signal: np.ndarray) -> None:
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["time_sec", "amplitude"])
        for t, s in zip(time, signal):
            writer.writerow([round(float(t), 6), round(float(s), 6)])


def main():
    scenario_path = "data/test_events/eq_dhaka_moderate.json"

    stations = {
        "ST01": 0.0,
        "ST02": 0.3,
        "ST03": 0.6
    }

    scenario = load_scenario(scenario_path)

    for station_id, delay in stations.items():
        time, signal = generate_waveform(scenario)

        # Shift waveform slightly
        time = time + delay

        output_path = f"data/generated_waveforms/{station_id}.csv"
        save_waveform_csv(output_path, time, signal)

        print(f"{station_id} generated -> {output_path}")


if __name__ == "__main__":
    main()