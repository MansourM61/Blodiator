'''
********************************************************************************

Python Script: gfxpolygon Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxPolygon class the polygon block in
Blodiator. This module is a wrapper for tk.Canvas.create_polygon command.


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
             1- The class is rededined based on the new GfxObject Ver 0.0.6.
             2- 'center' and 'size' are adjustable.
             3- 'fill' parameter bug is fixed.

********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext
from . import gfxobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxPolygon: '


#################################################
DEF_NAME = 'polygon'  # default name
POINT_LIST = [[20, 20], [20, 100], [200, 200]]  # line point list
CAT = 'primitive'  # default category
COLOR_NORMAL = ('black', 'white')  # default color for normal state
COLOR_DISABLED = ('pink', 'blue')  # default color for disabled state
COLOR_SELECTED = ('red', 'green')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'cyan')  # default color for erroneous state
BRUSH_NORMAL = (5.0, (0, ))  # default line thickness and style for normal state
BRUSH_DISABLED = (2.0, (0, ))  # default line thickness and style for disabled state
BRUSH_SELECTED = (3.0, (0, ))  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (4.0, (0, ))  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
FILLED = True  # default fill mode
JOINT = tk.ROUND  # default joint style
CURVATURE = (False, 3)  #  default curvature
#################################################


# GfxPolygon class: this is the polygon class
# {
class GfxPolygon(gfxobject.GfxObject):
  """
  Draws primitive shape of polygon.
  
  Define an instance of 'GfxPolygon' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the polygon
      points = list of points coordinates
      cat = a string showing the category of the polygon
      fill = True the polygon is closed and filled, False the polygon is not filled
      joint = joint styles
      curvature = a tuple corresponding to (if the curvature is included, what is the order of curvature fitting)
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing a polygon
  in Blodiator.
  """
  
  version = '0.0.6'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, points=POINT_LIST, cat=CAT,
               fill=FILLED, joint=JOINT, curvature=CURVATURE, mode=MODE[0], std=None):
    """
    Construct a GfxPolygon
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the polygon
        points = list of points coordinates
        cat = a string showing the category of the polygon
        fill = True the polygon is closed and filled, False the polygon is not filled
        joint = joint styles
        curvature = a tuple corresponding to (if the curvature is included, what is the order of curvature fitting)
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    self.__ptsX = [x for x, y in points]
    self.__ptsY = [y for x, y in points]

    self.__filled = fill

    self.__joint = joint

    self.__curvatureFlag = curvature[0]
    self.__curvaturePar = curvature[1]    

    center = sum(self.__ptsX)/len(self.__ptsX), sum(self.__ptsY)/len(self.__ptsY)
    size = max(self.__ptsX) - min(self.__ptsX), max(self.__ptsY) - min(self.__ptsY)
    
    super(GfxPolygon, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center, size=size,
                                  cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    txt = super(GfxPolygon, self).__repr__()

    txt += '; points = {0}; join = {1};'\
           ' curvature (flag, spline step) = ({2}, {3})'.\
           format(str(self.points), self.__joint,\
                  str(self.__curvatureFlag), self.__curvaturePar)  # generate formatted text

    return txt
  # } __repr__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the polygon on the canvas
    
    input: none
    output: none
    """
    
    points = []

    for x, y in zip(self.__ptsX, self.__ptsY):
      points += [x]
      points += [y]

    if self.__filled == False:
      points += [self.__ptsX[0]]
      points += [self.__ptsY[0]]
      
    fg = self.color[0]
    bg = self.color[1]

    if self.__filled == False:
      self.sheetCanvas.create_line(points, joinstyle=self.__joint, smooth=self.__curvatureFlag,\
                                   splinesteps=self.__curvaturePar, fill=fg, tags=self.tag)
    else:
      self.sheetCanvas.create_polygon(points, joinstyle=self.__joint, smooth=self.__curvatureFlag,\
                                   splinesteps=self.__curvaturePar, outline=fg, fill=bg, tags=self.tag)

    super(GfxPolygon, self).draw()
  # } draw func

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the pokygon color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    super(GfxPolygon, self).update_color()

    fg = self.color[0]
    bg = self.color[1]
   
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle
    
    if self.__filled == False:
      self.sheetCanvas.itemconfig(item, fill=fg)  # set foreground color property
    else:
      self.sheetCanvas.itemconfig(item, outline=fg)  # set foreground color property      
      self.sheetCanvas.itemconfig(item, fill=bg)  # set background color property      
  # } size setter func  

  # update_shape func: update the color
  # {
  def update_shape(self):
    """
    Updates the polygon on the canvas
    
    input: none
    output: none
    """
    
    points = []

    for x, y in zip(self.__ptsX, self.__ptsY):
      points += [x]
      points += [y]

    if self.__filled == False:
      points += [self.__ptsX[0]]
      points += [self.__ptsY[0]]

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.coords(item, points)
  # } update_shape func  

  # update_joint func: update the joint
  # {
  def update_joint(self):
    """
    Updates the polygon joint style on the canvas
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, joinstyle=self.__joint)
  # } update_joint func  

  # update_curvature func: update the curvature
  # {
  def update_curvature(self):
    """
    Updates the polygon curvature on the canvas
    
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
  
  # property: cap join
  # joint getter func: object joint property getter
  # {
  @property
  def joint(self):
    """
    Class property getter: joint style
    """
    
    return self.__joint
  # } joint getter func

  # joint setter func: object joint property setter
  # {
  @joint.setter
  def joint(self, joint):
    """
    Class property setter: joint style
    """
    
    self.__joint = joint

    self.update_joint()
  # } joint setter func

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

# } GfxPolygon class


# main func: contains code to test GfxPolygon class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("500x500")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=400, height=400)
  canvas.pack()
  
  obj1 = GfxPolygon(sheetCanvas=canvas, points=POINT_LIST, fill=True, std=CT, mode=MODE[2], tag='OBJ1')
  obj2 = GfxPolygon(sheetCanvas=canvas, points=POINT_LIST, fill=False, std=CT, mode=MODE[2], tag='OBJ2')

  obj1.mode = MODE[0]
  obj2.mode = MODE[2]

  obj1.draw()
  obj2.draw()
  
  canvas.create_rectangle(obj2.boundary)
  canvas.create_rectangle(obj2.bbox)

  CT.Print(str(obj1.center))
  
  print(repr(obj1))

  CT.Print('\n')

  obj1.mode = MODE[3]
  obj2.mode = MODE[3]

  obj1.center = (200, 200)
  obj2.center = (200, 200)
  
  CT.Print(str(obj1.center))

  CT.Print('\n')

  CT.Print(str(obj1.size))

  obj1.size = (20, 50)

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
