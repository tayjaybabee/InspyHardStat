from inspy_hard_stat.utils import return_wanted
from inspy_hard_stat.config.factory import ConfigFactory
from inspy_hard_stat.config.constants import DEFAULT_DIRS
from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type
from typing import Optional


# Create a singleton class to handle alternate directories
class AlternateDirs:
    _INSTANCE = None
    CONFIG = ConfigFactory('alternate_dirs', auto_load=True)
    CACHE = CONFIG.config
    DEFAULT_DIRS = DEFAULT_DIRS

    def __new__(cls, *args, **kwargs):
        if cls._INSTANCE is None:
            cls._INSTANCE = super().__new__(cls)
        return cls._INSTANCE

    def __init__(self):
        if not hasattr(self, '_initialized'):
            if not self.CACHE.has_section('USER'):
                self.CACHE.add_section('USER')

            self._dirs = None

            # Dynamically create the properties for each option in the 'USER' section
            for key in self.directories.keys():

                # Create a getter for the property
                getter = self._create_getter(key)

                # Create a setter for the property
                setter = self._create_setter(key)

                # Dynamically assign the property to the class
                setattr(self.__class__, key, property(getter, setter))

            self._initialized = True

    @property
    def cache(self):
        """
        Alias for the CACHE attribute.

        Returns:
            ConfigFactory:
                The ConfigFactory object for the alternate directories.
        """
        return self.CACHE

    @property
    def config(self):
        """
        Alias for the CONFIG attribute.

        Returns:
            ConfigParser:
                The ConfigParser object for the alternate directories.
        """
        return self.CONFIG

    @property
    def directories(self) -> dict:
        """
        The important directories to the application and their location if not the default.

        Returns:
            dict

        """
        if not self._dirs and self.CACHE.has_section('USER'):
            self._dirs = {key: value for key, value in self.CACHE.items('USER')}

        return self._dirs

    @property
    def dirs(self):
        return self.directories

    def _create_getter(self, key):
        """
        Create a getter for the given key from the directories dictionary.

        Parameters:
            key (str):
                The key to create a getter for.

        Returns:
            function:
                The getter function for the given key.

        """
        def getter(instance):
            return instance.directories.get(key, None)
        return getter

    def _create_setter(self, key):
        """
        Create a setter for the given key from the directories dictionary.

        Parameters:
            key (str):
                The key to create a setter for.

        Returns:
            function:
                The setter function for the given key.

        """
        def setter(instance, value):
            instance.directories[key] = value
            setattr(instance.config, key, value)
        return setter

    def __getattr__(self, name):
        # Use `__dict__` to avoid infinite recursion
        if 'directories' in self.__dict__ and name in self.directories:
            return self.directories[name]

        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        # To handle setting attributes in directories
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self.directories[name] = value
            setattr(self.config, name, value)

    def __iter__(self):
        return iter(self.directories.items())


class ADDict(dict, AlternateDirs):
    def __init__(self, *args, **kwargs):
        # Initialize the AlternateDirs part of the class
        AlternateDirs.__init__(self)

        # Initialize the dictionary with any provided key-value pairs
        dict.__init__(self, return_wanted(self))

    def __getattr__(self, name):
        """Allow access to dictionary values as attributes."""
        # First check if the attribute is part of the dictionary
        if name in self:
            return self[name]

        # Otherwise, fall back to normal attribute lookup
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __setattr__(self, name, value):
        """
        Override __setattr__ to store values in the dictionary and keep them
        in sync with the config object (if AlternateDirs uses it).
        """
        if name.startswith('_'):
            # Internal attributes should be set normally, not as dict items
            super().__setattr__(name, value)
        else:
            # Set the dictionary item
            self[name] = value

            # If the config attribute exists, sync the value to the config
            if hasattr(self, 'config'):
                setattr(self.config, name, value)

    def __iter__(self):
        """Allow iteration over the dictionary's key-value pairs."""
        return iter(self.items())


# Create an instance of the AlternateDirs class
ALTERNATE_DIRS = AlternateDirs()

AD_DICT = ADDict()


# Create a function to get the alternate directories
def get_alternate_dirs():
    """
    Get the alternate directories.

    Returns:
        dict:
            The alternate directories.
    """
    return ALTERNATE_DIRS.directories


def alternate_dir_assigned():
    """
    Check if any alternate directories have been assigned.

    Returns:
        bool:
            True if any alternate directories have been assigned, otherwise False.
    """
    return any(ALTERNATE_DIRS.directories.values())


def alternate_dirs_assigned() -> Optional[list[dict]]:
    """
    Return a list of dictionaries containing the alternate directories that have been assigned.

    Returns:
        Optional(list[dict]):
            A list of dictionaries containing the alternate directories that have been assigned, or None if no alternate
            directories have been assigned.
    """
    if not alternate_dir_assigned():
        return None

    return [{item: value} for (item, value) in ALTERNATE_DIRS.directories.items() if value]
