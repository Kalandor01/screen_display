import math
import os
import sys
#pip
# try to remove it without the background being weird
import colorama as col
# local imports
from screen_display.enums import Styles, Colors, Wrap_styles
from screen_display.text import Text_style
from screen_display.acc_console_font import get_size


class Text:
    """
    Text object for a `Screen` object.\n
    `wrap_style` specifies if the text wraps, where the first character of the next line starts to get drawn.\n
    If `cutoff` is true, when the text reches the end of the line (no matter if it will wrap or not), the last few characters will be replaced with the `cutoff_str`.\n
    WILL ONLY UPDATE ON THE SCREEN IF IT GETS UPDATED FROM `request_update` OR FROM THE SCREEN WITH `update_text`, `update_texts` OR `update_all`!
    """
    def __init__(self, text:str, x:int, y:int, style:Text_style=None, wrap=False, wrap_style:Wrap_styles=Wrap_styles.LEFT, cutoff=False, cutoff_str="..."):
        self.text = str(text)
        self.x = int(x)
        self.y = int(y)
        self.wrap = bool(wrap)
        if style == None:
            style = Text_style()
        self.style = style
        self.wrap_style = Wrap_styles(wrap_style)
        self.cutoff = bool(cutoff)
        self.cutoff_str = str(cutoff_str)
    
    
    def request_update(self, screen:'Screen'):
        """
        Tries to update this text from the screen.
        """
        return screen.update_text(self)


class Simple_text:
    """
    Minimal text object.\n
    Should only be used by a `Screen` object.
    """
    def __init__(self, text:str, x:int, y:int, style:Text_style=None):
        self.text = str(text)
        self.x = int(x)
        self.y = int(y)
        if style == None:
            style = Text_style()
        self.style = style
    
    
    def display(self, screen:'Screen'):
        screen.change_style(self.style)
        screen.write_to(self.text, self.x, self.y)


class Screen_text:
    """
    `Screen` object specific text object.\n
    Should only be used by a `Screen` object.
    """
    def __init__(self, text:Text, screen:'Screen'):
        self.sc = screen
        self.text_obj = text
        self.text:list[Simple_text] = []
        self.blank:list[Simple_text] = []
        self.update()
    
    
    def update(self):
        """
        Recalculates the `text` and `blank` `Simple_Text` lists, from the `text` `Text` object, and the parrent `Screen`.
        """
        self.text:list[Simple_text] = []
        self.blank:list[Simple_text] = []
        if self.text_obj.wrap:
            x_pos = min(self.text_obj.x, self.sc.width - 1)
            y_pos = min(self.text_obj.y, self.sc.height - 1)
            self.text.append(
                Simple_text(self.text_obj.text, x_pos, y_pos, self.text_obj.style))
            self.blank.append(
                Simple_text(" " * (len(self.text_obj.text)), x_pos, y_pos, self.sc.default_style))
        else:
            if self.text_obj.x + 1 < self.sc.width and self.text_obj.y + 1 < self.sc.height:
                if self.sc.width - (self.text_obj.x + len(self.text_obj.text)) < 0:
                    text = self.text_obj.text[:(self.sc.width - (self.text_obj.x + len(self.text_obj.text)))]
                else:
                    text = self.text_obj.text
                self.text.append(
                    Simple_text(text, self.text_obj.x, self.text_obj.y, self.text_obj.style))
                self.blank.append(
                    Simple_text(" " * (len(text)), self.text_obj.x, self.text_obj.y, self.sc.default_style))                
        
    
    def display(self):
        for text in self.text:
            text.display(self.sc)
    
    
    def erase(self):
        for blank in self.blank:
            blank.display(self.sc)


# MIGHT NOT BE A GOOD IDEA?!
class Border:
    def __init__(self, width:int=None, height:int=None, default_style:Text_style=None, title:str=None, in_terminal=True, subscreen=False, offset_x=0, offset_y=0):
        self.width = width
        self.height = height
        self.default_style = default_style
        self.title = title
        self.in_terminal = in_terminal
        self.subscreen = subscreen
        self.offset = [offset_x, offset_y]
        self.texts:list[Screen_text] = []
    
    
    def update(self, sc):
        pass

class Screen:

    _INITIALISED = False
    _MIN_WIDTH_VSC = 30
    MIN_WIDTH = -1
    MIN_HEIGHT = 1


    def __init__(self, width:int=None, height:int=None, default_style:Text_style=None, title:str=None, in_terminal=True, subscreen=False, offset_x=0, offset_y=0, border:Border=None):
        self.width = width
        self.height = height
        self.default_style = default_style
        self.title = title
        self.in_terminal = in_terminal
        self.subscreen = subscreen
        self.offset = [offset_x, offset_y]
        self.texts:list[Screen_text] = []
        self.border = border
        if not self.subscreen:
            self.init()
        else:
            self.sub_init()
    

    def __del__(self):
        if self._INITIALISED:
            self.deinit()


    def init(self):
        """
        Initalises all variables.\n
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
            if self.border != None:
                self.update_border()
    

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
            if self.border != None:
                self.update_border()


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
        sys.stdout.write("\x1b[0m")
    

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
        # sys.stdout.write("\x1b[H")
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


    def change_size(self, rerender=True):
        """
        This is the only method that changes the terminal size, because changing it will clear all text.\n
        If `rerender` is True, it will automaticaly rerender the screen after it has bee cleared.
        """
        os.system(f"mode {self.width}, {self.height}")
        self.render()
    

    def change_title(self, title:str):
        """
        Changes the terminal's title.
        """
        os.system("title " + str(title))


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
    

    def write_to(self, text:str, x:int, y:int):
        """
        Writes text to specified coordinates.
        """
        self.move_cursor(min(x, self.width - 1), min(y, self.height - 1))
        sys.stdout.write(text)
    

    def add_texts(self, texts:Text|list[Text]):
        """
        Adds (a) `Screen_text` object(s) to the list that will be displayed if `render()` is run.
        """
        if type(texts) == Text:
            self.texts.append(Screen_text(texts, self))
        else:
            for text in texts:
                self.texts.append(Screen_text(text, self))
    

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
            text.display()
        #clear
        self.change_style(self.default_style)
    
    
    def erase_all(self):
        """
        Erases all text from the `texts` list.
        """
        #clear
        self.reset_color()
        self.reset_cursor()
        self.change_default_style(self.default_style)
        #render
        for text in self.texts:
            text.erase()
        #clear
        self.change_style(self.default_style)
    
    
    def update_border(self):
        self.border.update(self)
        
    
    def update_texts(self):
        for text in self.texts:
            text.update()
            
    
    def update_all(self):
        self.border.update(self)
        for text in self.texts:
            text.update()
    
    
    def update_text(self, text:Text):
        """
        Tries to update a specific text from this screen (if it exists).
        """
        updated = False
        for sc_text in self.texts:
            if sc_text.text_obj == text:
                sc_text.update()
                updated = True
                break
        return updated