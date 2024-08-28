"""
This module contains the SingletonMeta class.

Classes:
    SingletonMeta

Functions:
    None

Exceptions:
    None

Decorators:
    None

Misc Variables:
    None

Since:
    1.0.0
"""

class SingletonMeta(type):
    """A thread-safe implementation of Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Create a new instance of the class if it does not already exist.

        Parameters:
            *args:
            **kwargs:

        Returns:
            cls:
                The instance of the class.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
