import traceback
from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class RichRenderableError(Exception):
    """
    Base class for errors that can be rendered using the Rich library. This class provides a common method to render
    exceptions in a visually appealing way.
    """

    DIVIDER_OPTS = {
            'text':  f'\n{"-" * 30}\n',
            'style': 'bold green'
            }
    DIVIDER_PAIR = (DIVIDER_OPTS['text'], DIVIDER_OPTS['style'])
    SECTION_DIVIDER = Text(*DIVIDER_PAIR)

    @property
    def file_raised(self):
        return self.get_file_raised()

    @property
    def line_number(self):
        return self.get_line_number()

    def find_frame(self):
        tb = traceback.extract_stack()
        for frame in reversed(tb):
            if 'errors' not in frame.filename:
                return frame
        return None

    def get_file_raised(self):
        if frame := self.find_frame():
            return frame.filename

    def get_line_number(self):
        if frame := self.find_frame():
            return frame.lineno

    def __init__(self, message: str = None, code: int = 0):
        super().__init__(message or 'An error occurred')

        self.render()

    def build_additional_info(self):
        """
        Builds the additional information to be displayed with the error.
        """
        message = None
        if hasattr(self, 'info_collection') and len(self.info_collection) > 0:
            for info in self.info_collection:
                message += f'    - {info}\n'

        return message or self.additional_info

    def get_additional_renderable(self):
        line_number, file_name = self.line_number, self.file_raised
        assembled = [
                self.SECTION_DIVIDER,
                Text('\nAdditional Information:\n', 'italic cyan'),
                Text(f'\n    {self.build_additional_info()}\n', 'yellow'),
                self.SECTION_DIVIDER,
                Text('Error Information:', 'italic cyan'),
                Text(f'\n    File Raised: {file_name}', 'yellow'),
                Text(f'\n    Line Number: {line_number}', 'yellow'),
                ]

        return assembled

    def render(self):
        """
        Render the exception using the Rich library.
        """

        console = Console()
        console.print(self)

    def __rich_console__(self, console: Console, options: dict):
        error_title = Text(f"Exception Raised: {self.__class__.__name__}", style="bold red")
        text = [
                Text(f'Message: \n    {self.args[0]}\n', style="bold white"),
                ]

        if hasattr(self, 'additional_info'):
            text.extend(self.get_additional_renderable())

        # You can customize the Panel appearance here
        panel = Panel(Text.assemble(*text), title=error_title, border_style="bright_red", expand=False)

        yield panel



class InspyHardStatError(RichRenderableError):
    __base_message = 'An error occurred in the Inspy-Hard-Stat package.'
    __info_unavailable = 'No additional information is available.'

    def __init__(self, message=None, code=0):
        """Initializes the InspyHardStatError with an optional message and code."""
        print(self.__class__.__name__)
        self.__info_collection = []
        self._additional_info = message if message is not None else self.__info_unavailable
        self.__code = code
        self.__message = self.build_message()
        super().__init__(self.__message, self.__code)

    @property
    def additional_info(self):
        """Returns additional information about the error."""
        return self._additional_info

    @additional_info.setter
    def additional_info(self, new_info):
        """Sets additional information about the error."""
        self.__info_collection.append(new_info)

    @property
    def code(self):
        """Returns the error code."""
        return self.__code

    @property
    def info_collection(self):
        """Returns the collection of additional information."""
        return self.__info_collection

    def build_message(self):
        """Constructs the full error message."""
        return f'{self.__base_message}\n\n{(" " * 4)}{self.__class__.__name__}'
