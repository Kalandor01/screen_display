"""
This package provides utility for writing to the terminal as if it were a screen.
"""

__version__ = '1.1'

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
COLOR_DEFAULT = -1
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
STYLE_DEFAULT = -1


class Text_style:
    def __init__(self, fore_color=COLOR_DEFAULT, back_color=COLOR_DEFAULT, text_type=STYLE_DEFAULT):
        self.fore_color = int(fore_color)
        self.back_color = int(back_color)
        self.text_type = int(text_type)


class Screen_text:
    def __init__(self, text:str, x:int, y:int, style:Text_style=None, wrap=False):
        self.text = str(text)
        self.x = int(x)
        self.y = int(y)
        self.wrap = bool(wrap)
        if style == None:
            style = Text_style()
        self.style = style
    
    def display(self, screen):
        screen.change_color(self.style.fore_color, self.style.back_color, self.style.text_type)
        screen.write_to(self.text, self.x, self.y, self.wrap)


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
        self.change_default_color(self.default_style)
        if title != None:
            self.change_title(title)
        self.texts:list[Screen_text] = []
    

    def __del__(self):
        if self._INITIALISED:
            self.deinit()


    def deinit(self):
        """
        Resets everything and disposes colorama.
        """
        if self._INITIALISED:
            self._INITIALISED = False
            self.__del__()
            self.reset()
            col.deinit()
    

    def reset_color(self):
        """
        Resets current text colors/style.
        """
        sys.stdout.write(col.Style.RESET_ALL)
    

    def reset_all_color(self):
        """
        Resets current, deafult and terminal colors/style.
        """
        self.default_style.fore_color = COLOR_RESET
        self.default_style.back_color = COLOR_RESET
        self.default_style.text_type = STYLE_NORMAL
        self.reset_color()
        self.change_default_color(self.default_style)


    def reset_cursor(self):
        """
        Moves the cursor to the beggining of the bottom line.
        """
        #sys.stdout.write("\x1b[H")
        self.move_cursor(0, self.height - 1)


    def reset(self):
        """
        Resets all color and the cursor.
        """
        self.reset_all_color()
        self.reset_cursor()
    

    def clear(self):
        """
        Clears the screen.
        """
        sys.stdout.write("\x1b[2J")


    def set_width(self, width:int):
        """
        Sets the variable for screen width.\n
        DOESN'T ACTUALY CHANGE SCREEN SIZE.
        """
        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
        self.width = width
    

    def set_height(self, height:int):
        """
        Sets the variable for screen height.\n
        DOESN'T ACTUALY CHANGE SCREEN SIZE.
        """
        if height < self.MIN_HEIGHT:
            height = self.MIN_HEIGHT
        self.height = height


    def change_size(self):
        """
        This is the only method that changes the terminal size, becouse changing it will clear all text.
        """
        os.system(f"mode {self.width}, {self.height}")
    

    def change_title(self, title:str):
        """
        Changes the terminal's title.
        """
        win32.SetConsoleTitle(str(title))


    def _convert_color(self, color:int):
        colors = [COLOR_RESET, COLOR_BLACK, COLOR_RED, COLOR_GREEN, COLOR_YELLOW, COLOR_BLUE, COLOR_MAGENTA, COLOR_CYAN, COLOR_WHITE, COLOR_LIGHTBLACK, COLOR_LIGHTRED, COLOR_LIGHTGREEN, COLOR_LIGHTYELLOW, COLOR_LIGHTBLUE, COLOR_LIGHTMAGENTA, COLOR_LIGHTCYAN, COLOR_LIGHTWHITE]
        colors_mapped = [-1, "0", "4", "2", "6", "1", "5", "3", "7", "8", "C", "A", "E", "9", "D", "B", "F"]
        try:
            return colors_mapped[colors.index(color)]
        except ValueError:
            return colors_mapped[0]


    def _change_terminal_color(self):
        f_color = self._convert_color(self.default_style.fore_color)
        b_color = self._convert_color(self.default_style.back_color)
        if f_color == -1:
            f_color = self._convert_color(self.default_style.fore_color)
        if b_color == -1:
            b_color = self._convert_color(self.default_style.back_color)
        os.system(f"color {b_color}{f_color}")


    def change_default_color_exp(self, fore_color:int=None, back_color:int=None, style:int=None):
        """
        `change_default_color` expanded.
        """
        # Background color overrides foreground color in vscode.
        if fore_color != None:
            self.default_style.fore_color = fore_color
        if back_color != None:
            self.default_style.back_color = back_color
        if style != None:
            self.default_style.text_type = style
        self._change_terminal_color()


    def change_default_color(self, style:Text_style):
        """
        Changes the default color/style, for color afer a rendered text object, and the default terminal color.\n
        Changes ALL previously printed text's colors.
        """
        self.change_default_color_exp(style.fore_color, style.back_color, style.text_type)


    def change_color(self, fore_color:int=None, back_color:int=None, style=STYLE_DEFAULT):
        """
        Changes the current color/style of the terminal.
        """
        # Background color overrides foreground color in vscode.
        if fore_color != None:
            if fore_color == -1:
                fore_color = self.default_style.fore_color
            sys.stdout.write(f"\x1b[{30 + fore_color}m")
        if back_color != None:
            if back_color == -1:
                back_color = self.default_style.back_color
            sys.stdout.write(f"\x1b[{40 + back_color}m")
        if style == -1:
                style = self.default_style.text_type
        sys.stdout.write(f"\x1b[{style}m")
    

    def change_color_o(self, style:Text_style):
        """
        `change_color` OOP.
        """
        # Background color overrides foreground color in vscode.
        self.change_color(style.fore_color, style.back_color, style.text_type)
    

    def move_cursor(self, x:int, y:int):
        """
        Moves the cursor.
        """
        sys.stdout.write(f"\x1b[{y+1};{x+1}H")
    

    def write_to(self, text:str, x:int, y:int, wrap=True):
        """
        Writes text to specified coordinates.
        """
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
    

    def add_texts(self, texts:Screen_text|list[Screen_text]):
        """
        Adds (a) `Screen_text` object(s) to the list that will be displayed if `render()` is run.
        """
        if type(texts) == Screen_text:
            self.texts.append(texts)
        else:
            for text in texts:
                self.texts.append(text)
    

    def render(self):
        """
        Displays all `Screen_text` objects from the `texts` variable.
        """
        #clear
        self.reset_color()
        self.reset_cursor()
        sc.clear()
        self.change_default_color(self.default_style)
        #render
        for text in self.texts:
            self.change_color_o(text.style)
            self.write_to(text.text, text.x, text.y, text.wrap)
        #clear
        self.change_color_o(self.default_style)


def delete_last_line():
    "Use this function to delete the last line in the terminal."

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
    sc = Screen(None, None, Text_style(COLOR_LIGHTBLACK, COLOR_LIGHTRED), "test")
    print(sc.width, sc.height)
    s1 = Text_style(COLOR_RED, COLOR_LIGHTBLUE, STYLE_DIM)
    s2 = Text_style(COLOR_BLUE, COLOR_GREEN)
    sc.add_texts([Screen_text("HAHAH", 5, 10, s1), Screen_text("hmmmmmmmmmmmm", 0, 2, s2), Screen_text("12345678901234567890", 50, 10, s1), Screen_text("lllll", 16, 6)])
    sc.render()
    sc.reset_cursor()
    input()
    sc.deinit()
