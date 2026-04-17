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


def main() -> None:
    filepath = "data/generated_waveforms/station_ST01.csv"
    result = detect_p_wave(filepath, threshold=0.10)

    if result:
        print("P-wave detected!")
        print(result)
    else:
        print("No trigger found.")


if __name__ == "__main__":
    main()