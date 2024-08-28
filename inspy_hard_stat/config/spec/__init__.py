import json
from dataclasses import dataclass, asdict
from pathlib import Path


CONFIG_SYSTEM_NAMES = [
    'logger',
    'serial',
    'alternate_dirs',
    'lhm',
    'developer_mode'
]


def get_file_dir():
    return Path(__file__).parent


@dataclass(frozen=True)
class SpecFiles:
    logger:         Path = get_file_dir().joinpath('logger_config.json')
    alternate_dirs: Path = get_file_dir().joinpath('alternate_dirs_config.json')
    serial:         Path = get_file_dir().joinpath('serial_config.json')
    lhm:            Path = get_file_dir().joinpath('lhm_config.json')
    developer_mode: Path = get_file_dir().joinpath('developer_mode_config.json')


SPEC_FILE_PATHS = SpecFiles()


class ConfigSpec:
    SPEC_DIR = get_file_dir()

    SPEC_FILE_PATHS = asdict(SpecFiles())

    _instances = {}

    def __new__(cls, config_system):

        config_system = config_system.lower()

        if config_system not in cls._instances:
            instance = super(ConfigSpec, cls).__new__(cls)
            cls._instances[config_system] = instance

        return cls._instances[config_system]

    def __init__(self, config_system, skip_auto_load=False):

        config_system = config_system.lower()

        if not hasattr(self, '_initialized'):
            self._initialized = True
            self.__config_system = None
            self.__defaults = None
            self.__file_path = None
            self.__spec = None

            self.config_system = config_system

            if not skip_auto_load:
                self.spec

    @property
    def config_system(self):

        return self.__config_system

    @config_system.setter
    def config_system(self, new):

        if new.lower() not in CONFIG_SYSTEM_NAMES:
            from inspy_hard_stat.config.errors import InvalidConfigSystemError

            raise InvalidConfigSystemError(new, CONFIG_SYSTEM_NAMES)
        self.__config_system = new

    @property
    def defaults(self):

        if not self.__defaults and self.__spec:
            self.__defaults = self._extract_defaults()

        return self.__defaults

    @property
    def file_path(self):

        if not self.__file_path and self.config_system:
            self.__file_path = getattr(SPEC_FILE_PATHS, self.config_system)
        return self.__file_path

    @property
    def spec(self):

        if not self.__spec and self.file_path:
            self.__spec = self._load_spec_from_file()

        return self.__spec

    def _load_spec_from_file(self) -> dict:
        """
        Load the JSON file containing the configuration specification.

        Returns:
            dict: The JSON data loaded from the file.
        """

        with open(self.file_path, 'r') as f:
            return json.load(f)

    def _extract_defaults(self) -> dict:
        """
        Extract default values from the configuration specification.

        Returns:
            dict: A dictionary of default values from the configuration specification.
        """
        defaults = {}

        for key, value in self.spec.items():
            default_value = value.get('default', '')
            defaults[key] = str(default_value) if default_value is not None else ''

        return defaults

    def __str__(self):

        return json.dumps(self.spec, indent=4)

    def __repr__(self):

        return f'<ConfigSpec: {self.config_system} | @{hex(id(self))}>'


def are_specs_loaded():
    return hasattr(globals(), 'CONFIG_SPECS')


def get_config_specs():
    if not are_specs_loaded():
        globals()['CONFIG_SPECS'] = {}
        for system in CONFIG_SYSTEM_NAMES:
            globals()['CONFIG_SPECS'][system] = ConfigSpec(system)

    return globals()['CONFIG_SPECS']


if not are_specs_loaded():
    CONFIG_SPECS = get_config_specs()
    del get_config_specs
    del are_specs_loaded

__all__ = [
        'ConfigSpec',
        'CONFIG_SPECS',

        ]
