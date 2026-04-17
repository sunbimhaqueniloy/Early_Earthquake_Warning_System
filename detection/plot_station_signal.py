import pandas as pd
import matplotlib.pyplot as plt


def main() -> None:
    filepath = "data/generated_waveforms/station_ST01.csv"
    data = pd.read_csv(filepath)

    plt.figure(figsize=(12, 5))
    plt.plot(data["time_sec"], data["amplitude"], linewidth=1)
    plt.title("Simulated Earthquake Waveform - Station ST01")
    plt.xlabel("Time (seconds)")
    plt.ylabel("Amplitude")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()