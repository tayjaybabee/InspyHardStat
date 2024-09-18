from prompt_toolkit.shortcuts.dialogs import yes_no_dialog, radiolist_dialog

from inspy_hard_stat.apps.backup_restore.ui.dialogs.constants import (DEFAULT_DIALOG_STYLE as DIALOG_STYLE,
                                                                      DEFAULT_WARNING_STYLE as WARNING_STYLE)
from inspy_hard_stat.apps.backup_restore.ui.dialogs.utils import loop_radio_list
from inspy_hard_stat.log_engine import Loggable
from inspy_hard_stat.apps.backup_restore.ui import MOD_LOGGER as PARENT_LOGGER


MOD_LOGGER = PARENT_LOGGER.get_child('dialogs')



def warning_dialog(title, text):
    return yes_no_dialog(
        title=title,
        text=text,
        style=WARNING_STYLE
    )


class BackupSelectionDialog(Loggable):
    """
    A dialog for selecting a backup.

    Attributes:

        backup_dict (dict):
            The backup dictionary.

        burned (bool):
            Whether the dialog has been burned.

        answer (str):
            The answer to the dialog.

        dialog (Application):
            The dialog to be displayed to the user.

        warning_dialog (Application):
            The warning dialog to be displayed to the user.
    """
    STYLE = DIALOG_STYLE
    WARNING_DIALOG = warning_dialog(
            'No backup selected',
            text='You have not selected a config for restoration. Would you like to exit?'
            )
    def __init__(self, backup_dict):
        """
        Initialize the dialog.

        Parameters:
            backup_dict (dict):
                The backup dictionary.
        """
        super().__init__(parent_log_device=MOD_LOGGER)
        self.class_logger.debug(f'Received backup_dict for config system; {backup_dict}')
        self.backup_dict = backup_dict

        self.__burned = False
        self.__answer = None

    @property
    def answer(self):
        """
        The answer to the dialog.

        Returns:
            str
        """
        if not self.burned:
            return None

        return self.__answer

    @property
    def burned(self):
        """
        Whether the dialog has been burned.

        Returns:
            bool
        """
        return self.__burned

    @property
    def dialog(self):
        """
        The dialog to be displayed to the user.

        Returns:
            Application
        """
        if not self.burned and self.answer is None:
            return radiolist_dialog(
                title='Select Backup to Restore',
                text='Choose a backup to restore:',
                values=list(self.__get_choices()),
                style=DIALOG_STYLE
            )

        return None

    @property
    def warning_dialog(self):
        """
        The warning dialog to be displayed to the user.

        Returns:
            Application
        """
        return self.WARNING_DIALOG

    def __get_choices(self):
        """
        Get the choices for the dialog.

        Returns:
            Generator
        """
        for file, name in self.backup_dict.items():
            yield (file, name)

    def __run(self):
        """
        Run the dialog.

        Returns:
            Application
        """
        log = self.create_logger()

        log.debug('Entering loop...')

        return loop_radio_list(
                self.dialog,
                warning_dialog=self.warning_dialog
                )

    def run(self):
        """
        Run the dialog.

        Returns:
            Application
        """
        if not self.burned:
            self.__answer = self.__run()
            self.__burned = True

        return self.__answer


class SystemSelectionDialog:
    """
    A dialog for selecting a configuration system.

    Attributes:

            backup_dict (dict):
                The backup dictionary.

            burned (bool):
                Whether the dialog has been burned.

            answer (str):
                The answer to the dialog.

            dialog (Application):
                The dialog to be displayed to the user.

            warning_dialog (Application):
                The warning dialog to be displayed
    """
    STYLE = DIALOG_STYLE
    WARNING_DIALOG = warning_dialog(
        'No Config System Selected',
        text='You need to select a configuration system to continue. Would you like to exit?',

    )
    def __init__(self, backup_dict):
        """
        Initialize the dialog.

        Parameters:
            backup_dict (dict):
                The backup dictionary.:
        """
        self.backup_dict = backup_dict
        self.__burned = False
        self.__answer = None

    @property
    def answer(self):
        """
        The answer to the dialog.

        Returns:
            str

        """
        return self.__answer

    @property
    def burned(self):
        """
        Whether the dialog has been burned.

        Returns:
            bool
        """
        return self.__burned

    @property
    def dialog(self):
        """
        The dialog to be displayed to the user.

        Returns:
            Application
        """
        if not self.burned and self.answer is None:
            return radiolist_dialog(
                title='Select Configuration System',
                text='Choose a configuration system to restore:',
                values=list(self.__get_choices()),
                style=DIALOG_STYLE
            )
        return None

    @property
    def warning_dialog(self):
        """
        The warning dialog to be displayed to the user.

        Returns:
            Application
        """
        return self.WARNING_DIALOG

    def __get_choices(self):
        """
        Get the choices for the dialog.

        Returns:
            Generator
        """
        for system in self.backup_dict.keys():
            yield system, system

    def __run(self):
        """
        Run the dialog.

        Returns:
            Application
        """
        choices = list(self.__get_choices())

        selected_system_prompt = radiolist_dialog(
                title='Select Configuration System',
                text='Choose a configuration system to restore:',
                values=choices,
                style=DIALOG_STYLE
        )

        return loop_radio_list(selected_system_prompt, warning_dialog=self.WARNING_DIALOG)

    def run(self):
        """
        Run the dialog.

        Returns:
            Application
        """
        if not self.burned:
            self.__answer = self.__run()

        if self.answer:
            self.__burned = True

        return self.__answer
