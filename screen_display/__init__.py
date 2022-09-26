"""
This package provides utility for writing to the terminal as if it were a screen.
"""

__version__ = '1.3.3'

from enum import Enum
import math
import os
import sys
from acc_console_font import get_size
#pip
import colorama as col
from colorama import win32

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


class Text_style:
    def __init__(self, fore_color=Colors.DEFAULT, back_color=Colors.DEFAULT, text_type=Styles.DEFAULT):
        self.fore_color = Colors(fore_color)
        self.back_color = Colors(back_color)
        self.text_type = Styles(text_type)


class Screen_text:
    def __init__(self, text:str, x:int, y:int, style:Text_style=None, wrap=False):
        self.text = str(text)
        self.x = int(x)
        self.y = int(y)
        self.wrap = bool(wrap)
        if style == None:
            style = Text_style()
        self.style = style
    
    def display(self, screen:'Screen'):
        screen.change_style(self.style)
        screen.write_to(self.text, self.x, self.y, self.wrap)


class Screen:

    _INITIALISED = False
    _MIN_WIDTH_VSC = 30
    MIN_WIDTH = -1
    MIN_HEIGHT = 1


    def __init__(self, width:int=None, height:int=None, default_style:Text_style=None, title:str=None, in_terminal=True, subscreen=False, offset_x=0, offset_y=0):
        self.width = width
        self.height = height
        self.default_style = default_style
        self.title = title
        self.in_terminal = in_terminal
        self.subscreen = subscreen
        self.offset = [offset_x, offset_y]
        self.texts:list[Screen_text] = []
        if not self.subscreen:
            self.init()
        else:
            self.sub_init()
    

    def __del__(self):
        if self._INITIALISED:
            self.deinit()


    def init(self):
        """
        Initalises all variables + colorama.\n
        This method is automaticaly run if the screen isn't a subscreen.
        """
        if not self._INITIALISED:
            self._INITIALISED = True
            col.init()
            if not self.in_terminal or get_size()[0] < 1:
                self.MIN_WIDTH = self._MIN_WIDTH_VSC
            else:
                self.MIN_WIDTH = math.ceil(120 / get_size()[0])
            # set size
            if self.width == None:
                self.width = os.get_terminal_size().columns
            if self.height == None:
                self.height = os.get_terminal_size().lines
            self.set_width(self.width)
            self.set_height(self.height)
            self.change_size()
            if self.default_style == None:
                self.default_style = Text_style()
            self.change_default_style(self.default_style)
            if self.title != None:
                self.change_title(self.title)
    

    def sub_init(self):
        """
        Initalises all variables.\n
        This method is automaticaly run if the screen is initalised as a subscreen to another screen.
        """
        if not self._INITIALISED:
            self._INITIALISED = True
            self.MIN_WIDTH = 1
            # set size
            # max size = parrent size?
            if self.width == None:
                self.width = os.get_terminal_size().columns - self.offset[0]
            if self.height == None:
                self.height = os.get_terminal_size().lines - self.offset[1]
            self.set_width(self.width)
            self.set_height(self.height)
            if self.default_style == None:
                self.default_style = Text_style()
            self.change_default_style(self.default_style)
            if self.title != None:
                pass
                # small screen title??????


    def deinit(self):
        """
        Resets everything and disposes colorama.\n
        Should be writen after you don't plan on using the screen anymore because otherwise `←[` text might show up.
        """
        if self._INITIALISED:
            self._INITIALISED = False
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
        self.reset_color()
        self.change_default_style_exp(Colors.RESET, Colors.RESET, Styles.NORMAL)


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
        DOESN'T ACTUALY CHANGE SCREEN SIZE.\n
        For that, use `change_size` instead.
        """
        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
        if self.subscreen:
            max_w = os.get_terminal_size().columns
            if width + self.offset[0] > max_w:
                width = max_w - self.offset[0]
        self.width = width
    

    def set_height(self, height:int):
        """
        Sets the variable for screen height.\n
        DOESN'T ACTUALY CHANGE SCREEN SIZE.\n
        For that, use `change_size` instead.
        """
        if height < self.MIN_HEIGHT:
            height = self.MIN_HEIGHT
        if self.subscreen:
            max_h = os.get_terminal_size().lines
            if height + self.offset[1] > max_h:
                height = max_h - self.offset[1]
        self.height = height


    def change_size(self):
        """
        This is the only method that changes the terminal size, because changing it will clear all text.
        """
        os.system(f"mode {self.width}, {self.height}")
    

    def change_title(self, title:str):
        """
        Changes the terminal's title.
        """
        win32.SetConsoleTitle(str(title))


    def _convert_color(self, color:Colors):
        """
        Converts the color from Colors enum to a console accepted equivalent.
        """
        colors = [Colors.BLACK, Colors.RED, Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.MAGENTA, Colors.CYAN, Colors.WHITE, Colors.LIGHTBLACK, Colors.LIGHTRED, Colors.LIGHTGREEN, Colors.LIGHTYELLOW, Colors.LIGHTBLUE, Colors.LIGHTMAGENTA, Colors.LIGHTCYAN, Colors.LIGHTWHITE]
        colors_mapped = ["0", "4", "2", "6", "1", "5", "3", "7", "8", "C", "A", "E", "9", "D", "B", "F"]
        try:
            return colors_mapped[colors.index(color)]
        except ValueError:
            return -1


    def _change_terminal_color(self):
        """
        Changes the color of the terminal to the deffault color of the screen, or black and white.
        """
        f_color = self._convert_color(self.default_style.fore_color)
        b_color = self._convert_color(self.default_style.back_color)
        if f_color == -1:
            f_color = self._convert_color(Colors.WHITE)
        if b_color == -1:
            b_color = self._convert_color(Colors.BLACK)
        os.system(f"color {b_color}{f_color}")


    def change_default_style_exp(self, fore_color:Colors=None, back_color:Colors=None, style:Styles=None):
        """
        `change_default_style` expanded.
        """
        # Background color overrides foreground color in vscode.
        if fore_color != None:
            if fore_color == Colors.DEFAULT or fore_color == Colors.RESET:
                self.default_style.fore_color = Colors.WHITE
            else:
                self.default_style.fore_color = fore_color
        if back_color != None:
            if back_color == Colors.DEFAULT or back_color == Colors.RESET:
                self.default_style.back_color = Colors.BLACK
            else:
                self.default_style.back_color = back_color
        if style != None:
            if style == Styles.DEFAULT:
                self.default_style.text_type = Styles.NORMAL
            else:
                self.default_style.text_type = style
        self._change_terminal_color()


    def change_default_style(self, style:Text_style):
        """
        Changes the default color/style, for color afer a rendered text object, and the default terminal color.\n
        Changes ALL previously printed text's colors.
        """
        self.change_default_style_exp(style.fore_color, style.back_color, style.text_type)


    def change_style_exp(self, fore_color:Colors=None, back_color:Colors=None, style:Styles=None):
        """
        `change_default_style` expanded.
        """
        # Background color overrides foreground color in vscode.
        if fore_color != None:
            if fore_color == Colors.DEFAULT:
                fore_color = self.default_style.fore_color
            sys.stdout.write(f"\x1b[{30 + fore_color.value}m")
        if back_color != None:
            if back_color == Colors.DEFAULT:
                back_color = self.default_style.back_color
            sys.stdout.write(f"\x1b[{40 + back_color.value}m")
        if style != None:
            if style == Styles.DEFAULT:
                style = self.default_style.text_type
            sys.stdout.write(f"\x1b[{style.value}m")
    

    def change_style(self, style:Text_style):
        """
        Changes the current color/style of the terminal.
        """
        # Background color overrides foreground color in vscode.
        self.change_style_exp(style.fore_color, style.back_color, style.text_type)
    

    def move_cursor(self, x:int, y:int):
        """
        Moves the cursor.
        """
        sys.stdout.write(f"\x1b[{self.offset[1]+y+1};{self.offset[0]+x+1}H")
    

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
        self.clear()
        self.change_default_style(self.default_style)
        #render
        for text in self.texts:
            self.change_style(text.style)
            self.write_to(text.text, text.x, text.y, text.wrap)
        #clear
        self.change_style(self.default_style)


def delete_last_line():
    "Use this function to delete the last line in the terminal."

    #cursor up one line
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')


def color_test():
    """
    windows 8.1 terminal:
    - color accuracy: 9/10
    - foreground/background color interaction: seemingly perfect?
    vscode terminal:
    - color accuracy: 10/10
    - foreground/background color interaction: wierd: almost none, best in bright mode
    """
    # setup
    sc_test = Screen(title="Color test")
    # 1. line
    sc_test.write_to("#", 1, 2)
    for color in Colors._member_names_:
        if Colors[color] != Colors.DEFAULT:
            print(end=color[0])
    print("#")
    # 2-4. line
    for style in Styles._member_names_:
        if Styles[style] != Styles.DEFAULT:
            print(end=" " + style[0])
            for color in Colors._member_names_:
                if Colors[color] != Colors.DEFAULT:
                    sc_test.change_style_exp(Colors[color], Colors[color], Styles[style])
                    print(end="X")
            sc_test.change_style_exp(Colors.DEFAULT, Colors.DEFAULT, Styles.NORMAL)
            print("#")
    # 5. line
    sc_test.write_to("#", 1, 6)
    for _ in range(len(Colors._member_names_)):
        print(end="#")
    # end
    input()
    sc_test.deinit()


def __test_run():
    # color_test()
    sc = Screen(None, 15, Text_style(Colors.LIGHTBLACK, Colors.LIGHTRED), "test", True, False, 0, 0)
    # sc.init()
    print(sc.width, sc.height)
    s1 = Text_style(Colors.RED, Colors.LIGHTBLUE, Styles.DIM)
    s2 = Text_style(Colors.BLUE, Colors.GREEN)
    sc.add_texts([Screen_text("HAHAH", 5, 10, s1), Screen_text("hmmmmmmmmmmmm", 0, 2, s2), Screen_text("12345678901234567890", 50, 10, s1), Screen_text("lllll", 16, 6)])
    sc.render()
    sc.reset_cursor()
    input()
    # sc.clear()
    sc.deinit()


# __test_run()