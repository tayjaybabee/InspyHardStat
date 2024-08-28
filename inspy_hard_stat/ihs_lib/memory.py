import psutil
from inspyre_toolbox.conversions.bytes import ByteConverter


def get_memory_stats():
    return psutil.virtual_memory()


def get_memory_stat_dict():
    memory_stats = get_memory_stats()
    memory_stat_dict = {
        'total': memory_stats.total,
        'available': memory_stats.available,
        'percent': memory_stats.percent,
        'used': memory_stats.used,
        'free': memory_stats.free
    }
    return memory_stat_dict


def get_used_string(stat_dict, round_to=2):
    used = ByteConverter(stat_dict['used'], 'byte').get_lowest_safe_conversion()
    return f"Used: {round(used[1], round_to)} {used[0]}s"


def get_free_string(stat_dict, round_to=2):
    free = ByteConverter(stat_dict['free'], 'byte').get_lowest_safe_conversion()
    return f"Free: {round(free[1], round_to)} {free[0]}s"

def get_used_free_string():
    mem_dict = get_memory_stat_dict()

    used_str = get_used_string(mem_dict)

    free_str = get_free_string(mem_dict)

    return f"{used_str}, {free_str}"
