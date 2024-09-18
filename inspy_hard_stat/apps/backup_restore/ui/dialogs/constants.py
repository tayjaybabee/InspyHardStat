"""
This module contains constants for the dialogs used in the config restore app.

Attributes:

    DEFAULT_DIALOG_STYLE (Style):
        The default style for the dialog.

    DEFAULT_WARNING_STYLE (Style):
        The default style for the warning dialog.
"""
from prompt_toolkit.styles import Style


DEFAULT_DIALOG_STYLE = Style.from_dict({
    'dialog':            'bg:teal',
    'dialog.body':       'bg:grey fg:white',
    'dialog.shadow':     'bg:black',
    'dialog frame.label': 'bg:blue fg:white',  # Title
})


DEFAULT_WARNING_STYLE = Style.from_dict({
    'dialog':            'bg:teal',
    'dialog.body':       'bg:red fg:black bold',
    'dialog.shadow':     'bg:black',
    'dialog frame.label': 'bg:blue fg:white',  # Title
})
