from argparse import ArgumentParser, Namespace
from inspy_hard_stat.log_engine import LOG_LEVELS
from inspy_hard_stat.config.developer import DEV_MODE
from inspy_hard_stat.about.version import PYPI_VERSION_INFO, PyPiVersionInfo
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type
from typing import Type
from inspy_hard_stat.cli.arguments.meta import SingletonMeta
from inspy_hard_stat.cli.arguments.utils import is_argument_registered
from inspy_hard_stat.config.developer import DEV_MODE
from inspy_hard_stat.log_engine.config import LOGGER_CONFIG


class IHSParser(metaclass=SingletonMeta):
    """
    Singleton class for the main argument parser.
    This is the core shared library used across multiple executables.
    """

    def __init__(self, prog: str, description: str):
        self.parser = ArgumentParser(prog=prog, description=description)
        self.subparsers = None
        self._configured = False

    @property
    def universal_arguments(self) -> ArgumentParser:
        """Return the universal argument parser."""
        if not is_argument_registered(self.parser, '-l'):
            self.parser.add_argument(
                    '-l', '--log-level'
                    )
        return self.parser

    def register_arguments(self, register_func):
        """Register arguments by passing a function that configures the parser."""
        if not self._configured:
            register_func(self.parser)
            self._configured = True

    def parse_args(self) -> Namespace:
        """Parse the command-line arguments and return the result."""
        return self.parser.parse_args()


def build_main_parser(parser: ArgumentParser) -> IHSParser:
    pass



class BaseSubcommand:
    """
    Base class for subcommands.
    Each subclass should implement the 'add_subcommand' method.
    """

    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.add_subcommand()

    def add_subcommand(self):
        """Method to be overridden by subclasses to add their specific subcommand."""
        raise NotImplementedError("Subclasses must implement this method.")


class ParsedArgs:
    """
    A class to handle argument parsing for the Inspy-Hard-Stat command-line tool.

    Attributes:
        parser (ArgumentParser): An argument parser for the command-line interface.
    """

    DEVELOPER_MODE = DEV_MODE
    VALID_LOG_LEVELS = LOG_LEVELS + [level.lower() for level in LOG_LEVELS]

    def __init__(self, prog, description, ver_obj):
        """
        Instantiate the argument parser.

        Parameters:
            prog (str):
                The name of the program.

            description (str):
                A description of the program.

            ver_obj (PyPiVersionInfo):
                An object representing the version information.

        Properties:
            parser (ArgumentParser):
                A prepared :class:`argparse.ArgumentParser` object.
        """
        self.__parsed = None
        self.__parser = None

        self.parser = ArgumentParser(prog, description)
        self.__subcommands = self.parser.add_subparsers(dest='subcommand', title='Sub-Commands')

        self.register_core_arguments(ver_obj)
        self.load_subcommands()
        self.handle_dev_mode()

    def handle_dev_mode(self):
        """
        Handle the developer mode arguments.

        Returns:
            None
        """
        if self.DEVELOPER_MODE.is_enabled:
            self.DEVELOPER_MODE.args_parser = self
            self.DEVELOPER_MODE.add_developer_commands_to_parser(self.parser)

    @property
    def parsed_args(self):
        """
        Parse the command-line arguments and return the result.

        Returns:
            Namespace:
                The parsed command-line arguments.
        """
        if self.__parsed is None:
            self.__parsed = self.parser.parse_args()
        return self.__parsed

    @property
    def parser(self):
        """
        ArgumentParser: An argument parser for the command-line interface.
        """
        return self.__parser

    @parser.setter
    @validate_type(ArgumentParser)
    def parser(self, new):
        self.__parser = new

    @property
    def subcommands(self):
        return self.__subcommands

    def parse_args(self):
        """
        Parse the command-line arguments and return the result.

        Returns:
            Namespace:
                The parsed command-line arguments.
        """
        return self.parsed_args

    def register_core_arguments(self, ver_obj: PyPiVersionInfo):
        """
        Register the core arguments for the argument parser.

        Parameters:
            ver_obj (PyPiVersionInfo):
                An object representing the version information.

        Returns:
            None
        """
        self.parser.add_argument(
            '-l', '--log-level',
            choices=self.VALID_LOG_LEVELS,
            default='info'
        )

        self.parser.add_argument('-V', '--version', action='version', version=str(ver_obj))

        self.parser.add_argument(
            '-C', '--config-filepath',
            action='store',
            type=str,
            help='The path of a currently existing config file or where you want a new one written to.',
            default='~/Inspyre-Softworks/Inspy-Hard-Stat/config/config.ini'
        )

        self.parser.add_argument(
            '-S', '--silence-log-start',
            required=False,
            help='Do not let the logger print its initialization information.',
            action='store_true',
            default=False
        )

        self.parser.add_argument(
            '-r', '--use-rich',
            required=False,
            help='Use the Rich library for output formatting.',
            action='store_true',
            default=False
        )

    def load_subcommands(self):
        """
        Create sub-commands for the passed :class:`argparse.ArgumentParser` object.

        Returns:
            ArgumentParser:
                The same object that was passed but with the following sub-commands:

                - get-public:
                    Return the external IP to the command-line and nothing else.

                - get-host:
                    Return the hostname to the command-line and nothing else.

                - get-local:
                    Return the local IP-Address to the command-line and nothing else.

                - get-all:
                    Return the public IP, private IP, and hostname to the command-line and immediately exit.

                - print-version-info:
                    Print a pretty table of the version information for this program.
        """
        self.parser.add_subparsers()
