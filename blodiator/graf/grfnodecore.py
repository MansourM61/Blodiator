'''
********************************************************************************

Python Script: grfnodecore Module
Writter: Mojtaba Mansour Abadi
Date: 7 Feburary 2019

This Python script is compatible with Python 3.x.
The script is used to define GrfNodeCore class the node in
Blodiator. The node used in the block diagrams is handled by this class.

GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:

Ver 0.0.7: 29 January 2019;
             first code

Ver 0.0.8: 7 Feburary 2019;
             1- center changing is fixed.

Ver 0.0.31: 24 June 2019;
             1- logging is added.

Ver 0.0.32: 28 June 2019;
             1- Class is changed to GrfNodeCore.

Ver 0.0.36: 3 July 2019;
             1- node/connector loading properties are added.
            
********************************************************************************
'''


import tkinter as tk

from ..etc import cntsheetcanavs
from ..etc import coloredtext
from . import grfobject
from ..grafix import gfxcircle


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GrfNodeCore: '


#################################################
DEF_NAME = 'node'  # default name
CENTER = (300, 300)  # default center coordinate
SIZE = 10  # default size
CAT = 'graph'  # default category
COLOR_NORMAL = ('black', 'black')  # default color for normal state
COLOR_DISABLED = ('pink', 'pink')  # default color for disabled state
COLOR_SELECTED = ('red', 'red')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'yellow')  # default color for erroneous state
BRUSH_NORMAL = (1.0, [])  # default line thickness and style for normal state
BRUSH_DISABLED = (1.0, [])  # default line thickness and style for disabled state
BRUSH_SELECTED = (1.0, [])  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (1.0, [])  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
POSITION = ('N', 'S', 'E', 'W')  # position of the port
BOUNDARY_MARGIN = 0  # default boundary margin
IN_PORT = ['0', None, None, None]  # default input port
OUT_PORT = [ ['0', None, None, None], ['0', None, None, None] ]  # default output port
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfNodeCore class: this is the node class for blockdiagram objects
# {
class GrfNodeCore(grfobject.GrfObject):
  """
  Node item in the Blodiator.
  
  Define an instance of 'GrfNodeCore' with appropriate arguments:
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
  node item in Blodiator. Functions such as updating center, color,
  brush, tag, label, input and output ports, mode, etc are defined in this class.
  """
 
  version = '0.0.36'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME, center=CENTER,
               size=SIZE, mode=MODE[0], inPort=IN_PORT, outPort=OUT_PORT,
               con_type=SIG_TYPE[0], color_type=CON_COLOR, std=None):
    """
    Construct a GrfNodeCore
    
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


    self.std.Print('Initialising GrfNodeCore', fg, bg, style, src)
    self.__size = size

    colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, COLOR_ERRONEOUS]
    brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

    colorset = dict(zip(MODE, colorList))
    brushset = dict(zip(MODE, brushList))

    super(GrfNodeCore, self).__init__(sheetCanvas=sheetCanvas, cat=cat, label=label, center=center,
                                  mode=mode, colorset=colorset, brushset=brushset, color_type=color_type,
                                  inPort=inPort, outPort=outPort, con_type=con_type, std=std)
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
 
    txt = super(GrfNodeCore, self).__repr__()

    txt += '; size = {0}'.format(self.__size)  # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """

    txt = super(GrfNodeCore, self).__str__()

    inID = self.inPort[0]

    outID = [P[0] for P in self.outPort]

    txt += '; input ID = {0}; output ID = {1}'.format(inID, outID)  # generate formatted text
    return txt
  # } __str__ func

  # __contains__ func: in dunar
  # {
  def __contains__(self, arg):
    """
    Class in dunar function.
    """

    return arg in self.grfx[0]
  # } __contains__ func
  # < inherited functions section >

  # < class functions section >
  # initBlock func: initialise the object
  # {
  def initBlock(self):
    """
    Initialises the node graphics on the canvas
    
    input: none
    output: none
    """
    
    self.std.Print('Setting up GrfNodeCore', fg, bg, style, src)

    tag = self.label + '-circle'

    obj = []

    obj.append(gfxcircle.GfxCircle(sheetCanvas=self.sheetCanvas, tag=tag, center=self.center,
                                   size=self.__size, mode=self.mode, std=self.std))

    obj[0].colorset = self.colorset
    obj[0].brushset = self.brushset

    self.grfx = obj
    self.update_bbox()

    self.update_color()
    self.update_brush()

  # } initBlock func

  # update_bbox func: update the bounding box
  # {
  def update_bbox(self):
    """
    Updates the node bounding box
    
    input: none
    output: none
    """ 
    
    centX, centY = self.center

    brush_thickness = self.brush[0]

    margin = self.__size + brush_thickness + BOUNDARY_MARGIN

    self.bbox = [int(centX - margin), int(centY - margin),
                 int(centX + margin), int(centY + margin)]
  # } update_bbox func

  # update_center func: update the center
  # {
  def update_center(self):
    """
    Updates the node center
    
    input: none
    output: none
    """ 
    
    self.grfx[0].center = self.center

    self.update_bbox()
  # } update_center func  

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the connector color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
    
    
    colorset = self.colorset
    
    self.grfx[0].colorset = colorset
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
    
    self.grfx[0].brushset = brushset
    pass
  # } update_brush func  

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

    return self.inPort[0]
  # } inPortID getter func

  # inPortID setter func: input port id setter
  # {
  @inPortID.setter
  def inPortID(self, inPort_id):
    """
    Class property setter: input port ID
    """
    
    self.__inPort_id = inPort_id
    inPort = [inPort_id, None, None, None]
    self.inPort = inPort    
  # } inPortID setter func

  # property: size
  # size getter func: output size getter
  # {
  @property
  def size(self):
    """
    Class property getter: node size
    """    

    return self.__size
  # } size getter func

  # size setter func: size setter
  # {
  @size.setter
  def size(self, size):
    """
    Class property setter: node size
    """    

    self.__size = size
    self.grfx[0].size = size
  # } size setter func


  # property: outPortID
  # outPortID getter func: output port id getter
  # {
  @property
  def outPortID(self):
    """
    Class property getter: output port ID
    """

    return self.outPort[0]
  # } outPortID getter func

  # outPortID setter func: output port id setter
  # {
  @outPortID.setter
  def outPortID(self, outPort_id):
    """
    Class property setter: output port ID
    """

    self.__outPort_id = outPort_id
    outPort = [outPort_id, None, None, None]
    self.outPort = outPort    
  # } outPortID setter func
  # < getter and setter functions section >
# } GrfNodeCore class


# main func: contains code to test GrfNodeCore class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("600x600")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=600, height=600)
  canvas.pack()

  obj = GrfNodeCore(sheetCanvas=canvas, label='graph', std=CT)

  obj.draw()

#  CT.Print(repr(obj))

  CT.Print('\n')

  obj.mode = MODE[2]

 # CT.Print(repr(obj))

  obj.center = (100, 100)

  obj.mode = MODE[0]
  
  obj.center = (300, 100)
  
  print(obj.bbox)

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
