'''
********************************************************************************

Python Script: grfnode Module
Writter: Mojtaba Mansour Abadi
Date: 7 Feburary 2019

This Python script is compatible with Python 3.x.
The script is used to define GrfNode class the node in
Blodiator. This class is a child of GrfNodeCore class.


GrfNode          GrfConnector        GrfBlock
|                |                   |
|                |                   |
GrfNodeCore      GrfConnectorCore    GrfBlockCore
|                |                   |
|                |                   |
|_____________GrfObject______________|


History:
    
Ver 0.0.33: 28 January 2019;
             first code

Ver 0.0.36: 3 July 2019;
             1- node/connector loading properties are added.
            
********************************************************************************
'''


import tkinter as tk

from ..etc import cntsheetcanavs
from ..etc import coloredtext
from . import grfnodecore


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GrfNode: '


#################################################
DEF_NAME = 'node'  # default name
CENTER = (300, 300)  # default center coordinate
SIZE = 10  # default size
CAT = 'graph'  # default category
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
IN_PORT = ['0', None, None, None]  # default input port
OUT_PORT = [ ['0', None, None, None], ['0', None, None, None] ]  # default output port
SIG_TYPE = ('none', 'logical', 'electrical', 'optical')  # available signal type
CON_COLOR = {'none': 'black', 'logical': 'blue', 'electrical': 'green', 'optical': 'red'}  # connector colour
#################################################


# GrfNode class: this is the node class for blockdiagram objects
# {
class GrfNode(grfnodecore.GrfNodeCore):
  """
  Node item in the Blodiator.
  
  Define an instance of 'GrfNode' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the block
      label = item label
      size = size of the node
      inPort = list containing information about input ports of the item
      outPort = list containing information about output ports of the item
      cat = a string showing the category of the block
      con_type = connection type: ('none', 'logical', 'electrical', 'optical')
      color_type = a tuple containing colors for different coneection type
      mode = state of the block: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class controls higher level aspects of a node item.
  """
 
  version = '0.0.36'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, cat=CAT, label=DEF_NAME,
               center=CENTER, size=SIZE, mode=MODE[0], color_type=CON_COLOR,
               inPort=IN_PORT, outPos=OUT_PORT, con_type=SIG_TYPE[0], std=None):
    """
    Construct a GrfNode
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the block
        label = item label
        size = size of the node
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

    self.std.Print('Initialising GrfNode', fg, bg, style, src)

    super(GrfNode, self).__init__(sheetCanvas=sheetCanvas, cat=cat, label=label, center=center,
                                  size=size, con_type=con_type, color_type=color_type,
                                  mode=mode, inPort=IN_PORT, outPort=OUT_PORT, std=std)
    
    color_set = self.colorset
    self.color_type = CON_COLOR
    color_set[MODE[0]] = (self.color_type[self.con_type], self.color_type[self.con_type])   
    self.colorset = color_set
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GrfNode, self).__repr__()

    txt += '; signal type' + self.con_type  # generate formatted text
    return txt
  # } __repr__ func

  # __str__ func: str dunar
  # {
  def __str__(self):
    """
    Class str dunar function.
    """
    
    txt = super(GrfNode, self).__str__()

    txt += '; signal type' + self.con_type  # generate formatted text
    return txt
  # } __str__ func

  # < class functions section >

  # < getter and setter functions section >
  # < getter and setter functions section >

# } GrfNode class


# main func: contains code to test GrfNode class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("600x600")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=600, height=600)
  canvas.pack()

  obj = GrfNode(sheetCanvas=canvas, label='graph', std=CT)

  obj.draw()

#  CT.Print(repr(obj))

  CT.Print('\n')

  obj.mode = MODE[2]

 # CT.Print(repr(obj))

  obj.center = (100, 100)

  obj.mode = MODE[0]
  
  obj.center = (300, 100)
  
  print(obj.bbox)

  obj.con_type = SIG_TYPE[0]

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
