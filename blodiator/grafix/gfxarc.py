'''
********************************************************************************

Python Script: gfxarc Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxArc class the arc block in
Blodiator. This module is a wrapper for tk.Canvas.create_arc command.


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
             1- 'colorset' and 'brushset' are corrected.

********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxArc: '


#################################################
DEF_NAME = 'arc'  # default name
CENTER = (200, 200)  # default center coordinate
SIZE = (50, 25)  # default size
ANG = (0, 90)  # start and stop anggles
CAT = 'primitive'  # default category
COLOR_NORMAL = ('black', 'white')  # default color for normal state
COLOR_DISABLED = ('pink', 'blue')  # default color for disabled state
COLOR_SELECTED = ('red', 'green')  # default color for selected state
COLOR_ERRONEOUS = ('magenta', 'cyan')  # default color for erroneous state
BRUSH_NORMAL = (1.0, (5, ))  # default line thickness and style for normal state
BRUSH_DISABLED = (2.0, (6, ))  # default line thickness and style for disabled state
BRUSH_SELECTED = (3.0, (7, ))  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (4.0, (8, ))  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
#################################################


# GfxArc class: this is the arc class
# {
class GfxArc(gfxobject.GfxObject):
  """
  Draws primitive shape of arc.
  
  Define an instance of 'GfxArc' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the arc
      center = center of the arc
      ang = start and stop angle of the arc
      size = size of the arc 
      cat = a string showing the category of the arc
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing an arc
  in Blodiator.
  """

  version = '0.0.6'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, center=CENTER, size=SIZE, ang=ANG,
               cat=CAT, mode=MODE[0], std=None):
    """
    Construct a GfxArc
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the arc
        center = center of the arc
        ang = start and stop angle of the arc
        size = size of the arc
        cat = a string showing the category of the arc
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    self.__radiusX, self.__radiusY = size[0] // 2, size[1] // 2  # set the radii of arc
    self.__angStart, self.__angStop = ang[0], ang[1]  # set the angle range

    super(GfxArc, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center,
                                  size=size, cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func

  # from_radii func: from radii initialiser
  # {
  @classmethod
  def from_radii(cls, sheetCanvas=None, tag=DEF_NAME, center=CENTER, radii=SIZE, ang=ANG,
                 cat=CAT, mode=MODE[0], std=None):
    """
    Construct a GfxArc based on the vertical and horizontal radii rather than size
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the arc
        center = center of the arc
        ang = start and stop angle of the arc
        radii = horizontal and vertical radius values
        cat = a string showing the category of the sha[e]
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    size = radii[0] * 2, radii[1] * 2  # set the size of oval

    return cls(sheetCanvas=sheetCanvas, tag=tag, center=center, size=size,
               ang=ANG, cat=cat, mode=mode, std=std)  # initialise the parent
  # } from_radii func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """

    txt = super(GfxArc, self).__repr__()

    txt += '; radii = ({0}, {1}); angle (start, stop) = ({2}, {3})'\
           .format(self.__radiusX, self.__radiusY, self.__angStart, self.__angStop)  # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """

    txt = super(GfxArc, self).__str__()

    txt += '; radii = ({0}, {1}); angle (start, stop) = ({2}, {3})'\
           .format(self.__radiusX, self.__radiusY, self.__angStart, self.__angStop)  # generate formatted text
    return txt
  # } __str__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the arc on the canvas
    
    input: none
    output: none
    """

    extent = self.__angStop - self.__angStart
    self.sheetCanvas.create_arc(self.bbox, start=self.__angStart,
                                extent=extent, style=tk.ARC,tags=self.tag)

    super(GfxArc, self).draw()
    
    self.update_color()
  # } draw func
  
  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the arc color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    super(GfxArc, self).update_color()

    color = self.color
   
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.itemconfig(item, outline=color[0])  # set foreground color property
  # } size setter func  
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

  # property: angles
  # angles getter func: object angles getter
  # {
  @property
  def angles(self):
    """
    Class property getter: angles
    """
    return self.__angStart, self.__angStop
  # } radii getter func

  # angles setter func: object angles setter
  # {
  @angles.setter
  def angles(self, ang):
    """
    Class property setter: angles
    """
    self.__angStart, self.__angStop = ang[0], ang[1]
    
    extent = self.__angStop - self.__angStart

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.itemconfig(item, start=self.__angStart)  # set start angle property
    self.sheetCanvas.itemconfig(item, extent=extent)  # set angle extent property
  # } angles setter func

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

# } GfxArc class


# main func: contains code to test GfxArc class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("300x300")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=400, height=400)
  canvas.pack()
  obj = GfxArc(sheetCanvas=canvas, std=CT, tag='OBJ1')
  obj.draw()

  canvas.create_rectangle(obj.bbox)
  
  CT.Print(repr(obj))

  CT.Print('\n')

  obj.radii = (60, 25)
  obj.mode = MODE[3]

  CT.Print(repr(obj))

  obj.center = (50, 50)

  canvas.create_rectangle(obj.boundary)


  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, (8.0, [])]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  obj.colorset = CS

  obj.brushset = BS

  obj.mode = MODE[2] 

  CT.Print(str(obj.colorset))
  
  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
