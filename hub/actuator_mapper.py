def map_command_to_actuators(command: dict) -> dict:
    """
    Convert logical device commands into final actuator states.
    """
    return {
        "hub_id": command["target_id"],
        "active_mode": command["mode"],
        "gas_valve_state": "CLOSED" if command["gas_off"] else "OPEN",
        "nonessential_power": "OFF" if (command["main_power_off"] or command["essential_only"]) else "ON",
        "essential_power": "ON" if command["essential_only"] else "UNCHANGED",
        "alarm_state": "ON" if command["alarm"] else "OFF",
        "lift_state": "STOPPED" if command["lift_stop"] else "RUNNING",
        "exit_unlock": "ON" if command["unlock_exit"] else "OFF"
    }