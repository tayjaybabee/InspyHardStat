from inspyre_toolbox.ver_man import PyPiVersionInfo
from inspyre_toolbox.ver_man.helpers import get_version_from_file
from pathlib import Path


VERSION_FILE_PATH = Path(__file__).parent.joinpath('VERSION')

VERSION_INFO = get_version_from_file(VERSION_FILE_PATH)

PYPI_VERSION_INFO = PyPiVersionInfo('inspy-hard-stat')
