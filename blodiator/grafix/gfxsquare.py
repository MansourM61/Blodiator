'''
********************************************************************************

Python Script: gfxsquare Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxSquare class the square block in
Blodiator. This class is a child of GfxRectangle class.


GfxCircle   GfxPies    GfxSquare       GfxLine     GfxPolygon   GfxImage     GfxText
|           |          |               |           |            |            |
|           |          |               |           |            |            |
GfxOval     GfxArc     GfxRectangle    |           |            |            |
|           |          |               |           |            |            |
|           |          |               |           |            |            |
|___________|__________|___________GfxObject_______|____________|____________|


Histoty:
    
Ver 0.0.0: 25 January 2019;
             first code

Ver 0.0.5: 28 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.5. 

Ver 0.0.6: 29 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.6. 

********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxrectangle


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxSquare: '


#################################################
DEF_NAME = 'square'  # default name
CENTER = (50, 50)  # default center coordinate
SIZE = 25  # default size
CAT = 'primitive'  # default category
COLOR_NORMAL = ('black', 'white')  # default color for normal state
COLOR_DISABLED = ('pink', 'blue')  # default color for disabled state
COLOR_SELECTED = ('red', 'green')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'cyan')  # default color for erroneous state
BRUSH_NORMAL = (1.0, (5, ))  # default line thickness and style for normal state
BRUSH_DISABLED = (2.0, (6, ))  # default line thickness and style for disabled state
BRUSH_SELECTED = (3.0, (7, ))  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (4.0, (8, ))  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
#################################################


# GfxSquare class: this is the square class
# {
class GfxSquare(gfxrectangle.GfxRectangle):
  """
  Draws primitive shape of square.
  
  Define an instance of 'GfxSquare' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the rectangle
      size = size of the rectangle
      cat = a string showing the category of the rectangle
      center = center of the rectangle
      mode = state of the rectangle: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing a square
  in Blodiator.
  """
  
  version = '0.0.6'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, center=CENTER, size=SIZE,
               cat=CAT, mode=MODE[0], std=None):
    """
    Construct a GfxSquare
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the rectangle
        center = center of the rectangle
        size = length of the square
        cat = a string showing the category of the rectangle
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    self.__length = size  # length of the square

    super(GfxSquare, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center,
                                  size=(size, size), cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func
  # < inherited functions section >
  # < class functions section >

  # < getter and setter functions section >
  # property: length
  # length getter func: object length getter
  # {
  @property
  def length(self):
    """
    Class property getter: length
    """
    
    return self.__length
  # } length getter func

  # length setter func: object length setter
  # {
  @length.setter
  def length(self, length):
    """
    Class property setter: length
    """
    
    self.__length = length
    gfxrectangle.GfxRectangle.size.fset(self, (length, length))
  # } length setter func

  # property: size
  # size setter func: object width and height size setter
  # {
  @gfxrectangle.GfxRectangle.size.setter
  def size(self, size):
    """
    Class property setter: size
    """
    
    gfxrectangle.GfxRectangle.size.fset(self, (size, size))
    self.__length = size  # set the radius of oval
  # } size setter func
  
  # < getter and setter functions section >

# } GfxSquare class


# main func: contains code to test GfxSquare class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("300x300")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=200, height=200)
  canvas.pack()
  obj1 = GfxSquare(sheetCanvas=canvas, std=CT, tag='OBJ1')
  
  obj1.draw()
  
  canvas.create_rectangle(obj1.boundary)
  canvas.create_rectangle(obj1.bbox)
  
  print(repr(obj1))

  CT.Print('\n')

  obj1.length = 50

  obj1.center = (150, 50)

  print(repr(obj1))

  CT.Print('\n')

  print(repr(obj1))

  obj1.mode = MODE[3]

  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, (8.0, [])]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  obj1.colorset = CS
  obj1.brushset = BS

  canvas.create_rectangle(obj1.boundary)
  canvas.create_rectangle(obj1.bbox)

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
