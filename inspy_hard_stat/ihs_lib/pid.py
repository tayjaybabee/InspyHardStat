import os
import psutil
from typing import Optional
from inspy_hard_stat.config.constants import FILE_SYSTEM_DEFAULTS
from atexit import register, unregister


DEFAULT_PID_FP = FILE_SYSTEM_DEFAULTS['dirs']['data'] / 'lhm.pid'
DEFAULT_PROC_NAME = 'LibreHardwareMonitor.exe'


def find_process_by_pid(pid: int) -> Optional[dict]:
    """
    Find a process by its PID.

    Parameters:
        pid (int):
            The PID of the process.

    Returns:
        Optional[dict]:
            The process if found, otherwise None.
    """
    try:
        process = psutil.Process(pid)
        process_info = {
            'pid': process.pid,
            'name': process.name(),
            'status': process.status(),
            'create_time': process.create_time(),
            'cpu_usage': process.cpu_percent(interval=0.1),
            'memory_usage': process.memory_info().rss
        }
        return process_info
    except psutil.NoSuchProcess:
        return None


def find_pids_by_name(name: str, strict_case: bool = False) -> list:
    """
    Find all PIDs by the process name.

    Parameters:
        name (str):
            The name of the process to search for.

        strict_case (bool):
            If True, the process name comparison is case-sensitive.

    Returns:
        list:
            A list of PIDs that match the process name.
    """
    if not strict_case:
        name = name.lower()

    pids = []
    for proc in psutil.process_iter(['pid', 'name']):
        proc_name = proc.info['name'].lower() if not strict_case else proc.info['name']
        if proc_name == name:
            pids.append(proc.info['pid'])

    return pids


def load_pid_from_file(pid_file_path: str) -> Optional[int]:
    """
    Load a PID from a file.

    Parameters:
        pid_file_path (str):
            The path to the PID file.

    Returns:
        Optional[int]:
            The PID if found, otherwise None.
    """
    try:
        with open(pid_file_path, 'r') as pid_file:
            pid_str = pid_file.read().strip()
            if pid_str.isdigit():
                return int(pid_str)
            else:
                print(f"Invalid PID value in file: {pid_str}")
                return None
    except FileNotFoundError:
        print(f"PID file not found at {pid_file_path}.")
        return None


def load_and_validate_pid(
        pid_file_path: str         = DEFAULT_PID_FP,
        expected_process_name: str = DEFAULT_PROC_NAME,
        strict_case: bool           = False
    ) -> Optional[int]:
    """
    Load a PID from a file, verify if the process exists and matches the expected name.
    If valid, return the PID. Otherwise, delete the PID file.

    Parameters:
        pid_file_path (str): The path to the PID file.
        expected_process_name (str): The expected name of the process.
        strict_case (bool): If True, the process name comparison is case-sensitive.

    Returns:
        Optional[int]: The PID if valid, otherwise None.
    """
    pid = None

    if not strict_case:
        expected_process_name = expected_process_name.lower()

    pid = load_pid_from_file(pid_file_path)

    if pid is None:
        return False

    pid_proc = find_process_by_pid(pid)

    if pid_proc:
        pid_proc_name = pid_proc['name'].lower() if not strict_case else pid_proc['name']

        if pid_proc_name == expected_process_name:
            from atexit import register
            register(remove_pid_file_and_unregister)
            return pid
        else:
            print(f"Process name '{pid_proc['name']}' does not match expected '{expected_process_name}'.")
            remove_pid_file(pid_file_path)
            return None
    else:
        print(f"No process with PID {pid} is running.")
        remove_pid_file(pid_file_path)


def remove_pid_file(file_path: str = DEFAULT_PID_FP):
    """
    Remove the PID file.

    Parameters:
        file_path (str):
            The path to the PID file.
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass



def remove_pid_file_and_unregister(file_path: str = DEFAULT_PID_FP):
    """
    Remove the PID file and unregister the cleanup function.

    Parameters:
        file_path (str):
            The path to the PID file.
    """
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
    finally:
        unregister(remove_pid_file_and_unregister)


def create_pid_file(pid: int, file_path: str = DEFAULT_PID_FP):
    """
    Create a PID file containing the given PID.

    Parameters:
        pid (int):
            The PID to write to the file.

        file_path (str):
            The path to the file to write the PID to.
    """
    with open(file_path, 'w') as f:
        f.write(str(pid))

    register(remove_pid_file_and_unregister)
