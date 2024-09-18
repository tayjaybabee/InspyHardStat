from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type
from inspy_hard_stat.config import ConfigFactory
from inspy_hard_stat.utils import search_file_for_user_line, get_provisioned_path_str
from warnings import warn
from dataclasses import dataclass
from pathlib import Path


CONFIG = ConfigFactory('lhm', auto_load=True)


def check_config():
    """
    Check the configuration file for the user's name.

    Returns:
        bool: True if the user's name is found in the configuration file, False otherwise.
    """
    user_line = search_file_for_user_line(CONFIG.config_file_path)

    if not user_line and CONFIG.loaded_config:
        warn('Config is loaded but hasn\'t been updated with user information.')
        return False
    elif not user_line and not CONFIG.loaded_config:
        warn('Config is not loaded and user information is missing.')
        return False
    elif user_line and not CONFIG.loaded_config:
        warn('Config file contains user configuration but is not loaded.')
        return False

    return True


@dataclass
class Config:
    def __init__(self, config: ConfigFactory = CONFIG):
        self.__config = None
        self.config = config

    @property
    def auto_start(self):
        if self.config:
            return self.config.auto_start

    @auto_start.setter
    @validate_type(bool)
    def auto_start(self, new):
        if self.config:
            self.config.auto_start = new

    @property
    def config(self):
        return self.__config

    @config.setter
    @validate_type(ConfigFactory)
    def config(self, new):
        self.__config = new
        check_config()

    @property
    def executable_path(self):
        if self.config:
            return self.config.executable_path

    @executable_path.setter
    @validate_type(str, Path, preferred_type=str)
    def executable_path(self, new):
        if self.config:
            self.config.executable_path = get_provisioned_path_str(new)

    @property
    def host(self):
        if self.config:
            return self.config.host

    @host.setter
    @validate_type(str)
    def host(self, new):
        if self.config:

            if new.startswith('http://') or new.startswith('https://'):
                new = new.split('://')[1]

            if ':' in new:
                self.port = new.split(':')[-1].replace('/', '')
                new = new.split(':')[0]

            self.config.host = new

    @property
    def password(self):
        if self.config:
            return self.config.password

    @password.setter
    @validate_type(str)
    def password(self, new):
        if self.config:
            self.config.password = new

    @property
    def port(self):
        if self.config:
            return int(self.config.port)

    @port.setter
    @validate_type(int, str, preferred_type=int)
    def port(self, new):
        if self.config:
            self.config.port = str(new)

    @property
    def url(self):
        if self.config:
            return f'http://{self.host}:{self.port}'

    @property
    def user_name(self):
        if self.config:
            return self.config.user_name

    @user_name.setter
    @validate_type(str)
    def user_name(self, new):
        if self.config:
            self.config.user_name = new

    def __str__(self):
        return f"Config: {self.config}"

    def __repr__(self):
        return f"Config: {self.config}"
