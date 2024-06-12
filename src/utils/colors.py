from enum import Enum


class Color:
    BLACK = (0, 0, 0)
    DARK_BLUE = (0, 0, 170)
    DARK_GREEN = (0, 170, 0)
    DARK_CYAN = (0, 170, 170)
    DARK_RED = (170, 0, 0)
    DARK_MAGENTA = (170, 0, 170)
    ORANGE = (255, 170, 0)
    LIGHT_GRAY = (170, 170, 170)
    DARK_GRAY = (85, 85, 85)
    LIGHT_BLUE = (85, 85, 255)
    LIGHT_GREEN = (85, 255, 85)
    LIGHT_CYAN = (85, 255, 255)
    LIGHT_RED = (255, 85, 85)
    LIGHT_MAGENTA = (255, 85, 255)
    YELLOW = (255, 255, 85)
    WHITE = (255, 255, 255)


colors = {
    '0': Color.BLACK,
    '1': Color.DARK_BLUE,
    '2': Color.DARK_GREEN,
    '3': Color.DARK_CYAN,
    '4': Color.DARK_RED,
    '5': Color.DARK_MAGENTA,
    '6': Color.ORANGE,
    '7': Color.LIGHT_GRAY,
    '8': Color.DARK_GRAY,
    '9': Color.LIGHT_BLUE,
    'a': Color.LIGHT_GREEN,
    'b': Color.LIGHT_CYAN,
    'c': Color.LIGHT_RED,
    'd': Color.LIGHT_MAGENTA,
    'e': Color.YELLOW,
    'f': Color.WHITE
}
