'''
********************************************************************************

Python Script: gfxcircle Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxCircle class the circle block in
Blodiator. This module is a child of GfxOval class.


GfxCircle   GfxPies    GfxSquare       GfxLine     GfxPolygon   GfxImage     GfxText
|           |          |               |           |            |            |
|           |          |               |           |            |            |
GfxOval     GfxArc     GfxRectangle    |           |            |            |
|           |          |               |           |            |            |
|           |          |               |           |            |            |
|___________|__________|___________GfxObject_______|____________|____________|


Histoty:

Ver 0.0.5: 28 January 2019;
             first code

Ver 0.0.6: 29 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.6. 

********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxoval


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxCircle: '


#################################################
DEF_NAME = 'circle'  # default name
CENTER = (50, 50)  # default center coordinate
SIZE = 24  # default size
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


# GfxCircle class: this is the circle class
# {
class GfxCircle(gfxoval.GfxOval):
  """
  Draws primitive shape of circle.
  
  Define an instance of 'GfxCircle' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the circle
      center = center of the circle
      size = size of the circle
      cat = a string showing the category of the circle
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing a circle
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
    Construct a GfxCircle
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the circle
        center = center of the circle
        size = size of the circle
        cat = a string showing the category of the circle
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    self.__radius = size // 2  # set the radii of oval

    super(GfxCircle, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center,
                                  size=(size, size), cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func

  # from_radius func: from radius initialiser
  # {
  @classmethod
  def from_radius(cls, sheetCanvas=None, tag=DEF_NAME, center=CENTER, radius=SIZE,
                 cat=CAT, mode=MODE[0], std=None):
    """
    Construct a GfxCircle based on the radius rather than size
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the circle
        center = center of the circle
        radius = circle radius value
        cat = a string showing the category of the circle
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    size = radius * 2  # set the size of oval

    return cls(sheetCanvas=sheetCanvas, tag=tag, center=center,
               size=size, cat=cat, mode=mode, std=std)  # initialise the parent
  # } from_radii func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GfxCircle, self).__repr__()

    txt += '; radius = {0}'.format(self.__radius)  # generate formatted text

    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GfxCircle, self).__str__()

    txt += '; radius = {0}'.format(self.__radius)  # generate formatted text

    return txt
  # } __str__ func
  # < inherited functions section >

  # < getter and setter functions section >
  # property: radius
  # radius getter func: object radius getter
  # {
  @property
  def radius(self):
    """
    Class property getter: radius
    """
    
    return self.__radius
  # } radius getter func

  # radius setter func: object radius setter
  # {
  @radius.setter
  def radius(self, radius):
    """
    Class property setter: radius
    """
    
    self.__radius = radius
    size = radius * 2, radius * 2  # set the size of oval
    gfxoval.GfxOval.size.fset(self, size)
  # } radii setter func

  # property: size
  # size setter func: object width and height size setter
  # {
  @gfxoval.GfxOval.size.setter
  def size(self, size):
    """
    Class property getter: size
    """
    
    gfxoval.GfxOval.size.fset(self, (size, size))
    self.__radius = size  # set the radius of oval
  # } size setter func
  # < getter and setter functions section >

# } GfxOval class


# main func: contains code to test GfxCircle class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("300x300")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=300, height=300)
  canvas.pack()
  obj1 = GfxCircle(sheetCanvas=canvas, center=(100, 100), std=CT, tag='OBJ1')
  obj2 = GfxCircle.from_radius(sheetCanvas=canvas, std=CT, mode = MODE[2], tag='OBJ2')
  obj1.draw()
  obj2.draw()
  
  print(repr(obj1))
  CT.Print('\n')
  print(repr(obj2))

  obj2.radius = 50
  
  print(repr(obj1))
  CT.Print('\n')
  print(repr(obj2))

  obj1.mode = MODE[3]
  obj2.mode = MODE[3]

  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, (8.0, [])]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  canvas.create_rectangle(obj2.boundary)
  canvas.create_rectangle(obj2.bbox)

  obj2.center = (300, 300)
  canvas.create_rectangle(obj2.bbox)

  obj1.colorset = CS
  obj2.brushset = BS

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
