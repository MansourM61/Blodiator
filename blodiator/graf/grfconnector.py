'''
********************************************************************************

Python Script: grfconnector Module
Writter: Mojtaba Mansour Abadi
Date: 7 February 2019

This Python script is compatible with Python 3.x.
The script is used to define GrfConnector class the connector in
Blodiator. This class is a child of GrfConnectorCore class.


GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:
    
Ver 0.0.32: 28 June 2019;
             first code

Ver 0.0.36: 3 July 2019;
             1- node/connector loading properties are added.
            
********************************************************************************
'''


import tkinter as tk

from ..etc import cntsheetcanavs
from ..etc import coloredtext
from . import grfconnectorcore
from . import grfobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GrfConnector: '


#################################################
DEF_NAME = 'connector'  # default name
CAT = 'graph'  # default category
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
IN_PORT = ('0', (30, 30), None, None)  # default input port
OUT_PORT = ('0', (200, 100), None, None)  # default output port
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfConnector class: this is the connector class for blockdiagram objects
# {
class GrfConnector(grfconnectorcore.GrfConnectorCore):
  """
  Connector item in the Blodiator.
  
  Define an instance of 'GrfConnector' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the block
      label = item label
      inPort = list containing information about input ports of the item
      outPort = list containing information about output ports of the item
      cat = a string showing the category of the block
      con_type = connection type: ('none', 'logical', 'electrical', 'optical')
      color_type = a tuple containing colors for different coneection type
      mode = state of the block: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class controls higher level aspects of a connector item.
  """
  
  version = '0.0.36'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME,
               mode=MODE[0], inPort=IN_PORT, outPort=OUT_PORT,
               color_type=CON_COLOR, con_type=SIG_TYPE[0], std=None):
    """
    Construct a GrfConnector
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the block
        label = item label
        inPort = list containing information about input ports of the item
        outPort = list containing information about output ports of the item
        cat = a string showing the category of the block
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
      
    self.std.Print('Initialising GrfConnector', fg, bg, style, src)

    self.__con_type = con_type

    super(GrfConnector, self).__init__(sheetCanvas=sheetCanvas, cat=cat, label=label,
                                       mode=mode, inPort=inPort, outPort=outPort,
                                       con_type=con_type, color_type=color_type, std=std)
    
    color_set = self.colorset
    self.color_type = color_type
    color_set[MODE[0]] = (self.color_type[self.con_type], self.color_type[self.con_type])   
    self.colorset = color_set
  # } __init__ func


  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GrfConnector, self).__repr__()

    txt += '; signal type' + self.__con_type  # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GrfConnector, self).__repr__()

    txt += '; signal type' + self.__con_type  # generate formatted text
    return txt
  # } __str__ func
  # < inherited functions section >

  # < class functions section >  
  # < class functions section >

  # < getter and setter functions section >
  # < getter and setter functions section >
# } GrfConnector class


# main func: contains code to test GrfConnector class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("600x600")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=600, height=600)
  canvas.pack()
  
  obj = None

  obj = GrfConnector(sheetCanvas=canvas, label='graph1', std=CT)
  obj.draw()
  obj.inPortPos = (580, 400)
  obj.outPortPos = (20, 402)
  obj.mode = MODE[0]
  obj.con_type = SIG_TYPE[1]

  A = [obj]

  obj.color_type = CON_COLOR

  obj = GrfConnector(sheetCanvas=canvas, label='graph2', std=CT)
  obj.draw()
  obj.inPortPos = (20, 202)
  obj.outPortPos = (580, 200)
  obj.mode = MODE[0]
  obj.con_type = SIG_TYPE[2]
  
  A.append(obj)

  canvas.create_rectangle((30, 30, 200, 100))

  obj.color_type = CON_COLOR
  
#  A[1].color_type = CON_COLOR

#  print((20, 402) in obj)
  
#  print(obj)
  
#  print(obj1.brushset)
  
#  print(obj.bbox)
##  for i in range(0, 20):
##    Pos = obj.outPortPos
##    obj.outPortPos = (Pos[0], Pos[1] + 1)
  
  for obj in A:
       obj.mode = MODE[0]

  for obj in A:
        print(obj.colorset)


  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
