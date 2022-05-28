import time

import sys
# pip install
# makes ANSI escape sequences usable in win 8
import colorama

def delete_last_line():
    "Use this function to delete the last line in the STDOUT"

    #cursor up one line
    sys.stdout.write('\x1b[1A')
    sys.stdout.write('\x1b[1A')

    #delete last line
    sys.stdout.write('\x1b[2K')


if __name__ == "__main__":
    colorama.init()
    print("hello")
    print("this line will be deleted after 2 seconds")
    time.sleep(2)
    delete_last_line()
    print("wow")
    print("override part of line    ")
