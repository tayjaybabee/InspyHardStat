from pathlib import Path

BOOLEAN_VALUES = {
        'true': True,
        'false': False,
        'yes': True,
        'no': False,
        'on': True,
        'off': False,
        '1': True,
        '0': False,
        1: True,
        0: False,
        }



TYPE_MAPPING = {
        'str': str,
        'string': str,
        'int': int,
        'integer': int,
        'float': float,
        'bool': bool,
        'boolean': bool,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'frozenset': frozenset,
        'bytes': bytes,
        'bytearray': bytearray,
        'memoryview': memoryview,
        'path': Path,
        }


def bool_lookup(value):
    """
    Looks up a boolean value by name or value.

    Parameters:
        value:
            The value to look up.

    Returns:
        bool:
            The boolean value that corresponds to the given value.
    """
    return BOOLEAN_VALUES.get(value)


def type_lookup(type_name: str):
    """
    Looks up the type by name in the TYPE_MAPPING dictionary.

    Parameters:
        type_name (str):
            The name of the type to look up.

    Returns:
        type:
            The type object that corresponds to the given name.
    """
    return TYPE_MAPPING.get(type_name)


def convert_str_to_type(value: str, type_name: str):
    """
    Converts a string to the given type.

    Parameters:
        value (str):
            The value to convert.

        type_name (str):
            The name of the type to convert the value to.

    Returns:
        type:
            The converted value.
    """
    if type_name == 'bool':
        return bool_lookup(value)

    return type_lookup(type_name)(value)


def is_default_value(config, key, value):
    """
    Check if the value is the default value for the key in the configuration.

    Args:
        config (Config):
            The configuration object to check.
        key (str):
            The key to check.
        value:
            The value to check.

    Returns:
        bool: True if the value is the default value for the key in the configuration, False otherwise.
    """
    return config.config.get('DEFAULT', key) == value
