from inspy_hard_stat.errors import InspyHardStatError


class BackupRestoreError(InspyHardStatError):
    pass


class NoConfigSystemSelectedError(BackupRestoreError):
    """
    Raised when no configuration system is selected.
    """

    def __init__(self, secondary_message=None):
        self._additional_info = 'No configuration system selected'

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
        return f'NoConfigSystemSelectedError: {self._additional_info}'


class NoBackupSelectedError(BackupRestoreError):
    """
    Raised when no backup is selected.
    """

    def __init__(self, secondary_message=None):
        self._additional_info = 'No backup selected'

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
        return f'NoBackupSelectedError: {self._additional_info}'
