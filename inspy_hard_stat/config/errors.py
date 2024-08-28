from typing import Union, Optional
from inspy_hard_stat.errors import InspyHardStatError


class IHSConfigError(InspyHardStatError):
    """
    Base class for configuration errors.

    Inherits from:
        - inspy_hard_stat.errors.InspyHardStatError
    """
    default_message = 'An error occurred while processing the configuration.'


class InvalidConfigSystemError(IHSConfigError, ValueError):
    """
    Raised when an invalid configuration system is provided.

    Inherits from:
        - inspy_hard_stat.errors.InspyHardStatError
        - ValueError
    """
    default_message = 'The provided configuration system is invalid.'

    def __init__(self, config_system: str, valid_systems: list, message: str=None):
        """
        Initialize the exception.

        Parameters:
            config_system (str):
                The invalid configuration system.

            valid_systems (list):
                A list of valid configuration systems.

            message (str):
                An additional message to include with the exception.
        """
        message = message or f'Invalid configuration system: {config_system}. Valid systems: {valid_systems}'
        super().__init__(message)


class ConfigBackupDirectoryNonExistentError(IHSConfigError, NotADirectoryError):
    """
    Raised when a backup directory does not exist.

    Inherits from:
        - inspy_hard_stat.errors.InspyHardStatError
        - NotADirectoryError
    """

    def __init__(self, backup_dir, secondary_message=None):
        """
        Initialize the exception.

        Parameters:
            backup_dir (str):
                The path to the backup directory.

            secondary_message (str):
                An additional message to include with the exception.
        """
        self._additional_info = f'Backup directory does not exist: {backup_dir}'

        if secondary_message:
            self._additional_info += f'\n{secondary_message}'

        self._line_number = self.get_line_number()
        self._file_raised = self.get_file_raised()

        super().__init__(self._additional_info)

    @property
    def line_number(self):
        return self._line_number

    @property
    def file_raised(self):
        return self._file_raised

    def __str__(self):
        return f'ConfigBackupDirectoryNonExistentError: {self._additional_info}'


class ConfigBackupFileExistsError(IHSConfigError, FileExistsError):
    """
    Raised when a backup file already exists.

    Inherits from:
        - inspy_hard_stat.errors.InspyHardStatError
        - FileNotFoundError
    """

    def __init__(self, backup_file, secondary_message=None):
        """
        Initialize the exception.

        Parameters:
            backup_file (str):
                The path to the backup file.

            secondary_message (str):
                An additional message to include with the exception.
        """
        self._additional_info = f'Backup file already exists: {backup_file}'

        if secondary_message:
            self._additional_info += f'\n{secondary_message}'

        self._line_number = self.get_line_number()
        self._file_raised = self.get_file_raised()

        super().__init__(self._additional_info)

    @property
    def line_number(self):
        return self._line_number

    @property
    def file_raised(self):
        return self._file_raised

    def __str__(self):
        return f'ConfigBackupFileExistsError: {self._additional_info}'


class ConfigDirectoryNonExistentError(IHSConfigError, FileNotFoundError):

    def __init__(self, config_dir, secondary_message=None):
        self._additional_info = f'Configuration directory does not exist: {config_dir}'

        if secondary_message:
            self._additional_info += f'\n{secondary_message}'

        self._line_number = self.get_line_number()
        self._file_raised = self.get_file_raised()

        super().__init__(self._additional_info)

    @property
    def line_number(self):
        return self._line_number

    @property
    def file_raised(self):
        return self._file_raised

    def __str__(self):
        return f'ConfigDirectoryNonExistentError: {self._additional_info}'


class ForbiddenActionError(IHSConfigError):
    """
    Raised when an action is forbidden.

    Inherits from:
        - inspy_hard_stat.errors.InspyHardStatError
    """

    def __init__(self, action: str, secondary_message: Optional[str]=None):
        """
        Initialize the exception.

        Parameters:
            action:
            secondary_message:
        """
        self._additional_info = f'Forbidden action: {action}'

        if secondary_message:
            self._additional_info += f'\n{secondary_message}'

        self._line_number = self.get_line_number()
        self._file_raised = self.get_file_raised()

        super().__init__(self._additional_info)

    @property
    def line_number(self):
        return self._line_number

    @property
    def file_raised(self):
        return self._file_raised

    def __str__(self):
        return f'ForbiddenActionError: {self._additional_info}'
