from enum import Enum, auto
from tkinter import CENTER

class Colors(Enum):
    BLACK       = 0
    RED         = 1
    GREEN       = 2
    YELLOW      = 3
    BLUE        = 4
    MAGENTA     = 5
    CYAN        = 6
    WHITE       = 7
    RESET       = 9
    DEFAULT     = -1
    #extra colors
    LIGHTBLACK  = 60
    LIGHTRED    = 61
    LIGHTGREEN  = 62
    LIGHTYELLOW = 63
    LIGHTBLUE   = 64
    LIGHTMAGENTA= 65
    LIGHTCYAN   = 66
    LIGHTWHITE  = 67


class Styles(Enum):
    BRIGHT      = 1
    DIM         = 2
    NORMAL      = 22
    DEFAULT     = -1


class Wrap_styles(Enum):
    LEFT    = auto()
    CENTER  = auto()
    RIGHT   = auto()
    UNDER   = auto()