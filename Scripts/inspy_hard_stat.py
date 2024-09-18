from time import sleep
from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import CONFIG
from inspy_hard_stat.ihs_lib.libre_hw_monitor.utils import is_lhwmon_running
import os
import atexit


print(os.getpid())


def main_loop():
    acc = 0
    while True:
        acc += 1
        try:
            sleep(1)
            print("Main loop running...")
            print(f"Libre Hardware Monitor running: {is_lhwmon_running(CONFIG.executable_path)}")
        except KeyboardInterrupt:
            print("\nExiting main loop...")
            print(acc)
            break



if __name__ == '__main__':
    main_loop()
