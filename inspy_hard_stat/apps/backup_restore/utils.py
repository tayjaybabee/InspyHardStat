import os
import re
from datetime import datetime
from inspy_hard_stat.apps.backup_restore.constants import BACKUP_DIR


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
            if config_name not in backup_dict:
                backup_dict[config_name] = {}
            backup_dict[config_name][file] = f"{config_name} - {readable_time}"

    return backup_dict
