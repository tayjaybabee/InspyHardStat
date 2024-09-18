from inspy_hard_stat.cli.arguments import IHSParser
from argparse import ArgumentParser


class ConfigRestoreParser(IHSParser):
    def __init__(self):
        super().__init__('ihs-config-restore', 'Restore the configuration of inspy-hard-stat.')
        self.__parser = None
        self.register_arguments(self.register_parser)

    def register_parser(self, parser: ArgumentParser):

        parser.add_argument(
                '--backup-file',
                help='The backup file to restore the configuration from. If not specified, you will be shown a prompt with'
                     ' a list of available backup files to choose from, or you can choose to restore the latest '
                     'backup file with the --restore-latest option.',
                required=False,
                )
        parser.add_argument(
                '--restore-latest',
                help='Restore the latest backup file. If a backup file is specified, this option is ignored.',
                action='store_true',
                required=False,
                )
        parser.add_argument(
                '--restore-to-default',
                help='Restore the configuration to the default configuration.',
                action='store_true',
                required=False,
                )
        parser.add_argument(
                '--open-config-dir',
                help='Open the configuration directory in the file manager after the restore operation is complete.',
                action='store_true',
                required=False,
                )
