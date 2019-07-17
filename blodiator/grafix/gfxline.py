'''
********************************************************************************

Python Script: gfxline Module
Writter: Mojtaba Mansour Abadi
Date: 28 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxLine class the line block in
Blodiator. This module is a wrapper for tk.Canvas.create_line command.


GfxCircle   GfxPies    GfxSquare       GfxLine     GfxPolygon   GfxImage     GfxText
|           |          |               |           |            |            |
|           |          |               |           |            |            |
GfxOval     GfxArc     GfxRectangle    |           |            |            |
|           |          |               |           |            |            |
|           |          |               |           |            |            |
|___________|__________|___________GfxObject_______|____________|____________|


Histoty:

Ver_00_00_0: 25 January 2019;
             first code

Ver 0.0.5: 28 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.5. 

Ver 0.0.6: 29 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.6.
             2- 'center' and 'size' are adjustable.

Ver 0.0.36: 3 July 2019;
             1- arrow update is added.
            
********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxLine: '


#################################################
DEF_NAME = 'line'  # default name
POINT_LIST = [[20, 20], [20, 100], [100, 100], [100, 20]]  # line point list
CAT = 'primitive'  # default category
COLOR_NORMAL = ('black', 'white')  # default color for normal state
COLOR_DISABLED = ('pink', 'blue')  # default color for disabled state
COLOR_SELECTED = ('red', 'green')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'cyan')  # default color for erroneous state
BRUSH_NORMAL = (5.0, (2, ))  # default line thickness and style for normal state
BRUSH_DISABLED = (2.0, (4, ))  # default line thickness and style for disabled state
BRUSH_SELECTED = (3.0, (5, ))  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (4.0, (1, ))  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
ARROW = (True, (16, 30, 9))  # default arrow style
CAP = tk.PROJECTING  # default cap style
JOINT = tk.ROUND  # default joint style
CURVATURE = (False, 3)  #  default curvature
THICKNESS = 3  # line thickness
#################################################


# GfxLine class: this is the line class
# {
class GfxLine(gfxobject.GfxObject):
  """
  Draws primitive shape of line.
  
  Define an instance of 'GfxLine' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the line
      points = list of points coordinates
      arrow = a list corresponding to arrow style
      cat = a string showing the category of the line
      cap_joint = a tuple corresponding to cap and joint styles
      curvature = a tuple corresponding to (if the curvature is included, what is the order of curvature fitting)
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing a line
  in Blodiator.
  """
  
  version = '0.0.36'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, points=POINT_LIST, cat=CAT,
               arrow=ARROW, cap_joint=(CAP, JOINT), curvature=CURVATURE, mode=MODE[0],
               std=None):
    """
    Construct a GfxLine
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the line
        points = list of points coordinates
        arrow = a list corresponding to arrow style
        cat = a string showing the category of the line
        cap_joint = a tuple corresponding to cap and joint styles
        curvature = a tuple corresponding to (if the curvature is included, what is the order of curvature fitting)
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
 
    self.__ptsX = [x for x, y in points]
    self.__ptsY = [y for x, y in points]

    self.__arrowFlag = arrow[0]
    self.__arrowPat = arrow[1]

    self.__cap = cap_joint[0]
    self.__joint = cap_joint[1]

    self.__curvatureFlag = curvature[0]
    self.__curvaturePar = curvature[1]

    center = sum(self.__ptsX)/len(self.__ptsX), sum(self.__ptsY)/len(self.__ptsY)
    size = max(self.__ptsX) - min(self.__ptsX), max(self.__ptsY) - min(self.__ptsY)
    
    super(GfxLine, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center, size=size,
                                  cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GfxLine, self).__repr__()

    txt += '; points = {0}; arrow (flag, pattern) = ({1}, {2}); (cap, join) = ({3}, {4});'\
           ' curvature (flag, spline step) = ({5}, {6})'.\
           format(str(self.points), str(self.__arrowFlag), self.__arrowPat, self.__cap,\
                  self.__joint, str(self.__curvatureFlag), self.__curvaturePar)  # generate formatted text

    return txt
  # } __repr__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the line(s) on the canvas
    
    input: none
    output: none
    """
    
    points = []

    for x, y in zip(self.__ptsX, self.__ptsY):
      points += [x]
      points += [y]

    arrow = tk.NONE if self.__arrowFlag == False else tk.LAST

    color = self.color[0]

    self.sheetCanvas.create_line(points, arrow=arrow, arrowshape=self.__arrowPat,\
                                 capstyle=self.__cap, joinstyle=self.__joint,\
                                 smooth=self.__curvatureFlag, splinesteps=self.__curvaturePar,\
                                 fill=color, tags=self.tag, width=1)

    super(GfxLine, self).draw()
  # } draw func

  # erase func: erase the line
  # {
  def erase(self):
    """
    Erases the line(s) on the canvas
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.delete(item)  # delete the line
  # } erase func  


  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the line(s) color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    super(GfxLine, self).update_color()

    color = self.color
   
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    self.sheetCanvas.itemconfig(item, fill=color[0])  # set foreground color property
  # } size setter func  

  # update_shape func: update the color
  # {
  def update_shape(self):
    """
    Updates the line(s) on the canvas
    
    input: none
    output: none
    """
    
    points = []

    for x, y in zip(self.__ptsX, self.__ptsY):
      points += [x]
      points += [y]

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.coords(item, points)
  # } update_shape func  

  # update_arrow func: update the arrow
  # {
  def update_arrow(self):
    """
    Updates the line(s) arrow style on the canvas
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    arrow = tk.NONE if self.__arrowFlag == False else tk.LAST

    self.sheetCanvas.itemconfig(item, arrow=arrow)
    self.sheetCanvas.itemconfig(item, arrowshape=self.__arrowPat)
  # } update_arrow func  

  # update_capjoint func: update the cap and join
  # {
  def update_capjoint(self):
    """
    Updates the line(s) cap and joint styles on the canvas
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, capstyle=self.__cap)
    self.sheetCanvas.itemconfig(item, joinstyle=self.__joint)
  # } update_capjoint func  

  # update_curvature func: update the curvature
  # {
  def update_curvature(self):
    """
    Updates the line(s) curvature on the canvas
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, smooth=self.__curvatureFlag)
    self.sheetCanvas.itemconfig(item, splinesteps=self.__curvaturePar)
  # } update_curvature func
  # < class functions section >

  # < getter and setter functions section >
  # property: points
  # points getter func: object points getter
  # {
  @property
  def points(self):
    """
    Class property getter: points set
    """
    
    points = [[x, y] for x, y in zip(self.__ptsX, self.__ptsY)]

    return points
  # } points getter func

  # points setter func: object points setter
  # {
  @points.setter
  def points(self, points):
    """
    Class property setter: points set
    """
    
    self.__ptsX = [x for x, y in points]
    self.__ptsY = [y for x, y in points]

    center = sum(self.__ptsX)/len(self.__ptsX), sum(self.__ptsY)/len(self.__ptsY)
    size = max(self.__ptsX) - min(self.__ptsX), max(self.__ptsY) - min(self.__ptsY)

    gfxobject.GfxObject.center.fset(self, center)
    gfxobject.GfxObject.size.fset(self, size)

    self.update_shape()
  # } points setter func
  
  # property: arrow
  # arrow getter func: object arrow getter
  # {
  @property
  def arrow(self):
    """
    Class property getter: arrow style list
    """
    
    return self.__arrowFlag, self.__arrowPat
  # } arrow getter func

  # arrow setter func: object arrow setter
  # {
  @arrow.setter
  def arrow(self, arrow):
    """
    Class property setter: arrow style list
    """
    
    self.__arrowFlag = arrow[0]
    self.__arrowPat = arrow[1]

    self.update_arrow()
  # } arrow setter func

  # property: cap join
  # capjoin getter func: object cap and joint getter
  # {
  @property
  def capjoint(self):
    """
    Class property getter: cap joint style tuple
    """
    
    return self.__cap, self.__joint
  # } arrow getter func

  # arrow setter func: object cap and joint setter
  # {
  @capjoint.setter
  def capjoint(self, capjoint):
    """
    Class property setter: cap joint style tuple
    """
    
    self.__cap = capjoint[0]
    self.__joint = capjoint[1]

    self.update_capjoint()
  # } arrow setter func

  # property: curvature
  # curvature getter func: object curvature getter
  # {
  @property
  def curvature(self):
    """
    Class property getter: curvature tuple
    """
    
    return self.__curvatureFlag, self.__curvaturePar
  # } curvature getter func

  # curvature setter func: object curvature setter
  # {
  @curvature.setter
  def curvature(self, curvature):
    """
    Class property setter: curvature tuple
    """
    
    self.__curvatureFlag = curvature[0]
    self.__curvaturePar = curvature[1]

    self.update_curvature()
  # } curvature setter func

  # property: center
  # center setter func: object center setter
  # {
  @gfxobject.GfxObject.center.setter
  def center(self, center):
    """
    Class property setter: center
    """
    
    self.__ptsX = [x + center[0] - self.center[0] for x in self.__ptsX]
    self.__ptsY = [y + center[1] - self.center[1] for y in self.__ptsY]

    gfxobject.GfxObject.center.fset(self, center)

    self.update_shape()  # update the center
  # } center setter func

  # property: size
  # size setter func: object size setter
  # {
  @gfxobject.GfxObject.size.setter
  def size(self, size):
    """
    Class property setter: size
    """
    
    center_org = self.center

    self.__ptsX = [(x)*size[0]//self.size[0] for x in self.__ptsX]
    self.__ptsY = [(y)*size[1]//self.size[1] for y in self.__ptsY]

    center_new = sum(self.__ptsX)/len(self.__ptsX), sum(self.__ptsY)/len(self.__ptsY)

    gfxobject.GfxObject.center.fset(self, center_new)
    gfxobject.GfxObject.size.fset(self, size)

    self.center = center_org  # update the center
    # } size setter func
  # < getter and setter functions section >

# } GfxLine class


# main func: contains code to test GfxLine class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("300x300")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=300, height=300)
  canvas.pack()
  
  obj1 = GfxLine(sheetCanvas=canvas, points=[[20, 20], [200, 200]], std=CT, mode=MODE[2], tag='OBJ1')

  obj1.draw()

  obj1.arrow= (False, (16, 30, 9))

  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  obj1.colorset = CS
  obj1.brushset = BS

  obj1.mode = MODE[0]
  
  
  
  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
