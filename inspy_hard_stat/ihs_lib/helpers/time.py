from inspyre_toolbox.syntactic_sweets.classes.decorators.type_validation import validate_type

class   Seconds:

    def __init__(self, seconds, round_to=2):
        self.__seconds = None
        self.__round_to = None

        self.round_to = round_to
        self.seconds = seconds
    @property
    def greater_than_minute(self):
        return self.seconds >= 60

    @property
    def greater_than_hour(self):
        return self.seconds >= 3600

    @property
    def round_to(self):
        return self.__round_to

    @round_to.setter
    @validate_type(int)
    def round_to(self, new):
        self.__round_to = new

    @property
    def seconds(self):
        return self.__seconds

    @property
    def minutes(self):
        return round(self.seconds / 60, self.round_to)

    @property
    def hhmmss(self):
        return {
            'hours': self.seconds // 3600,
            'minutes': (self.seconds % 3600) // 60,
            'seconds': self.seconds % 60
        }

    @property
    def hours(self):
        return round(self.minutes / 60, self.round_to)

    @property
    def hours_and_minutes(self):
        return {
            'hours': self.minutes // 60,
            'minutes': self.minutes % 60
        }

    @property
    def hour_minute_string(self):
        hm = self.hours_and_minutes

        # -- Figure out the hours string.
        hours = round(hm['hours'], self.round_to)

        if hours.is_integer():
            hours = int(hours)

        hours_str = f"{hours} hour" if hours == 1 else f"{hours} hours"

        # -- If there are no minutes, return the hours string alone.
        if hm['minutes'] <= 0:
            return hours_str

        # -- Figure out the minutes string.
        minutes = round(hm['minutes'], self.round_to)

        if minutes.is_integer():
            minutes = int(minutes)

        minutes_str = f"{minutes} minute" if minutes == 1 else f"{minutes} minutes"

        # -- Return the result.
        return f"{hours_str}, and {minutes_str}"

    @seconds.setter
    @validate_type(int)
    def seconds(self, value):
        self.__seconds = value



def is_hour_or_greater(minutes) -> bool:
    """
    Check if the number of minutes is an hour or greater.

    Parameters:
        minutes (int):
            The number of minutes to check.

    Returns:
        bool:
            True if the number of minutes is an hour or greater; False otherwise.

    Examples:
        >>> is_hour_or_greater(60)
        True
        >>> is_hour_or_greater(59)
        False
    """
    return minutes >= 60

def minutes_to_hours(minutes, force_int=False, round_to=2, force=False) -> float:
    """
    Convert minutes to a float value representing hours.

    Parameters:
        minutes (int):
            The number of minutes to convert.

        force_int (bool):
            If True, the result will be rounded to the nearest integer. Optional; default is False.

        round_to (int):
            The number of decimal places to round to. Optional; default is 2. Ignored if :param:`force_int` is True.

        force (bool):
            If True, the result will include hours even if the minutes are less than 60. Optional; default is False.

    Returns:
        float:
            The number of hours.

    Examples:
        >>> minutes_to_hours(60)
        1.0
        >>> minutes_to_hours(90)
        1.5
        >>> minutes_to_hours(90, force_int=True)
        2
    """
    if not is_hour_or_greater(minutes) and not force:
        raise ValueError("Minutes must be greater than or equal to 60.")

    hours = minutes / 60

    if force_int:
        return round(hours)
    return round(hours, round_to)


def minutes_to_hours_and_minutes(minutes, force=False) -> dict:
    """
    Convert minutes to a string representing hours and minutes.

    Parameters:
        minutes (int):
            The number of minutes to convert.

        force (bool):
            If True, the result will include hours even if the minutes are less than 60. Optional; default is False.

    Returns:
        dict:
            A dictionary containing the hours and minutes.

    Examples:
        >>> minutes_to_hours_and_minutes(90)
        {'hours': 1, 'minutes': 30}

    """
    if not is_hour_or_greater(minutes) and not force:
        raise ValueError("Minutes must be greater than or equal to 60.")

    # Fill the dictionary with the hours and minutes.
    res = {
            'hours': minutes // 60,
            'minutes': minutes % 60
            }

    # Return the result.
    return res


def get_hour_minute_string(minutes, force=False) -> str:
    """
    Get a string representing hours and minutes.

    Parameters:
        minutes (int):
            The number of minutes to convert.

        force (bool):
            If True, the result will include hours even if the minutes are less than 60. Optional; default is False.

    Returns:
        str:
            A string representing the hours and minutes.

    Examples:
        >>> get_hour_minute_string(90)
        '1 hour, 30 minutes'
    """
    # Get the hours and minutes as a dictionary.
    hm = minutes_to_hours_and_minutes(minutes, force)

    # Get the hours and minutes as strings.
    hours_str = f"{hm['hours']} hour" if hm['hours'] == 1 else f"{hm['hours']} hours"
    minutes_str = f"{hm['minutes']} minute" if hm['minutes'] == 1 else f"{hm['minutes']} minutes"

    # Return the result.
    return f"{hours_str}, {minutes_str}"


def seconds_to_hours(seconds, force_int=False, round_to=2, force=False) -> float:
    """
    Convert seconds to a float value representing hours.

    Parameters:
        seconds (int):
            The number of seconds to convert.

        force_int (bool):
            If True, the result will be rounded to the nearest integer. Optional; default is False.

        round_to (int):
            The number of decimal places to round to. Optional; default is 2. Ignored if :param:`force_int` is True.

        force (bool):
            If True, the result will include hours even if the seconds are less than 60. Optional; default is False.

    Returns:
        float:
            The number of hours.

    Examples:
        >>> seconds_to_hours(3600)
        1.0
        >>> seconds_to_hours(5400)
        1.5
        >>> seconds_to_hours(5400, force_int=True)
        2
    """
    minutes = seconds / 60
    return minutes_to_hours(minutes, force_int, round_to, force)


__all__ = [
    'is_hour_or_greater',
    'minutes_to_hours',
    'minutes_to_hours_and_minutes',
    'get_hour_minute_string'
]
