"""

"""
from pathlib import Path
from inspy_hard_stat.log_engine import ROOT_LOGGER as PARENT_LOGGER
from inspy_hard_stat.config.spec import CONFIG_SPECS
from inspy_hard_stat.config.factory import ConfigFactory
from inspy_hard_stat.config.constants import FILE_SYSTEM_DEFAULTS


MOD_LOGGER = PARENT_LOGGER.get_child('config')


# Define the configuration systems, their specifications, and the default file paths for the configuration files for
# each system.
CONFIG_SYSTEMS = {
        'core':                  {
                'spec':    CONFIG_SPECS['serial'].file_path,
                'default': Path(FILE_SYSTEM_DEFAULTS['files']['config']['core']).expanduser().resolve().absolute()
                },
        'logger':                {
                'spec':    CONFIG_SPECS['logger'].file_path,
                'default': Path(FILE_SYSTEM_DEFAULTS['files']['config']['logger']).expanduser().resolve().absolute()
                },
        'alternate_dirs': {
                'spec':    CONFIG_SPECS['alternate_dirs'].file_path,
                'default': Path(FILE_SYSTEM_DEFAULTS['files']['alternate_dirs'])
                },
        }

# Load the configuration files for the alternate directories.
# This is for when the user has specified alternate directories for the cache, config, data, log, and temp directories,
# and the configuration file is not in the default location.
NON_DEFAULT_DIRS = ConfigFactory('alternate_dirs', auto_load=True)

if NON_DEFAULT_DIRS.config_dir:
    logger_config_dir = Path(NON_DEFAULT_DIRS.config_dir).expanduser().resolve().absolute()
else:
    logger_config_dir = CONFIG_SYSTEMS['logger']['default'].parent

LOGGER_CONFIG = ConfigFactory('logger', auto_load=True, config_dir_path = logger_config_dir)


if LOGGER_CONFIG.config.get('USER', 'log_level', fallback=None) and LOGGER_CONFIG.loaded_config:
    from inspy_hard_stat.log_engine import ROOT_LOGGER
    log_level = LOGGER_CONFIG.config.get('USER', 'log_level')
    ROOT_LOGGER.set_level(console_level=log_level)
