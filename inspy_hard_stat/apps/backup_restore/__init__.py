import os
from warnings import warn
import shutil
from inspy_hard_stat.log_engine import ROOT_LOGGER as PARENT_LOGGER

APP_LOGGER = PARENT_LOGGER.get_child('IHSConfigRestore')
from inspy_hard_stat.apps.backup_restore.errors import NoConfigSystemSelectedError, NoBackupSelectedError
from inspy_hard_stat.apps.backup_restore.ui.dialogs import BackupSelectionDialog, SystemSelectionDialog
from inspy_hard_stat.apps.backup_restore.utils import find_backups, BACKUP_DIR


def restore_backup(backup_folder, original_folder, selected_backup):
    src_path = os.path.join(backup_folder, selected_backup)
    config_name = f'{selected_backup.split("_")[0]}.ini'
    dest_path = os.path.join(original_folder, config_name)
    shutil.copy(src_path, dest_path)
    print(f'Restored {config_name} from {selected_backup}')



def main():
    """Restore a configuration backup."""

    backups = find_backups()

    if not backups:

        print("No backups found.")
        return

    system_select_dialog = SystemSelectionDialog(backups)

    selected_system = system_select_dialog.run()

    if not selected_system:
        warn('User did not select a configuration system.')
        raise NoConfigSystemSelectedError('User left dialog without making a selection.')


    config_file_select_dialog = BackupSelectionDialog(backups[selected_system])

    selected_config_file = config_file_select_dialog.run()

    if not selected_config_file:
        warn('User did not select a configuration-file backup to restore.')
        raise NoBackupSelectedError('User left dialog without making a selection.')

    restore_backup(BACKUP_DIR, BACKUP_DIR.parent, selected_config_file)

if __name__ == "__main__":
    main()
