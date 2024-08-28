

def is_float_integer(value: float) -> bool:
    """
    Check if a float value is an integer.

    Parameters:
        value (float):
            The float value to check.

    Returns:
        bool:
            True if the float value is an integer; False otherwise.

    Examples:
        >>> is_float_integer(1.0)
        True
        >>> is_float_integer(1.1)
        False
    """
    return value.is_integer()
