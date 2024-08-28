import os
import re
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
import shutil
from inspy_hard_stat.ihs_lib.libre_hw_monitor.config import CONFIG


BACKUP_DIR = CONFIG.config_dir_path.joinpath('backups')


def find_backups(backup_folder=BACKUP_DIR):
    backup_files = os.listdir(backup_folder)
    backup_dict = {}

    for file in backup_files:
        match = re.match(r'(\w+)_(\d{8})_(\d{6}).bak', file)
        if match:
            config_name = match.group(1)
            date_str = match.group(2)
            time_str = match.group(3)
            timestamp = datetime.strptime(date_str + time_str, '%Y%m%d%H%M%S')
            readable_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            backup_dict[file] = f"{config_name} - {readable_time}"

    return backup_dict

def select_backup(backup_dict):
    choices = [(file, name) for file, name in backup_dict.items()]
    selected_backup = radiolist_dialog(
        title='Select Backup to Restore',
        text='Choose a backup to restore:',
        values=choices
    ).run()

    return selected_backup

def restore_backup(backup_folder, original_folder, selected_backup):
    src_path = os.path.join(backup_folder, selected_backup)
    config_name = f'{selected_backup.split("_")[0]}.ini'
    dest_path = os.path.join(original_folder, config_name)
    shutil.copy(src_path, dest_path)
    print(f'Restored {config_name} from {selected_backup}')

def main():
    """Restore a configuration backup."""
    backup_folder = BACKUP_DIR
    original_folder = BACKUP_DIR.parent

    backups = find_backups(backup_folder)
    if not backups:
        print("No backups found.")
        return

    selected_backup = select_backup(backups)
    if selected_backup:
        restore_backup(backup_folder, original_folder, selected_backup)
    else:
        print("No backup selected.")

if __name__ == "__main__":
    main()
