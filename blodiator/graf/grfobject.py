'''
********************************************************************************

Python Script: grfobject Module
Writter: Mojtaba Mansour Abadi
Date: 7 Feburary 2019

This Python script is compatible with Python 3.x.
The script is used to define GrfObject class the root of all blocks in
Blodiator. This class is the abstract class and does not draw any blocks.


GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:
    
Ver 0.0.7: 30 January 2019;
             first code

Ver 0.0.8: 7 Feburary 2019;
             1- center changing is fixed.

Ver 0.0.16: 4 June 2019;
             1- reordering the object is added.

Ver 0.0.30: 24 June 2019;
             1- canvas property is added.

Ver 0.0.31: 24 June 2019;
             1- logging is added.

Ver 0.0.36: 3 July 2019;
             1- node/connector loading properties are added.
            
Ver 0.0.39: 11 July 2019;
             1- signal type is corrected.
             2- color/connector type property is fixed.

********************************************************************************
'''


import tkinter as tk

from ..etc import cntsheetcanavs
from ..etc import coloredtext



style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GrfObject: '


#################################################
DEF_NAME = 'graph'  # default name
CENTER = (0, 0)  # default center coordinate
SIZE = (0, 0)  # default size
CAT = 'root'  # default category
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
BOUNDARY_MARGIN = 0  # default boundary margin
COLOR = ('black', 'white')  # default color
BRUSH = (1.0, [])  # default line thickness and style
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfObject class: this is the abstract parent class for blockdiagram objects
# {
class GrfObject(object):
  """
  Abstract class for block diagram items.
  
  Define an instance of 'BlodiatorBase' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the shape
      label = item label
      center = center of the shape
      colorset = tuple containing the shape color set (outline and filling colors for all different modes)
      brushset = tuple containing the shape brush set (line thickness and style for all different modes)
      cat = a string showing the category of the shape
      con_type = connection type: ('none', 'logical', 'electrical', 'optical')
      inPort = list containing information about input ports of the item
      outPort = list containing information about output ports of the item
      color_type = a tuple containing colors for different coneection type
      func = function associated with the item
      mode = state of the item: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing and managing 
  block diagram items in Blodiator. Functions such as updating center, color,
  brush, tag, label, input and output ports, mode, etc are defined in this class.
  """
  
  version = '0.0.39'  # version of the class

  ObjOrder = 0   # object order in the canvas

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
  
  is_within = lambda point, box: ((point[0] >= box[0]) and (point[0] <= box[2]) and
                                  (point[1] >= box[1]) and (point[1] <= box[3]))  # check if a point is within a box
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
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME, center=CENTER, colorset=None,
               brushset=None, mode=MODE[0], con_type=SIG_TYPE[0], inPort=None, outPort=None,
               color_type=CON_COLOR ,func=None, std=None):
    """
    Construct a GrfObject
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the shape
        label = item label
        center = center of the shape
        colorset = tuple containing the shape color set (outline and filling colors for all different modes)
        brushset = tuple containing the shape brush set (line thickness and style for all different modes)
        cat = a string showing the category of the shape
        con_type = connection type: ('none', 'logical', 'electrical', 'optical')
        inPort = list containing information about input ports of the item
        outPort = list containing information about output ports of the item
        color_type = a tuple containing colors for different coneection type
        func = function associated with the item
        mode = state of the item: 'normal', 'disabled', 'selected', 'erroneous'
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

    self.__shapeorder = GrfObject.ObjOrder
    GrfObject.ObjOrder = GrfObject.ObjOrder + 1
    
    self.__cat = cat
    self.__label = label
    self.__centX, self.__centY = center
    self.__fg, self.__bg = COLOR
    self.__thickness, self.__lnStyle = BRUSH
    self.__colorset = colorset
    self.__brushset = brushset    
    self.__mode = mode
    self.__inPort = inPort
    self.__outPort = outPort
    self.__function = func
    self.__grfx = []
    self.__bbox = (0, 0, 0, 0)
    self.__con_type = con_type
    self.__color_type = color_type

    self.initBlock()
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = 'cat = \'{0}\'; label = \'{1}\'; center (x, y) = ({2}, {3});'\
        ' bounding box (x0, y0, x1, y1) = {4}; mode = {5};'\
        ' function = {6}; input port = {7}; output port = {8}'\
        .format(self.__cat, self.__label, self.__centX, self.__centY,
                self.bbox, self.__mode, self.__function,\
                self.__inPort, self.__outPort)  # generate formatted text

    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = 'label = \'{0}\'; center (x, y) = ({1}, {2});'\
        ' mode = {3}; function = {4}; input port = {5}; output port = {6}'\
        .format(self.__label, self.__centX, self.__centY, self.__mode, self.__function,\
                self.__inPort, self.__outPort)  # generate formatted text

    return txt
  # } __str__ func

  # __contains__ func: in dunar
  # {
  def __contains__(self, arg):
    """
    Class in dunar function.
    """
    
    return None
  # } __contains__ func
  # < inherited functions section >

  # < class functions section >
  # raise func: raise the object on the canvas
  # {
  def raise_order(self):
    """
    Raises the order of the item in the canvas
    
    input: none
    output: none
    """
    
    for obj in self.__grfx:
      item = self.__sheetCanvas.find_withtag(obj.tag)
      self.__sheetCanvas.tag_raise(item)

  # } raise func


  # lower func: lower the object on the canvas
  # {
  def lower_order(self):
    """
    lowers the order of the item in the canvas
    
    input: none
    output: none
    """    
    
    for obj in self.__grfx:
      item = self.__sheetCanvas.find_withtag(obj.tag)
      self.__sheetCanvas.tag_lower(item)

  # } lower func

  
  # erase func: erase the object from the canvas
  # {
  def erase(self):
    """
    Erases the item from the canvas
    
    input: none
    output: none
    """
    
    for obj in self.__grfx:
      obj.erase()

    self.__grfx = None      
  # } erase func

  # bring_2_front func: update the bounding box
  # {
  def bring_2_front(self):
    """
    Raises the item to the toppest position on the canvas
    
    input: none
    output: none
    """
    
    for obj in self.grfx:
      item = self.__sheetCanvas.find_withtag(obj.tag)
      self.__sheetCanvas.tag_raise(item)
      
    self.__shapeorder = GrfObject.ObjOrder
    GrfObject.ObjOrder = GrfObject.ObjOrder + 1
      
  # } bring_2_front func

  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the items on the canvas
    
    input: none
    output: none
    """
    
    for obj in self.__grfx:
      obj.draw()
      
    self.update_bbox()
  # } draw func

  # initBlock func: initialise the object
  # {
  def initBlock(self):
    """
    Initialises the item graphics on the canvas
    
    input: none
    output: none
    """
    
    self.update_bbox()
  # } initBlock func

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the item color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    pass
  # } update_color func  

  # update_brush func: update the brush
  # {
  def update_brush(self):
    """
    Updates the item brush set (line thickness and style for all different modes)
    
    input: none
    output: none
    """
    
    pass
  # } update_brush func  

  # update_bsheet func: update the canvas sheet boundary
  # {
  def update_bsheet(self):
    """
    Updates the sheet boundary (not used)
    
    input: none
    output: none
    """
    
    self.canvasWidth = int(self.__sheetCanvas.cget("width"))  # width of sheet
    self.canvasHeight = int(self.__sheetCanvas.cget("height"))  # height of sheet
  # } update_bsheet func  

  # update_mode func: update the mode
  # {
  def update_mode(self):
    """
    Updates the item mode ('normal', 'disabled', 'selected', 'erroneous')
    
    input: none
    output: none
    """ 
    
    for obj in self.__grfx:
      obj.mode = self.__mode      
  # } update_mode func  

  # update_center func: update the center
  # {
  def update_center(self):
    """
    Updates the item center
    
    input: none
    output: none
    """ 
    
    self.update_bbox()
  # } update_center func  

  # update_bbox func: update the bounding box
  # {
  def update_bbox(self):
    """
    Updates the item bounding box
    
    input: none
    output: none
    """ 
    
    pass
  # } update_bbox func  
  # < class functions section >

  # < getter and setter functions section >
  # property: grfx
  # grfx getter func: graph shape getter
  # {
  @property
  def grfx(self):
    """
    Class property getter: the list containing the items graphics
    """
    
    return self.__grfx
  # } grfx getter func

  # grfx setter func: graph graph shape setter
  # {
  @grfx.setter
  def grfx(self, grfx):
    """
    Class property setter: the list containing the items graphics
    """
    
    self.__grfx = grfx
  # } grfx setter func  

  # property: cat
  # cat getter func: graph cat getter
  # {
  @property
  def cat(self):
    """
    Class property getter: category
    """
    
    return self.__cat
  # } cat getter func

  # cat setter func: graph cat setter
  # {
  @cat.setter
  def cat(self, cat):
    """
    Class property setter: category
    """
    
    self.__cat = cat
  # } cat setter func  

  # property: label
  # label getter func: graph label getter
  # {
  @property
  def label(self):
    """
    Class property getter: label
    """
    
    return self.__label
  # } label getter func

  # label setter func: graph label setter
  # {
  @label.setter
  def label(self, label):
    """
    Class property setter: label
    """
    
    self.__label = label
  # } label setter func  

  # property: function
  # function getter func: graph function getter
  # {
  @property
  def function(self):
    """
    Class property getter: associated function
    """
    
    return self.__function
  # } function getter func

  # function setter func: graph function setter
  # {
  @function.setter
  def function(self, function):
    """
    Class property setter: associated function
    """
    
    self.__function = function
  # } function setter func  

  # property: mode
  # mode getter func: graph mode getter
  # {
  @property
  def mode(self):
    """
    Class property getter: mode ('normal', 'disabled', 'selected', 'erroneous')
    """
    
    return self.__mode
  # } mode getter func

  # mode setter func: graph mode setter
  # {
  @mode.setter
  def mode(self, mode):
    """
    Class property setter: mode ('normal', 'disabled', 'selected', 'erroneous')
    """
    
    self.__mode = mode
    self.update_mode()
  # } mode setter func  

  # property: center
  # center getter func: graph center getter
  # {
  @property
  def center(self):
    """
    Class property getter: center
    """
    
    return self.__centX, self.__centY
  # } center getter func

  # center setter func: graph center setter
  # {
  @center.setter
  def center(self, center):
    """
    Class property setter: center
    """
    
    self.__centX, self.__centY = center
    self.update_center()
  # } center setter func

  # property: inPort
  # inPort getter func: graph input port getter
  # {
  @property
  def inPort(self):
    """
    Class property getter: input port
    """
    
    return self.__inPort
  # } inPort getter func

  # inPort setter func: graph center setter
  # {
  @inPort.setter
  def inPort(self, inPort):
    """
    Class property setter: input port
    """
    
    self.__inPort = inPort
  # } inPort setter func

  # property: outPort
  # outPort getter func: graph input port getter
  # {
  @property
  def outPort(self):
    """
    Class property getter: output port
    """
    
    return self.__outPort
  # } outPort getter func

  # outPort setter func: graph center setter
  # {
  @outPort.setter
  def outPort(self, outPort):
    """
    Class property setter: output port
    """
    
    self.__outPort = outPort
  # } outPort setter func

  # property: bbox
  # bbox getter func: bounding box getter
  # {
  @property
  def bbox(self):
    """
    Class property getter: bounding box
    """
    
    return self.__bbox
  # } bbox getter func
  
  # bbox setter func: bounding box setter
  # {
  @bbox.setter
  def bbox(self, bbox):
    """
    Class property setter: bounding box
    """
    
    self.__bbox = bbox
  # } bbox setter func

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
    Class property getter: the item color set (outline and filling colors for all different modes)
    """
    
    return self.__colorset
  # } colorset getter func

  # colorset setter func: object color set setter
  # {
  @colorset.setter
  def colorset(self, colorset):
    """
    Class property setter: the item color set (outline and filling colors for all different modes)
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
    Class property getter: the item brush set (line thickness and style for all different modes)
    """
    
    return self.__brushset
  # } brushset getter func

  # brushset setter func: object brush set setter
  # {
  @brushset.setter
  def brushset(self, brushset):
    """
    Class property setter: the item brush set (line thickness and style for all different modes)
    """
    
    self.__brushset = brushset
    self.update_brush()  # update the brush
  # } brushset setter func

  
  # property: shape order
  # shaperorder getter func: shaper order set getter
  # {
  @property
  def shapeorder(self):
    """
    Class property getter: the item order in canvas
    """
    
    return self.__shapeorder
  # } shapeorder getter func

  # shaperorder setter func: shaper order set setter
  # {
  @shapeorder.setter
  def shapeorder(self, shapeorder):
    """
    Class property setter: the item order in canvas
    """
    
    self.__shapeorder = shapeorder
  # } shapeorder setter func

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

    for obj in self.grfx:
      obj.sheetCanvas = sheetCanvas
    
  # } sheetCanvas setter func


  # property: con_type
  # con_type getter func: connector type getter
  # {
  @property
  def con_type(self):
    """
    Class property getter: connection type ('none', 'logical', 'electrical', 'optical')
    """
    
    return self.__con_type
  # } con_type getter func

  # con_type setter func: connector type setter
  # {
  @con_type.setter
  def con_type(self, con_type):
    """
    Class property setter: connection type ('none', 'logical', 'electrical', 'optical')
    """
    
    color_narmal = self.__colorset[MODE[0]]
    color_selected = self.__colorset[MODE[1]]
    color_disabled = self.__colorset[MODE[2]]
    color_erroneous = self.__colorset[MODE[3]]

#    color_set = self.__colorset
    
#    normal_colorset = color_set[MODE[0]]

    self.__con_type = con_type
    
    Color = [self.__color_type[self.__con_type]]
    
    for col in color_narmal[1:]:
      Color.append(col)
        
    colorList = tuple([Color, color_selected, color_disabled, color_erroneous])

    color_set = dict(zip(MODE, colorList))
        
    self.__colorset = color_set
    self.update_color()  # update the color
  # } con_type setter func

  # property: color_type
  # color_type getter func: color type getter
  # {
  @property
  def color_type(self):
    """
    Class property getter: connection colors set ('none', 'logical', 'electrical', 'optical')
    """
    
    return self.__color_type
  # } color_type getter func

  # color_type setter func: color type setter
  # {
  @color_type.setter
  def color_type(self, color_type):
    """
    Class property setter: connection colors set ('none', 'logical', 'electrical', 'optical')
    """
    
    color_narmal = self.__colorset[MODE[0]]
    color_selected = self.__colorset[MODE[1]]
    color_disabled = self.__colorset[MODE[2]]
    color_erroneous = self.__colorset[MODE[3]]

#    color_set = self.__colorset
#    
#    normal_colorset = color_set[MODE[0]]
#    
    self.__color_type = color_type
        
    Color = [self.__color_type[self.__con_type]]
    
    for col in color_narmal[1:]:
      Color.append(col)
        
    colorList = tuple([Color, color_selected, color_disabled, color_erroneous])

    color_set = dict(zip(MODE, colorList))
 
    self.__colorset = color_set
    self.update_color()  # update the color
  # } color_type setter func

  # < getter and setter functions section >
# } GrfObject class


# main func: contains code to test GrfObject class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("800x800")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=600, height=600)
  canvas.pack()

  obj = GrfObject(sheetCanvas=canvas, label='graph', std=CT)

  obj.draw()

  CT.Print(repr(obj))

  CT.Print('\n')
  
  CT.Print(str(obj))

  CT.Print('\n')
  
  CT.Print(str(obj.bbox))
  
  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
