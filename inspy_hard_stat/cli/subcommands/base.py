class BaseSubcommand:
    """
    Base class for subcommands.
    Each subclass should implement the 'add_subcommand' method.
    """

    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.add_subcommand()

    def add_subcommand(self):
        """Method to be overridden by subclasses to add their specific subcommand."""
        raise NotImplementedError("Subclasses must implement this method.")
