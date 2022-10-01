"""
This package provides utility for writing to the terminal as if it were a screen.
"""

__version__ = '1.4.1.1'
from msvcrt import getch
from time import sleep
# local imports
if __name__ == "__main__":
    from enums import Colors, Styles, Wrap_styles
    from text import Text_style
    from screen import Text, Simple_text, Screen_text, Screen
    from acc_console_font import get_size
else:
    from screen_display.enums import Colors, Styles, Wrap_styles
    from screen_display.text import Text_style
    from screen_display.screen import Text, Simple_text, Screen_text, Screen
    from screen_display.acc_console_font import get_size

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


def render_loop(sc:Screen):
    while True:
        # off
        for text in sc.texts:
            text.erase()
            sc.reset_cursor()
            sleep(0.05)
        # on
        for text in sc.texts:
            text.display()
            sc.reset_cursor()
            sleep(0.05)


def __test_run():
    # color_test()
    sc = Screen(None, 15, Text_style(Colors.LIGHTBLACK, Colors.LIGHTRED), "test", True, False, 0, 0)
    # sc.init()
    print(sc.width, sc.height)
    s1 = Text_style(Colors.RED, Colors.LIGHTBLUE, Styles.DIM)
    s2 = Text_style(Colors.BLUE, Colors.GREEN)
    s3 = Text_style(Colors.MAGENTA, Colors.LIGHTBLACK, Styles.BRIGHT)
    sc.add_texts([Text("hahahahahahaha", 25, 0, s3), Text("HAHAH", 5, 10, s1), Text("hmmmmmmmmmmmm", 0, 2, s2), Text("12345678901234567890", 50, 10, s1), Text("hehehehe", 1, 12, s3), Text("lllll", 16, 6)])
    sc.render()
    render_loop(sc)
    # sc.reset_cursor()
    # getch()
    # sc.erase_all()
    # sc.reset_cursor()
    # getch()
    # sc.clear()
    sc.deinit()
    getch()


if __name__ == "__main__":
    __test_run()