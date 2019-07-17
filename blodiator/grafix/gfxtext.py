'''
********************************************************************************

Python Script: gfxtext Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxText class the text block in
Blodiator. This module is a wrapper for tk.Canvas.create_line command.


GfxCircle   GfxPies    GfxSquare       GfxLine     GfxPolygon   GfxImage     GfxText
|           |          |               |           |            |            |
|           |          |               |           |            |            |
GfxOval     GfxArc     GfxRectangle    |           |            |            |
|           |          |               |           |            |            |
|           |          |               |           |            |            |
|___________|__________|___________GfxObject_______|____________|____________|


Histoty:
    
Ver 0.0.5: 29 January 2019;
             first code

Ver 0.0.6: 29 January 2019;
             1- The class is defined based on the new GfxObject Ver 0.0.6.
             2- 'center' and 'size' are adjustable.

********************************************************************************
'''


import tkinter as tk
from tkinter import font as tkf

from ..etc import coloredtext
from . import gfxobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxText: '


#################################################
DEF_NAME = 'text'  # default name
CENTER = (20, 100)  # default center coordinate
CAT = 'primitive'  # default category
COLOR_NORMAL = ('black', 'white')  # default color for normal state
COLOR_DISABLED = ('pink', 'blue')  # default color for disabled state
COLOR_SELECTED = ('red', 'green')  # default color for selected state
COLOR_ERRONEOUS = ('yellow', 'cyan')  # default color for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
FONT_NAME = 'Helvetica' # default font name
FONT_SIZE = 36  # default font size
FONT_STYLE = 'bold'  # default font style
ANCHOR = tk.CENTER  # default text anchor
JUSTIFY = tk.CENTER  # default text justify
TEXT = 'Text'  # default text
#################################################


# GfxText class: this is the text class
# {
class GfxText(gfxobject.GfxObject):
  """
  Draws primitive shape of text.
  
  Define an instance of 'GfxText' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the rectangle
      font = tuple containing font properties (font name, font size, font style)
      cat = a string showing the category of the rectangle
      text = string to be displayed
      text_adj = tuple containing the text adjustment properties (anchor, justification)
      mode = state of the rectangle: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing a text
  in Blodiator.
  """
  version = '0.0.6'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, center=CENTER,
               cat=CAT, font=(FONT_NAME, FONT_SIZE, FONT_STYLE),
               text=TEXT, text_adj=(ANCHOR, JUSTIFY), mode=MODE[0], std=None):
    """
    Construct a GfxText
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the rectangle
        font = tuple containing font properties (font name, font size, font style)
        text = string to be displayed
        cat = a string showing the category of the rectangle
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        text_adj = tuple containing the text adjustment properties (anchor, justification)
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
    
    self.__fontName = font[0]
    self.__fontSize = font[1]
    self.__fontStyle = font[2]

    self.__text = text

    width = FONT_SIZE * len(text)
    height = FONT_SIZE

    self.__anchor = text_adj[0]
    self.__justify = text_adj[1]    
    
    super(GfxText, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center, size=(width, height),
                                  cat=cat, mode=mode, std=std)  # initialise the parent
  # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GfxText, self).__repr__()

    txt += '; font (name, size, style) = ({0}, {1}, {2});'\
           ' text = {3}; text adjustment (anchor, justify) = ({4}, {5})'.\
           format(self.__fontName, self.__fontSize, self.__fontStyle, \
                  self.__text, self.__anchor, self.__justify)  # generate formatted text

    return txt
  # } __repr__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the text on the canvas
    
    input: none
    output: none
    """
    
    font = tkf.Font(family=self.__fontName, size=self.__fontSize, weight=self.__fontStyle)

    fg = self.color[0]

    self.sheetCanvas.create_text(self.center, anchor=self.__anchor,
                                 justify=self.__justify, font=self.font,
                                 text=self.__text, fill=fg, tags=self.tag)
  # } draw func

  # update_color func: update the color
  # {
  def update_color(self):
    """
    Updates the text color set (text colors for all different modes)
    
    input: none
    output: none
    """
    
    super(GfxText, self).update_color()

    fg = self.color[0]

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, fill=fg)  # set foreground color property
  # } size setter func  

  # update_text func: update the text
  # {
  def update_text(self):
    """
    Updates the text string
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, text=self.text)  # set foreground color property
  # } update_text func  

  # update_joint func: update the font
  # {
  def update_font(self):
    """
    Updates the text font properties (font name, font size, font style)
    
    input: none
    output: none
    """
    
    font = tkf.Font(family=self.__fontName, size=self.__fontSize, weight=self.__fontStyle)

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, font=font)
  # } update_joint func  

  # update_adjustment func: update the adjustment
  # {
  def update_adjustment(self):
    """
    Updates the text adjustment properties (anchor, justification)
    
    input: none
    output: none
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, anchor=self.__anchor)
    self.sheetCanvas.itemconfig(item, justify=self.__justify)
  # } update_adjustment func

  # update_center func: update center of the object
  # {
  def update_center(self):
    """
    Updates the shape center, left blank delibrately
    
    input: none
    output: none
    """
    
    pass    
  # } update_center func

  # update_line func: update line thickness and style of the object
  # {
  def update_brush(self):
    """
    Updates the shape brush set (line thickness and style for all different modes),
    left delibrately
    
    input: none
    output: none
    """
    
    pass
  # } update_line func

  # < class functions section >

  # < getter and setter functions section >
  # property: adjustment
  # anchor getter func: object adjustment getter
  # {
  @property
  def adjustment(self):
    """
    Class property getter: adjustment tuple (anchor, justification)
    """
    
    return self.__anchor, self.__justify
  # } adjustment getter func

  # adjustment setter func: object adjustment setter
  # {
  @adjustment.setter
  def adjustment(self, text_adj):
    """
    Class property setter: adjustment tuple (anchor, justification)
    """
    
    self.__anchor = text_adj[0]
    self.__justify = text_adj[1]    

    self.update_adjustment()
  # } adjustment setter func
  
  # property: font
  # font getter func: object font property getter
  # {
  @property
  def font(self):
    """
    Class property getter: font tuple (font name, font size, font style)
    """
    
    return self.__fontName, self.__fontSize, self.__fontStyle
  # } font getter func

  # font setter func: object font property setter
  # {
  @font.setter
  def font(self, font):
    """
    Class property setter: font tuple (font name, font size, font style)
    """
    
    self.__fontName = font[0]
    self.__fontSize = font[1]
    self.__fontStyle = font[2]

    self.update_font()
  # } font setter func

  # property: text
  # text getter func: object text getter
  # {
  @property
  def text(self):
    """
    Class property getter: text string
    """
    
    return self.__text
  # } text getter func

  # text setter func: object text setter
  # {
  @text.setter
  def text(self, text):
    """
    Class property setter: text string
    """
    
    self.__text = text

    self.update_text()
  # } text setter func

  # property: color set
  # colorset setter func: object color set setter
  # {
  @gfxobject.GfxObject.colorset.setter
  def colorset(self, colorset):
    """
    Class property setter: the text color set (outline and filling colors for all different modes)
    """
    
    gfxobject.GfxObject.colorset.fset(self, colorset)

    self.update_color()  # update the color
  # } colorset setter func

  # property: bbox
  # bbox getter func: bounding box line getter
  # {
  @gfxobject.GfxObject.bbox.getter
  def bbox(self):
    """
    Class property getter: bounding box
    """
    
    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    return self.sheetCanvas.bbox(item)
  # } bbox getter func

  # center setter func: object center coordinate setter
  # {
  @gfxobject.GfxObject.center.setter
  def center(self, center):
    """
    Class property setter: center
    """
    
    delX = center[0] - gfxobject.GfxObject.center.fget(self)[0]
    delY = center[1] - gfxobject.GfxObject.center.fget(self)[1]
    
    gfxobject.GfxObject.center.fset(self, center)

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.move(item, delX, delY)  # move the text
  # } center setter func
  # < getter and setter functions section >
# } GfxText class


# main func: contains code to test GfxText class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("500x500")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=500, height=500)
  canvas.pack()
  
  obj1 = GfxText(sheetCanvas=canvas, text='Hi', std=CT, tag='OBJ1', center=(200, 200))
  obj2 = GfxText(sheetCanvas=canvas, text='Bye\nSee You', std=CT, tag='OBJ2')

  obj1.draw()
  obj2.draw()
  
  canvas.create_rectangle(obj1.bbox)
##  canvas.create_rectangle(obj2.bbox)
##
##  obj1.center = (200, 200)
##  obj2.center = (200, 300)
##
##  CT.Print('\n')
##
##  canvas.create_rectangle(obj1.boundary)
##  canvas.create_rectangle(obj2.bbox)

  obj1.mode = MODE[2]

  print(repr(obj1))

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
