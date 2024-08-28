import hashlib
import os
import atexit
from inspy_hard_stat.log_engine import Loggable
from inspy_hard_stat.config import MOD_LOGGER as PARENT_LOGGER
import sys

MOD_LOGGER = PARENT_LOGGER.get_child('developer')


class DeveloperMode(Loggable):
    FILE_PATH = os.path.expanduser('~/marauders_map.txt')
    PHRASE_HASH = '6f844a7353f3efaa4ed034307517e7539328f8a87d0c5e8c3ef092628f72f0f1'
    EXIT_PHRASE_HASH = '63c70ebaeea11709264f348698fdb8b6a064e24d90762bf00cb86fb7a39a6614'
    LOCK_FILE_PATH = os.path.expanduser('~/dev.lock')

    def __init__(self, parsed_args_class=None):
        """
        Initialize the DeveloperMode class and check for the existence of the developer mode
        file. If the file exists and contains the secret phrase, developer mode is enabled.
        """
        super().__init__(MOD_LOGGER)
        self.__args_parser = None
        self.__atexit_registered = False
        self.class_logger.debug('Checking for developer mode file...')
        self.__is_enabled = None
        if self.is_enabled:
            self.class_logger.info('Developer mode is enabled')
            if not self.is_locked:
                self.register_disable_event()
            self.class_logger.debug('Registered developer mode disablement on exit')

    @property
    def args_parser(self):
        """
        ip_reveal_headless.config.arguments.ParsedArgs:
            A property to get the argument parser.
        """
        return self.__args_parser

    @args_parser.setter
    def args_parser(self, new):
        """
        Set the argument parser.

        Args:
            new (ip_reveal_headless.config.arguments.ParsedArgs): The new argument parser.
        """
        self.__args_parser = new

    @property
    def atexit_registered(self):
        """
        bool:
            A property to check if the developer mode disablement event is registered.
        """
        return self.__atexit_registered

    @property
    def is_enabled(self):
        """
        bool:
            A property to check if developer mode is enabled.
        """
        if self.__is_enabled is None:
            self.is_enabled = self._check_file()
        return self.__is_enabled

    @is_enabled.setter
    def is_enabled(self, new):
        """
        Set the developer mode status.

        Args:
            new (bool): The new developer mode status.
        """
        if new and not self.__is_enabled:
            self.__is_enabled = self._check_file()
        elif not new and self.__is_enabled:
            self.__is_enabled = False
            self.disable()
            atexit.unregister(self._disable_developer_mode)
        else:
            self.__is_enabled = new

    @property
    def is_locked(self):
        """
        bool:
            A property to check if developer mode is locked.
        """
        return self._check_lock()

    def add_developer_commands_to_parser(self, parser=None):
        """
        Add developer mode commands to the provided parser.

        Args:
            parser (ArgumentParser): The parser to which the developer mode commands will be added.

        Returns:
            None
        """
        if parser is None:
            parser = self.args_parser.parser

        developer_group = parser.add_argument_group('Developer Mode')
        developer_group.add_argument(
            '--fake-version',
            action='store',
            help='Set a fake version number for the program',
        )

        subparsers = self.args_parser.subcommands

        if not self.is_locked:

            subparsers.add_parser(
                    'lock-dev-mode',
                    help='Lock developer mode, preventing it from being disabled on exit',
                    )

            developer_group.add_argument(
                '--lock-dev-mode',
                action='store_true',
                help='Lock developer mode into its current state, making dev-mode persistent across runs',
            )
        else:
            subparsers.add_parser(
                    'unlock-dev-mode',
                    help='Unlock developer mode, allowing it to be disabled on exit',
                    )

            developer_group.add_argument(
                '--unlock-dev-mode',
                action='store_true',
                help='Unlock developer mode, allowing it to be disabled on exit',
            )

        subparsers.add_parser(
                'get-dev-mode-status',
                help='Get the status of developer mode',
                )

    def disable(self):
        """
        Disable developer mode.

        Returns:
            None
        """
        log = self.create_logger()

        log.debug('Disabling developer mode...')
        self.is_enabled = False

        log.debug('Unregistering developer mode disablement on exit...')
        self.unregister_disable_event()

        self._disable_developer_mode()

    def handle_developer_args(self, args):
        """
        Handle the developer mode arguments.

        Args:
            args (Namespace): The arguments to be handled.

        Returns:
            None
        """
        from rich import print as rprint
        log = self.create_logger()

        if self.is_locked:

            if args.unlock_dev_mode:
                log.info('Unlocking developer mode...')
                self.unlock_developer_mode()
        elif args.lock_dev_mode:
            log.info('Locking developer mode...')
            self.lock_developer_mode()
            sys.exit()

        if args.subcommand == 'unlock-dev-mode':
            log.info('Unlocking developer mode...')
            self.unlock_developer_mode()
            sys.exit()
        elif args.subcommand== 'lock-dev-mode':
            log.info('Locking developer mode...')
            self.lock_developer_mode()
            sys.exit()
        elif args.subcommand == 'get-dev-mode-status':
            status = self.get_dev_mode_status()
            rprint(status)

            sys.exit()


        if args.fake_version:
            log.info(f'Setting fake version number: {args.fake_version}')
            self.set_fake_version(args.fake_version)

    def get_dev_mode_status(self, as_dict=False):
        log = self.create_logger()


        enabled_str = '[green][bold]enabled[/bold][/green]' if self.is_enabled else '[red][bold]disabled[/bold][/red]'
        log.debug(f'Developer mode is {enabled_str}')
        locked_str = '[red][bold]locked[/bold][/red]' if self.is_locked else ('[green][bold]unlocked[/bold]['
                                                                              '/green]')
        log.debug(f'Developer mode is {locked_str}')

        if as_dict:
            return {
                'enabled': self.is_enabled,
                'locked': self.is_locked,

                    }
        return f'\n[cyan]Developer mode[/cyan] is {enabled_str} and {locked_str}\n'

    def lock_developer_mode(self):
        """
        Create a 'dev.lock' file to lock developer mode into its current state.

        Returns:
            None
        """
        with open(self.LOCK_FILE_PATH, 'w') as file:
            file.write('Developer mode is locked')

        self.unregister_disable_event()

    def unlock_developer_mode(self):
        """
        Remove the 'dev.lock' file to unlock developer mode.

        Returns:
            None
        """
        log = self.create_logger()

        log.debug('Checking if locked...')
        if self.is_locked:
            log.info('Unlocking developer mode...')
            os.remove(self.LOCK_FILE_PATH)
            log.debug(f'Removed {self.LOCK_FILE_PATH}, dev-mode unlocked!')
            log.warning('Developer mode is now unlocked, leaving the program before locking it again will disable '
                        'dev-mode!')

        self.register_disable_event()

    def register_disable_event(self):
        """
        Register the event that disables developer mode.

        Returns:
            None
        """
        log = self.create_logger()

        if self.atexit_registered:
            log.warning('Developer mode disable event is already registered')

        if self.is_locked:
            log.debug('Developer mode is locked, not registering disable event')
            return

        atexit.register(self._disable_developer_mode)

        log.info(
                'Registered developer mode disable event, developer mode will be disabled on exit, to prevent this, '
                'run the program with --lock-dev-mode'
                 )

        self.__atexit_registered = True

    def unregister_disable_event(self):
        """
        Unregister the event that disables developer mode.

        Returns:
            None
        """
        if not self.atexit_registered:
            self.warning('Developer mode disable event is not registered')
            return

        atexit.unregister(self._disable_developer_mode)

        self.__atexit_registered = False

    def _check_file(self):
        """
        Check for the existence of the developer mode file and its contents.

        Returns:
            bool:
                True if the developer mode file exists and contains the secret phrase, False otherwise.
        """
        log = self.create_logger()
        log.debug('Checking for developer mode file...')
        if os.path.exists(self.FILE_PATH):
            log.debug('Developer mode file exists')
            with open(self.FILE_PATH, 'r') as file:
                content = file.read().strip()
                log.debug('Checking developer mode file contents for secret phrase...')
                if hashlib.sha256(content.encode()).hexdigest() == self.PHRASE_HASH:
                    log.debug('Developer mode file contains secret phrase')
                    return True
                else:
                    log.debug('Developer mode file does not contain secret phrase')
                    return False
        else:
            log.debug('Developer mode file does not exist')
        return False

    def _check_lock(self):
        """
        Check for the existence of the developer mode lock file.

        Returns:
            bool:
                True if the developer mode lock file exists, False otherwise.
        """
        log = self.create_logger()
        log.debug('Checking for developer mode lock file...')

        return os.path.exists(self.LOCK_FILE_PATH)


    def _disable_developer_mode(self):
        """
        Disable developer mode by writing "Mischief managed" to the developer mode file.

        Returns:
            None
        """
        log = self.create_logger()
        log.info('Disabling developer mode...')
        with open(self.FILE_PATH, 'w') as file:
            log.debug('Writing disable phrase to developer mode file...')
            file.write(self.EXIT_PHRASE_HASH)
        log.info('Developer mode disabled')


DEV_MODE = DeveloperMode()
