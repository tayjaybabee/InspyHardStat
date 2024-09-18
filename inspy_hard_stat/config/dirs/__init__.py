from pathlib import Path
from inspy_hard_stat.config.factory import ConfigFactory
from inspy_hard_stat.config.constants import DEFAULT_DIRS


CACHE_DIR = Path(DEFAULT_DIRS['cache'])
CACHE_FP = CACHE_DIR.joinpath('cache.ini')

DEFAULT_CONFIG_DIR = Path(DEFAULT_DIRS['config'])

CONFIG_DIR = Path(DEFAULT_DIRS['config']) / 'lhm.ini' if not CACHE_FP.exists() else get_config_dir_from_cache()
