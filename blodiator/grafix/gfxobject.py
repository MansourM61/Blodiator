'''
********************************************************************************

Python Script: gfxobject Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxObject class the root of all shapes in
Blodiator. This class is the abstract class and does not draw any shapes.


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
             1- Removing 'absMove' and 'relMove' functions,
             2- _std and _sheetCanvas are changed to std and sheetCanvas, respectively,
             3- Variables are set to local,
             4- Updating the object after changing the property is added.

Ver 0.0.5: 27 January 2019;
             1- The class is redefined,
             2- 'state' and different color and line versions are added.

Ver 0.0.6: 29 January 2019;
             1- 'canvasSheet' is set to private and getter is added.
             2- 'size', 'center', 'color' update functions are added.
             3- 'mode' function is modified.
             4- 'boundary' property is added.

Ver 0.0.10: 24 Feburary 2019;
             1- erase methods is added.

Ver 0.0.11: 14 March 2019;
             1- 'in' dunar is added.
             2- 'in' dunar is modified to consider tolerance.
             3- 'delete' function is added.

Ver 0.0.30: 24 June 2019;
             1- canvas property is added.

Ver 0.0.31: 24 June 2019;
             1- logging is added.

Ver 0.0.36: 3 July 2019;
             1- update properties are added.
            
********************************************************************************
'''


import tkinter as tk

from ..etc import coloredtext


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxObject: '


#################################################
DEF_NAME = 'object'  # default name
CENTER = (0, 0)  # default center coordinate
SIZE = (0, 0)  # default size
CAT = 'root'  # default category
COLOR_NORMAL = ('black', 'white')  # default color for normal state
COLOR_DISABLED = ('pink', 'blue')  # default color for disabled state
COLOR_SELECTED = ('red', 'green')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'cyan')  # default color for erroneous state
BRUSH_NORMAL = (5.0, [])  # default line thickness and style for normal state
BRUSH_DISABLED = (2.0, (6, ))  # default line thickness and style for disabled state
BRUSH_SELECTED = (3.0, (7, ))  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (4.0, (8, ))  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
BOUNDARY_MARGIN = 0  # default boundary margin
SELECT_TOL = 10  # selection tolerance
#################################################


# GfxObject class: this is the abstract parent class for blockdiagram objects
# {
class GfxObject(object):
  """
  Abstract class for shapes.
  
  Define an instance of 'GfxObject' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the shape
      center = center of the shape
      size = size of the shape
      cat = a string showing the category of the shape
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing and managing 
  shapes in Blodiator. Functions such as updating center, color, brush, tag, label,
  mode, etc are defined in this class.
  """

  version = '0.0.36'  # version of the class

  # < class functions section >
  # is_within inline func: check if a point is inside a box
  # {  
  """
  Internal function.
  
  Checks if a point is inside a box
  
  input:
      point = coordinate of the point
      box = coordinate of the corners of the box
  output:
      True/False = if the point is/is not inside the box
  """
  is_within = lambda point, box: ((point[0] >= min(box[0] - SELECT_TOL, box[2] + SELECT_TOL)) and
                                  (point[0] <= max(box[0] - SELECT_TOL, box[2] + SELECT_TOL)) and
                                  (point[1] >= min(box[1] - SELECT_TOL, box[3] + SELECT_TOL)) and
                                  (point[1] <= max(box[1] - SELECT_TOL, box[3] + SELECT_TOL)))  # check if a point is within a box
  # } is_within inline func

  # put_within inline func: put the point inside the box
  # {
  """
  Internal function.
  
  Makes sure a point lays inside the box
  
  input:
      point = coordinate of the point
      box = coordinate of the corners of the box
  output:
      point = new coordinate of the point
  """
  put_within = lambda point, box: (min(box[2], max(box[0], point[0])),
                                   min(box[3], max(box[1], point[1]))) # put the point within the box
  # } put_within inline func
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, center=CENTER, size=SIZE,
               cat=CAT, mode=MODE[0], std=None):
    """
    Construct a GfxObject
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the shape
        center = center of the shape
        size = size of the shape
        cat = a string showing the category of the shape
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    if std is None:
      print('\n' + src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std

    if sheetCanvas is None:
      print('\n' + src + ': Please specify the canvas of the blockdiagram sheet!')
      exit()
    else:
      self.__sheetCanvas = sheetCanvas  # canvas of the blockdiagram sheet

    self.__cat = cat  # shape catogory
    self.__tag = tag  # tag attached to the object
    self.__centX, self.__centY = center[0], center[1]  # x and y coordinates of bounding box center
    self.__width, self.__height = size[0], size[1]  # width and height of bounding box center
    self.__mode = mode  # object mode
    self.__boundaryMargin = BOUNDARY_MARGIN

    colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, COLOR_ERRONEOUS]
    brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

    self.__colorset = dict(zip(MODE, colorList))
    self.__brushset = dict(zip(MODE, brushList))

    self.__boundary = []
    
    self.__fg, self.__bg = (self.__colorset[self.__mode])[0],\
                           (self.__colorset[self.__mode])[1]  # object forground and background colors
    self.__thickness, self.__lnStyle = (self.__brushset[self.__mode])[0],\
                                       (self.__brushset[self.__mode])[1]  # object line thickness and style
    self.update_bbox()
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """

    txt = 'shape = \'{0}\'; tag = \'{1}\'; center (x, y) = ({2}, {3});'\
        ' size (width, height) = ({4}, {5}); bounding box (x0, y0, x1, y1) = {6}; mode = {7};'\
        ' color (foreground, background) = ({8}, {9}); line (thickness, style) = ({10}, {11})'\
        .format(self.__cat, self.__tag, self.__centX, self.__centY,
                self.__width, self.__height, self.bbox, self.__mode,
                self.__fg, self.__bg, self.__thickness, self.__lnStyle)  # generate formatted text

    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """

    txt = 'shape = \'{0}\'; center (x, y) = ({1}, {2});'\
        ' (width, height) = ({3}, {4}); mode = {5}'\
        .format(self.__cat, self.__centX, self.__centY,\
                self.__width, self.__height, self.__mode)  # generate formatted text

    return txt
  # } __str__ func

  # __contains__ func: in dunar
  # {
  def __contains__(self, arg):
    """
    Class in dunar function.
    """

    return GfxObject.is_within(arg, self.bbox)
  # } __contains__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the shape on the canvas
    
    input: none
    output: none
    """

    item = self.__sheetCanvas.find_withtag(self.__tag)  # retirieve object handle

    self.__sheetCanvas.itemconfig(item, width=self.__thickness)  # set thickness properties
    self.__sheetCanvas.itemconfig(item, dash=self.__lnStyle)  # set thickness properties

    self.update_bbox()  # update bounding and margin box
  # } draw func

  # erase func: erase the object
  # {
  def erase(self):
    """
    Erases the shape on the canvas
    
    input: none
    output: none
    """

    item = self.__sheetCanvas.find_withtag(self.__tag)  # retirieve object handle

    self.__sheetCanvas.delete(item)
  # } erase func

  # update_bm_boxes func: update bounding and margin boxes
  # {
  def update_bbox(self):
    """
    Updates the bounding box of the shape
    
    input: none
    output: none
    """

    self.__bbox = [self.__centX - self.__width // 2, self.__centY - self.__height // 2,
                  self.__centX + self.__width // 2, self.__centY + self.__height // 2]  # boundig box (x0, y0, x1, y1)
  # } update_bm_boxes func

  # update_size func: update size of the object
  # {
  def update_shape(self):
    """
    Updates the shape on the canvas
    
    input: none
    output: none
    """
    
    item = self.__sheetCanvas.find_withtag(self.__tag)  # retirieve object handle
    self.__sheetCanvas.coords(item, self.__bbox)  # set new size
  # } update_shape func

  # update_line func: update line thickness and style of the object
  # {
  def update_brush(self):
    """
    Updates the shape brush set (line thickness and style for all different modes)
    
    input: none
    output: none
    """

    self.__thickness, self.__lnStyle = (self.__brushset[self.__mode])[0],\
                                       (self.__brushset[self.__mode])[1]  # object line thickness and style
    
    style = []
    for s in self.__lnStyle:
      style.append(int(s))
    
    item = self.__sheetCanvas.find_withtag(self.__tag)  # retirieve object handle
    self.__sheetCanvas.itemconfig(item, width=self.__thickness)  # set thickness properties
    self.__sheetCanvas.itemconfig(item, dash=style)  # set thickness properties
  # } update_line func

  # update_color func: update color of the object
  # {
  def update_color(self):
    """
    Updates the shape color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """

    self.__fg, self.__bg = (self.__colorset[self.__mode])[0],\
                           (self.__colorset[self.__mode])[1]  # object forground and background colors
  # } update_color func

  # update_center func: update center of the object
  # {
  def update_center(self):
    """
    Updates the shape center
    
    input: none
    output: none
    """
    
    self.update_bbox()  # update bounding and margin box
    self.update_shape()  # update the shape
  # } update_center func


  # update_size func: update size of the object
  # {
  def update_size(self):
    """
    Updates the shape size
    
    input: none
    output: none
    """
    
    self.update_bbox()  # update bounding and margin box
    self.update_shape()  # update the shape
  # } update_size func

  # < class functions section >

  # < getter and setter functions section >
  # property: cat
  # category getter func: object category getter
  # {
  @property
  def category(self):
    """
    Class property getter: category
    """

    return self.__cat
  # } category getter func

  # category setter func: object category setter
  # {
  @category.setter
  def category(self, cat):
    """
    Class property setter: category
    """

    self.__cat = cat
  # } category setter func

  # property: tag
  # tag getter func: object tag getter
  # {
  @property
  def tag(self):
    """
    Class property getter: tag
    """

    return self.__tag
  # } label getter func

  # tag setter func: object tag setter
  # {
  @tag.setter
  def tag(self, tag):
    """
    Class property setter: tag
    """

    item = self.__sheetCanvas.find_withtag(self.__tag)  # retirieve object handle
    self.__sheetCanvas.dtag(item, self.__tag)  # remove the tag
    self.__sheetCanvas.itemconfig(item, tags=tag)  # set tag property
    self.__tag = tag
  # } tag setter func

  # property: center
  # center getter func: object center coordinate getter
  # {
  @property
  def center(self):
    """
    Class property getter: center
    """

    return self.__centX, self.__centY
  # } center getter func

  # center setter func: object center coordinate setter
  # {
  @center.setter
  def center(self, center):
    """
    Class property setter: center
    """

    self.__centX, self.__centY = center

    self.update_center()
  # } center setter func

  # property: size
  # size getter func: object width and height size getter
  # {
  @property
  def size(self):
    """
    Class property getter: size (width, height)
    """

    return self.__width, self.__height
  # } size getter func

  # size setter func: object width and height size setter
  # {
  @size.setter
  def size(self, size):
    """
    Class property setter: size (width, height)
    """

    self.__width, self.__height = size[0], size[1]
    self.update_size()
  # } size setter func

  # property: mode
  # mode getter func: object mode getter
  # {
  @property
  def mode(self):
    """
    Class property getter: mode ('normal', 'disabled', 'selected', 'erroneous')
    """

    return self.__mode
  # } mode getter func

  # mode setter func: object mode setter
  # {
  @mode.setter
  def mode(self, mode):
    """
    Class property setter: mode ('normal', 'disabled', 'selected', 'erroneous')
    """

    self.__mode = mode
    self.update_brush()  # update the brush
    self.update_color()  # update the color
  # } mode setter func

  # property: color
  # color getter func: object foreground and background colors getter
  # {
  @property
  def color(self):
    """
    Class property getter: foreground and background colors of the shape at the current mode
    """

    return self.__fg, self.__bg
  # } color getter func

  # property: brush
  # brush getter func: object line thickness and style getter
  # {
  @property
  def brush(self):
    """
    Class property setter: line thickness and style of the shape at the current mode
    """

    return self.__thickness, self.__lnStyle
  # } brush getter func

  # property: color set
  # colorset getter func: object color set getter
  # {
  @property
  def colorset(self):
    """
    Class property getter: the shape color set (outline and filling colors for all different modes)
    """

    return self.__colorset
  # } colorset getter func

  # colorset setter func: object color set setter
  # {
  @colorset.setter
  def colorset(self, colorset):
    """
    Class property setter: the shape color set (outline and filling colors for all different modes)
    """

    self.__colorset = colorset
    self.update_color()  # update the color
  # } colorset setter func

  # property: brush set
  # brushset getter func: object brush set getter
  # {
  @property
  def brushset(self):
    """
    Class property getter: the shape brush set (line thickness and style for all different modes)
    """

    return self.__brushset
  # } brushset getter func

  # brushset setter func: object brush set setter
  # {
  @brushset.setter
  def brushset(self, brushset):
    """
    Class property setter: the shape brush set (line thickness and style for all different modes)
    """

    self.__brushset = brushset
    self.update_brush()  # update the brush
  # } brushset setter func

  # property: boundary margin
  # boundaryMargin getter func: object boundary margin getter
  # {
  @property
  def boundaryMargin(self):
    """
    Class property getter: boundary margin
    """

    return self.__boundaryMargin
  # } boundaryMargin getter func

  # brushset setter func: object brush set setter
  # {
  @boundaryMargin.setter
  def boundaryMargin(self, boundaryMargin):
    """
    Class property setter: boundary margin
    """

    self.__boundaryMargin = boundaryMargin
  # } boundaryMargin setter func

  # property: bbox
  # bbox getter func: bounding box line getter
  # {
  @property
  def bbox(self):
    """
    Class property getter: bounding box
    """

    return self.__bbox
  # } bbox getter func

  # property: boundary
  # boundary getter func: object boundary getter
  # {
  @property
  def boundary(self):
    """
    Class property setter: bounding box
    """

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    box = self.sheetCanvas.bbox(item)

    Margin = BOUNDARY_MARGIN + self.__thickness//2
    
    return (box[0] - Margin, box[1] - Margin,
            box[2] + Margin, box[3] + Margin)
  # } boundary getter func

  # property: sheetCanvas
  # sheetCanvas getter func: object sheet canvas getter
  # {
  @property
  def sheetCanvas(self):
    """
    Class property getter: canvas
    """

    return self.__sheetCanvas
  # } sheetCanvas getter func

  # sheetCanvas setter func: object sheetCanvas set setter
  # {
  @sheetCanvas.setter
  def sheetCanvas(self, sheetCanvas):
    """
    Class property setter: canvas
    """

    self.__sheetCanvas = sheetCanvas
  # } sheetCanvas setter func
  # < getter and setter functions section >

# } GfxObject class


# main func: contains code to test GfxObject class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("800x800")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=600, height=600)
  canvas.pack()

  obj = GfxObject(sheetCanvas=canvas, std=CT)
  
  CT.Print(text='dir: ' + str(dir(obj)))

  CT.Print('\n')

  obj.draw()

  print(repr(obj))

  CT.Print('\n')

  obj.category = 'cat test'
  obj.tag = 'tag test'
  obj.center = (20, 30)
  obj.size = (5, 10)
  obj.mode = MODE[3]

  CT.Print(text='category: ' + obj.category)
  CT.Print(text='label: ' + obj.tag)
  CT.Print(text='center: ' + str(obj.center))
  CT.Print(text='size: ' + str(obj.size))
  CT.Print(text='mode: ' + obj.mode)
  CT.Print(text='bbox: ' + str(obj.bbox))
  CT.Print(text='color set: ' + str(obj.colorset))
  CT.Print(text='brush set: ' + str(obj.brushset))

  CT.Print('\n')

  CT.Print(repr(obj))

  obj.tag = 'DIR'

  CT.Print('\n')

  CT.Print(repr(obj))
  
  colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, ('magenta', 'cyan')]
  brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

  CS = dict(zip(MODE, colorList))
  BS = dict(zip(MODE, brushList))

  obj.colorset = CS

  CT.Print(str(obj.colorset))

  CT.Print(str(obj.color))

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
