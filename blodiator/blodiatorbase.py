"""
********************************************************************************

Python Script: blodiatorbase Module
Writter: Mojtaba Mansour Abadi
Date: 21 June 2019

This Python script is compatible with Python 3.x.
The script is used to define BlodiatorBase class.
BlodiatorBase is the top class in the hierarchy. To use Blodiator, an 
instance of BlodiatorBase is needed.


BlodiatorBase
|
|____BlodiatorCore
     |
     |____object


Histoty:

Ver 0.0.25: 21 June 2019;
             first code

Ver 0.0.26: 22 June 2019;
             1- scrolling is added.

Ver 0.0.28: 23 June 2019;
             1- coordinate conversion is fixed.
             2- changing canvas size dynamically basd on windows size is added.

Ver 0.0.30: 24 June 2019;
             1- new/save/load diagram are added.

Ver 0.0.31: 25 June 2019;
             1- logging is added.
             2- Edit Property is added.

Ver 0.0.35: 30 June 2019;
             1- loading node property from file is added.
            
Ver 0.0.36: 3 July 2019;
             1- node/connector/block loading properties are added.
            
Ver 0.0.38: 7 July 2019;
             1- block type pop up menu is added.

Ver 0.0.39: 10 July 2019;
             1- block diagram verification is added.
             
Ver 0.0.40: 11 July 2019;
             1- 'run' command is added.
             2- generating the connection list is added.
             
********************************************************************************
"""


import tkinter as tk
import pickle
import xml.etree.ElementTree as ET

from .etc import blodiatorcore
from .etc import cntsheetcanavs
from .etc import coloredtext
from .etc import dlgeditproperty
from .graf import grfblock
from .graf import grfconnector
from .graf import grfnode


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'BlodiatorBase: '


#################################################
WINDOW_MARGIN = 25  # windows extra size margin (accounted for scrollbar width)
WIDTH = 600  # canvas width
HEIGHT = 600  # canvas height
OPR_MODE = {'idle': 0}  # operation modes of editor
KEY = {'zoom all': 'a', 'new diagram': 'n', 'write diagram': 'w', 'read diagram': 'r', 'edit property': 'e', 'block selection': 'l', 'verify diagram': 'v', 'run': 'u'}  # shortcuts with associated function
CURSOR = {'idle': 'arrow', 'scroll': 'fleur'}  # cursors with associated functions
DIAG_FILE_NAME = './diagrams/BlockDiagram.dat'  # block diagram file name
NODE_FILE_NAME = './config/NodeProperty.xml'  # node property file name
CONN_FILE_NAME = './config/ConnectorProperty.xml'  # connector property file name
BLCK_FILE_NAME = './config/BlockProperty.xml'  # block property file name
BLOCK_TYPE_FILE = './config/Block_Types.xml'  # block types file name
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
#################################################


# BlodiatorBase class: this is the blodiator base class
# {
class BlodiatorBase(blodiatorcore.BlodiatorCore):
  """
  Main class to use Blodiator.
  
  Define an instance of 'BlodiatorBase' with appropriate arguments:
      master = root widget
      size = (width, height) of diagram canvas
      node_file = address of xml file containing required properties of a 'node'
      connector_file = address of xml file containing required properties of a 'connector'
      block_file = address of xml file containing required properties of a 'block'
      block_types_file = address of xml file containing information about available types of blocks
      std = standard output which is an instance of 'ColoredText' class
      
  The class loads all properties from xml files and creates an instance of 'BlodiatorCore'
  class. It also handles several 'KeyPressed' events.
  Writing the diagrams to a file or reading them from a file is done by this class.
  The class also deals with verification/generating connection list and preparing the output
  for processing thread.
  """

  version = '0.0.39'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, master, size=(WIDTH, HEIGHT), node_file=NODE_FILE_NAME,
               connector_file=CONN_FILE_NAME, block_file=BLCK_FILE_NAME,
               block_types_file=BLOCK_TYPE_FILE, std=None):
    """
    Construct a BlodiatorBase
    
    input:
        master = root widget
        size = (width, height) of diagram canvas
        node_file = address of xml file containing required properties of a 'node'
        connector_file = address of xml file containing required properties of a 'connector'
        block_file = address of xml file containing required properties of a 'block'
        block_types_file = address of xml file containing information about available types of blocks
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    # make sure std is given
    if std is None:
      print(src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std

    self.std.Print('Initialising BlodiatorBase', fg, bg, style, src)
     
    self.__master = master
    
    self.__node_file = node_file
    self.__connector_file = connector_file
    self.__block_file = block_file
    
    self.__block_types_file = block_types_file

    # temperary variable to store diagrams
    self.__tmpObj = []

    # create the scroll bars
    self.__xscrollbar = tk.Scrollbar(master=master, orient=tk.HORIZONTAL)
    self.__xscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
    self.__yscrollbar = tk.Scrollbar(master=master)
    self.__yscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
    
    self.__block_type_menu = None
    
    super(BlodiatorBase, self).__init__(master=master, size=size, std=std)  # initialise the parent

    # initialise the scroll bars
    self.container.config(xscrollcommand=self.__xscrollbar.set, yscrollcommand=self.__yscrollbar.set, xscrollincrement = 10, yscrollincrement = 10)
    self.container.configure(scrollregion=self.container.bbox('all'))
  
    self.__xscrollbar.config(command=self.container.xview)
    self.__yscrollbar.config(command=self.container.yview)
    
    self.__loadproperties()  # load node/connector/block properties from file
    
#    super(BlodiatorBase, self).props()
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

    self.std.Print('Setting up BlodiatorBase', fg, bg, style, src)

    # setup message handlers for window changing size, and mouse wheel
    self.__master.bind('<Configure>', self.windowChange)
    self.container.bind('<MouseWheel>', self.mouseWheel)
    self.container.bind('<Button-2>', self.mouseWheelPressed)
    self.container.bind("<B2-Motion>",self.mouseWheelDrag)
    self.container.bind('<ButtonRelease-2>', self.mouseWheelReleased)
    
    self.perepareBlockMenu()
    
    # call setupApp function from 'BlodiatorCore' class
    blodiatorcore.BlodiatorCore.setupApp(self)
  # } setupApp func
  
  # keyPressed func: function handle for key pressed
  # {
  def keyPressed(self, event):
    """
    Internal function.
    
    Deals with the key pressed
    predefined keys put the operation mode is a specific state.
    See 'KEY' global variable for the list of keys.
    
    input: 
        event = pressed key
    output: none
    """

    key = (event.char).lower()

    # make sure the popup menu is closed
    self.__block_type_menu.place_forget()
    
    if key == KEY['zoom all']:
      self.zoom_all()
      pass
    elif key == KEY['new diagram']:
      self.newDiagram()
      pass
    elif key == KEY['write diagram']:
      self.writeDiagram()
      pass
    elif key == KEY['read diagram']:
      self.readDiagram()
      pass
    elif key == KEY['edit property']:
      self.editProperty(event)
      pass
    elif key == KEY['block selection']:
      self.blockSelection(event)
      pass
    elif key == KEY['verify diagram']:
      self.verifyDiagram()
      pass
    elif key == KEY['run']:
      self.runDiagram()
      pass
    else:  # if the pressed key is no handled whithin this class, let 'BlodiatorCore' handles it
      blodiatorcore.BlodiatorCore.keyPressed(self, event)
      pass
  # } keyPressed func


  # generateConnnectionList func: function handle to generate the connections list
  # {
  def generateConnnectionList(self):
    """
    Internal function.
    
    Generates the connections list for processing purposes
    
    input: none
    output:
        ConnList = generated list
    """
        
    self.std.Print('Generating the list of connections between blocks', fg, bg, style, src)

    ConnList = []    
    
    for block in self.blocks:
      input_ports = block.inPort
      output_ports = block.outPort

      # check all input ports of the block
      for inPort in input_ports:
        port_ID, port_Name, _, _, _ = inPort
        for conn in self.connectors:
          if conn.outPortID == port_ID:
            source, _ = self.find_ends_connector(conn, direction = -1)
            sink = port_ID
            item = (source[-1], sink)
            ConnList.append(item)
            pass
          pass
        pass
    
      # check all output ports of the block
      for outPort in output_ports:
        port_ID, port_Name, _, _, _ = outPort
        for conn in self.connectors:
          if conn.inPortID == port_ID:
            source = port_ID
            _, sink = self.find_ends_connector(conn, direction = +1)
            item = (source, sink[-1])
            ConnList.append(item)
            pass
          pass
        pass
      
      pass
  
    # remove any duplicates
    ConnList = list(set(ConnList))
    
    print('Connections List:')
    print('------------------------------------------------')
    
    for item in ConnList:
      print(item[0] + ' --> ' + item[1])
      pass
  
    return ConnList      
  # } generateConnnectionList func


  # runDiagram func: function handle to run the block diagrams
  # {
  def runDiagram(self):
    """
    Runs the block diagrams
    
    input: none
    output: nonr
    """
        
    self.std.Print('Executing the block diagrams', fg, bg, style, src)
            
    # find out how many error are in the block diagram.
    error_count = self.verifyDiagram()

    if (error_count > 0):  # if there are errors in the block diagrams
      self.std.Print(str(error_count) + ' number of errors were found in the block diagrams', fg, bg, style, src)
      self.std.Print('The block diagrams cannot be executed', fg, bg, style, src)
      return
    elif (self.blocks == [] and self.connectors == [] and self.nodes == []):  # if block diagram is empty
      self.std.Print('The block diagram is empty', fg, bg, style, src)
      self.std.Print('The block diagrams cannot be executed', fg, bg, style, src)
      return

    self.std.Print('The block diagrams are executed', fg, bg, style, src)
    
    ConnList = self.generateConnnectionList()

    # TODO: add the run section here!

    pass      
  # } runDiagram func


  # verifyDiagram func: function handle to verify the diagram
  # {
  def verifyDiagram(self):
    """
    Verifies the block diagrams connectivity, signal type, and non-feedback connections
    
    input = none
    output:
        error_count = number of errors in the block diagrams
    """

    self.std.Print('Verifying the block diagrams', fg, bg, style, src)
    
    for block in self.blocks:
      block.mode = MODE[0]
      pass
    
    for connector in self.connectors:
      connector.mode = MODE[0]
      pass
    
    for node in self.nodes:
      node.mode = MODE[0]
      pass
    
    error_count = 0
        
    print('Block Connectivity Report:')
    print('------------------------------------------------')

    for index_block, block in enumerate(self.blocks):
      print( str(index_block) + ': ' + block.label)
      print('~~~~~~~~~~~~~~~~~~~~~~~~')
      input_ports = block.inPort
      output_ports = block.outPort
        
      for index_inport, inPort in enumerate(input_ports):
        port_ID, port_Name, _, _, _ = inPort
        Conn_Flag = False
        for connector in self.connectors:
          if connector.outPortID == port_ID:
            Conn_name = connector.label
            Conn_Flag = True
            break
        if Conn_Flag == False:
          print(port_Name + ' of ' + block.label + ' is not connected')
          block.update_inport_mode(index_inport, MODE[3])
          error_count += 1
          pass
        elif Conn_Flag == True:
          print(port_Name + ' of ' + block.label + ' is correctly connected to ' + Conn_name)
          pass

      for index_outport, outPort in enumerate(output_ports):
        port_ID, port_Name, _, _, _ = outPort
        Conn_Flag = False
        Conn_name = ''
        for connector in self.connectors:
          if connector.inPortID == port_ID:
            Conn_name = connector.label
            Conn_Flag = True
            break
        if Conn_Flag == False:
          print(port_Name + ' of ' + block.label +  ' is not connected')
          block.update_outport_mode(index_outport, MODE[3])
          error_count += 1
          pass
        elif Conn_Flag == True:
          print(port_Name + ' of ' + block.label +  ' is correctly connected to ' + Conn_name)
          pass
    print('------------------------------------------------')
    
    print('Connector Connectivity Report:')
    print('------------------------------------------------')

    for index_connector, connector in enumerate(self.connectors):
      print( str(index_connector) + ': ' + connector.label)
      print('~~~~~~~~~~~~~~~~~~~~~~~~')
      if(connector.inPortID == '0'):
        print('Input is float')
        connector.mode = MODE[3]
        error_count += 1
        pass
      else:
        Flag = False
        for block in self.blocks:
          if Flag == True:
              break
          input_ports = block.inPort
          output_ports = block.outPort
          
          for port in input_ports:
            port_ID, port_Name, _, _, _ = port
            if(connector.inPortID == port_ID):
              print('Input of ' +  connector.label + ' is incorrectly connected to ' + port_Name + ' of ' + block.label)
              connector.mode = MODE[3]
              error_count += 1
              Flag = True
              break

          for port in output_ports:
            port_ID, port_Name, _, _, _ = port
            if(connector.inPortID == port_ID):
              print('Input of ' +  connector.label + ' is correctly connected to ' + port_Name + ' of ' + block.label)
              Flag = True
              break
          pass
        pass
    
      if(connector.outPortID == '0'):
        print('Output is float')
        connector.mode = MODE[3]
        error_count += 1
        pass
      else:
        Flag = False
        for block in self.blocks:
          if Flag == True:
              break
          input_ports = block.inPort
          output_ports = block.outPort
          
          for port in input_ports:
            port_ID, port_Name, _, _, _ = port
            if(connector.outPortID == port_ID):
              print('Output of ' +  connector.label + ' is correctly connected to ' + port_Name + ' of ' + block.label)
              Flag = True
              break

          for port in output_ports:
            port_ID, port_Name, _, _, _ = port
            if(connector.outPortID == port_ID):
              print('Output of ' +  connector.label + ' is incorrectly connected to ' + port_Name + ' of ' + block.label)
              connector.mode = MODE[3]
              error_count += 1
              Flag = True
              break
          pass
        pass    
    print('------------------------------------------------')

    print('Node Connectivity Report:')
    print('------------------------------------------------')

    for index_node, node in enumerate(self.nodes):
      outID = [P[0] for P in node.outPort]
      print( str(index_node) + ': ' + node.label)
      print('~~~~~~~~~~~~~~~~~~~~~~~~')
      if(node.inPortID == '0'):
        print('Input of ' + node.label + ' is float')
        node.mode = MODE[3]
        error_count += 1
        pass
      else:
        for con in self.connectors:
          if(con.outPortID == node.inPortID):
            if con.mode == MODE[3]:
              print('Input of ' + node.label + ' is connected to output of float ' + con.label)
              node.mode = MODE[3]
              error_count += 1
              pass
            else:
              print('Input of ' + node.label + ' is connected to output of ' + con.label)
              pass
            break
        pass
      if(outID[0] == '0'):
        print('Output 0 of ' + node.label + ' is float')
        node.mode = MODE[3]
        error_count += 1
        pass
    
      else:        
        for con in self.connectors:
          if(con.inPortID == outID[0]):
            if con.mode == MODE[3]:
              print('Output 0 of ' + node.label + ' is connected to input of float ' + con.label)
              node.mode = MODE[3]
              error_count += 1
              pass
            else:
              print('Output 0 of ' + node.label + ' is connected to input of ' + con.label)
              pass
            break
        pass
      if(outID[1] == '0'):
        print('Output 1 ' + node.label + ' is float')
        node.mode = MODE[3]
        error_count += 1
        pass
      else:        
        for con in self.connectors:
          if(con.inPortID == outID[1]):
            if con.mode == MODE[3]:
              print('Output 1 of ' + node.label + ' is connected to input of float ' + con.label)
              node.mode = MODE[3]
              error_count += 1
              pass
            else:
              print('Output 1 of ' + node.label + ' is connected to input of ' + con.label)
              pass
            break
        pass
    
    print('------------------------------------------------')

    print('Signal Type Report:')
    print('------------------------------------------------')
    
    for connector in self.connectors:
      con_sig_type = connector.con_type
      in_ID = connector.inPortID
      out_ID = connector.outPortID
      
      for block in self.blocks:
        input_ports = block.inPort
        output_ports = block.outPort
        
        for index_port, port in enumerate(input_ports):
          port_ID, port_Name, _, port_Type, _ = port
          
          if(out_ID == port_ID):
            if(con_sig_type != port_Type):
              print(connector.label + ' of ' + con_sig_type + ' is connected to ' + port_Name + ' of ' +  block.label +  ' of ' + port_Type)
              connector.mode = MODE[3]
              error_count += 1
              block.update_inport_mode(index_port, MODE[3])
              break
          pass
      
        for index_port, port in enumerate(output_ports):
          port_ID, port_Name, _, port_Type, _ = port
          
          if(in_ID == port_ID):
            if(con_sig_type != port_Type):
              print(connector.label + ' of ' + con_sig_type + ' is connected to ' + port_Name + ' of ' +  block.label +  ' of ' + port_Type)
              connector.mode = MODE[3]
              error_count += 1
              block.update_outport_mode(index_port, MODE[3])
              break
          pass

    print('------------------------------------------------')
      
    print('Unique Port Input Report:')
    print('------------------------------------------------')
    
    for index_block, block in enumerate(self.blocks):
      input_ports = block.inPort
        
      for index_port, inPort in enumerate(input_ports):
        port_ID, port_Name, _, _, _ = inPort
        NoI = 0
        for connector in self.connectors:
          if connector.outPortID == port_ID:
            NoI += 1
            pass
        if(NoI > 1):
          print(port_Name + ' of ' + block.label + ' has ' + str(NoI) + ' inputs')
          for connector in self.connectors:
            if connector.outPortID == port_ID:
              connector.mode = MODE[3]
              error_count += 1
          block.update_inport_mode(index_port, MODE[3])
          pass
     
    print('------------------------------------------------')
      
    print('None Feedback Loop Report:')
    print('------------------------------------------------')
    
    for conn in self.connectors:
        
      input_port, output_port = self.find_ends_connector(conn)

      if (input_port[0] == output_port[0]) and\
         (input_port[1] != None and output_port[1] != None):
        print(conn.label + ' forms a feedback from ' + input_port[1] +\
              ' to ' + output_port[1] + ' of ' + input_port[0])
        conn.mode = MODE[3]
        error_count += 1
        pass
    pass
    print('------------------------------------------------')

    return error_count

  # } verifyDiagram func
  

  # find_ends_connector func: function handle to prepare block pop up menu
  # {
  def find_ends_connector(self, conn, direction = 0):
    """
    Internal function.
    
    Finds terminations of a connector at given direction
    
    input:
        conn = connector to investigate
        direction = 0 -> find terminals at both input and output
                    -1 -> terminal at input
                    +1 terminal at output
    output:
        [input_port, output_port] = 
        each port is a list of [block label, port name, port ID]
        where block name is the name of the block connected to the terminal. It 
        is '0' if the connector end is float. Port name and ID refer to the port 
        connected to the terminal. They are both 'None' if terminal is float.
    """
    
    input_port = ['0', None, None]
    output_port = ['0', None, None]
    
    if(direction == 0):
      input_port, _ = self.find_ends_connector(conn, direction = -1)
      _, output_port = self.find_ends_connector(conn, direction = +1)
    
    elif(direction == -1):
      inport = conn.inPortID
      output_port = []
      
      if inport == '0':
        input_port = ['0', None, None]
    
      elif inport[0:4] == 'Node':          
        Flag = False
        
        for node in self.nodes:
          outID = [P[0] for P in node.outPort]
          
          if(Flag == True):
            break
        
          if (outID[0] == inport) or (outID[1] == inport):            
            for con in self.connectors:
              if con.outPortID == node.inPort[0]:
                 input_port, _ = self.find_ends_connector(con, direction = -1)
                 Flag = True
                 break
             
              pass
            pass
        
          pass
      
        pass
    
      elif inport[0:5] == 'Block':
        
        block_name = inport.split('-')[0]
        
        for block in self.blocks:
          if block.label == block_name:
             break
          pass

        output_ports = block.outPort
        for port in output_ports:
          port_ID, port_Name, _, _, _ = port
          if(conn.inPortID == port_ID):
            input_port = [block.label, port_Name, port_ID] 
            break
          pass
        pass
    
    elif(direction == +1):
      input_port = []
      outport = conn.outPortID

      if outport == '0':
        output_port = ['0', None, None]
    
      elif outport[0:4] == 'Node':          
        Flag = False
        
        for node in self.nodes:
          inID = node.inPort[0]
          
          if(Flag == True):
            break
        
          if (inID == outport):
            outID = [P[0] for P in node.outPort]

            for con in self.connectors:
              if (con.inPortID == outID[0]) or (con.inPortID == outID[1]):
                 _, output_port = self.find_ends_connector(con, direction = +1)
                 Flag = True
                 break
             
              pass
            pass
        
          pass
      
        pass
    
      elif outport[0:5] == 'Block':
        
        block_name = outport.split('-')[0]
        
        for block in self.blocks:
          if block.label == block_name:
             break
          pass

        input_ports = block.inPort
        for port in input_ports:
          port_ID, port_Name, _, _, _ = port
          if(conn.outPortID == port_ID):
            output_port = [block.label, port_Name, port_ID] 
            break
          pass
        pass

    return input_port, output_port

    pass
  # } find_ends_connector func
    

  # perepareBlockMenu func: function handle to prepare block pop up menu
  # {
  def perepareBlockMenu(self):
    """
    Internal function.
    
    Prepares block pop up menu entries based on available types of blocks
    
    input: none
    output: none
    """
    
    self.std.Print('Loading block types from the file', fg, bg, style, src)
    tree = ET.parse(self.__block_types_file)
    root = tree.getroot()
    blockname = root.attrib["name"]    
    type_root = root.findall("type")
    
    self.__block_type_name = []
    block_type_file = []
    
    for block_type in type_root:
        self.__block_type_name.append(block_type.attrib["name"])
        block_type_file.append(block_type.text)
        pass
    
    self.__block_type_file = dict(zip(self.__block_type_name, block_type_file))
    self.__om_variable = tk.StringVar()
    self.__om_variable.set(self.__block_type_name[0])
    self.__block_type_menu = tk.OptionMenu(self.container, self.__om_variable,\
                                           *self.__block_type_name, command=self.setBlockType)
    
    self.block_xml_file = self.__block_type_file[self.__om_variable.get()]
#    self.__block_type_menu(width=20)
    
    
#    self.__block_type_popup = Menu(self.container, tearoff=0)
#    
#    for block_title in self.__block_type_name:
#        self.__block_type_popup.add_radiobutton(label=block_title, command=self.setBlockType)
    pass
  # } perepareBlockMenu func
  
  
  # setBlockType func: function handle to set the block type
  # {
  def setBlockType(self, event):
    """Internal function.
    
    Sets the block type based on the pop up menu selection
    
    input:
        event = widget information
    output: none
    """        
        
    self.std.Print('Block type is set to ' + self.__om_variable.get(), fg, bg, style, src)

    self.__block_type_menu.place_forget()
    
    self.block_xml_file = self.__block_type_file[self.__om_variable.get()]
  # } setBlockType func


  # editProperty func: function handle to edit property of a block
  # {
  def editProperty(self, event):
    """Internal function.
    
    Edits property of a block
    
    input:
        event = coordinate of the cursor
    output: none
    """

    x, y = self.container.convert_coords((event.x, event.y), snap_mode=False)

    nodeOrder, connectorOrder, blockOrder = self.getSelectedOrder(x, y)

    maxOrder = max(blockOrder)
    self.__tmpObj = []
    for obj in self.blocks:
      if obj.shapeorder == maxOrder:
        self.__tmpObj = obj
        break
      pass

    if self.__tmpObj == []:
      return

    self.std.Print('Editing block property', fg, bg, style, src)

    properties = self.__tmpObj.properties

    dlg = dlgeditproperty.DlgEditProperty(master=self.__master, block_name=self.__tmpObj.block_name,\
                                          blocklabel=self.__tmpObj.label ,properties=properties, std=self.std)

    self.__tmpObj.parameters = dlg.returnedValues
    
  # } editProperty func

  # readDiagram func: function handle to read the diagram from a file
  # {
  def readDiagram(self):
    """
    Reads the diagram from a file
    
    input: none
    output: none
    """

    self.std.Print('Reading diagram from ' + str(DIAG_FILE_NAME), fg, bg, style, src)

    self.newDiagram()

    fileHandle = open(DIAG_FILE_NAME,'rb')
    data = pickle.load(fileHandle)    
    fileHandle.close()
    
    canvasData = data[0]

    grfs_data = data[1: ]

    node = []
    block = []
    connector = []

    for Obj in grfs_data[0]:
      Obj.sheetCanvas = self.container
      Obj.draw()
      cls_name = Obj.__class__.__name__
      if cls_name == 'GrfNode':
        Obj.update_color()
        Obj.update_brush()        
        Obj.update_mode()        
        Obj.update_bbox()
        node.append(Obj)
        pass
      elif cls_name == 'GrfBlock':
        Obj.update_color()
        Obj.update_brush()        
        Obj.update_mode()        
        Obj.update_bbox()
        Obj.update_font()
        Obj.update_geometry()
        block.append(Obj)
        pass
      elif cls_name == 'GrfConnector':
        Obj.update_color()
        Obj.update_brush()        
        Obj.update_mode()        
        Obj.update_arrow()
        Obj.update_bbox()
        connector.append(Obj)
        pass
      pass

    self.nodes = node
    self.blocks = block
    self.connectors = connector

    grfnode.GrfNode.ObjOrder = canvasData[0]

    self.draw_objects()

  # } readDiagram func

  # writeDiagram func: function handle to write the diagram into a file
  # {
  def writeDiagram(self):
    """
    Writes the diagram into a file
    
    input: none
    output: none
    """

    self.std.Print('Writing diagram to ' + str(DIAG_FILE_NAME), fg, bg, style, src)

    grfs_data = []
    for Obj in self.nodes:
      grfs_data.append(Obj)
      pass
    for Obj in self.blocks:
      grfs_data.append(Obj)
      pass
    for Obj in self.connectors:
      grfs_data.append(Obj)
      pass
    
    for Obj in grfs_data:
      Obj.sheetCanvas = None
      pass

    canvasData = list([grfnode.GrfNode.ObjOrder])
    data = [canvasData, grfs_data]
    fileHandle = open(DIAG_FILE_NAME,'wb')
    pickle.dump(data, fileHandle)    
    fileHandle.close()
    
    for Obj in grfs_data:
      Obj.sheetCanvas = self.container
      pass
  # } writeDiagram func


  # newDiagram func: function handle to clear existing diagram
  # {
  def newDiagram(self):
    """
    Clears the canvas and creates a new file
    
    input: none
    output: none
    """
    
    self.std.Print('Cleaning diagram canvas', fg, bg, style, src)

    for Obj in self.nodes:
        Obj.erase()
        pass
    self.nodes = []
    
    for Obj in self.blocks:
        Obj.erase()
        pass
    self.blocks = []

    for Obj in self.connectors:
        Obj.erase()
        pass
    self.connectors = []

    self.draw_objects()
  # } newDiagram func


  # readDiagram func: function handle to select block type
  # {
  def blockSelection(self, event):
    """
    Internal function.
    
    displays block type pop up menu
    
    input:
        event = coordinates of the cursor
    output: none
    """
    
    self.std.Print('Block selection popup menu', fg, bg, style, src)

#    try:
#        self.__block_type_menu.place(x=event.x, y=event.y)    
#        self.__block_type_popup.tk_popup(event.x_root, event.y_root, 0)
#    finally:
#        pass
#        self.__block_type_popup.grab_release()

    self.__block_type_menu.place(x=event.x, y=event.y)    

  # } blockSelection func


  # windowChange func: function handle when window size is changed
  # {
  def windowChange(self, event):
    """
    Internal function.
    
    Message handler dealing with window change. It changes the size of 
    the canvas and scrollbars accordingly
    
    input:
        event = new windows width and height
    output: none
    """

    
    self.__master.update()
    winWidth = self.__master.winfo_width()
    winHeight = self.__master.winfo_height()
#    print('Windows = {0}, {1}'.format(winWidth, winHeight))
    
    self.container.update()
#    canvasWidth = self.container.winfo_width()
#    canvasHeight = self.container.winfo_height()
#    print('Canvas = {0}, {1}'.format(canvasWidth, canvasHeight))
    
    regionSize = self.bbox
    regionWidth = abs(regionSize[2] - regionSize[0])
    regionHeight = abs(regionSize[3] - regionSize[1])
#    print('Region = {0}, {1}'.format(regionWidth, regionHeight))
    
    maxWidth = max(regionWidth, 0)
    maxHeight = max(regionHeight, 0)
#    print('Maximum = {0}, {1}'.format(maxHeight, maxWidth))

    self.__xscrollbar.update()
#    marginWidth = self.__yscrollbar.winfo_width()
#    marginHeight = self.__xscrollbar.winfo_height()
#    print('Scrollbar = {0}, {1}'.format(marginHeight, marginWidth))
    
    
    self.container.config(width=int(min(maxWidth, abs(winWidth - WINDOW_MARGIN))))
    self.container.config(height=int(min(maxHeight, abs(winHeight - WINDOW_MARGIN))))
#    print(min(maxWidth, abs(winWidth - WINDOW_MARGIN)))
#    if(maxWidth <= (winWidth - WINDOW_MARGIN)):
#        self.container.config(width=min(maxWidth, abs(winWidth - WINDOW_MARGIN)))
#        pass
    
#    if(maxHeight <= (winHeight - WINDOW_MARGIN)):
#    self.container.config(height = 100)
#        pass
    
    blodiatorcore.BlodiatorCore.draw_objects(self)
    self.container.update_region(self.bbox)
    pass
    
#    if maxWidth <= (winWidth - 25)
  # } draw_objects func
 
  
  # draw_objects func: draw the objects
  # {
  def draw_objects(self):
    """
    Internal function.
    
    It is called when the objects are redrawn. The code adjusts the size of the 
    canvas and scrollbars.
    
    input: none
    output: none
    """
        
    blodiatorcore.BlodiatorCore.draw_objects(self)
    
    self.windowChange(None)
    
    self.__xscrollbar.config(command=self.container.xview)
    self.__yscrollbar.config(command=self.container.yview)
  # } draw_objects func


  # keyPressed func: function handle for wheel change
  # {
  def mouseWheel(self, event):
    """
    Internal function.
    
    Not used
    
    input:
        event = pressed key
    output: none
    """
    
    pass
        
#    self.container.grid_zoom_org = 0, 0
#    scale = self.container.grid_scale
#    
#    if event.delta > 0:
#        scale = 2.0
#        pass
#    else:
#        scale = 0.5
#        pass
#    self.container.grid_scale = scale
  # } mouseWheel func


  # mouseWheelDrag func: function handle for draging mouse while whwwl is pressed
  # {
  def mouseWheelDrag(self,event):
    """
    Internal function.
    
    Message handler to deal with the mouse wheel draging
    
    input:
        event = coordinates of mouse cursor
    output: none
    """

    if (self._y - event.y < 0): self.container.yview("scroll", -1, "units")
    elif (self._y - event.y > 0): self.container.yview("scroll", 1, "units")
    if (self._x - event.x < 0): self.container.xview("scroll", -1, "units")
    elif (self._x - event.x > 0): self.container.xview("scroll", 1, "units")
    self._x = event.x
    self._y = event.y
  # } mouseWheelDrag func
  

  # keyPressed func: function handle for wheel pressed
  # {
  def mouseWheelPressed(self, event):
    """
    Internal function.
    
    Message handler to deal with the mouse wheel pressed
    
    input:
        event = coordinate of the mouse coordinate
    output: none
    """

    self.container.config(cursor=CURSOR['scroll'])
    self._y = event.y
    self._x = event.x
  # } mouseWheelPressed func

  # keyPressed func: function handle for wheel released
  # {
  def mouseWheelReleased(self, event):
    """
    Internal functions.
    
    Message handler to deal with the mouse wheel released
    
    input: 
        event = widget information
    output: none
    """

    self.container.config(cursor=CURSOR['idle'])
  # } mouseWheelPressed func


  # zoom_all func: function for zooming all
  # {
  def zoom_all(self):
    """
    Internal function.
    
    Not used
    
    input: none
    output: none
    """

    self.std.Print('Zooming all; not active', fg, bg, style, src)
    pass

  # } zoom_all func

  # __loadproperties func: function for loading node/connector/block properties
  # {
  def __loadproperties(self):
    """
    Internal function.
    
    Loads node/connector/block properties from corresponding xml files
    
    input: none
    output: none
    """


    self.std.Print('Loading node properties from the file', fg, bg, style, src)
    tree = ET.parse(self.__node_file)
    root = tree.getroot()
    blockname = root.attrib["name"]    
    color_root = root.find("color")
    color_normal = color_root.find("normal").text.split(',')
    color_disabled = color_root.find("disabled").text.split(',')
    color_selected = color_root.find("selected").text.split(',')
    color_erroneous = color_root.find("erroneous").text.split(',')
    colorList = (tuple(color_normal), tuple(color_disabled), tuple(color_selected), tuple(color_erroneous))
    colorset = dict(zip(MODE, colorList))    
    brush_root = root.find("brush")
    brush_normal = [float(x) for x in brush_root.find("normal").text.split(',')]
    brush_disabled = [float(x) for x in brush_root.find("disabled").text.split(',')]
    brush_selected = [float(x) for x in brush_root.find("selected").text.split(',')]
    brush_erroneous = [float(x) for x in brush_root.find("erroneous").text.split(',')]
    brushList = ((brush_normal, []), (brush_disabled, []), (brush_selected, []), (brush_erroneous, []))
    brushset = dict(zip(MODE, brushList)) 
    size = int(root.find("size").text)    
    type_root = root.find("type")
    type_none = type_root.find("none").text
    type_logical = type_root.find("logical").text
    type_electrical = type_root.find("electrical").text
    type_optical = type_root.find("optical").text
    typeList = (type_none, type_logical, type_electrical, type_optical)
    typeset = dict(zip(SIG_TYPE, typeList))
    self.__node_property = [colorset, brushset, size, typeset]


    self.std.Print('Loading connector properties from the file', fg, bg, style, src)
    tree = ET.parse(self.__connector_file)
    root = tree.getroot()
    blockname = root.attrib["name"]    
    color_root = root.find("color")
    color_normal = color_root.find("normal").text.split(',')
    color_disabled = color_root.find("disabled").text.split(',')
    color_selected = color_root.find("selected").text.split(',')
    color_erroneous = color_root.find("erroneous").text.split(',')
    colorList = (tuple(color_normal), tuple(color_disabled), tuple(color_selected), tuple(color_erroneous))
    colorset = dict(zip(MODE, colorList))    
    brush_root = root.find("brush")
    brush_normal = [float(x) for x in brush_root.find("normal").text.split(',')]
    brush_disabled = [float(x) for x in brush_root.find("disabled").text.split(',')]
    brush_selected = [float(x) for x in brush_root.find("selected").text.split(',')]
    brush_erroneous = [float(x) for x in brush_root.find("erroneous").text.split(',')]
    brushList = ((brush_normal[0], brush_normal[1:]), (brush_disabled[0], brush_disabled[1:]),\
                 (brush_selected[0], brush_selected[1:]), (brush_erroneous[0], brush_erroneous[1:]))
    brushset = dict(zip(MODE, brushList))
    arrow = tuple([int(x) for x in root.find("arrow").text.split(',')])
    type_root = root.find("type")
    type_none = type_root.find("none").text
    type_logical = type_root.find("logical").text
    type_electrical = type_root.find("electrical").text
    type_optical = type_root.find("optical").text
    typeList = (type_none, type_logical, type_electrical, type_optical)
    typeset = dict(zip(SIG_TYPE, typeList))
    self.__connector_property = [colorset, brushset, arrow, typeset]
    

    self.std.Print('Loading block properties from the file', fg, bg, style, src)
    tree = ET.parse(self.__block_file)
    root = tree.getroot()
    blockname = root.attrib["name"]    
    color_root = root.find("color")
    color_normal = color_root.find("normal").text.split(',')
    color_disabled = color_root.find("disabled").text.split(',')
    color_selected = color_root.find("selected").text.split(',')
    color_erroneous = color_root.find("erroneous").text.split(',')
    colorList = (tuple(color_normal), tuple(color_disabled), tuple(color_selected), tuple(color_erroneous))
    colorset = dict(zip(MODE, colorList))
    brush_root = root.find("brush")
    brush_normal = [float(x) for x in brush_root.find("normal").text.split(',')]
    brush_disabled = [float(x) for x in brush_root.find("disabled").text.split(',')]
    brush_selected = [float(x) for x in brush_root.find("selected").text.split(',')]
    brush_erroneous = [float(x) for x in brush_root.find("erroneous").text.split(',')]
    brushList = ((brush_normal, []), (brush_disabled, []), (brush_selected, []), (brush_erroneous, []))
    brushset = dict(zip(MODE, brushList))
    font_root = root.find("font")
    block_font_size = int(font_root.find("block-font-size").text)
    port_font_size = int(font_root.find("port-font-size").text)
    font_name = font_root.find("font-name").text
    font_style = font_root.find("font-style").text
    font_prop = tuple([block_font_size, port_font_size, font_name, font_style])
    geometry_root = root.find("geometry")
    e2p_horz_marg = int(geometry_root.find("edge-2-port-horizontal-margin").text)
    e2p_vert_marg = int(geometry_root.find("edge-2-port-vertical-margin").text)
    p2l_horz_marg = int(geometry_root.find("port-2-label-horizontal-margin").text)
    p2p_gap = int(geometry_root.find("port-2-port-gap").text)
    p2n_gap = int(geometry_root.find("port-2-name-gap").text)
    port_size = int(geometry_root.find("port-size").text)
    l2n_gap = int(geometry_root.find("label-2-name-gap").text)
    geo_prop = tuple([e2p_horz_marg, e2p_vert_marg, p2l_horz_marg, p2p_gap, p2n_gap, port_size, l2n_gap])
    type_root = root.find("type")
    type_none = type_root.find("none").text
    type_logical = type_root.find("logical").text
    type_electrical = type_root.find("electrical").text
    type_optical = type_root.find("optical").text
    typeList = (type_none, type_logical, type_electrical, type_optical)
    typeset = dict(zip(SIG_TYPE, typeList))
    self.__block_property = [colorset, brushset, font_prop, geo_prop, typeset]

    pass
  # } __loadproperties func


  # close_popup_menu func: function to close pop up menus
  # {
  def close_popup_menu(self):
    """
    Intenal function.
    
    Closes block type pop up menu
    
    input: none
    output: none
    """
    
    self.__block_type_menu.place_forget()
    pass
  # } close_popup_menu func
  # < class functions section >
  
  
  # < getter and setter functions section >
  # node_property getter func: node property getter
  # {
  @property
  def node_property(self):
    """
    Class property getter: node property
    """

    return self.__node_property
  # } node_property setter func

  # connector_property getter func: connector property getter
  # {
  @property
  def connector_property(self):
    """
    Class property getter: connector property
    """
    
#    print(self.__connector_property)

    return self.__connector_property
  # } connector_property setter func

  # block_property getter func: connector property getter
  # {
  @property
  def block_property(self):
    """
    Class property getter: block property
    """

    return self.__block_property
  # } block_property setter func

  # < getter and setter functions section >

# } BlodiatorBase class


# main func: contains code to test BlodiatorBase class
# {
def main():
  CT = coloredtext.ColoredText()

  CT.Print('Starting Blodiator', fg, bg, style, 'Root: ')

  root = tk.Tk()
  root.geometry("{0}x{1}".format(WIDTH + WINDOW_MARGIN, HEIGHT + WINDOW_MARGIN))
  root.title('Blodiator Base Test Bench')
  TestApp = BlodiatorBase(master=root, std=CT)

  root.mainloop()

  CT.Print('Closing Blodiator', fg, bg, style, 'Root: ')  
  pass
# } main func


if __name__ == '__main__':
  main()
