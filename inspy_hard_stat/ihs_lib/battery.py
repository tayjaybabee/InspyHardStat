import psutil
from inspy_hard_stat.ihs_lib.helpers.time import get_hour_minute_string, is_hour_or_greater, Seconds


def get_battery_status():
    return psutil.sensors_battery()


def get_battery_stat_dict():
    battery = get_battery_status()
    if battery is None:
        return None
    battery_stat_dict = {
            'percent':       battery.percent,
            'secsleft':      battery.secsleft,
            'power_plugged': battery.power_plugged
            }
    return battery_stat_dict


def get_battery_status_string(round_to=2):
    """
    Get the battery status as a string.

    Parameters:
        round_to (int):
            The number of decimal places to round to. Optional; default is 2.

    Returns:
        str:
            A string containing the battery status information.
    """
    battery_stats = get_battery_stat_dict()
    if battery_stats is None:
        return "Battery status is not available"

    status_str = f"Battery: {battery_stats['percent']}%\n"

    if not battery_stats['power_plugged']:
        secs = Seconds(battery_stats['secsleft'], round_to)
        if is_hour_or_greater(secs.minutes):
            status_str += f"Time Left: {secs.hour_minute_string}"
        else:
            status_str += f"Time Left: {secs} seconds"

        status_str += '\n'

    status_str += f"Power Plugged: {battery_stats['power_plugged']}"

    return status_str
