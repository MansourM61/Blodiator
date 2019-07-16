'''
********************************************************************************

Python Script: cntsheetcanvas Module
Writter: Mojtaba Mansour Abadi
Date: 20 Januarry 2019

This Python script is compatible with Python 3.x.
The script is used to define CntSheetCanvas class the container
Blodiator. This module provides required canvas information, panning, 
converting coordinates, drawing grids.


CntSheetCanvas
|
|____tk.Canvas


Histoty:

Ver 0.0.10: 26 Feburary 2019;
             first code

Ver 0.0.11: 8 March 2019;
             1- Snapping coordinate is added

Ver 0.0.31: 24 June 2019;
             1- logging is added.

********************************************************************************
'''


import tkinter as tk

from . import coloredtext
from ..grafix import gfxline


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'CanvasSheet: '


#################################################
WIDTH = 300  # canvas width
HEIGHT = 500  # canvas height
BACKGROUND_COLOR = 'white'  # canvas background color
GRID_STATE = True  # default grid state
GRID_X_STEP = 50  # default grid x spacing
GRID_Y_STEP = 50  # default frid y spacing
GRID_X_BRUSH = ('black', 1.0, (2, ))  # default line thickness and style for grid x
GRID_Y_BRUSH = ('red', 1.0, (2, ))  # default line thickness and style for grid x
MODE = ('normal', 'disabled', 'selected', 'erroneous')  # states of the object
#################################################


# CntSheetCanvas class: this is the sheet canvas class
# {
class CntSheetCanvas(tk.Canvas):
  """
  Wrapper class for tk.Canvas.
  
  Define an instance of 'CntSheetCanvas' with appropriate arguments:
      master = root widget
      size = (width, height) of diagram canvas
      std = standard output which is an instance of 'ColoredText' class
      
  The class creates a canvas and also deals with converting window coordinate 
  to canvas coordinate. The grids and guidelines are also managed in this class
  as well as required functions for panning and scrolling.
  """

  version = '0.0.31'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, master, size=(WIDTH, HEIGHT), std=None):
    """
    Construct a CntSheetCanvas
    
    input:
        master = root widget
        size = (width, height) of diagram canvas
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """

    if std is None:
      print('\n' + src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std

    self.std.Print('Initialising SheetCanvas', fg, bg, style, src)

    self.__width_neg = 0  # minimum x coordinate
    self.__height_neg = 0  # minimum y coordinate
    self.__width_pos = size[0]  # maximum x coordinate
    self.__height_pos = size[1]  # minimum y coordinate
    self.__background = BACKGROUND_COLOR
    self.__master = master

    self.__scale = 1
    self.__x_org_zoom = 0
    self.__y_org_zoom = 0

    self.__grid_state = GRID_STATE
    self.__grid_x_step = GRID_X_STEP
    self.__grid_y_step = GRID_Y_STEP
    self.__grid_x_brush = GRID_X_BRUSH
    self.__grid_y_brush = GRID_Y_BRUSH

    self.__grid_x = []
    self.__grid_y = []
    
    super(CntSheetCanvas, self).__init__(master=master,
                                         width=self.__width_pos,
                                         height=self.__height_pos,
                                         background=BACKGROUND_COLOR)

    self.updateGrids()    
  # } __init__ func
  # < inherited functions section >

  # < class functions section >
  # convert_coords func: convert coordinates
  # {
  def convert_coords(self, coords_raw, snap_mode, conversion_mode=True):
    """
    Converts windows coordinate to desired coordinate. It considers snapping 
    mode (on/off) and type of coversion (canvas to canvas/windows to canvas)
    
    input:
        coords_raw = raw input coordinate
        snap_mode = if snapping to the grid is considered (True) or not (False)
        conversion_mode = if it is a windows to canvas (True) or canvas to 
        canvas (False) conversion
    output:
        x, y = converted coordinates
    """
    
    if(conversion_mode == True):
        coords = [self.canvasx(coords_raw[0]), self.canvasy(coords_raw[1])]
        pass
    else:
        coords = coords_raw
        pass

    if snap_mode == False:
      return coords
    else:
      return round(coords[0]/self.__grid_x_step)*self.__grid_x_step,\
             round(coords[1]/self.__grid_y_step)*self.__grid_y_step
  # } convert_coords func


  # update_region func: update the canvas region
  # {
  def update_region(self, bbox):
    """
    Updates canvas region based on the input region
    
    input:
        bbox = region to be updated
    output: none
    """


    BBOX_raw = bbox
    
    BBOX_org = (self.__width_neg, self.__height_neg, self.__width_pos, self.__height_pos)
    
    if(BBOX_raw != BBOX_org):    
        self.__width_neg = BBOX_raw[0]
        self.__height_neg = BBOX_raw[1]
        self.__width_pos = BBOX_raw[2]
        self.__height_pos = BBOX_raw[3]
        self.updateGrids()
        self.configure(scrollregion=BBOX_raw)
        
        pass
    
#    print(BBOX_raw)
#    print(BBOX_org)
    
#    if (BBOX_org != BBOX_raw):
#        pass

  # } update_region func

  
  # draw_grids func: draw the object
  # {
  def draw_grids(self):
    """
    Draws the grids on the canvas
    
    input: none
    output: none
    """

    for obj in self.__grid_x:
      obj.draw()
      item = self.find_withtag(obj.tag)
      self.tag_lower(item)

    for obj in self.__grid_y:
      obj.draw()    
      item = self.find_withtag(obj.tag)
      self.tag_lower(item)

  # } draw_grids func
  
  # updateGrids func: update the grid
  # {
  def updateGrids(self):
    """
    Updates the grids on the canvas
    
    input: none
    output: none
    """


    for h_grid_x in self.__grid_x:
      h_grid_x.erase()

    for h_grid_y in self.__grid_y:
      h_grid_y.erase()
      
    self.__grid_x = []
    self.__grid_y = []

    if self.__grid_state == True:
      colorList = [[GRID_X_BRUSH[0]]*2, [GRID_X_BRUSH[0]]*2, [GRID_X_BRUSH[0]]*2, [GRID_X_BRUSH[0]]*2]
      brushList = [GRID_X_BRUSH[1:3], GRID_X_BRUSH[1:3], GRID_X_BRUSH[1:3], GRID_X_BRUSH[1:3]]
      CS = dict(zip(MODE, colorList))
      BS = dict(zip(MODE, brushList))
      
      y0 = self.__height_neg
      y1 = self.__height_pos
      dummy = []
      for i in range(0, int(self.__width_pos/self.__grid_x_step)):
        tag = 'grid-x-pos-' + str(i)
        x = (i + 1)*self.__grid_x_step
        pts = [ [x, y0], [x, y1] ]
        obj = gfxline.GfxLine(sheetCanvas=self, points=pts, arrow=(False, (1,1,1)),
                                 std=self.std, tag=tag)
        obj.colorset = CS
        obj.brushset = BS
        dummy.append(obj)
        pass
      
      for i in range(0, int(abs(self.__width_neg)/self.__grid_x_step) + 1):
        tag = 'grid-x-neg-' + str(i)
        x = -(i)*self.__grid_x_step
        pts = [ [x, y0], [x, y1] ]
        obj = gfxline.GfxLine(sheetCanvas=self, points=pts, arrow=(False, (1,1,1)),
                                 std=self.std, tag=tag)
        obj.colorset = CS
        obj.brushset = BS
        dummy.append(obj)
        pass
        
      self.__grid_x = dummy

      colorList = [[GRID_Y_BRUSH[0]]*2, [GRID_Y_BRUSH[0]]*2, [GRID_Y_BRUSH[0]]*2, [GRID_Y_BRUSH[0]]*2]
      brushList = [GRID_Y_BRUSH[1:3], GRID_Y_BRUSH[1:3], GRID_Y_BRUSH[1:3], GRID_Y_BRUSH[1:3]]
      CS = dict(zip(MODE, colorList))
      BS = dict(zip(MODE, brushList))
      
      x0 = self.__width_neg
      x1 = self.__width_pos
      dummy = []      
      for i in range(0, int(self.__height_pos/self.__grid_y_step)):
        tag = 'grid-pos-y-' + str(i)
        y = (i + 1)*self.__grid_y_step
        pts = [ [x0, y], [x1, y] ]
        obj = gfxline.GfxLine(sheetCanvas=self, points=pts, arrow=(False, (1,1,1)),
                                 std=self.std, tag=tag)
        obj.colorset = CS
        obj.brushset = BS
        above_tag = self.find_above(tag)
        if above_tag:
            self.tag_lower(above_tag, tag)
        dummy.append(obj)
        pass

      for i in range(0, int(abs(self.__height_neg)/self.__grid_y_step) + 1):
        tag = 'grid-neg-y-' + str(i)
        y = -(i)*self.__grid_y_step
        pts = [ [x0, y], [x1, y] ]
        obj = gfxline.GfxLine(sheetCanvas=self, points=pts, arrow=(False, (1,1,1)),
                                 std=self.std, tag=tag)
        obj.colorset = CS
        obj.brushset = BS
        above_tag = self.find_above(tag)
        if above_tag:
            self.tag_lower(above_tag, tag)
        dummy.append(obj)
        pass

      self.__grid_y = dummy

    self.draw_grids()
  # } updateGrids func
  
  # zoom func: zoom the sheet
  # {
  def zoom(self):
    """
    Zooms in/out the canvas. (under development)
    
    input: none
    output: none
    """


    self.scale("all", self.__x_org_zoom, self.__y_org_zoom, self.__scale, self.__scale)
  # } zoom func
  
  # start_pan func: start pan the sheet
  # {
  def start_pan(self, point):
    """
    Starts panning function based on input point
    
    input:
        point: start point coordinate
    output: none
    """

    self.scan_mark(point[0], point[1])
  # } start_pan func

  # stop_pan func: stop pan the sheet
  # {
  def stop_pan(self, point):
    """
    Stops panning function based on input point
    
    input:
        point: stop point coordinate
    output: none
    """

    self.scan_dragto(point[0], point[1], 1)
  # } stop_pan func
  # < class functions section >
  
  # < getter and setter functions section >
  # property: grid_zoom_org
  # grid_zoom_org getter func: grid zoom org getter
  # {
  @property
  def grid_zoom_org(self):
    """
    Class property getter: origin point of zoom operation
    """
    
    return self.__x_org_zoom, self.__y_org_zoom
  # } grid_zoom_org getter func

  # grid_scale setter func: grid zoom org setter
  # {
  @grid_zoom_org.setter
  def grid_zoom_org(self, grid_org_zoom):
    """
    Class property setter: origin point of zoom operation
    """

    self.__x_org_zoom, self.__y_org_zoom = grid_org_zoom
  # } grid_zoom_org setter func

  # property: grid_scale
  # grid_scale getter func: grid scale getter
  # {
  @property
  def grid_scale(self):
    """
    Class property getter: scale of zoom operation
    """

    return self.__scale
  # } grid_scale getter func

  # grid_scale setter func: grid scale setter
  # {
  @grid_scale.setter
  def grid_scale(self, grid_scale):
    """
    Class property setter: scale of zoom operation
    """

    self.__scale = grid_scale
    self.zoom()
  # } grid_scale setter func

  # property: grid_state
  # grid_state getter func: grid state getter
  # {
  @property
  def grid_state(self):
    """
    Class property getter: grid on/off state
    """

    return self.__grid_state
  # } grid_state getter func

  # grid_state setter func: grid state setter
  # {
  @grid_state.setter
  def grid_state(self, grid_state):
    """
    Class property setter: grid on/off state
    """

    self.__grid_state = grid_state

    self.updateGrids()
  # } grid_state setter func

  # property: grid_x_step
  # grid_x_step getter func: grid x step getter
  # {
  @property
  def grid_x_step(self):
    """
    Class property getter: grid x direction step
    """

    return self.__grid_x_step
  # } grid_x_step getter func

  # grid_x_step setter func: grid x step setter
  # {
  @grid_x_step.setter
  def grid_x_step(self, x_step):
    """
    Class property setter: grid x direction step
    """

    self.__grid_x_step = x_step

    self.updateGrids()
  # } grid_x_step setter func

  # property: grid_y_step
  # grid_y_step getter func: grid y step getter
  # {
  @property
  def grid_y_step(self):
    """
    Class property getter: grid y direction step
    """

    return self.__grid_y_step
  # } grid_y_step getter func

  # grid_y_step setter func: grid y step setter
  # {
  @grid_y_step.setter
  def grid_y_step(self, y_step):
    """
    Class property setter: grid y direction step
    """

    self.__grid_y_step = y_step

    self.updateGrids()
  # } grid_y_step setter func
  # < getter and setter functions section >

# } CntSheetCanvas class


# main func: contains code to test CntSheetCanvas class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  TestApp = CntSheetCanvas(master=root, std=CT, size=(WIDTH, HEIGHT))
  TestApp.create_rectangle([50,50, 200, 200])
  TestApp.pack()

  TestApp.grid_zoom_org = (10, 30)
  TestApp.grid_scale = 2
  TestApp.zoom()

#  TestApp.start_pan((50, 50))

 # TestApp.stop_pan((10, 50))


  root.mainloop()
  pass
# } main func


if __name__ == '__main__':
  main()
