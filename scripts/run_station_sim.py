import json
import sys
from pathlib import Path

# Add project root directory so Python can import detection package
sys.path.append(str(Path(__file__).resolve().parent.parent))

from detection.station_packetizer import detect_p_wave, build_station_trigger_packet

stations = ["ST01", "ST02", "ST03"]

all_packets = []

for station in stations:
    filepath = f"data/generated_waveforms/{station}.csv"

    result = detect_p_wave(filepath)

    if result:
        packet = build_station_trigger_packet(station, result)
        all_packets.append(packet)

# Save all packets
output_file = "data/generated_waveforms/all_triggers.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_packets, f, indent=2)

print("All station packets:")
print(json.dumps(all_packets, indent=2))
print(f"Saved to: {output_file}")