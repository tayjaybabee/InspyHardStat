import psutil
import platform
import cpuinfo
from inspy_hard_stat.ihs_lib.libre_hw_monitor.utils import is_lhwmon_running, start_libre_hw_monitor


class CPU:
    RAW_CPUINFO = cpuinfo.get_cpu_info()
    def __init__(self):
        self.__cores = psutil.cpu_count(logical=False)
        self.__name = self.RAW_CPUINFO['brand_raw']

    @property
    def cores(self):
        return self.__cores

    @property
    def name(self):
        return self.__name


def get_cpu_percent():
    return psutil.cpu_percent(interval=1)
