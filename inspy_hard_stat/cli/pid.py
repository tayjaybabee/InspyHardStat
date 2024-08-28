import os
import atexit


def create_pid_file(file_path):
    """Creates a PID file and registers a function to delete it on exit."""
    pid = os.getpid()

    # Write the PID to the file
    with open(file_path, 'w') as pid_file:
        pid_file.write(str(pid))

    # Register the cleanup function to delete the PID file on exit
    atexit.register(delete_pid_file, file_path)


def delete_pid_file(file_path):
    """Deletes the PID file."""
    if os.path.exists(file_path):
        os.remove(file_path)
