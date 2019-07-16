'''
********************************************************************************

Python Script: grfblockcore Module
Writter: Mojtaba Mansour Abadi
Date: 16 February 2019

This Python script is compatible with Python 3.x.
The script is used to define GrfBlockCore class the connector in
Blodiator. The block used in the block diagrams is handled by this class.


GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:
    
Ver 0.0.8: 16 February 2019;
             first code

Ver 0.0.31: 24 June 2019;
             1- logging is added.

Ver 0.0.32: 28 June 2019;
             1- 'block_name' property is added.
             2- class is changed to 'GrfBlockCore'.

Ver 0.0.33: 28 June 2019;
             1- port signal type is added.


Ver 0.0.38: 7 July 2019;
             1- block loading properties are added.
             2- source/manipulation/sink types of block is added.
             3- block name color is added.

Ver 0.0.39: 9 July 2019;
             1- signal type is corrected.

********************************************************************************
'''


import tkinter as tk

from ..etc import cntsheetcanavs
from ..etc import coloredtext
from . import grfobject
from ..grafix import gfxrectangle
from ..grafix import gfxcircle
from ..grafix import gfxtext


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GrfBlock: '


#################################################
DEF_NAME = 'block'  # default name
CENTER = (300, 300)  # default center coordinate
CAT = 'graph'  # default category
COLOR_NORMAL = ('black', 'white', 'yellow', 'red', 'green')  # default color for normal state (line, fill, text color, port line, port fill)
COLOR_DISABLED = ('pink', 'blue', 'pink', 'pink', 'pink')  # default color for disabled state
COLOR_SELECTED = ('red', 'green', 'red', 'red', 'red')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'cyan', 'yellow', 'yellow', 'yellow')  # default color for erroneous state
BRUSH_NORMAL = (1.0, ())  # default line thickness and style for normal state (line thickness, line style)
BRUSH_DISABLED = (1.0, ())  # default line thickness and style for disabled state
BRUSH_SELECTED = (1.0, ())  # default line thickness and style for selected state
BRUSH_ERRONEOUS = (1.0, ())  # default line thickness and style for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
BOUNDARY_MARGIN = 0  # default boundary margin
LABEL_NAME = 'Block'  # default block name
FONT_SIZE_BN = 36  # block name font size
FONT_SIZE_PL = 20  # port label font size
FONT_NAME = 'Helvetica' # default font name
FONT_STYLE = 'bold'  # default font style
IN_PORT = [ ['i-0', 'Input 1', 'I1', 'electrical', 'Input port 1, with ID of i-0, name of Input 1, attached to variable I1 of designated function'],
            ['i-1', 'Input 2', 'I2', 'electrical', 'Enter the value 2 (dB): '],
            ['i-2', 'Input 3', 'I3', 'electrical', 'Enter the value 3 (dB): '],
            ['i-3', 'Input 4', 'I4', 'electrical', 'Enter the value 4 (dB): '] ]  # default input port
OUT_PORT = [ ['o-0', 'Output 1', 'I1', 'logical', 'Output value 1 (dB)'],
             ['o-1', 'Output 2', 'I2', 'logical', 'Output value 2 (dB)'],
             ['o-2', 'Output 3', 'I3', 'electrical', 'Output value 3 (dB)'],
             ['o-3', 'Output 4', 'I4', 'optical', 'Output value 4 (dB)'],
             ['o-4', 'Output 5', 'I5', 'optical', 'Output value 5 (dB)'] ]  # default output port
PROPERTIES = [ ['Parameter 1', 'd', [0.0, 5], 3.5],\
               ['Parameter 2', 's', [], 'Default'],\
               ['Parameter 3', 'l', ['-2', '3.5', '3.9', 'Mode 1', 'Mode 2', 'Mode 3'], 2],\
               ['Parameter 4', 'd', [-20, 40], 33],\
               ['Parameter 5', 's', [], 'Text'],\
             ]  # properties (name, type, range, default value); d = number, s = string, l = list
FUNC = ['func', 'file'] # default function
E2P_HORZ_MARG = 10  # horizontal margin box edge to port
E2P_VERT_MARG = 10  # vertical margin box edge to port
P2L_MARG_MARG = 10  # horizontal margin port to port label
GAP_P2P = 20  # gap distance between ports
GAP_P2N = 10  # gap between port and block name
PORT_SIZE = 10  # port size
GAP_L2N = -50  # gap distance label and block name
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfBlockCore class: this is the block class for blockdiagram objects
# {
class GrfBlockCore(grfobject.GrfObject):
  """
  Block item in the Blodiator.
  
  Define an instance of 'GrfBlockCore' with appropriate arguments:
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
      properties = parameters designated to the block
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing and managing 
  block item in Blodiator. Functions such as updating center, color,
  brush, tag, label, input and output ports, mode, etc are defined in this class.
  """
  
  version = '0.0.39'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME, func=FUNC, center=CENTER,
               block_name=LABEL_NAME, mode=MODE[0], inPort=IN_PORT, outPort=OUT_PORT,
               con_type=SIG_TYPE[0], color_type=CON_COLOR, properties=PROPERTIES, std=None):
    """
    Construct a GrfBlockCore
    
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
        properties = parameters designated to the block
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    if std is None:
      print(src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std

    self.std.Print('Initialising GrfBlockCore', fg, bg, style, src)
    
    self.__no_input = len(inPort)
    self.__label_input = [Name_ for ID_, Name_, Var_, Type_, Desc_ in inPort]
    
    self.__no_output = len(outPort)
    self.__label_output = [Name_ for ID_, Name_, Var_, Type_, Desc_ in outPort]

    self.__selectedObj = None
    self.__selectedID = None
    self.__selectedPort = None

    self.__properties = properties

    self.__block_name = block_name
    
    colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, COLOR_ERRONEOUS]
    brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

    colorset = dict(zip(MODE, colorList))
    brushset = dict(zip(MODE, brushList))
        
    self.__block_font_size = FONT_SIZE_BN
    self.__port_font_size = FONT_SIZE_PL
    self.__font_name = FONT_NAME
    self.__font_style = FONT_STYLE    
        
    self.__e2p_horz_marg = E2P_HORZ_MARG
    self.__e2p_vert_marg = E2P_VERT_MARG
    self.__p2l_horz_marg = P2L_MARG_MARG
    self.__p2p_gap = GAP_P2P
    self.__p2n_gap = GAP_P2N
    self.__port_size = PORT_SIZE
    self.__l2n_gap = GAP_L2N
    
    super(GrfBlockCore, self).__init__(sheetCanvas=sheetCanvas, cat=cat, label=label, color_type=color_type,
                                   colorset=colorset, brushset=brushset, center=center, con_type=con_type,
                                   mode=mode, inPort=inPort, outPort=outPort, func=FUNC, std=std)
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GrfBlockCore, self).__repr__()

    txt += '; number of inputs = {0}; inputs = {1}; number of outputs = {2}; outputs = {3};'\
           'function file = {4}; function name = {5}'.format(self.__no_input, self.__no_output,
                            self.function[0], self.function[1]) # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GrfBlockCore, self).__str__()

    txt += '; number of inputs = {0}; number of outputs = {1}; function file = {2}'\
           '; function name = {3}'.format(self.__no_input, self.__no_output, self.function[0], self.function[1]) # generate formatted text
    return txt
  # } __str__ func

  # __contains__ func: in dunar
  # {
  def __contains__(self, arg):
    """
    Class in dunar function.
    """
    
    self.__selectedObj = None
    self.__selectedID = None
    self.__selectedPort = None
    
    inPorts = self.grfx[1:(self.__no_input + 1)]
    outPorts = self.grfx[(self.__no_input + 1):(self.__no_input + self.__no_output + 1)]
        
    if self.__no_input != 0:
      Ind = -1      
      for i, inP in enumerate(inPorts):
        port_prop = self.inPort[i]
        if arg in inP:
          self.__selectedObj = inP
          self.__selectedID = port_prop[0]
          self.__selectedPort = port_prop
          return True
        Ind -=1

    if self.__no_output != 0:
      Ind = +1      
      for j, inP in enumerate(outPorts):
        port_prop = self.outPort[j]
        if arg in inP:
          self.__selectedObj = inP
          self.__selectedID = port_prop[0]
          self.__selectedPort = port_prop
          return True
        Ind +=1
          
    box = self.grfx[0]
    if arg in box:
      self.__selectedObj = 0
      self.__selectedID = 0
      self.__selectedPort = 0
      return True

    return False
  # } __contains__ func  
  # < inherited functions section >

  # < class functions section >
  # initBlock func: initialise the object
  # {
  def initBlock(self):
    """
    Initialises the block graphics on the canvas
    
    input: none
    output: none
    """
    
    self.std.Print('Setting up GrfBlockCore', fg, bg, style, src)

    colorset = self.colorset
        
    normal_colorset = colorset[MODE[0]]
    disabled_colorset = colorset[MODE[1]]
    selected_colorset = colorset[MODE[2]]
    erroneous_colorset = colorset[MODE[3]]
    
    Intext_len = len(max(self.__label_input, key=len)) if (self.__no_input != 0) else 0
    Outtext_len = len(max(self.__label_output, key=len)) if (self.__no_output != 0) else 0

    width = 2*(self.__e2p_horz_marg + self.__port_size + self.__p2l_horz_marg + self.__l2n_gap) +\
            Intext_len*self.__port_font_size + \
            len(self.__block_name)*self.__block_font_size + \
            Outtext_len*self.__port_font_size
            

    height = 2*self.__e2p_vert_marg + max(self.__port_size*self.__no_input + self.__p2p_gap*(self.__no_input - 1) + 2*self.__port_font_size,
                                   self.__port_size*self.__no_output + self.__p2p_gap*(self.__no_output - 1) + 2*self.__port_font_size,
                                   self.__block_font_size)

    brushset = self.brushset
    inPorts = [None]*self.__no_input
    inPort_x = self.center[0] - width//2 + self.__e2p_horz_marg + self.__port_size//2
    inport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_input):
      port = self.inPort[i]
      type_color = self.color_type[port[3]]
      port_color_normal = (normal_colorset[4], type_color)
      colorList = [port_color_normal, disabled_colorset[4:], selected_colorset[4:], erroneous_colorset[4:]]
      colorset = dict(zip(MODE, colorList))
      tag = self.label + '-Input-' + str(i)
      center = inPort_x, inport_y + i*(self.__p2p_gap + self.__port_size)
      inPorts[i] = gfxcircle.GfxCircle(sheetCanvas=self.sheetCanvas, size=self.__port_size,
                                       center=center, std=self.std, tag=tag)
      inPorts[i].colorset = colorset
      inPorts[i].brushset = brushset

    colorList = [(normal_colorset[3], normal_colorset[3]), (disabled_colorset[3], disabled_colorset[3]),
                 (selected_colorset[3], selected_colorset[3]), (erroneous_colorset[3], erroneous_colorset[3])]
    colorset = dict(zip(MODE, colorList))
    inLabels = [None]*self.__no_input
    inPort_x = self.center[0] - width//2 + self.__e2p_horz_marg + self.__port_size + self.__p2l_horz_marg + Intext_len//2
    inport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_input):
      tag = self.label + '-Intext-' + str(i)
      center = inPort_x, inport_y + i*(self.__p2p_gap + self.__port_size)
      inLabels[i] = gfxtext.GfxText(sheetCanvas=self.sheetCanvas, text=self.__label_input[i],
                                    std=self.std, font=(self.__font_name, self.__port_font_size, self.__font_style),
                                    tag=tag, center=center, mode=self.mode,
                                    text_adj=(tk.W, tk.CENTER))
      inLabels[i].colorset = colorset

    brushset = self.brushset
    outPorts = [None]*self.__no_output
    outPort_x = self.center[0] + width//2 - self.__e2p_horz_marg - self.__port_size//2
    outport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_output):
      port = self.outPort[i]
      type_color = self.color_type[port[3]]
      port_color_normal = (normal_colorset[4], type_color)
      colorList = [port_color_normal, disabled_colorset[4:], selected_colorset[4:], erroneous_colorset[4:]]
      colorset = dict(zip(MODE, colorList))
      tag = self.label + '-Output-' + str(i)
      center = outPort_x, outport_y + i*(self.__p2p_gap + self.__port_size)
      outPorts[i] = gfxcircle.GfxCircle(sheetCanvas=self.sheetCanvas, size=self.__port_size,
                                        center=center, std=self.std, tag=tag)
      outPorts[i].colorset = colorset
      outPorts[i].brushset = brushset

    colorList = [(normal_colorset[3], normal_colorset[3]), (disabled_colorset[3], disabled_colorset[3]),
                 (selected_colorset[3], selected_colorset[3]), (erroneous_colorset[3], erroneous_colorset[3])]
    colorset = dict(zip(MODE, colorList))
    outLabels = [None]*self.__no_output
    outPort_x = self.center[0] + width//2 - self.__e2p_horz_marg - self.__port_size - self.__p2l_horz_marg - Outtext_len//2
    outport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_output):
      tag = self.label + '-Outtext-' + str(i)
      center = outPort_x, outport_y + i*(self.__p2p_gap + self.__port_size)
      outLabels[i] = gfxtext.GfxText(sheetCanvas=self.sheetCanvas, text=self.__label_output[i],
                                    std=self.std, font=(self.__font_name, self.__port_font_size, self.__font_style),
                                    tag=tag, center=center, mode=self.mode,
                                    text_adj=(tk.E, tk.CENTER))
      outLabels[i].colorset = colorset

    colorList = [(normal_colorset[2], normal_colorset[2]), (disabled_colorset[2], disabled_colorset[2]),
                 (selected_colorset[2], selected_colorset[2]), (erroneous_colorset[2], erroneous_colorset[2])]
    colorset = dict(zip(MODE, colorList))
    text_center_x = self.center[0] if (self.__no_input != 0) else\
                    (self.center[0] - width//2 + self.__e2p_horz_marg -\
                     0*round(self.__port_size*2) +\
                     len(self.__block_name)*self.__block_font_size//2)
    text_center_x = text_center_x if (self.__no_output != 0) else\
                    (self.center[0]  + width//2 - self.__e2p_horz_marg +\
                     0*round(self.__port_size*2) -\
                     len(self.__block_name)*self.__block_font_size//2)
    text_center = text_center_x, self.center[1]
    tag = self.label + '-Block_Name'
    blockName = gfxtext.GfxText(sheetCanvas=self.sheetCanvas, text=self.__block_name,
                                std=self.std, font=(self.__font_name, self.__block_font_size, self.__font_style),
                                tag=tag, center=text_center, mode=self.mode)
    blockName.colorset = colorset
    
    colorList = [normal_colorset[0:2], disabled_colorset[0:2], selected_colorset[0:2], erroneous_colorset[0:2]]
    colorset = dict(zip(MODE, colorList))
    brushset = self.brushset
    tag = self.label + '-Box'
    blockBox = gfxrectangle.GfxRectangle(sheetCanvas=self.sheetCanvas, std=self.std,
                                         tag=tag, center=self.center, mode=self.mode,
                                         size=(width, height))
    blockBox.colorset = colorset
    blockBox.brushset = brushset

    self.grfx = [blockBox] + inPorts + outPorts + inLabels + outLabels  + [blockName]
    self.update_bbox()
    
    pass
  # } initBlock func  

  # update_bbox func: update the bounding box
  # {
  def update_bbox(self):
    """
    Updates the block bounding box
    
    input: none
    output: none
    """ 
    
    self.bbox = self.grfx[0].bbox    

#    grfobject.GrfObject.bbox.fset(self, self.grfx[0].bbox)
    
  # } update_bbox func

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the block color set (outline and filling colors for all different modes)
    
    input: none
    output: none
    """
        
    colorset = self.colorset
    
    normal_colorset = colorset[MODE[0]]
    disabled_colorset = colorset[MODE[1]]
    selected_colorset = colorset[MODE[2]]
    erroneous_colorset = colorset[MODE[3]]

    colorList = [normal_colorset[0:2], disabled_colorset[0:2], selected_colorset[0:2], erroneous_colorset[0:2]]
    colorset = dict(zip(MODE, colorList))
    self.grfx[0].colorset = colorset
    
    colorList = [(normal_colorset[2], normal_colorset[2]), (disabled_colorset[2], disabled_colorset[2]),
                 (selected_colorset[2], selected_colorset[2]), (erroneous_colorset[2], erroneous_colorset[2])]
    colorset = dict(zip(MODE, colorList))
    self.grfx[-1].colorset = colorset
        
    pass
  # } update_color func

  # update_brush func: update the brush
  # {
  def update_brush(self):
    """
    Updates the block brush set (line thickness and style for all different modes)
    
    input: none
    output: none
    """
    
    brushset = self.brushset

    self.grfx[0].brushset = brushset
    pass
  # } update_brush func  


  # update_block func: update the block
  # {
  def update_block(self):
    """
    Updates the block graphics
    
    input: none
    output: none
    """
    
    Intext_len = len(max(self.__label_input, key=len)) if (self.__no_input != 0) else 0
    Outtext_len = len(max(self.__label_output, key=len)) if (self.__no_output != 0) else 0
            
    inPorts = self.grfx[1:(self.__no_input + 1)]
    outPorts = self.grfx[(self.__no_input + 1):(self.__no_input + self.__no_output + 1)]
    inLabels = self.grfx[(self.__no_input + self.__no_output + 1):(2*self.__no_input + self.__no_output + 1)]
    outLabels = self.grfx[(2*self.__no_input + self.__no_output + 1):-1]
    blockName = self.grfx[-1]
    blockBox = self.grfx[0]
    
    colorset = self.colorset
    
    normal_colorset = colorset[MODE[0]]
    disabled_colorset = colorset[MODE[1]]
    selected_colorset = colorset[MODE[2]]
    erroneous_colorset = colorset[MODE[3]]
            
    width = 2*(self.__e2p_horz_marg + self.__port_size + self.__p2l_horz_marg + self.__l2n_gap) +\
            Intext_len*self.__port_font_size + \
            len(self.__block_name)*self.__block_font_size + \
            Outtext_len*self.__port_font_size

    height = 2*self.__e2p_vert_marg + max(self.__port_size*self.__no_input + self.__p2p_gap*(self.__no_input - 1) + 2*self.__port_font_size,
                                   self.__port_size*self.__no_output + self.__p2p_gap*(self.__no_output - 1) + 2*self.__port_font_size,
                                   self.__block_font_size)

    brushset = self.brushset
    inPort_x = self.center[0] - width//2 + self.__e2p_horz_marg + self.__port_size//2
    inport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_input):
      port = self.inPort[i]
      type_color = self.color_type[port[3]]
      port_color_normal = (normal_colorset[4], type_color)
      colorList = [port_color_normal, disabled_colorset[4:], selected_colorset[4:], erroneous_colorset[4:]]
      colorset = dict(zip(MODE, colorList))
      center = inPort_x, inport_y + i*(self.__p2p_gap + self.__port_size)
      inPorts[i].size = self.__port_size
      inPorts[i].center = center
      inPorts[i].colorset = colorset
      inPorts[i].brushset = brushset
      pass

    colorList = [(normal_colorset[3], normal_colorset[3]), (disabled_colorset[3], disabled_colorset[3]),
                 (selected_colorset[3], selected_colorset[3]), (erroneous_colorset[3], erroneous_colorset[3])]
    colorset = dict(zip(MODE, colorList))
    inPort_x = self.center[0] - width//2 + self.__e2p_horz_marg + self.__port_size + self.__p2l_horz_marg + Intext_len//2
    inport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_input):
      center = inPort_x, inport_y + i*(self.__p2p_gap + self.__port_size)
      inLabels[i].font = (self.__font_name, self.__port_font_size, self.__font_style)
      inLabels[i].center = center
      inLabels[i].colorset = colorset
      pass

    brushset = self.brushset
    outPort_x = self.center[0] + width//2 - self.__e2p_horz_marg - self.__port_size//2
    outport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_output):
      port = self.outPort[i]
      type_color = self.color_type[port[3]]
      port_color_normal = (normal_colorset[4], type_color)
      colorList = [port_color_normal, disabled_colorset[4:], selected_colorset[4:], erroneous_colorset[4:]]
      colorset = dict(zip(MODE, colorList))
      center = outPort_x, outport_y + i*(self.__p2p_gap + self.__port_size)
      outPorts[i].size = self.__port_size
      outPorts[i].center = center
      outPorts[i].colorset = colorset
      outPorts[i].brushset = brushset
      pass

    colorList = [(normal_colorset[3], normal_colorset[3]), (disabled_colorset[3], disabled_colorset[3]),
                 (selected_colorset[3], selected_colorset[3]), (erroneous_colorset[3], erroneous_colorset[3])]
    colorset = dict(zip(MODE, colorList))
    outPort_x = self.center[0] + width//2 - self.__e2p_horz_marg - self.__port_size - self.__p2l_horz_marg - Outtext_len//2
    outport_y = self.center[1] - height//2 + self.__e2p_vert_marg + self.__port_size//2 + self.__port_font_size
    for i in range(0, self.__no_output):
      center = outPort_x, outport_y + i*(self.__p2p_gap + self.__port_size)
      outLabels[i].font = (self.__font_name, self.__port_font_size, self.__font_style)
      outLabels[i].center = center
      outLabels[i].colorset = colorset
      pass

    colorList = [(normal_colorset[2], normal_colorset[2]), (disabled_colorset[2], disabled_colorset[2]),
                 (selected_colorset[2], selected_colorset[2]), (erroneous_colorset[2], erroneous_colorset[2])]
    colorset = dict(zip(MODE, colorList))
    text_center_x = self.center[0] if (self.__no_input != 0) else\
                    (self.center[0] - width//2 + self.__e2p_horz_marg -\
                     0*round(self.__port_size*2) +\
                     len(self.__block_name)*self.__block_font_size//2)
    text_center_x = text_center_x if (self.__no_output != 0) else\
                    (self.center[0]  + width//2 - self.__e2p_horz_marg +\
                     0*round(self.__port_size*2) -\
                     len(self.__block_name)*self.__block_font_size//2)
    text_center = text_center_x, self.center[1]
    blockName.font = (self.__font_name, self.__block_font_size, self.__font_style)
    blockName.center = text_center
    blockName.colorset = colorset
    
    colorList = [normal_colorset[0:2], disabled_colorset[0:2], selected_colorset[0:2], erroneous_colorset[0:2]]
    colorset = dict(zip(MODE, colorList))
    brushset = self.brushset
    blockBox.size = width, height
    blockBox.center = self.center
    blockBox.colorset = colorset
    blockBox.brushset = brushset

    self.update_bbox()
    pass
  # } update_block func  

  # update_type func: update the type
  # {
  def update_type(self):
    """
    Updates the block connection type ('none', 'logical', 'electrical', 'optical'),
    left blank delibrately
    
    input: none
    output: none
    """

    pass
  # } update_type func  


  # update_font func: update the font
  # {
  def update_font(self):
    """
    Updates the block font (font name, block font size, port label font size, font style)
    
    input: none
    output: none
    """
    
    self.__block_font_size, self.__port_font_size,\
    self.__font_name, self.__font_style = self.__font_prop

    self.update_block()

    pass
  # } update_font func  

  # update_geometry func: update the geometry
  # {
  def update_geometry(self):
    """
    Updates the block geometry
    (
     edge to port horizontal margin, edge to port vertical margin,
     port to port label horizontal margin, port to port vertical gap,
     port size, port label to block name horizontal gap     
    )
    
    input: none
    output: none
    """
    
    self.__e2p_horz_marg, self.__e2p_vert_marg,\
    self.__p2l_horz_marg, self.__p2p_gap, self.__p2n_gap,\
    self.__port_size, self.__l2n_gap = self.__geo_prop

    self.update_block()
    pass
  # } update_geometry func  

  # property: center
  # center setter func: graph center setter
  # {
  @grfobject.GrfObject.center.setter
  def center(self, center):
    """
    Class property setter: center
    """
    
    center_1 = grfobject.GrfObject.center.fget(self)

    deltX = center[0] - center_1[0]
    deltY = center[1] - center_1[1]

    for obj in self.grfx:
      obj_cent = obj.center
      obj_x = obj_cent[0] + deltX
      obj_y = obj_cent[1] + deltY
      obj.center = (obj_x, obj_y)

    grfobject.GrfObject.center.fset(self, center)
    grfobject.GrfObject.bbox.fset(self, self.grfx[0].bbox)
  # } center setter func
  
  # < class functions section >

  # < getter and setter functions section >
  # property: selectedObj
  # selected object getter func: block selected object getter
  # {
  @property
  def selectedObj(self):
    """
    Class property getter: selected object (any of input/output ports or the body)
    """
    
    return self.__selectedObj
  # } selectedObj getter func

  # property: selectedID
  # selected ID getter func: block selected ID getter
  # {
  @property
  def selectedID(self):
    """
    Class property getter: ID of selected object (any of input/output ports or the body)
    """
    
    return self.__selectedID
  # } selectedID getter func

  # property: selectedPort
  # selected port getter func: block selected port getter
  # {
  @property
  def selectedPort(self):
    """
    Class property getter: selected port (any of input/output ports)
    """
    
    return self.__selectedPort
  # } selectedPort getter func

  # property: no_of_inputs
  # no of inputs getter func: no of inputs ID getter
  # {
  @property
  def no_of_inputs(self):
    """
    Class property getter: number of input ports
    """
    
    return self.__no_input
  # } no_of_inputs getter func

  # property: no_of_outputs
  # no of outputs getter func: no of outputs ID getter
  # {
  @property
  def no_of_outputs(self):
    """
    Class property getter: number of output ports
    """
    
    return self.__no_output
  # } no_of_outputs getter func


  # property: properties
  # properties getter func: properties getter
  # {
  @property
  def properties(self):
    """
    Class property getter: block properties
    """
    
    return self.__properties
  # }properties getter func

  # properties setter func: properties setter
  # {
  @properties.setter
  def properties(self, prop):
    """
    Class property setter: block properties
    """

    self.__properties = prop
  # } properties setter func

  # parameters getter func: parameters getter
  # {
  @property
  def parameters(self):
    """
    Class property getter: block parameters
    """
    
    param = []

    for prop in self.__properties:
      param.append(prop[-1])
      pass

    return param
  # } parameters setter func

 # parameters setter func: parameters setter
  # {
  @parameters.setter
  def parameters(self, param):
    """
    Class property setter: block parameters
    """
    
    for index, prop in enumerate(self.__properties):
      prop[-1] = param[index]
      pass
  # } parameters setter func

  # block name getter func: block name getter
  # {
  @property
  def block_name(self):
    """
    Class property getter: block name
    """
    
    return self.__block_name
  # } block_name setter func

 # block name setter func: block name setter
  # {
  @block_name.setter
  def block_name(self, block_name):
    """
    Class property setter: block name
    """
    
    self.__block_name = block_name
  # } block_name setter func


  # property: font
  # font getter func: font getter
  # {
  @property
  def font_prop(self):
    """
    Class property getter: font properties (font name, block font size, port label font size, font style)
    """
    
    return self.__font_prop
  # } font getter func

  # font setter func: font setter
  # {
  @font_prop.setter
  def font_prop(self, font):
    """
    Class property setter: font properties (font name, block font size, port label font size, font style)
    """
    
    self.__font_prop = font
    self.update_font()
  # } font setter func

  # property: geometry
  # geometry getter func: geometry getter
  # {
  @property
  def geo_prop(self):
    """
    Class property getter: geometry properties
    (
     edge to port horizontal margin, edge to port vertical margin,
     port to port label horizontal margin, port to port vertical gap,
     port size, port label to block name horizontal gap     
    )
    """
    
    return self.__geo_prop
  # } geometry getter func

  # geometry setter func: geometry setter
  # {
  @geo_prop.setter
  def geo_prop(self, geometry):
    """
    Class property setter: geometry properties
    (
     edge to port horizontal margin, edge to port vertical margin,
     port to port label horizontal margin, port to port vertical gap,
     port size, port label to block name horizontal gap     
    )
    """
    
    self.__geo_prop = geometry
    self.update_geometry()
  # } geo_prop setter func

  # color_type setter func: color type setter
  # {
  @grfobject.GrfObject.color_type.setter
  def color_type(self, color_type):
    """
    Class property setter: connection colors set ('none', 'logical', 'electrical', 'optical')
    """
        
    grfobject.GrfObject.color_type.fset(self, color_type)
    self.update_geometry()
    
  # } color_type setter func
  # < getter and setter functions section >
# } GrfBlockCore class


# main func: contains code to test GrfBlockCore class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("900x900")
  root.title('Sheet Test Bench')

  Object = []

  canvas = cntsheetcanavs.CntSheetCanvas(master=root, std=CT, size=(600, 600))

  canvas.pack()
  
#  i = len(Object)
#  obj = GrfBlock(sheetCanvas=canvas, label='graph' + str(i), std=CT, center=(200, 200))
#  Object.append(obj)
#  obj = None
  
#  i = len(Object)
#  obj = GrfBlock(sheetCanvas=canvas, label='graph' + str(i), std=CT, center=(100, 100))
#  Object.append(obj)
#  obj = None

  i = len(Object)
  obj = GrfBlockCore(sheetCanvas=canvas, label='graph' + str(i), std=CT, center=(500, 500))
  Object.append(obj)
#  obj = None
  
#  for obj in Object:
#    print('----------------')
#    print(obj)
#    obj.draw()

  obj.draw()
##  obj_2.draw()
##  obj_1.mode = MODE[1]
  obj.center = (300, 300)
  
  print(obj.bbox)
  
  obj.update_block()
  
  print(obj.outPort)

##  for i in range(0, 20):
##    Pos = obj.outPortPos
##    obj.outPortPos = (Pos[0], Pos[1] + 1)

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
