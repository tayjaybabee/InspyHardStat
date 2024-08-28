"""
This module provides functions to get disk space statistics.

Functions:
    get_disk_stats(root_dir='/'):
        Get disk space statistics.

    get_disk_stat_dict(root_dir='/'):
        Get disk space statistics as a dictionary.

    get_used_string(stat_dict, round_to=2):
        Get the used disk space as a string.

    get_free_string(stat_dict, round_to=2, unit=None):
        Get the free disk space as a string.

    get_used_free_string(root_dir='/', round_to=2, match_unit=False):
        Get the used and free disk space as a string.
"""
import psutil
from inspyre_toolbox.conversions.bytes import ByteConverter


def get_disk_stats(root_dir='/'):
    """
    Get disk space statistics.

    Parameters:
        root_dir (str):
            The root directory to check disk space usage. Optional; default is '/'.

    Returns:
        psutil._common.sdiskusage:
            A named tuple representing disk space usage statistics.
            It contains the following attributes:
                - total:
                    total disk space, in bytes.

                - used:
                    used disk space, in bytes.

                - free:
                    free disk space, in bytes.

                - percent:
                    percentage of disk space used.
    """
    return psutil.disk_usage(root_dir)


def get_disk_stat_dict(root_dir='/', ):
    """
    Get disk space statistics as a dictionary.

    Parameters:
        root_dir (str):
            The root directory to check disk space usage. Optional; default is '/'.

    Returns:
        dict:
            A dictionary containing the following keys:
                - total:
                    total disk space, as a float.

                - used:
                    used disk space, as a float.

                - free:
                    free disk space, as a float.

                - percent:
                    percentage of disk space used., as a float.
    """
    disk_stats = get_disk_stats(root_dir)
    disk_stat_dict = {
        'total': disk_stats.total,
        'used': disk_stats.used,
        'free': disk_stats.free,
        'percent': disk_stats.percent
    }
    return disk_stat_dict


def get_used_string(stat_dict, round_to=2):
    """
    Get the used disk space as a string.

    Parameters:
        stat_dict (dict):
            A dictionary containing disk space statistics. You can use `get_disk_stat_dict()` to get this dictionary.

        round_to (int):
            The number of decimal places to round to. Optional; default is 2.

    Returns:
        str:
            A string with the used disk space, in the following format:
            "Used: <used_space> <unit>s
    """
    used = ByteConverter(stat_dict['used'],'byte').get_lowest_safe_conversion()

    return f"Used: {round(used[1], round_to)} {used[0]}s"


def get_free_string(stat_dict, round_to=2, unit=None):
    """
    Get the free disk space as a string.

    Parameters:
        stat_dict (dict):
            A dictionary containing disk space statistics. You can use `get_disk_stat_dict()` to get this dictionary.

        round_to (int):
            The number of decimal places to round to. Optional; default is 2.

        unit (str):
            The unit to convert the free space to. Optional; default is None.
    """
    if not unit:
        free = ByteConverter(stat_dict['free'],'byte').get_lowest_safe_conversion()
    else:
        free = (unit, ByteConverter(stat_dict['free'],'byte').convert(unit))

    return f"Free: {round(free[1], round_to)} {free[0]}s"


def get_used_free_string(root_dir='/', round_to=2, match_unit=False):
    """
    Get the used and free disk space as a string.

    Parameters:
        root_dir (str):
            The root directory to check disk space usage. Optional; default is '/'.

        round_to (int):
            The number of decimal places to round to. Optional; default is 2.

        match_unit (bool):
            Whether to match the unit of the used and free space. Optional; default is False.

    Returns:
        str:
            A string with the used and free disk space, in the following format:
            "Used: <used_space> <unit>, Free: <free_space> <unit>"
    """
    disk_stat_dict = get_disk_stat_dict(root_dir)

    used_str = get_used_string(disk_stat_dict)

    used_str_unit = used_str.split(' ')[-1]
    used_str_unit = used_str_unit.replace('s', '')

    free_str = get_free_string(disk_stat_dict, round_to, None if not match_unit else used_str_unit)

    return f"{used_str}, {free_str}"
