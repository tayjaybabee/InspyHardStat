"""
Utility functions for working with argparse arguments.

Functions:
    is_argument_registered

Since:
    1.0.0
"""

from argparse import ArgumentParser

def is_argument_registered(parser: ArgumentParser, argument: str) -> bool:
    """
    Check if an argument is already registered with the ArgumentParser.

    Parameters:
        parser (ArgumentParser): The argument parser to check.
        argument (str): The argument to check, e.g., '--log-level'.

    Returns:
        bool: True if the argument is already registered, False otherwise.
    """
    for action in parser._actions:
        if argument in action.option_strings:
            return True
    return False
