import psutil
from typing import Union
import os
import ctypes
import ctypes.wintypes
from inspy_hard_stat.ihs_lib.pid import (create_pid_file, find_process_by_pid, find_pids_by_name,
                                         load_and_validate_pid, DEFAULT_PID_FP)
from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import CONFIG
from inspy_hard_stat.config.constants import FILE_SYSTEM_DEFAULTS
from inspyre_toolbox.proc_man import kill_by_pid



GPU_INFO_TEMPLATE = {
                'Name': '',
                'Voltages': {},
                'Powers': {},
                'Clocks': {},
                'Temperatures': {},
                'Load': {}
            }



def parse_voltages(child):
    voltages = {}
    for voltage in child['Children']:
        voltages[voltage['Text']] = voltage['Value']
    return voltages


def parse_powers(child):
    powers = {}
    for power in child['Children']:
        powers[power['Text']] = power['Value']
    return powers


def parse_clocks(child):
    """
    Parse the clock information from the given JSON data.

    Parameters:
        child (dict):
            A dictionary containing the JSON data.

    Returns:
        dict:
            A dictionary containing the clock information.
    """
    clocks = {}
    for clock in child['Children']:
        clocks[clock['Text']] = clock['Value']
    return clocks


def parse_temperatures(child):
    """
    Parse the temperature information from the given JSON data.

    Parameters:
        child (dict):
            A dictionary containing

    Returns"
        dict:
            A dictionary containing the temperature information.
    """
    temps = {}
    for temp in child['Children']:
        temps[temp['Text']] = temp['Value']
    return temps


def parse_loads(child):
    """
    Parse the load information from the given JSON data.

    Parameters:
        child (dict):
            A dictionary containing the JSON data.

    Returns:
        dict:
            A dictionary containing the load information.
    """
    loads = {}
    for load in child['Children']:
        loads[load['Text']] = load['Value']
    return loads


def extract_gpu_info(item):
    """
    Extract GPU information from the given JSON data.

    Parameters:
        item (dict):
            A dictionary containing the JSON data.

    Returns:
        dict:
            A dictionary containing the GPU information.
    """
    gpu_info = GPU_INFO_TEMPLATE.copy()
    gpu_info['Name'] = item['Text']

    for child in item['Children']:
        if 'Voltages' in child['Text']:
            gpu_info['Voltages'] = parse_voltages(child)
        elif 'Powers' in child['Text']:
            gpu_info['Powers'] = parse_powers(child)
        elif 'Clocks' in child['Text']:
            gpu_info['Clocks'] = parse_clocks(child)
        elif 'Temperatures' in child['Text']:
            gpu_info['Temperatures'] = parse_temperatures(child)
        elif 'Load' in child['Text']:
            gpu_info['Load'] = parse_loads(child)

    return gpu_info


def find_gpus(children):
    """
    Find GPU information in the given JSON data.

    Parameters:
        children (list):
            A list of dictionaries containing the JSON data.
    """
    gpus = []
    for item in children:
        if 'Text' in item and ('GPU' in item['Text'] or 'Radeon' in item['Text']):
            gpus.append(extract_gpu_info(item))
        elif 'Children' in item:
            gpus.extend(find_gpus(item['Children']))
    return gpus


def is_lhwmon_running(exe_path: str, return_pid: bool = False) -> Union[bool, int]:
    """
    Check if Libre Hardware Monitor is running.

    Parameters:
        exe_path (str):
            The path to the Libre Hardware Monitor executable.

        return_pid (bool):
            If True, return the PID of the running process

    Returns:
        Union[bool, int]:
            bool:
                True if Libre Hardware Monitor is running; False otherwise.
            int:
                The PID of the running process. Only returned if `return_pid` is :bool:`True`.
    """
    fields = ['exe', 'name']

    if return_pid:
        fields.append('pid')

    for proc in psutil.process_iter(fields):
        try:
            if proc.info['exe'] == exe_path:
                if return_pid:
                    return proc.info['pid']
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return False


def start_libre_hw_monitor(exe_path: str = CONFIG.executable_path) -> Union[int, None]:
    """
    Start Libre Hardware Monitor with administrator privileges and retrieve the PID.

    Parameters:
        exe_path (str):
            The path to the Libre Hardware Monitor executable.
    """
    pid = None
    pid = load_and_validate_pid(DEFAULT_PID_FP)

    if pid is not None and pid and find_process_by_pid(pid):
            print(f"Libre Hardware Monitor is already running with PID: {pid}")
            return pid

    pid = is_lhwmon_running(exe_path, return_pid=True) if is_lhwmon_running(exe_path) else None

    if pid:
        print(f"Libre Hardware Monitor is already running with PID: {pid}")
    else:
        try:
            # Define the necessary constants and structures
            SEE_MASK_NOCLOSEPROCESS = 0x00000040
            SEE_MASK_FLAG_NO_UI = 0x00000400
            SW_SHOWNORMAL = 1

            class SHELLEXECUTEINFO(ctypes.Structure):
                _fields_ = [
                    ("cbSize", ctypes.wintypes.DWORD),
                    ("fMask", ctypes.wintypes.ULONG),
                    ("hwnd", ctypes.wintypes.HWND),
                    ("lpVerb", ctypes.wintypes.LPCWSTR),
                    ("lpFile", ctypes.wintypes.LPCWSTR),
                    ("lpParameters", ctypes.wintypes.LPCWSTR),
                    ("lpDirectory", ctypes.wintypes.LPCWSTR),
                    ("nShow", ctypes.c_int),
                    ("hInstApp", ctypes.wintypes.HINSTANCE),
                    ("lpIDList", ctypes.c_void_p),
                    ("lpClass", ctypes.wintypes.LPCWSTR),
                    ("hkeyClass", ctypes.wintypes.HKEY),
                    ("dwHotKey", ctypes.wintypes.DWORD),
                    ("hIcon", ctypes.wintypes.HANDLE),
                    ("hProcess", ctypes.wintypes.HANDLE),
                ]

            # Initialize the SHELLEXECUTEINFO structure
            sei = SHELLEXECUTEINFO()
            sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
            sei.fMask = SEE_MASK_NOCLOSEPROCESS | SEE_MASK_FLAG_NO_UI
            sei.hwnd = None
            sei.lpVerb = "runas"
            sei.lpFile = exe_path
            sei.lpParameters = ""
            sei.lpDirectory = os.path.dirname(exe_path)
            sei.nShow = SW_SHOWNORMAL
            sei.hInstApp = None
            sei.lpIDList = None
            sei.lpClass = None
            sei.hkeyClass = None
            sei.dwHotKey = 0
            sei.hIcon = None
            sei.hProcess = None

            # Call ShellExecuteEx to run the executable as administrator
            if not ctypes.windll.shell32.ShellExecuteExW(ctypes.byref(sei)):
                raise ctypes.WinError()

            # Get the process handle and retrieve the PID
            hProcess = sei.hProcess
            pid = ctypes.windll.kernel32.GetProcessId(hProcess)

            print(f"Started Libre Hardware Monitor with PID: {pid}")

            # Optionally, you might want to wait for the process to initialize
            # or perform additional checks here.

            # Close the process handle
            ctypes.windll.kernel32.CloseHandle(hProcess)

        except Exception as e:
            print(f"Failed to start Libre Hardware Monitor: {e}")

    if pid:
        create_pid_file(pid)

        if CONFIG.kill_on_exit:
            from atexit import register
            from inspy_hard_stat.ihs_lib.pid import remove_pid_file_and_unregister
            register(remove_pid_file_and_unregister)
            register(kill_by_pid, pid=pid)

    return pid
