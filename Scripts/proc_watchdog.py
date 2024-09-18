import os
import sys
import time
import subprocess
import psutil
import ctypes
from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import CONFIG

class LibreHardwareMonitorWatchdog:
    def __init__(self, script_name, libre_monitor_path):
        self.script_name = script_name
        self.libre_monitor_path = libre_monitor_path
        self.libre_monitor_process = None

    def is_admin(self):
        """Check if the script is running with administrator privileges."""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def run_as_admin(self):
        """Rerun the script with administrator privileges."""
        print("Elevating privileges...")
        log_file = os.path.join(os.path.dirname(__file__), "watchdog_log.txt")
        with open(log_file, "w") as log:
            log.write("Running as admin...\n")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, f"{CONFIG.executable_path}".join(sys.argv), None, 1
        )
        sys.exit()

    def is_script_running(self):
        """Check if the specified Python script is running."""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] in ('python.exe', 'pythonw.exe'):
                # Check if the script name is part of the command line arguments
                if any(self.script_name in cmd for cmd in proc.info['cmdline']):
                    return True
        return False

    def start_libre_monitor(self):
        """Start Libre Hardware Monitor with administrator privileges."""
        if self.libre_monitor_process is None or self.libre_monitor_process.poll() is not None:
            print("Starting Libre Hardware Monitor...")
            self.libre_monitor_process = subprocess.Popen([self.libre_monitor_path], shell=True)
            print(f"Libre Hardware Monitor started with PID {self.libre_monitor_process.pid}")

    def stop_libre_monitor(self):
        """Stop Libre Hardware Monitor."""
        if self.libre_monitor_process is not None:
            print("Stopping Libre Hardware Monitor...")
            self.libre_monitor_process.terminate()
            self.libre_monitor_process.wait()
            print("Libre Hardware Monitor stopped.")
            self.libre_monitor_process = None

    def run(self):
        """Main loop that monitors the Python script and Libre Hardware Monitor."""
        log_file = os.path.join(os.path.dirname(__file__), "watchdog_log.txt")
        try:
            with open(log_file, "a") as log:
                log.write("Starting watchdog...\n")
                while True:
                    if self.is_script_running():
                        self.start_libre_monitor()
                    else:
                        log.write(f"{self.script_name} is not running. Exiting...\n")
                        break

                    time.sleep(5)  # Check every 5 seconds
        finally:
            with open(log_file, "a") as log:
                self.stop_libre_monitor()
                log.write("Watchdog stopped.\n")

if __name__ == "__main__":
    script_name = "inspy_hard_stat.py"  # Replace with your Python script's name
    libre_monitor_path = CONFIG.executable_path  # Replace with the path to Libre Hardware Monitor

    watchdog = LibreHardwareMonitorWatchdog(script_name, libre_monitor_path)

    if not watchdog.is_admin():
        watchdog.run_as_admin()
    else:
        watchdog.run()
