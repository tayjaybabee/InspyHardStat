from inspy_logger import InspyLogger, Loggable
from inspy_logger.constants import LEVELS as LOG_LEVELS
from sys import argv


if '--dev-mode' in argv:
    ROOT_LOGGER = InspyLogger('inspy-hard-stat', console_level='debug',)
    ROOT_LOGGER.debug('Development mode enabled.')
else:
    ROOT_LOGGER = InspyLogger('inspy-hard-stat', console_level='info')


__all__ = [
        'Loggable',
        'ROOT_LOGGER'
        ]
