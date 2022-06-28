"""
This package provides utility for writing to the terminal as if it were a screen.
"""

__version__ = '1.0'

import os
import sys
#pip
import colorama as col
from colorama import win32


#colors
COLOR_BLACK = 0
COLOR_RED = 1
COLOR_GREEN = 2
COLOR_YELLOW = 3
COLOR_BLUE = 4
COLOR_MAGENTA = 5
COLOR_CYAN = 6
COLOR_WHITE = 7
COLOR_RESET = 9
#extra colors
COLOR_LIGHTBLACK = 60
COLOR_LIGHTRED = 61
COLOR_LIGHTGREEN = 62
COLOR_LIGHTYELLOW = 63
COLOR_LIGHTBLUE = 64
COLOR_LIGHTMAGENTA = 65
COLOR_LIGHTCYAN = 66
COLOR_LIGHTWHITE = 67
#styles
STYLE_BRIGHT    = 1
STYLE_DIM       = 2
STYLE_NORMAL    = 22


class Text_style:
    def __init__(self, fore_color=COLOR_RESET, back_color=COLOR_RESET, text_type=STYLE_NORMAL):
        self.fore_color = int(fore_color)
        self.back_color = int(back_color)
        self.text_type = int(text_type)


class Screen:

    _INITIALISED = False
    MIN_WIDTH = 15
    _MIN_WIDTH_VSC = 30
    MIN_HEIGHT = 1


    def __init__(self, width:int=None, height:int=None, default_style:Text_style=None, title:str=None, in_terminal=True):
        self._INITIALISED = True
        col.init()
        if not in_terminal:
            self.MIN_WIDTH = self._MIN_WIDTH_VSC
        # set size
        if width == None:
            width = os.get_terminal_size().columns
        if height == None:
            height = os.get_terminal_size().lines
        self.set_width(width)
        self.set_height(height)
        self.change_size()
        if default_style == None:
            default_style = Text_style()
        self.default_style = default_style
        if title != None:
            self.change_title(title)
    

    def __del__(self):
        if self._INITIALISED:
            self.deinit()


    def deinit(self):
        if self._INITIALISED:
            self._INITIALISED = False
            self.__del__()
            self.reset()
            col.deinit()
    

    def reset_color(self):
        self.default_style.fore_color = COLOR_RESET
        self.default_style.back_color = COLOR_RESET
        self.default_style.text_type = STYLE_NORMAL
        sys.stdout.write(col.Style.RESET_ALL)


    def reset(self):
        self.reset_color()
        self.move_cursor(0, self.height)


    def set_width(self, width:int):
        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
        self.width = width
    

    def set_height(self, height:int):
        if height < self.MIN_HEIGHT:
            height = self.MIN_HEIGHT
        self.height = height


    def change_size(self):
        """
        This is the only method that changes the terminal size, becouse changing it will clear all text.
        """
        os.system(f"mode {self.width}, {self.height}")
    

    def change_title(self, title:str):
        win32.SetConsoleTitle(str(title))


    def _convert_color(self, color:int):
        colors = [COLOR_BLACK, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE, COLOR_LIGHTBLACK, COLOR_LIGHTRED, COLOR_LIGHTGREEN, COLOR_LIGHTYELLOW, COLOR_LIGHTBLUE, COLOR_LIGHTMAGENTA, COLOR_LIGHTCYAN, COLOR_LIGHTWHITE]
        colors_mapped = ["0", "4", "2", "6", "1", "5", "3", "7", "8", "C", "A", "E", "9", "D", "B", "F"]
        try:
            return colors_mapped[colors.index(color)]
        except ValueError:
            return colors_mapped[0]


    def _change_terminal_color(self):
        f_color = self._convert_color(self.default_style.fore_color)
        b_color = self._convert_color(self.default_style.back_color)
        os.system(f"color {b_color}{f_color}")


    def change_default_color(self, fore_color:int=None, back_color:int=None, style:int=None):
        """
        Changes the default text/background color + text style, for color afer a rendered text object, and the default terminal color.\n
        Changes ALL previously printed text's colors.
        """
        # Background color overrides foreground color in vscode.
        if fore_color != None:
            self.default_style.fore_color = fore_color
        if back_color != None:
            self.default_style.back_color = back_color
        if style != None:
            self.default_style.text_type = style
        self._change_terminal_color()


    def change_color(self, fore_color:int=None, back_color:int=None, style=STYLE_NORMAL):
        # Background color overrides foreground color in vscode.
        if fore_color != None:
            sys.stdout.write(f"\x1b[{30 + fore_color}m")
        if back_color != None:
            sys.stdout.write(f"\x1b[{40 + back_color}m")
        sys.stdout.write(f"\x1b[{style}m")
    

    def move_cursor(self, x:int, y:int):
        sys.stdout.write(f"\x1b[{y+1};{x+1}H")
    

    # cursor_pos = win32.GetConsoleScreenBufferInfo().dwCursorPosition
    def write_to(self, text:str, x:int, y:int, wrap=True):
        if wrap:
            self.move_cursor(min(x, self.width - 1), min(y, self.height - 1))
            sys.stdout.write(text)
        else:
            if x + 1 < self.width and y + 1 < self.height:
                self.move_cursor(x, y)
                if self.width - (x + len(text)) < 0:
                    sys.stdout.write(text[:(self.width - (x + len(text)))])
                else:
                    sys.stdout.write(text)


class Screen_text:
    def __init__(self, text:str, x:int, y:int, wrap=False, style:Text_style=None):
        self.text = str(text)
        self.x = int(x)
        self.y = int(y)
        self.wrap = bool(wrap)
        if style == None:
            style = Text_style()
        self.style = style
    
    def display(self, screen:Screen):
        screen.change_color(self.style.fore_color, self.style.back_color, self.style.text_type)
        screen.write_to(self.text, self.x, self.y, self.wrap)


def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')


def color_test():
    sc_test = Screen(title="Color test")
    sc_test.move_cursor(1, 2)
    print(end="##################")
    sc_test.move_cursor(1, 3)
    print(end="#")
    colors = [COLOR_BLACK, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE, COLOR_LIGHTBLACK, COLOR_LIGHTRED, COLOR_LIGHTGREEN, COLOR_LIGHTYELLOW, COLOR_LIGHTBLUE, COLOR_LIGHTMAGENTA, COLOR_LIGHTCYAN, COLOR_LIGHTWHITE]
    for color in colors:
        sc_test.change_color(None, color)
        print(end=" ")
    sc_test.change_color(None, COLOR_RESET)
    print(end="#")
    sc_test.move_cursor(1, 4)
    print(end="##################")
    sc_test.deinit()


if __name__ == "__main__":
    sc = Screen(title="test")
    print(sc.width, sc.height)
    sc.reset()
    #print("here")
    sc.deinit()
    input()
