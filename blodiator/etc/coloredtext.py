'''
********************************************************************************

Python Script: coloredtext Module
Writter: Mojtaba Mansour Abadi
Date: 20 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to colour and changethe style of text. Three possible
modes are avaiable: 1) no colour, 2) console, and 3) shell.


ColoredText
|
|.


History:
    
Ver_00_00_0: 7 September 2017;
             first code

Ver_00_00_1: 20 January 2019;
             1- Comments were added to the class definition and memeber functions,
             2- Indents were corrected according to sublime_text ver 3.0 software,
             3- Class variables were introduced,
             4- Static functions were introduced.

********************************************************************************
'''


import sys


#################################################
NO_COLORED = 0  # no color mode
CON_COLORED = 1  # console colored mode
SHL_COLORED = 2  # shell colored mode
#################################################


# ColoredText class: this is the modified version of canvas which contains the blocks
# {
class ColoredText:
  """
  Console wrapper class.
  
  Define an instance of 'ColoredText' with appropriate arguments:
      text_mode = depending on the available console pick the proper mode.
      
  The static functions in this class, provide required formatting and printing 
  tools for displaying the messages in approporiate form.
  """

  version = '1.0'

  Shell_FG = {'black': 'SYNC',
              'dark red': 'COMMENT',
              'red': 'stderr',
              'green': 'STRING',
              'yellow': 'KEYWORD',
              'blue': 'DEFINITION',
              'purple': 'BUILTIN',
              'cyan': 'console',
              'white': 'hit',
              'black+pink': 'ERROR',
              'black+grey': 'sel'
              }  # available foreground colour for shell mode (brown colour is considered to be cyan)

  Console_Style = {'normal': 0,
                   'fg light': 1,
                   'fg dark': 2,
                   'italic': 3,
                   'underlined': 4,
                   'bg light': 5,
                   'bg dark': 6,
                   'reversed': 7
                   }  # available styles for console mode

  Console_FG = {'black': 30,
                'red': 31,
                'green': 32,
                'yellow': 33,
                'blue': 34,
                'purple': 35,
                'cyan': 36,
                'white': 37
                }  # available foreground colour for console mode

  Console_BG = {'black': 40,
                'red': 41,
                'green': 42,
                'yellow': 43,
                'blue': 44,
                'purple': 45,
                'cyan': 46,
                'white': 47
                }  # available background colour for console mode

  Print = None  # use this function to print a message at the standard console
  Shell = None  # class variable for shell output

  # __init__ func: initialiser
  # {
  def __init__(self, text_mode=NO_COLORED):
    """
    Construct a ColoredText
    
    input:
        text_mode = depending on the available console pick the proper mode.
    output: none
    """

    if(text_mode == CON_COLORED):  # if text mode is colored console

      ColoredText.Print = ColoredText.Prn_Con_Col

    elif(text_mode == SHL_COLORED):  # if text mode is colored shell

      try:
        ColoredText.Shell = sys.stdout.shell
      except AttributeError:
        raise RuntimeError("you must run this program in IDLE")

      ColoredText.Print = ColoredText.Prn_Shl_Col

    else:  # if text mode is no color

      ColoredText.Print = ColoredText.Prn_No_Col
  # } __init__ func

  # Prn_No_Col func: print with no colour
  # {
  @staticmethod
  def Prn_No_Col(self, text='', fg='', bg='', style='', src=''):
    """
    This function is called when output is not colored
    
    input:
        text = the text to be displaced        
        fg = is ignored
        bg = is ignored
        style = is ignored
        src = source of message
    output: none
    """

    print(src + text)
  # } Prn_No_Col func

  # Prn_Shl_Col func: print whithin shell environment
  # {
  @staticmethod
  def Prn_Shl_Col(self, text='', fg='black', bg='', style='', src=''):
    """
    This function is called when output is is colored shell mode
    
    input:
        text = the text to be displaced        
        fg = foreground color
        bg =  is ignored
        style = is ignored
        src = source of message
    output: none
    """

    ColoredText.Shell.write(src + text + '\n', ColoredText.Shell_FG[fg])
  # } Prn_Shl_Col func

  # Prn_Con_Col func: print whithin console environment
  # {
  @staticmethod
  def Prn_Con_Col(self, text='', fg='white', bg='black', style='normal', src=''):
    """
    This function is called when output is is colored console mode
    
    input:
        text = the text to be displaced        
        fg = foreground color
        bg =  background color
        style = text style
        src = source of message
    output: none
    """

    frm = ';'.join([str(ColoredText.Console_Style[style]), str(ColoredText.Console_FG[fg]), str(ColoredText.Console_BG[bg])])
    S = '\033[' + frm + 'm' + src + text + '\033[0m'
    print(S)
    # } Prn_Con_Col

# } ColoredText class


# main func: contains code to test ColoredText class
# {
def main():
  CT = ColoredText(text_mode=SHL_COLORED)
  CT.Print(text='Hello', fg='red', bg='black', style='normal', src='coloredtext module: ')
# } main func


if __name__ == '__main__':
  main()
