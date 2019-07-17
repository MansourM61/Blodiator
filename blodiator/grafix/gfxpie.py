'''
********************************************************************************

Python Script: gfxpie Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxPie class the pie block in
Blodiator. This module is a child of GfxArc class.


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
             1- 'colorset' and 'brushset' are corrected.

********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxarc


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxPie: '


#################################################
DEF_NAME = 'pie'  # default name
CENTER = (200, 200)  # default center coordinate
SIZE = (50, 25)  # default size
ANG = (0, 90)  # start and stop anggles
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


# GfxPie class: this is the pie class
# {
class GfxPie(gfxarc.GfxArc):
  """
  Draws primitive shape of pie.
  
  Define an instance of 'GfxPie' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the pie
      center = center of the pie
      ang = start and stop angle of the arc
      size = size of the pie
      cat = a string showing the category of the pie
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
        tag = a string used by tkinter to identify the pie
        center = center of the pie
        ang = start and stop angle of the arc
        size = size of the pie
        cat = a string showing the category of the pie
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    super(GfxPie, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center,
                                  size=size, cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the pie on the canvas
    
    input: none
    output: none
    """
    
    super(GfxPie, self).draw()

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.itemconfig(item, style=tk.PIESLICE)  # set foreground color property
    
    self.update_color()
  # } draw func

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the pie color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    super(GfxPie, self).update_color()

    color = self.color
   
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.itemconfig(item, fill=color[1])  # set foreground color property
  # } update_color func  
  # < class functions section >

  # < getter and setter functions section >
  # < getter and setter functions section >

# } GfxPie class


# main func: contains code to test GfxPie class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("300x300")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=400, height=400)
  canvas.pack()
  obj = GfxPie(sheetCanvas=canvas, std=CT, tag='OBJ1')
  
  obj.draw()

  canvas.create_rectangle(obj.boundary)
  canvas.create_rectangle(obj.bbox)

  print(repr(obj))

  CT.Print('\n')

  obj.center = (150, 150)

  obj.radii = (60, 25)
  obj.mode = MODE[3]

  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, (8.0, [])]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  obj.colorset = CS
  obj.brushset = BS

  canvas.create_rectangle(obj.boundary)
  canvas.create_rectangle(obj.bbox)

  print(repr(obj))

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
