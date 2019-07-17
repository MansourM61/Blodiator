"""
********************************************************************************

Python Script: Blodiator Test
Writter: Mojtaba Mansour Abadi
Date: 16 July 2019

This Python script is compatible with Python 3.x.
The script is for testing Blodiator


Histoty:

Ver 0.0.44: 16 July 2019;
             first code

********************************************************************************
"""


import tkinter as tk

from blodiator.etc import coloredtext
from blodiator import blodiatorbase


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'Blodiator: '


#################################################
WINDOW_MARGIN = 25  # windows extra size margin (accounted for scrollbar width)
WIDTH = 600  # canvas width
HEIGHT = 600  # canvas height
#################################################


# main func: contains code to test BlodiatorBase class
# {
def main():
  CT = coloredtext.ColoredText()

  CT.Print('Starting Blodiator', fg, bg, style, 'Root: ')

  root = tk.Tk()
  root.geometry("{0}x{1}".format(WIDTH + WINDOW_MARGIN, HEIGHT + WINDOW_MARGIN))
  root.title('Blodiator Base Test Bench')
  TestApp = blodiatorbase.BlodiatorBase(master=root, std=CT)

  root.mainloop()

  CT.Print('Closing Blodiator', fg, bg, style, 'Root: ')  
  pass
# } main func


if __name__ == '__main__':
  main()
