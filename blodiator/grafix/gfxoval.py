'''
********************************************************************************

Python Script: gfxoval Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxOval class the oval block in
Blodiator. This module is a wrapper for tk.Canvas.create_oval command.


GfxCircle   GfxPies    GfxSquare       GfxLine     GfxPolygon   GfxImage     GfxText
|           |          |               |           |            |            |
|           |          |               |           |            |            |
GfxOval     GfxArc     GfxRectangle    |           |            |            |
|           |          |               |           |            |            |
|           |          |               |           |            |            |
|___________|__________|___________GfxObject_______|____________|____________|


Histoty:
    
Ver 0.0.0: 24 January 2019;
             first code
             
Ver 0.0.1: 25 January 2019;
             1- The problem with inhiretance is fixed,
             2- Color updating is added.

Ver 0.0.5: 28 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.5. 

Ver 0.0.6: 29 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.6. 

********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxOval: '


#################################################
DEF_NAME = 'oval'  # default name
CENTER = (50, 50)  # default center coordinate
SIZE = (50, 25)  # default size
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


# GfxOval class: this is the oval class
# {
class GfxOval(gfxobject.GfxObject):
  """
  Draws primitive shape of oval.
  
  Define an instance of 'GfxOval' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the oval
      center = center of the oval
      size = size of the oval
      cat = a string showing the category of the oval
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
    Construct a GfxOval
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the oval
        center = center of the oval
        size = size of the oval
        cat = a string showing the category of the oval
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    self.__radiusX, self.__radiusY = size[0] // 2, size[1] // 2  # set the radii of oval

    super(GfxOval, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center,
                                  size=size, cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func

  # from_radii func: from radii initialiser
  # {
  @classmethod
  def from_radii(cls, sheetCanvas=None, tag=DEF_NAME, center=CENTER, radii=SIZE,
                 cat=CAT, mode=MODE[0], std=None):
    """
    Construct a GfxCircle based on the vertical and horizontal radii rather than size
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the oval
        center = center of the oval
        radii = horizontal and vertical radius values
        cat = a string showing the category of the sha[e]
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    size = radii[0] * 2, radii[1] * 2  # set the size of oval

    return cls(sheetCanvas=sheetCanvas, tag=tag, center=center,
               size=size, cat=cat, mode=mode, std=std)  # initialise the parent
  # } from_radii func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GfxOval, self).__repr__()

    txt += '; radii = ({0}, {1})'.format(self.__radiusX, self.__radiusY)  # generate formatted text

    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GfxOval, self).__str__()

    txt += '; radii = ({0}, {1})'.format(self.__radiusX, self.__radiusY)  # generate formatted text

    return txt
  # } __str__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the oval on the canvas
    
    input: none
    output: none
    """
    
    self.sheetCanvas.create_oval(self.bbox, tags=self.tag)

    super(GfxOval, self).draw()

    self.update_color()
  # } draw func

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the oval color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    super(GfxOval, self).update_color()

    color = self.color
   
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.itemconfig(item, outline=color[0])  # set foreground color property
    self.sheetCanvas.itemconfig(item, fill=color[1])  # set background color property
  # } update_color func  
  # < class functions section >

  # < getter and setter functions section >
  # property: radii
  # radii getter func: object radii getter
  # {
  @property
  def radii(self):
    """
    Class property getter: vertical and horizontal radii
    """
    
    return self.__radiusX, self.__radiusY
  # } radii getter func

  # line setter func: object radii setter
  # {
  @radii.setter
  def radii(self, radii):
    """
    Class property setter: vertical and horizontal radii
    """
    
    self.__radiusX, self.__radiusY = radii[0], radii[1]
    self.size = radii[0] * 2, radii[1] * 2  # set the size of oval
    gfxobject.GfxObject.size.fset(self, self.size)
  # } radii setter func

  # property: size
  # size setter func: object width and height size setter
  # {
  @gfxobject.GfxObject.size.setter
  def size(self, size):
    """
    Class property setter: size
    """
    
    gfxobject.GfxObject.size.fset(self, size)
    self.__radiusX, self.__radiusY = size[0] // 2, size[1] // 2  # set the radii of oval
  # } size setter func
  # < getter and setter functions section >

# } GfxOval class


# main func: contains code to test GfxOval class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("300x300")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=200, height=200)
  canvas.pack()
  obj1 = GfxOval(sheetCanvas=canvas, center=(100, 100), std=CT, tag='OBJ1')
  obj2 = GfxOval.from_radii(sheetCanvas=canvas, std=CT, tag='OBJ2')

  obj1.draw()
  obj2.draw()
  
  canvas.create_rectangle(obj2.boundary)
  canvas.create_rectangle(obj2.bbox)

  print(repr(obj1))
  CT.Print('\n')
  print(repr(obj2))
  
  obj2.radii = (25, 25)

  obj2.center = (150, 150)
  
  print(repr(obj1))
  CT.Print('\n')
  print(repr(obj2))

  obj1.mode = MODE[3]
  obj2.mode = MODE[3]

  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, (8.0, [])]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  obj1.colorset = CS
  obj2.brushset = BS

  canvas.create_rectangle(obj2.boundary)
  canvas.create_rectangle(obj2.bbox)

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
