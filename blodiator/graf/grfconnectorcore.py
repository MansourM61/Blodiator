'''
********************************************************************************

Python Script: GrfConnectorCore Module
Writter: Mojtaba Mansour Abadi
Date: 7 February 2019

This Python script is compatible with Python 3.x.
The script is used to define GrfConnectorCore class the connector in
Blodiator. The connector used in the block diagrams is handled by this class.


GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:
    
Ver 0.0.7: 3 February 2019;
             first code

Ver 0.0.8: 7 February 2019;
             1- Multiple boundary boxes feature is added.
             2- '__contains__' dunar is added.

Ver 0.0.11: 11 March 2019;
             1- The direction of the arrows bug is fixed.
             2- 'str' and 'repr' are fixed.
             2- 'in' dunar is fixed.

Ver 0.0.11: 14 March 2019;
             1- The 'erase' method is added.

Ver 0.0.15: 3 June 2019;
             1- 'selectedWire' is added.         

Ver 0.0.31: 24 June 2019;
             1- logging is added.

Ver 0.0.32: 28 June 2019;
             1- Class is chanfged to GrfConnectorCore.
             2- Changin mode and colorset is added.

Ver 0.0.36: 3 July 2019;
             1- node/connector loading properties are added.
            
********************************************************************************
'''


import tkinter as tk

from ..etc import cntsheetcanavs
from ..etc import coloredtext
from . import grfobject
from ..grafix import gfxline



style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GrfConnectorCore: '


#################################################
DEF_NAME = 'connector'  # default name
CENTER = (300, 300)  # default center coordinate
SIZE = 10  # default size
CAT = 'graph'  # default category
COLOR_NORMAL = ('black', 'black')  # default color for normal state
COLOR_DISABLED = ('pink', 'pink')  # default color for disabled state
COLOR_SELECTED = ('red', 'red')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'yellow')  # default color for erroneous state
BRUSH_NORMAL = (5, [])  # normal brush thickness
BRUSH_DISABLED = (2, [2,])  # disabled brush thickness
BRUSH_SELECTED = (1, [2,])  # selected brush thickness
BRUSH_ERRONEOUS = (2, [1, 1,])  # erroneous brush thickness
BRUSH_THICKNESS = 1  # default brush thickness
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
BOUNDARY_MARGIN = 0  # default boundary margin
IN_PORT = ('0', (30, 30), None, None)  # default input port
OUT_PORT = ('0', (200, 100), None, None)  # default output port
INIT_LEN = 10  # initial length
ARROW = (12, 25, 9)  # default arrow style
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfConnectorCore class: this is the connector class for blockdiagram objects
# {
class GrfConnectorCore(grfobject.GrfObject):
  """
  Connector item in the Blodiator.
  
  Define an instance of 'GrfConnectorCore' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the block
      label = item label
      cat = a string showing the category of the block
      inPort = list containing information about input ports of the item
      outPort = list containing information about output ports of the item
      con_type = connection type: ('none', 'logical', 'electrical', 'optical')
      color_type = a tuple containing colors for different coneection type
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing and managing 
  connector item in Blodiator. Functions such as updating center, color,
  brush, tag, label, input and output ports, mode, etc are defined in this class.
  """
  
  version = '0.0.36'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME,
               mode=MODE[0], inPort=IN_PORT, outPort=OUT_PORT,
               con_type=SIG_TYPE[0], color_type=CON_COLOR, std=None):
    """
    Construct a GrfConnectorCore
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the block
        label = item label
        center = center of the block
        cat = a string showing the category of the block
        inPort = list containing information about input ports of the item
        outPort = list containing information about output ports of the item
        con_type = connection type: ('none', 'logical', 'electrical', 'optical')
        color_type = a tuple containing colors for different coneection type
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    if std is None:
      print(src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std


    self.std.Print('Initialising GrfConnectorCore', fg, bg, style, src)

    self.grfx = []

    self.__inPort_id = inPort[0]
    self.__inPort_Pos = inPort[1]

    self.__outPort_id = outPort[0]
    self.__outPort_Pos = outPort[1]

    self.__selectedWire = None

    self.__arrow = ARROW

    center = (self.__inPort_Pos[0] + self.__outPort_Pos[0])//2,\
             (self.__inPort_Pos[1] + self.__outPort_Pos[1])//2

    colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, COLOR_ERRONEOUS]
    brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

    colorset = dict(zip(MODE, colorList))
    brushset = dict(zip(MODE, brushList))

    super(GrfConnectorCore, self).__init__(sheetCanvas=sheetCanvas, cat=cat, label=label,
                                       colorset=colorset, brushset= brushset, color_type=color_type,
                                       center=center, mode=mode, con_type=con_type, std=std)

    inPort, outPort = self.reg_pts()

    self.inPort = (self.__inPort_id, inPort, None, None)
    self.outPort = (self.__outPort_id, outPort, None, None)    
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GrfConnectorCore, self).__repr__()

    txt += '; points = ({0}, {1})'.format(self.inPortPos, self.outPortPos)  # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GrfConnectorCore, self).__str__()

    inID = self.inPort[1]

    outID = self.outPort[1]

    txt += '; input ID = ({0}); output ID = ({1})'.format(inID, outID)  # generate formatted text
    return txt
  # } __str__ func

  # __contains__ func: in dunar
  # {
  def __contains__(self, arg):
    """
    Class in dunar function.
    """
    
    line = self.grfx

    for i in range(0, 3):
      obj = line[i]
      if arg in obj:
        Flag = True
        self.__selectedWire = obj
        break
    else:
      Flag = False
      self.__selectedWire = None

    return Flag
  # } __contains__ func  
  # < inherited functions section >

  # < class functions section >  
  # calc_pts func: calculate the points
  # {
  def calc_pts(self):
    """
    Internal function.
    
    Calculates the coordinates of the start/middle/stop points of the connector
    
    input: none
    output:
        (x, y) = coordinates of the start/middle/stop points
        ArrowFlag = if a flag is needed for each section of the connector
        (x_dir, y_dir) = +1/-1 if direction is along positive/negative axis
    """
    
    x_s, y_s = self.__inPort_Pos
    x_e, y_e = self.__outPort_Pos

    minVertLen = max(ARROW)

    delX = x_e - x_s
    delY = y_e - y_s

    x_dir = +1 if delX > 0 else (-1 if delX < 0 else 0)
    y_dir = +1 if delY > 0 else (-1 if delY < 0 else 0)

    x = [x_s, x_s + delX//2, x_s + delX//2, x_e,
         x_s + (delX//4 + minVertLen//2)*abs(x_dir),
         x_s + (delX//2)*abs(x_dir),
         x_s + (3*delX//4 + minVertLen//2)*abs(x_dir)]

    y = [y_s, y_s, y_e, y_e,
         y_s,
         y_s + (delY//2 + minVertLen//2)*abs(y_dir),
         y_e]

    ArrowFlag = [False]*4 + [abs(delX//4) >= minVertLen] + [abs(delY//2) >= minVertLen] + [abs(delX//4) >= minVertLen]

    return x, y, ArrowFlag, x_dir, y_dir
  # } calc_pts func  

  # initBlock func: initialise the object
  # {
  def initBlock(self):
    """
    Initialises the connector graphics on the canvas
    
    input: none
    output: none
    """
    
    self.std.Print('Setting up GrfConnectorCore', fg, bg, style, src)

    x, y, ArrowFlag, x_dir, y_dir = self.calc_pts()
    
    tag = self.label + '-line-'

    Line = [None] * 6

    for i in range(0, 3):
      pts = [ [x[i], y[i]], [x[i + 1], y[i + 1]] ]
      ar = (False, ARROW)
      Line[i] = gfxline.GfxLine(sheetCanvas=self.sheetCanvas, points=pts, std=self.std,
                                mode=self.mode, arrow=ar, cap_joint=(tk.ROUND, tk.ROUND),
                                tag=tag + str(i))

    min_x = x[4] - x_dir
    max_x = x[4] + x_dir
    pts = [ [min_x, y[4]], [max_x, y[4]] ]
    Line[3] = gfxline.GfxLine(sheetCanvas=self.sheetCanvas, points=pts, std=self.std,
                            mode=self.mode, arrow=(ArrowFlag[4], ARROW), tag=tag + '3')

    min_y = y[5] - y_dir
    max_y = y[5] + y_dir    
    pts = [ [x[5], min_y], [x[5], max_y] ]
    Line[4] = gfxline.GfxLine(sheetCanvas=self.sheetCanvas, points=pts, std=self.std,
                            mode=self.mode, arrow=(ArrowFlag[5], ARROW), tag=tag + '4')

    min_x = x[6] - x_dir
    max_x = x[6] + x_dir    
    pts = [ [min_x, y[6]], [max_x, y[6]] ]
    Line[5] = gfxline.GfxLine(sheetCanvas=self.sheetCanvas, points=pts, std=self.std,
                            mode=self.mode, arrow=(ArrowFlag[6], ARROW), tag=tag + '5')

    self.grfx = Line
    
    center = (x[0] + x[3])//2,\
             (y[0] + y[3])//2
    
    grfobject.GrfObject.center.fset(self, center)

    self.update_bbox()

    self.update_color()
    self.update_brush()
    self.update_arrow()
    
  # } initBlock func  

  # update_ends func: update the end points
  # {
  def update_ends(self):
    'function to update the bounding box; no input; no output'

    x, y, ArrowFlag, x_dir, y_dir = self.calc_pts()

    Line = self.grfx

    for i in range(0, 3):
      pts = [ [x[i], y[i]], [x[i + 1], y[i + 1]] ]
      Line[i].points = pts

    min_x = x[4] - x_dir
    max_x = x[4] + x_dir
    pts = [ [min_x, y[4]], [max_x, y[4]] ]
    Line[3].points = pts
    Line[3].arrow= (ArrowFlag[4], ARROW)

    min_y = y[5] - y_dir
    max_y = y[5] + y_dir
    pts = [ [x[5], min_y], [x[5], max_y] ]
    Line[4].points = pts
    Line[4].arrow= (ArrowFlag[5], ARROW)

    min_x = x[6] - x_dir
    max_x = x[6] + x_dir    
    pts = [ [min_x, y[6]], [max_x, y[6]] ]
    Line[5].points = pts
    Line[5].arrow= (ArrowFlag[6], ARROW)

    self.reset_ports()
  # } update_ends func  

  # update_bbox func: update the bounding box
  # {
  def update_bbox(self):
    """
    Updates the connector bounding box
    
    input: none
    output: none
    """ 
    
    self.bbox = [self.__inPort_Pos[0], self.__inPort_Pos[1], \
                 self.__outPort_Pos[0], self.__outPort_Pos[1]]    
  # } update_bbox func  
  

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the connector color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    color_set = self.colorset
    
    for line in self.grfx:
      line.colorset = color_set
      
    pass
  # } update_color func

  # update_brush func: update the brush
  # {
  def update_brush(self):
    """
    Updates the connector brush set (line thickness and style for all different modes)
    
    input: none
    output: none
    """
    
    brushset = self.brushset
    
    for line in self.grfx:
      line.brushset = brushset

    pass
  # } update_brush func  


  # update_arrow func: update the arrow
  # {
  def update_arrow(self):
    """
    Updates the connector arrow style
    
    input: none
    output: none
    """
    
    self.grfx[3].arrow = self.grfx[3].arrow[0], self.__arrow
    self.grfx[4].arrow = self.grfx[4].arrow[0], self.__arrow
    self.grfx[5].arrow = self.grfx[5].arrow[0], self.__arrow

    pass
  # } update_brush func  


  # reg_pts func: register the line sections
  # {
  def reg_pts(self):
    """
    Internal functions.
    
    Populates the lists of input and output information
    
    input: none
    output: 
        inP = input port information list
        outP = output port information list
    """
    
    x, y, ArrowFlag, x_dir, y_dir = self.calc_pts()

    inP = [ x[0:6], y[0:6], ArrowFlag[0:6] ]
    outP = [ x[6], y[6], ArrowFlag[6] ]

    return inP, outP
  # } reg_pts func

  # reset_ports func: reset the line sections
  # {
  def reset_ports(self):
    """
    Internal functions.
    
    Resets the port according to new geometry, etc.
    
    input: none
    output: none
    """
    
    inPort, outPort = self.reg_pts()

    self.inPort = (self.__inPort_id, inPort, None, None)
    self.outPort = (self.__outPort_id, outPort, None, None)    

    center = (self.__inPort_Pos[0] + self.__outPort_Pos[0])//2,\
             (self.__inPort_Pos[1] + self.__outPort_Pos[1])//2
    
    grfobject.GrfObject.center.fset(self, center)
  # } reset_ports func  

  # < class functions section >

  # < getter and setter functions section >
  # property: inPortID
  # inPortID getter func: input port id getter
  # {
  @property
  def inPortID(self):
    """
    Class property getter: input port ID
    """
    
    return self.__inPort_id
  # } inPortID getter func

  # inPortID setter func: input port id setter
  # {
  @inPortID.setter
  def inPortID(self, inPort_id):
    """
    Class property setter: input port ID
    """

    self.__inPort_id = inPort_id
    inPort = self.inPort[1]
    self.inPort = (self.__inPort_id, inPort, None, None)
  # } inPortID setter func

  # property: outPortID
  # outPortID getter func: output port id getter
  # {
  @property
  def outPortID(self):
    """
    Class property getter: output port ID
    """

    return self.__outPort_id
  # } outPortID getter func

  # outPortID setter func: output port id setter
  # {
  @outPortID.setter
  def outPortID(self, outPort_id):
    """
    Class property setter: output port ID
    """

    self.__outPort_id = outPort_id
    outPort = self.outPort[1]
    self.outPort = (self.__outPort_id, outPort, None, None)    

  # } outPortID setter func

  # property: inPortPos
  # inPortPos getter func: input port position getter
  # {
  @property
  def inPortPos(self):
    """
    Class property getter: inport port position
    """

    return self.__inPort_Pos
  # } inPortPos getter func

  # inPortPos setter func: input port position setter
  # {
  @inPortPos.setter
  def inPortPos(self, inPort_Pos):
    """
    Class property setter: inport port position
    """

    self.__inPort_Pos = inPort_Pos
    self.update_ends()
  # } inPortPos setter func

  # property: arrow
  # arrow getter func: arrow getter
  # {
  @property
  def arrow(self):
    """
    Class property getter: connector arrow style
    """

    return self.__arrow
  # } arrow getter func

  # arrow setter func: arrow setter
  # {
  @arrow.setter
  def arrow(self, arrow):
    """
    Class property setter: connector arrow style
    """

    self.__arrow = arrow
    self.update_arrow()
  # } arrow setter func

  # property: outPortPos
  # outPortPos getter func: output port position getter
  # {
  @property
  def outPortPos(self):
    """
    Class property getter: output port position
    """

    return self.__outPort_Pos
  # } outPortPos getter func

  # outPortPos setter func: output port position setter
  # {
  @outPortPos.setter
  def outPortPos(self, outPort_Pos):
    """
    Class property setter: output port position
    """

    self.__outPort_Pos = outPort_Pos
    self.update_ends()
  # } outPortPos setter func

  # property: selectedWire
  # selectedWire getter func: selected wire getter
  # {
  @property
  def selectedWire(self):
    """
    Class property getter: selected section of the connector
    """

    return self.__selectedWire
  # } selectedWire getter func

  # < getter and setter functions section >
# } GrfConnectorCore class


# main func: contains code to test GrfConnectorCore class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("600x600")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=600, height=600)
  canvas.pack()

  obj = GrfConnectorCore(sheetCanvas=canvas, label='graph', std=CT)

  obj.draw()

  canvas.create_rectangle((30, 30, 200, 100))

  obj.mode = MODE[0]

  obj.inPortPos = (580, 400)
  obj.outPortPos = (20, 402)

  print(obj.brushset)
  
  print(obj.bbox)
##  for i in range(0, 20):
##    Pos = obj.outPortPos
##    obj.outPortPos = (Pos[0], Pos[1] + 1)

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
