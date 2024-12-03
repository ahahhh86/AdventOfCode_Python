"""
simple functions to make the console output more colorful
"""

def get_color(name: str) -> str:
    """
    translates a color name into the ANSI escape sequence
    invalid input return the default color
    :param name: name of the color
    :type name: str
    :return: ANSI escape sequence
    :rtype: str
    """
    color_switch = {
        'red': '\033[31m',
        'green': '\033[32m',
        'yellow': '\033[33m',
        'blue': '\033[34m',
        'magenta': '\033[35m',
        'cyan': '\033[36m',
        'white': '\033[37m',
        'reset': '\033[0m',
    }

    if name in color_switch:
        return color_switch[name]
    else:
        return color_switch['reset']


def str_colored(value: str, color: str, default: str = 'reset') -> str:
    """
    changes the color of a string and returns to the default color at the end
    :param value: string to change color
    :type value: str
    :param color: name of the color (see get_color())
    :type color: str
    :param default: name of the default color
    :type default: str
    :return: value in another color
    :rtype: str
    """
    return f'{get_color(color)}{value}{get_color(default)}'


def print_colored(value: str, color: str) -> None:
    """
    prints a string in another color
    :param value: string to change color
    :type value: str
    :param color: name of the color (see get_color())
    :type color: str
    :return: value in another color
    :rtype: str
    """
    print(str_colored(value, color))
