def get_color(color: str) -> str:
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

    if color in color_switch:
        return color_switch[color]
    else:
        return color_switch['reset']



def str_colored(value: str, color: str, default: str = 'reset') -> str:
    return f'{get_color(color)}{value}{get_color(default)}'



def print_colored(value: str, color: str) -> None:
    print(str_colored(value, color))
