from inspyre_toolbox.sys_man.operating_system.checks import is_windows


if is_windows():
    from inspy_hard_stat.crypt.win32 import *
