"""
This package provides utility for writing to the terminal as if it were a screen.
"""

__version__ = '1.0'

import os
import sys
#pip
import colorama as col
# from colorama import win32


class Screen:

    INITIALISED = False
    MIN_WIDTH = 15
    MIN_WIDTH_VSC = 30
    MIN_HEIGHT = 1

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

    # ANSI esc chars

    def __init__(self, width:int=None, height:int=None, in_terminal=True):
        self.INITIALISED = True
        col.init()
        if not in_terminal:
            self.MIN_WIDTH = self.MIN_WIDTH_VSC
        # set size
        if width == None:
            width = os.get_terminal_size().columns
        if height == None:
            height = os.get_terminal_size().lines
        self.set_width(width)
        self.set_height(height)
        self.change_size()
    

    def __del__(self):
        if self.INITIALISED:
            self.deinit()


    def deinit(self):
        self.reset()
        if self.INITIALISED:
            self.INITIALISED = False
            self.__del__()
            col.deinit()
    

    def reset_color(self):
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


def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')


if __name__ == "__main__":
    sc = Screen(152, 25, False)
    print(sc.width, sc.height)
    # sc.change_color(sc.COLOR_GREEN, sc.COLOR_RED, sc.STYLE_BRIGHT)
    # sc.write_to("A123456789", 7, 15)
    # sc.write_to("B123456789", 182, 54)
    # sc.write_to("C123456789", 10, 5, False)
    # sc.write_to("D123456789", 150, 17, False)
    # sc.write_to("E123456789", 180, 18, False)
    # sc.write_to("F123456789", 15, 40, False)
    # sc.write_to("G123456789", 1000, 1000, False)
    sc.reset()
    #print("here")
    sc.deinit()
    input()
