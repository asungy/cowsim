import colorama

colorama.init()

# Foreground colors
FORES = {
    "black": colorama.Fore.BLACK,
    "blue": colorama.Fore.BLUE,
    "cyan": colorama.Fore.CYAN,
    "green": colorama.Fore.GREEN,
    "magenta": colorama.Fore.MAGENTA,
    "red": colorama.Fore.RED,
    "white": colorama.Fore.WHITE,
    "yellow": colorama.Fore.YELLOW,
}

# Background colors
BACKS = {
    "black": colorama.Back.BLACK,
    "blue": colorama.Back.BLUE,
    "cyan": colorama.Back.CYAN,
    "green": colorama.Back.GREEN,
    "magenta": colorama.Back.MAGENTA,
    "red": colorama.Back.RED,
    "white": colorama.Back.WHITE,
    "yellow": colorama.Back.YELLOW,
}

# Stylizing options
BRIGHTNESS = {
    "bright": colorama.Style.BRIGHT,
    "dim": colorama.Style.DIM,
    "normal": colorama.Style.NORMAL,
}


def color_string(content, color, brightness=BRIGHTNESS["normal"]) -> None:
    return f"{brightness}{color}{content}{colorama.Style.RESET_ALL}"
