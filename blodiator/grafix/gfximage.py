'''
********************************************************************************

Python Script: gfximage Module
Writter: Mojtaba Mansour Abadi
Date: 29 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define GfxImage class the image block in
Blodiator. This module is a wrapper for tk.Canvas.create_image command.


GfxCircle   GfxPies    GfxSquare       GfxLine     GfxPolygon   GfxImage     GfxText
|           |          |               |           |            |            |
|           |          |               |           |            |            |
GfxOval     GfxArc     GfxRectangle    |           |            |            |
|           |          |               |           |            |            |
|           |          |               |           |            |            |
|___________|__________|___________GfxObject_______|____________|____________|


Histoty:
    
Ver 0.0.6: 29 January 2019;
             first code

********************************************************************************
'''


import tkinter as tk
from PIL import Image, ImageTk

from ..etc import coloredtext
from . import gfxobject


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'GfxImage: '


#################################################
DEF_NAME = 'image'  # default name
CENTER = (100, 100)  # default center coordinate
SIZE = (200, 200)  # default image size
CAT = 'primitive'  # default category
IMAGE_NORMAL = 'Pic_1.jpg'  # default image for normal state
IMAGE_DISABLED = 'Pic_2.jpg'  # default image for disabled state
IMAGE_SELECTED = 'Pic_3.jpg'  # default image for selected state
IMAGE_ERRONEOUS = 'Pic_4.jpg'  # default image for erroneous state
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
TRIMMING = ('crop', 'scale')  # image trimming technique
ANCHOR = tk.CENTER  # default image anchor
#################################################


# GfxImage class: this is the image class
# {
class GfxImage(gfxobject.GfxObject):
  """
  Draws primitive shape of image.
  
  Define an instance of 'GfxImage' with appropriate arguments:
      sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
      tag = a string used by tkinter to identify the image
      center = center of the image
      size = size of the image
      cat = a string showing the category of the image
      trim = image trimming technique: 'crop', 'scale'
      mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
      std = standard output which is an instance of 'ColoredText' class
      
  This class contains the required fundamental functions for drawing an image
  in Blodiator.
  """
  
  version = '0.0.6'  # version of the class

  # < class functions section >
  anchor = ANCHOR  
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, sheetCanvas=None, tag=DEF_NAME, center=CENTER,
               cat=CAT, size=SIZE, mode=MODE[0], trim=TRIMMING[0], std=None):
    """
    Construct a GfxImage
    
    input:
        sheetCanvas = an instance of the canvas. For Blodiator it is an instance of CntSheetCanvas
        tag = a string used by tkinter to identify the image
        center = center of the image
        size = size of the image
        cat = a string showing the category of the image
        trim = image trimming technique: 'crop', 'scale'
        mode = state of the object: 'normal', 'disabled', 'selected', 'erroneous'
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """
 
    imageList = [IMAGE_NORMAL, IMAGE_DISABLED, IMAGE_SELECTED, IMAGE_ERRONEOUS]

    self.__trimming = trim

    self.__imageset = dict(zip(MODE, imageList))

    iconList = [[], [], [], []]

    self.__iconset = dict(zip(MODE, iconList))

    super(GfxImage, self).__init__(sheetCanvas=sheetCanvas, tag=tag, center=center, size=size,
                                  cat=cat, mode=mode, std=std)  # initialise the parent

    for m in MODE:
      self.upload_icon(m)

    self.__icon = self.__iconset[mode]
 # } __init__ func

  # __repr__ func: repr dunar
  # {
  def __repr__(self):
    """
    Class repr dunar function.
    """
    
    txt = super(GfxImage, self).__repr__()

    txt += '; image = {0}'.\
           format(str(self.__imageset))  # generate formatted text

    return txt
  # } __repr__ func
  # < inherited functions section >

  # < class functions section >
  # draw func: draw the object
  # {
  def draw(self):
    """
    Draws the image on the canvas
    
    input: none
    output: none
    """
    
    self.sheetCanvas.create_image(self.center, anchor=GfxImage.anchor, image=self.__icon, tag=self.tag)
  # } draw func

  # update_icon func: update the icons
  # {
  def upload_icon(self, mode=MODE[0]):
    """
    Internal functions.
    
    Uploads the image into the canvas.
    
    input:
        mode =  state of the object: 'normal', 'disabled', 'selected', 'erroneous'
    output: none
    """
    
    self.__iconset[mode] = []
    
    image = Image.open(self.__imageset[mode])

    imgWidth, imgHeight = image.size
    centX, centY = imgWidth//2, imgHeight//2

    width, height = self.size

    if self.__trimming == 'crop':
      area = (centX - width//2, centY - height//2,
              centX + width//2, centY + height//2)

      modImage = image.crop(area)
    else:
      modImage = image.resize((width, height), Image.ANTIALIAS)

    self.__iconset[mode] = ImageTk.PhotoImage(modImage)      
  # } update_icon func  
  
  # update_line func: update line thickness and style of the object
  # {
  def update_brush(self):
    """
    Updates the image brush set (line thickness and style for all different modes),
    left blank delibrately
    
    input: none
    output: none
    """
    
    pass
  # } update_line func

  # update_color func: update color of the object
  # {
  def update_color(self):
    """
    Updates the image color set (outline and filling colors for all different modes),
    left blank delibrately
    
    input: none
    output: none
    """
    
    pass
  # } update_color func

  # update_image func: update the image
  # {
  def update_icon(self):
    """
    Updates the image in the canvas
    
    input: none
    output: none
    """
    
    self.__icon = (self.__iconset[self.mode])

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.itemconfig(item, image=self.__icon)  # set image property
  # } size setter func  

  # update_size func: update the size
  # {
  def update_size(self):
    """
    Updates the size of the image in the canvas
    
    input: none
    output: none
    """
    
    for m in MODE:
      self.upload_icon(m)
    self.update_icon()  # update the icon
  # } update_size func

  # update_center func: update center of the object
  # {
  def update_center(self):
    """
    Updates the image center, left blank delibrately
    
    input: none
    output: none
    """
    
    pass
  # } update_center func
  # < class functions section >
  
  # < getter and setter functions section >
  # property: trimming
  # trimming getter func: object trimming set getter
  # {
  @property
  def trimming(self):
    """
    Class property getter: trimming mode
    """
    
    return self.__trimming
  # } trimming getter func

  # trimming getter func: object trimming setter
  # {
  @trimming.setter
  def trimming(self, trimming):
    """
    Class property setter: trimming mode
    """
    
    self.__trimming = trimming

    self.upload_icon(self.mode)
    self.update_icon()  # update the icon
  # } trimming setter func

  # property: image set
  # imageset getter func: object image set getter
  # {
  @property
  def imageset(self):
    """
    Class property getter: image set (pictures for different modes)
    """
    
    return self.__imageset
  # } imageset getter func

  # imageset getter func: object image set setter
  # {
  @imageset.setter
  def imageset(self, imageset):
    """
    Class property setter: image set (pictures for different modes)
    """
    
    self.__imageset = imageset
    for m in MODE:
      self.upload_icon(m)
    self.update_icon()  # update the icon
  # } imageset setter func

  # property: center
  # center setter func: object center coordinate setter
  # {
  @gfxobject.GfxObject.center.setter
  def center(self, center):
    """
    Class property getter: center
    """
    
    delX = center[0] - gfxobject.GfxObject.center.fget(self)[0]
    delY = center[1] - gfxobject.GfxObject.center.fget(self)[1]
    
    gfxobject.GfxObject.center.fset(self, center)

    item = self.sheetCanvas.find_withtag(self.tag)  # retirieve object handle

    self.sheetCanvas.move(item, delX, delY)  # move the image
  # } center setter func

  # property: mode
  # mode setter func: object mode setter
  # {
  @gfxobject.GfxObject.mode.setter
  def mode(self, mode):
    """
    Class property setter: mode ('normal', 'disabled', 'selected', 'erroneous')
    """
    
    gfxobject.GfxObject.mode.fset(self, mode)

    self.update_icon()  # update the color
  # } mode setter func

  # property: size
  # size setter func: object size setter
  # {
  @gfxobject.GfxObject.size.setter
  def size(self, size):
    """
    Class property setter: size (width, height)
    """
    
    gfxobject.GfxObject.size.fset(self, size)
  # } size setter func
  # < getter and setter functions section >
# } GfxLine class


# main func: contains code to test GfxImage class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("500x500")
  root.title('Sheet Test Bench')

  canvas = tk.Canvas(root, width=500, height=500)
  canvas.pack()
  
  obj = GfxImage(sheetCanvas=canvas, trim=TRIMMING[0], std=CT, tag='OBJ1')

  obj.draw()

  canvas.create_rectangle(obj.boundary)
  canvas.create_rectangle(obj.bbox)

  obj.center = (250, 100)

  canvas.create_rectangle(obj.boundary)
  canvas.create_rectangle(obj.bbox)

  obj.trimming = TRIMMING[0]

  obj.size = (50, 1000)

  obj.mode = MODE[2]

  root.mainloop()
# } main func


if __name__ == '__main__':
  main()
