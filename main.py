import sys
import colorama
import os


class Screen:
    import os
    import sys
    # pip install
    import colorama

    MIN_WIDTH = 15
    MIN_WIDTH_VSC = 30
    MIN_HEIGHT = 1

    # ANSI esc chars
    colorama.init()

    def __init__(self, width:int=None, height:int=None, in_terminal=True):
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
        self.deinit()

    def deinit(self):
        self.reset()
        colorama.deinit()
    
    def reset(self):
        sys.stdout.write("\x1b[0m")
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
    
    def change_color(self, color):
        sys.stdout.write(f"\x1b[{color}m")
    
    def move_cursor(self, x:int, y:int):
        sys.stdout.write(f"\x1b[{x};{y}H")
    
    def write_to(self, text:str, x:int, y:int):
        self.move_cursor(x, y)
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
    # sc.change_color("36;45;1")
    sc.write_to("lollol", 15, 10)
    sc.write_to("lellel", 5, 1)
    # sc.reset()
    sc.write_to("hahaha", 55, 19)
    sc.write_to("f", 99, 8)
    sc.deinit()
    print("hmmmmmmmmmmmm")
    input()

