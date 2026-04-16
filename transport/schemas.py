def station_trigger_packet(station_id, time_sec, amplitude, confidence):
    return {
        "packet_type": "station_trigger",
        "station_id": station_id,
        "trigger_time_sec": time_sec,
        "peak_amplitude": amplitude,
        "confidence": confidence
    }