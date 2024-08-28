import psutil
from atexit import register, unregister
from typing import Union


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


def start_libre_hw_monitor(exe_path: str):
    """
    Start Libre Hardware Monitor.

    Parameters:
        exe_path (str):
            The path to the Libre Hardware Monitor executable.
    """
    pid = None
    pid = is_lhwmon_running(exe_path, return_pid=True) if is_lhwmon_running(exe_path) else None

    if pid:
        print(f"Libre Hardware Monitor is already running with PID: {pid}")
    else:

        try:
            proc = psutil.Popen(exe_path)
            pid = proc.pid
            print(f"Started Libre Hardware Monitor with PID: {pid}")
            create_pid_file()
        except FileNotFoundError as e:
            print(f"Failed to start Libre Hardware Monitor: {e}")

    return pid


def create_pid_file(pid: int, file_path: str):
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

    register(lambda: os.remove(file_path))
