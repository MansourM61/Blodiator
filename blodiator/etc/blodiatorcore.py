"""
********************************************************************************

Python Script: blodiatorcore Module
Writter: Mojtaba Mansour Abadi
Date: 27 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define Blodiator Base class.
BlodiatorBase is mostly dealing with drawing, selecting, moving, and removing 
digrams. It is better not to use it on its own. The child class 'BlodiatorBase' 
adds extra features.


BlodiatorBase
|
|____BlodiatorCore
     |
     |____object


Histoty:

Ver 0.0.10: 27 Feburary 2019;
             first code

Ver 0.0.11: 14 Feburary 2019;
             1- Mouse controlls are added,
             2- 'delete' function is added.
             3- 'delete' based on order is added.

Ver 0.0.13: 9 May 2019;
             1- 'selection' and remove selected was added.
             2- 'grid' and 'snap' are added.
             3- 'Esc' key is added.
             4- 'move' for block is added.
             
Ver 0.0.15: 3 June 2019;
             1- the lower and raise functons was not working.
                The order of objects couldn't be changed using canvas
                methods. It is fixed.
             2- snapping connector to the ports is added.
             3- moving connector is added.

Ver 0.0.18: 12 June 2019;
             1- the order of is changed after moving it.
             2- interactive movement of blocks is added.
             
Ver 0.0.19: 13 June 2019;
             1- adding node after a connecter is started from another connected is added.
             2- cancelling the node procedure is added.
             
Ver 0.0.21: 16 June 2019;
             1- add a node to the list is fixed.
             2- select a node is added.

Ver 0.0.23: 19 June 2019;             
             1- remove seleted connector attached to a node is added.
             2- remove a connector attached to a node is added.

Ver 0.0.24: 21 June 2019;             
             1- moving Node is added.

Ver 0.0.31: 24 June 2019;
             1- logging is added.

Ver 0.0.32: 29 June 2019;
             1- connector signal type is added.
             
Ver 0.0.34: 29 June 2019;
             1- signal type is added.
             
Ver 0.0.35: 30 June 2019;
             1- loading node property from file is added.
            
Ver 0.0.36: 3 July 2019;
             1- node/connector loading properties are added.
            
Ver 0.0.38: 7 July 2019;
             1- block type pop up menu is added.

Ver 0.0.39: 10 July 2019;
             1- signal type is corrected.
             2- issue with moving connectors and changing signal type is fixed.
             
********************************************************************************
"""


import tkinter as tk

from . import cntsheetcanavs
from . import coloredtext
from . import dlgeditproperty
from ..graf import grfnode
from ..graf import grfblock
from ..graf import grfconnector


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'BlodiatorCore: '


#################################################
CANVAS_MARGIN = 10  # canvas margin in pixel
WIDTH = 300  # canvas width
HEIGHT = 500  # canvas height
BACKGROUND_COLOR = 'white'  # canvas background color
GRID_STATE = True  # default grid state
GRID_X_STEP = 30  # default grid x spacing
GRID_Y_STEP = 30  # default grid y spacing
CONN_SNAP = True  # default behaviour of snapping to ports
CONN_SNAP_RAD = 5  # define the radius of snapping
GRID_X_BRUSH = ('black', 1.0, (2, ))  # default line thickness and style for grid x
GRID_Y_BRUSH = ('red', 1.0, (2, ))  # default line thickness and style for grid x
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
OPR_MODE = {'idle': 0, 'block': 1, 'connector': 2, 'node': 3, 'remove': 4, 'move': 5}  # operation modes of editor
KEY = {'block': 'b', 'connector': 'c', 'node': 'n', 'remove': 'd', 'move': 'm', 'grid': 'g', 'snap': 's', 'print': 'p', 'esc': '\x1b'}  # shortcuts with associated function
CURSOR = {'idle': 'arrow', 'block': 'cross blue', 'connector': 'circle	green', 'node': 'target magenta', 'remove': 'X_cursor red', 'move': 'hand2 black'}  # cursors with associated functions
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
XML_PROPERTY_FILE = 'Block_Type_Sink.xml'
#################################################


# BlodiatorCore class: this is the blodiator base class
# {
class BlodiatorCore(object):
  """
  This class deals with drawing, selecting, moving, and removing 
  digrams. It is the parent class for the main class.
  
  Define an instance of 'BlodiatorCore' with appropriate arguments:
      master = root widget
      size = (width, height) of diagram canvas
      std = standard output which is an instance of 'ColoredText' class
      
  The class includes all lists of created nodes, connectors, and blocks in the
  canvas. It also provides message handlers for selecting, moving and removing 
  various parts of block diagrams.
  """

  version = '0.0.39'  # version of the class

  # < class functions section >
  # union inline func: union two boxes
  # {  
  """union operation for two boxes"""
  union = lambda box_1, box_2: [min(box_1[0], box_1[2], box_2[0], box_2[2]),\
                                min(box_1[1], box_1[3], box_2[1], box_2[3]),\
                                max(box_1[0], box_1[2], box_2[0], box_2[2]),\
                                max(box_1[1], box_1[3], box_2[1], box_2[3])]  # check if a point is within a box
  # } union inline func
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, master, size=(WIDTH, HEIGHT), std=None):
    """
    Construct a BlodiatorCore
    
    input:
        master = root widget
        size = (width, height) of diagram canvas
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    if std is None:
      print(src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std

    self.std.Print('Initialising BlodiatorCore', fg, bg, style, src)

    self.__OprMode = OPR_MODE['idle']
    
    self.__master = master

    self.__Flag = False  # flag of creation mode

    self.__snap = False  # flag of snapping mode

    self.__indexObj = -1  # index of the selected object
    self.__typeObj = 'None'  # type of the selected object

    self.__Blocks = []  # list of blocks in the canvas
    self.__Connectors = []  # list of connectors in the canvas
    self.__Nodes = []  # list of nodes in the canvas
    
    self.__tmpObj = []  # temporary varible for newly createed object
    self.__tmpCons = []  # temporary varible for newly created connectors
    self.__tmpNode = []  # temporary varible for newly createed node
    
    self.__selectedPort = ''
    
    self.__blockCounter = 0
    self.__connecterCounter = 0
    self.__nodeCounter = 0
    self.__bbox = [0, 0, size[0], size[1]]
    self.__width = size[0]
    self.__height = size[1]
    
    self.__block_xml_file = XML_PROPERTY_FILE
    
    #  create a canvas object
    self.__container = cntsheetcanavs.CntSheetCanvas(master=master, std=std, size=size)
    self.__container.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
    
    self.setupApp()
  # } __init__ func
  # < inherited functions section >


  # < class functions section >  
  # setupApp func: setup the application gui
  # {
  def setupApp(self):
    """
    Internal function.
    
    Configures the application gui
    
    input: none
    output: none
    """

#    self.__container.pack()

    self.std.Print('Setting up BlodiatorCore', fg, bg, style, src)

    self.__container.focus_set()
    
    self.__container.bind('<Key>', self.keyPressed)
    self.__container.bind('<Motion>', self.mouseMotion)
    self.__container.bind('<Button-1>', self.mousePressed)
    self.__container.bind('<ButtonRelease-1>', self.mouseReleased)
  # } setupApp func

  # draw_objects func: draw the objects
  # {
  def draw_objects(self):
    """
    Internal function.
    
    It is called when the objects are redrawn. The code recalculates the 
    bounding box based on the existing objects in the canvas.
    
    input: none
    output: none
    """
         
    box = [0, 0, self.__width, self.__height]
        
    for Obj in self.__Blocks:
        box = BlodiatorCore.union(box, Obj.bbox)
        pass
        
    for Obj in self.__Nodes:
        box = BlodiatorCore.union(box, Obj.bbox)
        pass
    
    for Obj in self.__Connectors:
        box = BlodiatorCore.union(box, Obj.bbox)
        pass
    
    self.__bbox = [box[0] - CANVAS_MARGIN, box[1] - CANVAS_MARGIN,\
                   box[2] + CANVAS_MARGIN, box[3] + CANVAS_MARGIN]
    
  # } draw_objects func
 
  # keyPressed func: function handle for key pressed
  # {
  def keyPressed(self, event):
    """
    Internal function.
    
    Deals with the key pressed.
    predefined keys put the operation mode is a specific state.
    See 'KEY' global variable for the list of keys.
    
    input: 
        event = pressed key
    output: none
    """

    key = (event.char).lower()
    
    if key == KEY['print']:
      self.printItems()
    if key == KEY['block']:
       self.std.Print('Switching to block mode', fg, bg, style, src)
       self.__OprMode = OPR_MODE['block']
       self.__container.config(cursor=CURSOR['block'])
       self.__tmpObj = []
       self.__tmpCons = []
       self.__tmpNode = []
    elif key.lower() == KEY['connector']:
       self.std.Print('Switching to connector mode', fg, bg, style, src)
       self.__OprMode = OPR_MODE['connector']
       self.__container.config(cursor=CURSOR['connector'])      
    elif key.lower() == KEY['node']:
       self.std.Print('Switching to node mode; not active', fg, bg, style, src)
##       self.__OprMode = OPR_MODE['node']
##       self.__container.config(cursor=CURSOR['node'])      
    elif key.lower() == KEY['remove']:
       self.std.Print('Switching to remove mode', fg, bg, style, src)
       self.__OprMode = OPR_MODE['remove']
       self.__container.config(cursor=CURSOR['remove'])
       self.removeSelected()
       self.__tmpObj = []
       self.__tmpCons = []
       self.__tmpNode = []
    elif key.lower() == KEY['move']:
       self.std.Print('Switching to move mode', fg, bg, style, src)
       self.__OprMode = OPR_MODE['move']
       self.__container.config(cursor=CURSOR['move'])
       self.moveSelected()
    elif key.lower() == KEY['grid']:
       self.std.Print('Toggeling the grid', fg, bg, style, src)      
       self.__container.grid_state = not(self.__container.grid_state)
    elif key.lower() == KEY['snap']:
       self.std.Print('Toggeling the snap mode', fg, bg, style, src)      
       self.__snap = not(self.__snap)
    elif key.lower() == KEY['esc']:
      self.std.Print('Canceling the last operation', fg, bg, style, src)
      if self.__Flag == True:
        self.__tmpObj.erase()
        self.__tmpObj = []
        self.__Flag = False
        if len(self.__tmpNode) != len(self.__Nodes):
          for Obj in self.__Connectors:
              Obj.erase()
          for Obj in self.__Nodes:
              Obj.erase()

          # return all connectors to previous state
          self.__Connectors = []
          for Obj in self.__tmpCons:
            c = grfconnector.GrfConnector(sheetCanvas=self.__container, label='Connector' + str(self.__connecterCounter), std=self.std)
            c.inPortID = Obj.inPortID
            c.outPortID = Obj.outPortID
            c.inPortPos = Obj.inPortPos
            c.outPortPos = Obj.outPortPos
            c.con_type  = Obj.con_type 
            c.draw()
            
            colorset, brushset, arrow_set, typeset = self.connector_property
            
            c.colorset = colorset
            c.brushset = brushset
            c.arrow = arrow_set
            c.color_type = typeset
                    
            self.__Connectors.append(c)
            self.__connecterCounter +=1
            pass
            
          # return all nodes to previous state
          self.__Nodes = []
          for Obj in self.__tmpNode:
            c = grfnode.GrfNode(sheetCanvas=self.__container, label='Node' + str(self.__connecterCounter), std=self.std)
            c.center = Obj.center
            c.outPort = Obj.outPort
            c.inPort = Obj.inPort
            c.con_type  = Obj.con_type 
            c.draw()
            
            colorset, brushset, size_prop, typeset = self.node_property

            c.colorset = colorset
            c.brushset = brushset
            c.size = size_prop
            c.color_type = typeset
                    
            self.__Nodes.append(c)
            self.__nodeCounter +=1
            pass

          self.__tmpCons = []
          self.__tmpNode = []
          pass

      elif self.__OprMode == OPR_MODE['move'] and self.__indexObj != -1:
        self.__indexObj = -1
      self.std.Print('Switching to idle mode', fg, bg, style, src)
      self.__OprMode = OPR_MODE['idle']
      self.__container.config(cursor=CURSOR['idle'])
      self.close_popup_menu()
    else:
       self.std.Print('Switching to idle mode', fg, bg, style, src)
       self.__OprMode = OPR_MODE['idle']
       self.__container.config(cursor=CURSOR['idle'])
       self.close_popup_menu()
  # } keyPressed func

  # mousePressed func: function handle for mouse left button pressed
  # {
  def mousePressed(self, event):
    """
    Internal function.
    
    Message handler to deal with the mouse left button pressed.
    Depending on the operation mode, an appropriate function is called including 
    placing a block, placing connector, selecting/moving/removing objects.
    
    input: 
        event: mouse cursor position
    output: none
    """

    x, y = self.__container.convert_coords((event.x, event.y), snap_mode=self.__snap)

    if self.__OprMode == OPR_MODE['block']:
      self.placeBlock(x, y)
    elif self.__OprMode == OPR_MODE['connector']:
      self.__Flag = True
      self.placeConnector(x, y)
    elif self.__OprMode == OPR_MODE['remove']:
      self.removeObjAtCoor(x, y)
    elif self.__OprMode == OPR_MODE['move']:
      self.moveObj(x, y)
    else:
      self.selectObj(x, y)
         
    self.draw_objects()
    self.close_popup_menu()
  # } mousePressed func

  # mouseMotion func: function handle for mouse motion
  # {
  def mouseMotion(self, event):
    """
    Internal function.
    
    Message handler to deal with the mouse motion.
    Depending on the operation mode, an appropriate action is taken.
    For instance if the operation mode is creating 'connector', mouseMotion
    moves the output port of the connector in the canvas while the input port
    stays put.
    
    input: 
        event: mouse cursor position
    output: none
    """

    if self.__OprMode == OPR_MODE['connector'] and self.__Flag == True:
      self.connectorMotion(event)
      
    elif self.__OprMode == OPR_MODE['move'] and self.__indexObj != -1:
      if self.__typeObj == 'Block' and self.__Blocks[self.__indexObj].mode != 'selected':
        self.__Blocks[self.__indexObj].center = self.__container.convert_coords((event.x, event.y), snap_mode=self.__snap)
        for port in self.__Blocks[self.__indexObj].inPort:
          portID = port[0]
          ind_index = portID.find('-i-')
          index = int(portID[ind_index + 3:])

          element = self.__Blocks[self.__indexObj].grfx
          cent = element[index + 1].center
          
          for con in self.__Connectors:
            if portID == con.inPortID:
              con.inPortPos = cent
              pass
            if portID == con.outPortID:
              con.outPortPos = cent
              pass
            pass
          pass
        
        for port in self.__Blocks[self.__indexObj].outPort:
          portID = port[0]
          ind_index = portID.find('-o-')
          index = int(portID[ind_index + 3:])

          element = self.__Blocks[self.__indexObj].grfx
          cent = element[self.__Blocks[self.__indexObj].no_of_inputs + index + 1].center   
          for con in self.__Connectors:
            if portID == con.inPortID:
              con.inPortPos = cent
              pass
            if portID == con.outPortID:
              con.outPortPos = cent
              pass
            pass
          pass

        pass
      elif self.__typeObj == 'Connector' and self.__tmpObj != []:
        self.connectorMotion(event)
        pass
      
      elif self.__typeObj == 'Node' and self.__tmpObj != []:

          x, y = self.__container.convert_coords((event.x, event.y), snap_mode=self.__snap)
      
          self.__Nodes[self.__indexObj].center = x, y
          outNodeID = [P[0] for P in self.__tmpObj.outPort]
          inNodeID = self.__tmpObj.inPort[0]
                    
          for conObj in self.__Connectors:          
              if (outNodeID[0] == conObj.inPortID):
                  conObj.inPortPos = x, y
                  break
              pass
          
          for conObj in self.__Connectors:          
              if (outNodeID[1] == conObj.inPortID):
                  conObj.inPortPos = x, y
                  break
              pass
                    
          for conObj in self.__Connectors:          
              if (inNodeID == conObj.outPortID):
                  conObj.outPortPos = x, y
                  break
              pass
            

  # } mouseMotion func

  # connectorMotion func: function handle for mouse motion when drawing connector
  # {
  def connectorMotion(self, event):
    """
    Internal function.
    
    When creating/moving a connector, checks the mouse cursor location and snaps
    the port to any adjacent block ports.
    
    input: 
        event: mouse cursor position
    output: none
    """

    x, y = self.__container.convert_coords((event.x, event.y), snap_mode=False, conversion_mode=True)

    block = []
    ID = []
    sig_type = 'none'

    # if snapping the connectors to block port is enabled
    if CONN_SNAP == True:
      for Obj in self.__Blocks:
        if (x, y) in Obj:
          port = Obj.selectedObj
          if port != 0:
            x, y = port.center
            block = Obj.selectedObj
            ID = Obj.selectedID
            sig_type = Obj.selectedPort[3] 
            break

    if self.__selectedPort == 'in':
      self.__tmpObj.inPortPos = self.__container.convert_coords((x, y), self.__snap, conversion_mode=False)
      return ID, sig_type, self.__tmpObj.inPortPos
    elif self.__selectedPort == 'out':
      self.__tmpObj.outPortPos = self.__container.convert_coords((x, y), self.__snap, conversion_mode=False)
      return ID, sig_type, self.__tmpObj.outPortPos
    
  # } connectorMotion func

  # mouseReleased func: function handle for mouse left button released
  # {
  def mouseReleased(self, event):
    """
    Internal function.
    
    Message handler to deal with the mouse left button released.
    Depending on the operation mode, an appropriate action is taken.
    For instance if the operation mode is creating 'connector', mouseMotion
    assigns appropriate signal type to the connector.
    
    input: 
        event: mouse cursor position
    output: none
    """


    if self.__OprMode == OPR_MODE['connector'] and self.__Flag == True:
      ID, sig_type, self.__tmpObj.outPortPos = self.connectorMotion(event)
      if (ID != []):
        self.__tmpObj.outPortID = ID
        self.__tmpObj.con_type = sig_type
        pass
      else:
        self.__tmpObj.outPortID = '0'
        pass
        
      i = len(self.__Connectors)
      self.__Connectors.append(self.__tmpObj)
      self.__tmpObj = []
      self.__tmpCons = []
      self.__tmpNode = []
      self.__Flag = False
      pass
    elif self.__OprMode == OPR_MODE['move'] and self.__indexObj != -1:
      if self.__typeObj == 'Node':
          x, y = self.__container.convert_coords((event.x, event.y), self.__snap)
      
          self.__tmpObj.center = x, y
          outNodeID = [P[0] for P in self.__tmpObj.outPort]
          inNodeID = self.__tmpObj.inPort[0]
          
          for conObj in self.__Connectors:          
              if (outNodeID[0] == conObj.inPortID):
                  conObj.inPortPos = x, y
                  break
              pass
          
          for conObj in self.__Connectors:          
              if (outNodeID[1] == conObj.inPortID):
                  conObj.inPortPos = x, y
                  break
              pass
                    
          for conObj in self.__Connectors:          
              if (inNodeID == conObj.outPortID):
                  conObj.outPortPos = x, y
                  break
              pass

          self.__indexObj = -1
          self.__typeObj == 'None'
    
      elif self.__typeObj == 'Block':
        self.__Blocks[self.__indexObj].center = self.__container.convert_coords((event.x, event.y), self.__snap) 
        self.__Blocks[self.__indexObj].mode = 'normal'
        self.__indexObj = -1
        self.__typeObj == 'None'
        
        for port in self.__Blocks[self.__indexObj].inPort:
          portID = port[0]
          ind_index = portID.find('-i-')
          index = int(portID[ind_index + 3:])

          element = self.__Blocks[self.__indexObj].grfx
          cent = element[index + 1].center

          for con in self.__Connectors:
            if portID == con.inPortID:
              con.inPortPos = cent
              pass
            if portID == con.outPortID:
              con.outPortPos = cent
              pass
            pass
          pass
        
        for port in self.__Blocks[self.__indexObj].outPort:
          portID = port[0]
          ind_index = portID.find('-o-')
          index = int(portID[ind_index + 3:])

          element = self.__Blocks[self.__indexObj].grfx
          cent = element[self.__Blocks[self.__indexObj].no_of_inputs + index + 1].center   

          for con in self.__Connectors:
            if portID == con.inPortID:
              con.inPortPos = cent
              pass
            if portID == con.outPortID:
              con.outPortPos = cent
              pass
            pass
          pass
      
        pass
    
      if self.__typeObj == 'Connector': # and self.__Connectors[self.__indexObj].mode == 'normal':
        if self.__selectedPort == 'in':
          ID, sig_type, self.__tmpObj.inPortPos = self.connectorMotion(event)
          if (ID != []):
            self.__tmpObj.inPortID = ID            
            self.__tmpObj.con_type = sig_type
            pass
          else:
            self.__tmpObj.inPortID = '0'
#            self.__tmpObj.con_type = sig_type
            pass
          pass
        elif self.__selectedPort == 'out':
          ID, sig_type, self.__tmpObj.outPortPos = self.connectorMotion(event)
          if (ID != []):
            self.__tmpObj.outPortID = ID
            self.__tmpObj.con_type = sig_type
            pass
          else:
            self.__tmpObj.outPortID = '0'
#            self.__tmpObj.con_type = sig_type
            pass
          pass
        self.__tmpCons = []
        self.__tmpNode = []
        self.__tmpObj = []
        self.__Flag = False
        self.__indexObj = -1
        self.__typeObj = 'None'
        pass
      pass
      
    self.draw_objects()

  # } mouseReleased func

  # moveSelected func: move the selected object
  # {
  def moveSelected(self):
    """
    Internal function.
    
    Message handler to find selected object to move.
    
    input: none
    output: none
    """

    self.std.Print('Moving selected object', fg, bg, style, src)
    
    self.__indexObj = -1

    i = len(self.__Nodes)
    for Index in range(i - 1, -1, -1):
      obj = self.__Nodes[Index]
      if obj.mode == 'selected':
        self.__indexObj = Index
        self.__typeObj == 'Node'
        return

    i = len(self.__Connectors)
    for Index in range(i - 1, -1, -1):
      obj = self.__Connectors[Index]
      if obj.mode == 'selected':
        self.__indexObj = Index
        self.__typeObj == 'Connector'
        return

    i = len(self.__Blocks)
    for Index in range(i - 1, -1, -1):
      obj = self.__Blocks[Index]
      if obj.mode == 'selected':
        self.__indexObj = Index
        self.__typeObj == 'Block'
        return

  # } moveSelected func

  # removeSelected func: remove the selected object
  # {
  def removeSelected(self):
    """
    Internal function.
    
    Message handler to remove the selected object.
    
    input: none
    output: none
    """

    self.std.Print('Removing selected object', fg, bg, style, src)

    i = len(self.__Connectors)
    Temp = self.__Connectors
    self.__Connectors = []
    inPortID = '0'
    Flag = False
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      if obj.mode == 'selected':
        obj.erase()
        inPortID = obj.inPortID
        outPortID = obj.outPortID
        Flag = True
        continue
      else:
        self.__Connectors.append(obj)
    Temp = []
                           
    if Flag == True:

      if (inPortID != '0') or (outPortID != '0'):
        self.removeNode(inPortID, outPortID)

      self.__tmpObj = []
      self.__tmpCons = []
      self.__tmpNode = []
      self.__Flag = False
      self.__typeObj = ''
      self.__indexObj = -1
      self.__typeObj == 'None'
      self.__selectedPort = ''
      return

    i = len(self.__Blocks)
    Temp = self.__Blocks
    self.__Blocks = []
    Flag = False
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      if obj.mode == 'selected':
        obj.erase()
        Flag = True
        continue
      else:
        self.__Blocks.append(obj)
    Temp = []
    if Flag == True:
      self.__tmpObj = []
      self.__tmpCons = []
      self.__tmpNode = []
      self.__Flag = False
      self.__typeObj = ''
      self.__indexObj = -1
      self.__typeObj == 'None'
      self.__selectedPort = ''
      return    

    self.draw_objects()

  # } removeSelected func

  # selectObj func: function handle for selecting objects
  # {
  def selectObj(self, x, y):
    """
    Internal function.
    
    Message handler to deal with selecting objects.
    
    input:
        x, y = coordinate of the clicked mouse
    output: none
    """
    
    nodeOrder, connectorOrder, blockOrder = self.getSelectedOrder(x, y)
    
    self.__typeObj = 'None'
    i = len(self.__Nodes)
    Temp = self.__Nodes
    Flag = False
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      obj.mode = 'normal'

    i = len(self.__Connectors)
    Temp = self.__Connectors
    Flag = False
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      obj.mode = 'normal'

    i = len(self.__Blocks)
    Temp = self.__Blocks
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      obj.mode = 'normal'

    if nodeOrder == [-1] and connectorOrder == [-1] and blockOrder == [-1]:
        return
        
    elif (max(nodeOrder) > max(connectorOrder)) and (max(nodeOrder) > max(blockOrder)):
      
      self.__typeObj = 'Node'
      maxOrder = max(nodeOrder)
      i = len(self.__Nodes)
      Temp = self.__Nodes
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          obj.mode = 'selected'
          continue
        else:
          obj.mode = 'normal'
          continue

    elif (max(connectorOrder) > max(nodeOrder)) and (max(connectorOrder) > max(blockOrder)):
      
      self.__typeObj = 'Connector'
      maxOrder = max(connectorOrder)
      i = len(self.__Connectors)
      Temp = self.__Connectors
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          obj.mode = 'selected'
          continue
        else:
          obj.mode = 'normal'
          continue

    elif (max(blockOrder) > max(nodeOrder)) and (max(blockOrder) > max(connectorOrder)):
      
      self.__typeObj = 'Block'
      maxOrder = max(blockOrder)
      i = len(self.__Blocks)
      Temp = self.__Blocks
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          obj.mode = 'selected'
          continue
        else:
          obj.mode = 'normal'
          continue

    pass
  # } selectObj func

  # moveObj func: function to move the block
  # {
  def moveObj(self, x, y):
    """
    Internal function.
    
    Message handler to deal with moving the object.
    If the object is preselected, it is moved to the given coordinate.
    
    input:
        x, y = coordinate of the mouse cursor
    output: none
    """

    if self.__indexObj != -1 and self.__typeObj == 'Block':
      self.__Blocks[self.__indexObj].center = [x, y]
      self.__Blocks[self.__indexObj].mode = 'normal'
      self.__indexObj = -1
      self.__typeObj = 'None'
      
      for port in self.__Blocks[self.__indexObj].inPort:
        portID = port[0]
        ind_index = portID.find('-i-')
        index = int(portID[ind_index + 3:])
        
        element = self.__Blocks[self.__indexObj].grfx
        cent = element[index + 1].center
        
        for con in self.__Connectors:
          if portID == con.inPortID:
            con.inPortPos = cent
            pass
          if portID == con.outPortID:
            con.outPortPos = cent
            pass
          pass
        pass

      for port in self.__Blocks[self.__indexObj].outPort:
        portID = port[0]
        ind_index = portID.find('-o-')
        index = int(portID[ind_index + 3:])

        element = self.__Blocks[self.__indexObj].grfx
        cent = element[self.__Blocks[self.__indexObj].no_of_inputs + index + 1].center   

        for con in self.__Connectors:
          if portID == con.inPortID:
            con.inPortPos = cent
            pass
          if portID == con.outPortID:
            con.outPortPos = cent
            pass
          pass
        pass
  
      return
#    if self.__indexObj != -1 and self.__typeObj == 'Connector':
     # return
      
    nodeOrder, connectorOrder, blockOrder = self.getSelectedOrder(x, y)  

    if nodeOrder == [-1] and connectorOrder == [-1] and blockOrder == [-1]:
      self.__indexObj = -1
      self.__typeObj = 'None'

    elif (max(nodeOrder) > max(connectorOrder)) and (max(nodeOrder) > max(blockOrder)):
      maxOrder = max(nodeOrder)
      i = len(self.__Nodes)
      Temp = self.__Nodes
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          self.__indexObj = Index
          self.__typeObj = 'Node'
          break
      
      self.__tmpObj = obj
      self.__tmpObj.shapeorder = grfconnector.grfobject.GrfObject.ObjOrder
      outNodeID = [P[0] for P in obj.outPort]
      inNodeID = obj.inPort[0]
      
      for ind, conObj in enumerate(self.__Connectors):
          if (outNodeID[0] == conObj.inPortID) or \
          (outNodeID[1] == conObj.inPortID) or \
          (inNodeID == conObj.outPortID):
              conObj.bring_2_front()
              continue          

      self.__tmpObj.mode = MODE[0]
      self.__tmpObj.bring_2_front()
        
    elif (max(connectorOrder) > max(nodeOrder)) and (max(connectorOrder) > max(blockOrder)):
      maxOrder = max(connectorOrder)
      i = len(self.__Connectors)
      Temp = self.__Connectors
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          self.__indexObj = Index
          self.__typeObj = 'Connector'

          x_in, y_in = obj.inPortPos
          x_out, y_out = obj.outPortPos
          d_in = (x_in - x)**2 + (y_in - y)**2
          d_out = (x_out - x)**2 + (y_out - y)**2
          
          outPortFlag = False          
          for nodeObj in self.__Nodes:
              inNodeID = nodeObj.inPort[0]
              
              if (inNodeID == obj.outPortID):
                  outPortFlag = True
                  break
              pass
              
          inPortFlag = False
          for nodeObj in self.__Nodes:
              outNodeID = [P[0] for P in nodeObj.outPort]
              
              if (outNodeID[0] == obj.inPortID) or (outNodeID[1] == obj.inPortID):
                  inPortFlag = True
                  break
              pass
          
          if (outPortFlag == False) and (inPortFlag == False):
              self.__selectedPort = 'in' if d_in < d_out else 'out'
              pass
          elif (outPortFlag == True) and (inPortFlag == False):
              self.__selectedPort = 'in'
              pass
          elif (outPortFlag == False) and (inPortFlag == True):
              self.__selectedPort = 'out'
              pass
          else:
              self.__indexObj = -1
              self.__typeObj = 'None'
              break          
          
          self.__tmpObj = obj
          self.__tmpObj.bring_2_front()
          self.__tmpObj.shapeorder = grfconnector.grfobject.GrfObject.ObjOrder
          self.__tmpObj.mode = MODE[0]
          break
      
    elif (max(blockOrder) > max(nodeOrder)) and (max(blockOrder) > max(connectorOrder)):
      maxOrder = max(blockOrder)
      i = len(self.__Blocks)
      Temp = self.__Blocks
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          self.__indexObj = Index
          self.__typeObj = 'Block'
          self.__tmpObj = obj
          self.__tmpObj.mode = MODE[0]
          break

    pass
  # } moveObj func
  
  # placeBlock func: function to place the block
  # {
  def placeBlock(self, x, y):
    """
    Internal function.
    
    Message handler to deal with placing the block.
    The selected block type is used to place appropriate block on the canvas.
    
    input:
        x, y = coordinate of the mouse cursor
    output: none
    """

    self.std.Print('Placing block', fg, bg, style, src)

    self.__tmpObj = grfblock.GrfBlock(sheetCanvas=self.__container,\
                                      label='Block' + str(self.__blockCounter),\
                                      xml_file=self.block_xml_file, center=(x, y),\
                                      std=self.std)
    self.__tmpObj.draw()

    label = self.__tmpObj.label

    Port_Feat = []
    for i, port in enumerate(self.__tmpObj.inPort):
      portID = label + '-i-' + str(i)
      Port_Feat.append([portID, port[1], port[2], port[3], port[4]])

    self.__tmpObj.inPort = Port_Feat

    Port_Feat = []
    for i, port in enumerate(self.__tmpObj.outPort):
      portID = label + '-o-' + str(i)
      Port_Feat.append([portID, port[1], port[2], port[3], port[4]])

    self.__tmpObj.outPort = Port_Feat
    
    colorset, brushset, font_prop, geo_prop, typeset = self.block_property
           
    self.__tmpObj.colorset = colorset
    self.__tmpObj.brushset = brushset
    self.__tmpObj.font_prop = font_prop
    self.__tmpObj.geo_prop = geo_prop
    self.__tmpObj.color_type = typeset
 
    self.__Blocks.append(self.__tmpObj)
    self.__tmpObj = []
    self.__tmpCons = []
    self.__tmpNode = []
    self.__selectedPort = ''
    self.__Flag = False
    self.__blockCounter += 1

  # } placeBlock func

  # placeNode func: function to place the node
  # {
  def placeNode(self, x, y):
    """
    Internal function.
    
    Message handler to deal with placing the node.
    Depending on the original connector, appropriate signal type is 
    used to color the node.
    
    input:
        x, y = coordinate of the mouse cursor
    output: none
    """

    self.std.Print('Placing node', fg, bg, style, src)

    i = len(self.__Nodes)
    node = grfnode.GrfNode(sheetCanvas=self.__container, label='Node' + str(self.__nodeCounter), std=self.std)
    
    node.center = [x, y]

    label = node.label

    portID = label + '-i-0'
    inPort = [portID, None, None, None]
    node.inPort = inPort

    portID_1 = label + '-o-0'
    portID_2 = label + '-o-1'
    outPort = [ [portID_1, None, None, None], [portID_2, None, None, None] ]
    node.outPort = outPort

    node.draw()

    colorset, brushset, size_prop, typeset = self.node_property

    node.colorset = colorset
    node.brushset = brushset
    node.size = size_prop
    node.color_type = typeset

    self.__nodeCounter += 1

    return node

  # } placeNode func
  
  # placeConnector func: function to place the connector
  # {
  def placeConnector(self, x, y):
    """
    Internal function.
    
    Message handler to deal with placing the connector.
    The connector starts from input port and draging the mouse decides where
    the output port will sit.
    At first, the code checks if the coordinate lays on any block port. If 
    positive, the connector takes the type of the block port.
    Then it checks if input port concides with any existing connector. If 
    possitive, a node is placed and an connector extension is added to the 
    canvas.
    
    input:
        x, y = coordinate of the mouse cursor
    output: none
    """
    
    self.std.Print('Placing connector', fg, bg, style, src)
    
    ID = []
    sig_type = 'none'

    if CONN_SNAP == True:
      for Obj in self.__Blocks:
        if (x, y) in Obj:
          port = Obj.selectedObj
          if port != 0:
            x, y = port.center
            ID = Obj.selectedID
            sig_type = Obj.selectedPort[3] 
            break

    Index_con = -1
    OldCon = []
    con = []
    if ID == []:
      for i, conObj in enumerate(self.__Connectors):
        self.__tmpObj = conObj
        if (x, y) in conObj:
          con = self.placeNode(x, y)
          sig_type = conObj.con_type
          con.con_type = sig_type
          self.__tmpCons = self.__Connectors

          Temp = self.__Nodes
          self.__tmpNode = []
          for Obj in Temp:
             self.__tmpNode.append(Obj)

          self.__Nodes.append(con)
          OldCon = conObj
          Index_con = i
          break

      if con != []:
        Temp = self.__Connectors
        self.__Connectors = []
        for i, Obj in enumerate(Temp):
          if i == Index_con:
            Obj.erase()
            continue
          else:
            self.__Connectors.append(Obj)

        Temp = []

        nodeLabel = con.label
            
        OldCon_inPort = OldCon.inPort
        con_1 = grfconnector.GrfConnector(sheetCanvas=self.__container,\
                                          label='Connector' + str(self.__connecterCounter),\
                                          con_type=SIG_TYPE[0], std=self.std)
        con_1.inPortID = OldCon.inPortID
        con_1.inPortPos = OldCon.inPortPos
        con_1.outPortID = con.inPortID
        con_1.outPortPos = [x, y]
        con_1.con_type = sig_type
        con_1.draw()

        colorset, brushset, arrow_set, typeset = self.connector_property

        con_1.colorset = colorset
        con_1.brushset = brushset
        con_1.arrow = arrow_set
        con_1.color_type = typeset

        self.__Connectors.append(con_1)
        self.__connecterCounter += 1          

        OldCon_outPort = OldCon.outPort
        con_2 = grfconnector.GrfConnector(sheetCanvas=self.__container,\
                                          label='Connector' + str(self.__connecterCounter),\
                                          con_type=SIG_TYPE[0], std=self.std)
        con_2.outPortID = OldCon.outPortID
        con_2.outPortPos = OldCon.outPortPos
        con_2.inPortID = con.outPort[0][0]
        con_2.inPortPos = [x, y]
        con_2.con_type = sig_type
        con_2.draw()

        colorset, brushset, arrow_set, typeset = self.connector_property

        con_2.colorset = colorset
        con_2.brushset = brushset
        con_2.arrow = arrow_set
        con_2.color_type = typeset

        self.__Connectors.append(con_2)
        self.__connecterCounter += 1
        
        ID = con.outPort[1][0]

        pass
      pass
      
    x, y = self.__container.convert_coords((x, y), snap_mode=self.__snap, conversion_mode=False)

    i = len(self.__Connectors)
    self.__tmpObj = grfconnector.GrfConnector(sheetCanvas=self.__container,\
                                              label='Connector' + str(self.__connecterCounter),\
                                              con_type=SIG_TYPE[0], std=self.std)

    if(ID != []):
      self.__tmpObj.inPortID = ID
      pass
    else:
      self.__tmpObj.inPortID = '0'
      pass
      
    self.__tmpObj.inPortPos = [x, y]
    self.__tmpObj.outPortPos = [x + 1, y + 1]
    self.__tmpObj.con_type = sig_type
    self.__selectedPort = 'out'
    self.__tmpObj.draw()

    color_set, brush_set, arrow_set, type_set = self.connector_property
        
    self.__tmpObj.colorset = color_set
    self.__tmpObj.brushset = brush_set
    self.__tmpObj.arrow = arrow_set
    self.__tmpObj.color_type = type_set

    self.__connecterCounter += 1
    if con != []:
        con.bring_2_front()


#    for tmp in self.__Connectors:
#          print(tmp.colorset)
#    print(self.__tmpObj.colorset)
  # } placeConnector func
  
  # getSelectedOrder func: function to return order of selected objects
  # {
  def getSelectedOrder(self, x, y):
    """
    Internal function.
    
    Decides the order of objects with provided coordinate.
    
    input:
        x, y = coordinate of the mouse cursor
    output: 
        nodeOrder, connectorOrder, blockOrder = canvas order of 
        node/connector/block. The higher number, the topper the object
    """

    i = len(self.__Nodes)
    Temp = self.__Nodes
    nodeOrder = []
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      if (x, y) in obj:
        nodeOrder.append(obj.shapeorder)
        continue
      pass
  
    if nodeOrder == []:
        nodeOrder = [-1]
        pass
    
    i = len(self.__Connectors)
    Temp = self.__Connectors
    connectorOrder = []
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      if (x, y) in obj:
        connectorOrder.append(obj.shapeorder)
        continue
      pass

    if connectorOrder == []:
        connectorOrder = [-1]
        pass

    i = len(self.__Blocks)
    Temp = self.__Blocks
    blockOrder = []
    for Index in range(i - 1, -1, -1):
      obj = Temp[Index]
      if (x, y) in obj:
        blockOrder.append(obj.shapeorder)
        continue
      pass

    if blockOrder == []:
        blockOrder = [-1]
        pass

    return nodeOrder, connectorOrder, blockOrder
  # } getSelectedOrder func
  
  # removeObjAtCoor func: function to delete the toppest object at given coordinate
  # {
  def removeObjAtCoor(self, x, y):
    """
    Internal function.
    
    Deletes the toppest object at given coordinate.
    
    input:
        x, y = coordinate of the mouse cursor
    output: none
    """

    nodeOrder, connectorOrder, blockOrder = self.getSelectedOrder(x, y)
        
    if nodeOrder == [-1] and connectorOrder == [-1] and blockOrder == [-1]:
      return False

    elif (max(connectorOrder) > max(nodeOrder)) and (max(connectorOrder) > max(blockOrder)):
      maxOrder = max(connectorOrder)
      i = len(self.__Connectors)
      Temp = self.__Connectors
      self.__Connectors = []
      inPortID = '0'
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          inPortID = obj.inPortID
          outPortID = obj.outPortID
          obj.erase()
          continue
        else:
          self.__Connectors.append(obj)
      Temp = []

      if (inPortID != '0') or (outPortID != '0'):
        self.removeNode(inPortID, outPortID)
        pass

      return True

    elif (max(blockOrder) > max(nodeOrder)) and (max(blockOrder) > max(connectorOrder)):
      maxOrder = max(blockOrder)
      i = len(self.__Blocks)
      Temp = self.__Blocks
      self.__Blocks = []
      Flag = False
      for Index in range(i - 1, -1, -1):
        obj = Temp[Index]
        if obj.shapeorder == maxOrder:
          obj.erase()
          continue
        else:
          self.__Blocks.append(obj)
      Temp = []
      return True
    pass
  
    return
  # } removeObjAtCoor func

  # removeNode func: function to remove the node
  # {
  def removeNode(self, inPortID, outPortID):
    """
    Internal function.
    
    If a node is removed from the block diagrams, it deletes the attached 
    connectors and replaces the extension with proper connectors.
    
    input:
        inPortID, outPortID = input and output port IDs of connectors attached
         to the node.
    output: none
    """

    self.std.Print('Removing node', fg, bg, style, src)
    
    for indexNode, nodeObj in enumerate(self.__Nodes):

      inNodeID = nodeObj.inPort[0]
      sig_type = nodeObj.con_type

      outNodeID = [P[0] for P in nodeObj.outPort]

      if (inNodeID == outPortID):
        out_ID_1 = nodeObj.outPortID[0]
        out_ID_2 = nodeObj.outPortID[1]

        for indexCon_1, Con_1 in enumerate(self.__Connectors):
          if Con_1.inPortID == out_ID_1:
            break
          pass
                              
        for indexCon_2, Con_2 in enumerate(self.__Connectors):
          if Con_2.inPortID == out_ID_2:
            break
          pass
          
        i = len(self.__Nodes)
        Temp = self.__Nodes
        self.__Nodes = []
        for Index in range(i - 1, -1, -1):
          obj = Temp[Index]
          if Index == indexNode:
            obj.erase()
            continue
          else:
            self.__Nodes.append(obj)
            pass
          pass
        
        Temp = []

        for Index, inCon in enumerate(self.__Connectors):
          if Index == indexCon_1 or Index == indexCon_2:
            inCon.inPortID = '0'
            pass
          pass

        return
    
      elif (outNodeID[0] == inPortID) or (outNodeID[1] == inPortID):

        if (outNodeID[0] == inPortID):
          out_ID = nodeObj.outPortID[1]
          pass
        else:
          out_ID = nodeObj.outPortID[2]
          pass          
        in_ID = nodeObj.inPortID

        for indexCon_1, Con_1 in enumerate(self.__Connectors):
          if Con_1.inPortID == out_ID:
            break
          pass
                              
        for indexCon_2, Con_2 in enumerate(self.__Connectors):
          if Con_2.outPortID == in_ID:
            break
          pass
          
        i = len(self.__Nodes)
        Temp = self.__Nodes
        self.__Nodes = []
        for Index in range(i - 1, -1, -1):
          obj = Temp[Index]
          if Index == indexNode:
            obj.erase()
            continue
          else:
            self.__Nodes.append(obj)
            pass
          pass
        
        Temp = []

        i = len(self.__Connectors)
        Temp = self.__Connectors
        self.__Connectors = []
        for Index in range(i - 1, -1, -1):
          obj = Temp[Index]
          if (Index == indexCon_1) or (Index == indexCon_2):
            obj.erase()
            continue
          else:
            self.__Connectors.append(obj)
            pass
          pass
        
        Temp = []
        
        i = len(self.__Connectors)
        self.__tmpObj = grfconnector.GrfConnector(sheetCanvas=self.__container, label='Connector' + str(self.__connecterCounter), std=self.std)

        self.__tmpObj.inPortPos = Con_2.inPortPos
        self.__tmpObj.outPortPos = Con_1.outPortPos
        self.__tmpObj.inPortID = Con_2.inPortID
        self.__tmpObj.outPortID = Con_1.outPortID
        self.__tmpObj.con_type = sig_type
        self.__tmpObj.draw()
        
#        print(self.connector_property)
        
        color_set = self.connector_property[0]
        brush_set = self.connector_property[1]
        arrow_set = self.connector_property[2]
        type_set = self.connector_property[3]

        self.__tmpObj.colorset = color_set
        self.__tmpObj.brushset = brush_set
        self.__tmpObj.arrow = arrow_set
        self.__tmpObj.color_type = type_set

        self.__connecterCounter += 1
                       
        self.__Connectors.append(self.__tmpObj)
        self.__tmpObj = []
        self.__tmpCons = []
        self.__tmpNode = []

        break
      pass  
  
    return  
  # } removeNode func
  
  # close_popup_menu func: function to close pop up menus
  # {
  def close_popup_menu(self):
    """
    Internal function.
    
    Closes the block type pop up menu. It is defined in the child class
    
    input: none
    output: none
    """

  # } close_popup_menu func

  # printItems func: function to print out the items
  # {
  def printItems(self):
    """
    Internal function.
    
    Prints out the block diagram items available in the canvas
    
    input: none
    output: none
    """
    '; no input; no output'

    self.std.Print('Printing out items', fg, bg, style, src)

    print('\n')
    print('Items:')

    print('******** Blocks:')
    for index, obj in enumerate(self.__Blocks):
      print( str(index) + ' -')
      print(obj)
      print('------------------------------------------------')
      pass
    
    print('******** Connectors:')
    for index, obj in enumerate(self.__Connectors):
      print( str(index) + ' -')
      print(obj)
      print('------------------------------------------------')
      pass

    print('******** Nodes:')
    for index, obj in enumerate(self.__Nodes):
      print( str(index) + ' -')
      print(obj)
      print('------------------------------------------------')
      pass
  
    return  
  # } printItems func
  # < class functions section >
  
  
  # < getter and setter functions section >
  # property: nodes
  # nodes getter func: node array getter
  # {
  @property
  def nodes(self):
    """
    Class property getter: node list
    """

    return self.__Nodes
  # } nodes getter func

  # nodes setter func: node array setter
  # {
  @nodes.setter
  def nodes(self, nodes):
    """
    Class property setter: node list
    """

    self.__Nodes = nodes
  # } nodes setter func

  # property: blocks
  # blocks getter func: block array getter
  # {
  @property
  def blocks(self):
    """
    Class property getter: block list
    """

    return self.__Blocks
  # } blocks getter func

  # blocks setter func: block array setter
  # {
  @blocks.setter
  def blocks(self, blocks):
    """
    Class property setter: node arlistray
    """

    self.__Blocks = blocks
  # } blocks setter func

  # property: connectors
  # connectors getter func: connector array getter
  # {
  @property
  def connectors(self):
    """
    Class property getter: connector list
    """

    return self.__Connectors
  # } connectors getter func

  # connectors setter func: connector array setter
  # {
  @connectors.setter
  def connectors(self, connectors):
    """
    Class property getter: connector list
    """

    self.__Connectors = connectors
  # } connectors setter func

  # property: container
  # container getter func: object angles getter
  # {
  @property
  def container(self):
    """
    Class property setter: connector list
    """

    return self.__container
  # } container getter func
  
  # property: bbox
  # bbox getter func: bounding box getter
  # {
  @property
  def bbox(self):
    """
    Class property getter: bounding box based on the all block diagrams
    """

    return self.__bbox
  # } bbox getter func

  # property: block xml file
  # block_xml_file getter func: block xml file getter
  # {
  @property
  def block_xml_file(self):
    """
    Class property getter: xml file containing information about the block
    """

    return self.__block_xml_file
  # } block_xml_file getter func

  # block_xml_file setter func: block xml file setter
  # {
  @block_xml_file.setter
  def block_xml_file(self, block_xml_file):
    """
    Class property setter: xml file containing information about the block
    """

    self.__block_xml_file = block_xml_file
  # } block_xml_file setter func

  # node_property getter func: node property getter
  # {
  @property
  def node_property(self):
    """
    Class property getter: node property, defined in the child class
    """
    
    return []
  # } node_property setter func


  # connector_property getter func: connector property getter
  # {
  @property
  def connector_property(self):
    """
    Class property setter: connector property, defined in the child class
    """

    return []
  # } connector_property setter func

  # block_property getter func: block property getter
  # {
  @property
  def block_property(self):
    """
    Class property getter: block property, defined in the child class
    """

    return []
  # } block_property setter func
  
  # < getter and setter functions section >

# } BlodiatorCore class


# main func: contains code to test BlodiatorCore class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("500x500")
  root.title('Blodiator Base Test Bench')
  TestApp = BlodiatorCore(master=root, std=CT)

  root.mainloop()
  pass
# } main func


if __name__ == '__main__':
  main()
