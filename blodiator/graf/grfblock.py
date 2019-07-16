'''
********************************************************************************

Python Script: grfblock Module
Writter: Mojtaba Mansour Abadi
Date: 16 February 2019

This Python script is compatible with Python 3.x.
The script is used to define GfrBlock class in
Blodiator. This class is a child of GrfBlockCore class.


GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:
    
Ver 0.0.8: 27 June 2019;
             first code

Ver 0.0.32: 28 June 2019;
             1- loading information from xml file is added.
             2- the class is changed to 'GrfBlock'.

Ver 0.0.33: 28 June 2019;
             1- port signal type is added.

********************************************************************************
'''


import tkinter as tk
import xml.etree.ElementTree as ET

from ..etc import cntsheetcanavs
from ..etc import coloredtext
from . import grfblockcore


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'Block: '


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
XML_PROPERTY_FILE = 'Block_Type_Sink.xml'  # designated xml file containing information about the block
HOR_MARG_E2P = 10  # horizontal margin box edge to port
VERT_MARG_E2P = 10  # vertical margin box edge to port
MARG_P2L = 10  # horizontal margin port to port label
GAP_P2P = 20  # gap distance between ports
GAP_L2N = -50  # gap distance label and block name
PORT_SIZE = 10  # port size
GAP_P2N = 10  # gap between port and block name
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfBlock class: this is the block class for blockdiagram objects
# {
class GrfBlock(grfblockcore.GrfBlockCore):
  """
  Block item in the Blodiator.
  
  Define an instance of 'GrfBlock' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the block
      label = item label
      center = center of the block
      cat = a string showing the category of the block
      con_type = connection type: ('none', 'logical', 'electrical', 'optical')
      color_type = a tuple containing colors for different coneection type
      xml_file = xml file address containing parameters of the block
      mode = state of the block: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class controls higher level aspects of a block item such as parameters, etc.
  """
  
  version = '0.0.33'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME, center=CENTER,
               con_type=SIG_TYPE[0], mode=MODE[0], xml_file=XML_PROPERTY_FILE,
               color_type=CON_COLOR,std=None):
    """
    Construct a GrfBlock
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the block
        label = item label
        center = center of the block
        cat = a string showing the category of the block
        con_type = connection type: ('none', 'logical', 'electrical', 'optical')
        xml_file = xml file address containing parameters of the block
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

    self.std.Print('Initialising GrfBlock', fg, bg, style, src)

    self.__xml_file = xml_file

    self.__con_type = con_type

    self.__selectedObj = None
    self.__selectedID = None
    
    colorList = [COLOR_NORMAL, COLOR_DISABLED, COLOR_SELECTED, COLOR_ERRONEOUS]
    brushList = [BRUSH_NORMAL, BRUSH_DISABLED, BRUSH_SELECTED, BRUSH_ERRONEOUS]

    colorset = dict(zip(MODE, colorList))
    brushset = dict(zip(MODE, brushList))

    blockname, inport, outport, prop, func = self.__loadproprerties()
    
    super(GrfBlock, self).__init__(sheetCanvas=sheetCanvas, cat=cat, label=label, func=func,
                                   center=center, block_name=blockname, mode=mode,
                                   con_type=con_type, color_type=color_type,
                                   inPort=inport, outPort=outport, properties=prop, std=std)
    pass   
  # } __init__ func

  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GrfBlock, self).__repr__()

    txt += ';xml file = ' + self.__xml_file  # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GrfBlock, self).__str__()

    txt += ';xml file = ' + self.__xml_file  # generate formatted text
    return txt
  # } __str__ func
  # < inherited functions section >

  # < class functions section >
  # loadproprerties func: load properties from give file
  # {
  def __loadproprerties(self):
    """
    Internal function.
    
    Loads the parameters from the given xml file
    
    input: none
    output: none
    """
    
    self.std.Print('Loading block information from the file', fg, bg, style, src)

    tree = ET.parse(self.__xml_file)
    root = tree.getroot()

    blockname = root.attrib["name"]

    inport_root = root.find("inport")
    inport = []
    for item in inport_root.findall("port"):
      port_attr = item.attrib    
      port_id = port_attr["id"]
      port_name = port_attr["name"]
      port_var = port_attr["var"]
      port_type = port_attr["type"]
      port_desc = item.text
      port = [port_id, port_name, port_var, port_type, port_desc]
      inport.append(port)
      pass  

    outport_root = root.find("outport")
    outport = []
    for item in outport_root.findall("port"):
      port_attr = item.attrib    
      port_id = port_attr["id"]
      port_name = port_attr["name"]
      port_var = port_attr["var"]
      port_type = port_attr["type"]
      port_desc = item.text
      port = [port_id, port_name, port_var, port_type, port_desc]
      outport.append(port)
      pass
            
    prop_root = root.find("property")
    prop = []
    for item in prop_root.findall("parameter"):
      prop_attr = item.attrib
      prop_label = prop_attr["label"]
      prop_type = prop_attr["type"]
      prop_default_raw = prop_attr["default"]
      range_root = item.findall("range")
      if prop_type == 'd':
        prop_default = float(prop_default_raw)
        prop_rng = [float(range_root[0].text), float(range_root[1].text)]
        pass
      elif prop_type == 's':
        prop_default = prop_default_raw
        prop_rng = []
        pass
      elif prop_type == 'l':
        prop_default = int(prop_default_raw)
        prop_rng = []
        for rng in range_root:
          prop_rng.append(rng.text)
          pass
        pass
      pr = [prop_label, prop_type, prop_rng, prop_default]
      prop.append(pr)
      pass

    func_root = root.find("function")
    func_name = func_root.attrib["name"]
    func_file = func_root.text
    func = [func_name, func_file]
    
    return blockname, inport, outport, prop, func
  # } loadproprerties func



  # update_inport_mode func: update the inport mode
  # {
  def update_inport_mode(self, port_index, mode = MODE[0]):
    """
    Internal function.
    
    Updates the input ports mode ('normal', 'disabled', 'selected', 'erroneous')
    
    input: none
    output: none
    """ 
    
    inPorts = self.grfx[1:(self.no_of_inputs + 1)]

    port_index = max(0, port_index)
    port_index = min(self.no_of_inputs - 1, port_index)
    
    inPorts[port_index].mode = mode
    pass
  # } update_inport_mode func  

  
  # update_outport_mode func: update the outport mode
  # {
  def update_outport_mode(self, port_index, mode = MODE[0]):
    """
    Internal function.
    
    Updates the output ports mode ('normal', 'disabled', 'selected', 'erroneous')
    
    input: none
    output: none
    """ 
    
    outPorts = self.grfx[(self.no_of_inputs + 1):(self.no_of_inputs + self.no_of_outputs + 1)]

    port_index = max(0, port_index)
    port_index = min(self.no_of_outputs - 1, port_index)
        
    outPorts[port_index].mode = mode
    pass
  # } update_outport_mode func  

  
  
  # < class functions section >

  # < getter and setter functions section >
  # xm_file getter func: xm_file getter
  # {
  @property
  def xml_file(self):
    """
    Class property getter: xml file address containing the block parameters
    """
    
    return self.__xml_file
  # } xm_file setter func

  # < getter and setter functions section >
# } GrfBlock class


# main func: contains code to test GrfBlock class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("900x900")
  root.title('Sheet Test Bench')

  Object = []

  canvas = cntsheetcanavs.CntSheetCanvas(master=root, std=CT, size=(800, 800))

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
  obj = GrfBlock(sheetCanvas=canvas, label='graph' + str(i), std=CT, center=(500, 500))
  Object.append(obj)
#  obj = None
  
#  for obj in Object:
#    print('----------------')
#    print(obj)
#    obj.draw()

  obj.draw()
##  obj_2.draw()
##  obj_1.mode = MODE[1]
  obj.center = (400, 300)
  
  print(obj)
  
  print(obj.bbox)
  
  print(obj.xml_file)

##  for i in range(0, 20):
##    Pos = obj.outPortPos
##    obj.outPortPos = (Pos[0], Pos[1] + 1)

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
