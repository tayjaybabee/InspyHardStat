from platformdirs import AppDirs

from inspy_hard_stat.about import __AUTHOR__, __PROG_NAME__

APP_DIRS = AppDirs(appname=__PROG_NAME__, appauthor=__AUTHOR__)

CONFIG_SYSTEM_NAMES = [
        'serial',
        'logger',
        'alternate_dirs',
        'developer_mode'
        ]

FILE_SYSTEM_DEFAULTS = {
        'dirs':  {
                'cache':  APP_DIRS.user_cache_path,
                'config': APP_DIRS.user_config_path,
                'data':   APP_DIRS.user_data_path,
                'log':    APP_DIRS.user_log_path,
                'temp':   APP_DIRS.user_cache_path,
                },
        'files': {
                'cache':                 APP_DIRS.user_cache_path / 'cache.ini',
                'alternate_dirs': APP_DIRS.user_cache_path / 'alternate_dirs.json',

                'config':                {

                        'logger': APP_DIRS.user_config_path / 'logger.ini',
                        'core':   APP_DIRS.user_config_path / 'core.ini',
                        'serial': APP_DIRS.user_config_path / 'serial.ini',
                        'lhm':    APP_DIRS.user_config_path / 'lhm.ini',

                        },

                'log':                   APP_DIRS.user_log_path / 'log.ini',
                },
        }
