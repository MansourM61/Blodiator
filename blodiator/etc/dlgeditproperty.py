'''
********************************************************************************

Python Script: dlgeditproperty module
Writter: Mojtaba Mansour Abadi
Date: 21 June 2019

This Python script is compatible with Python 3.x.
The script is used to define Edit Property dialouge. Based on the parameters 
of the block, a proper modal dialog is generated and presented to the user.


DlgEditProperty
|
|____tk.Toplevel


History:
    
Ver 0.0.31: 25 June 2019;
             first code

********************************************************************************
'''


import tkinter as tk

from . import coloredtext


style = 'normal'
fg = 'purple'
bg = 'black'
src = 'EditProperty: '


#################################################
BLOCK_NAME = 'Generic Block'
BLOCK_LABEL = 'Block xxx'
PROPERTIES = [ ['Parameter 1', 'd', [0.0, 5], 3.5],\
               ['Parameter 2', 's', [], 'Default'],\
               ['Parameter 3', 'l', ['-2', '3.5', '3.9', 'Mode 1', 'Mode 2', 'Mode 3'], 2],\
               ['Parameter 4', 'd', [-20, 40], 33],\
               ['Parameter 5', 's', [], 'Text'],\
             ]  # properties (name, type, range, default value); d = number, s = string, l = list
#################################################


# DlgEditProperty class: this is the edit property dialouge class
# {
class DlgEditProperty(tk.Toplevel):
  """
  Modal dialog for editing properties of a block
  
  Define an instance of 'DlgEditProperty' with appropriate arguments:
      master = root widget
      block_name = block name
      blocklabel = block label
      properties = a list of parameters for a block. The format of each 
      parameter is [name, type, range, default value]; d = number, s = string, l = list
      std = standard output which is an instance of 'ColoredText' class
      
  The class creates a modal dialog populated with all parameters given by input.
  The class also checks the validity of the entries as well as updating the 
  parameters.
  """

  version = '0.0.31'  # version of the class

  # < class functions section >
  # < class functions section >

  # < inherited functions section >
  # __init__ func: initialiser dunar
  # {
  def __init__(self, master=None, block_name=BLOCK_NAME, blocklabel=BLOCK_LABEL, properties=PROPERTIES, std=None):
    """
    Construct a DlgEditProperty
    
    input:
        master = root widget
        block_name = block name
        blocklabel = block label
        properties = a list of parameters for a block. The format of each 
        parameter is [name, type, range, default value]; d = number, s = string, l = list
        std = standard output which is an instance of 'ColoredText' class
    output: none
    """


    if std is None:
      print(src + ': Please specify a standard output for messages!')
      exit()
    else:
      self.std = std

    self.__properties = properties
    self.__defaults = []
    self.__entries = []
    self.__returnedValues = []
    self.__Vars = []
    self.__block_name = block_name
    self.__block_label = blocklabel

    self.std.Print('Initialising EditProperty', fg, bg, style, src)
     
    self.__master = master

    tk.Toplevel.__init__(self, master)

    self.setupDialouge()
   
  # } __init__ func
  # < inherited functions section >


  # < class functions section >
  # setupDialouge func: function for setting up the dialouge
  # {
  def setupDialouge(self):
    """
    Sets up the modal dialog window
    
    input: none
    output: none
    """

#    self.geometry("350x100+%d+%d" % (self.__master.winfo_rootx(), self.__master.winfo_rooty()))
    
    self.title("Edit Property:")

    tk.Label(self, text='Block type: %s' % self.__block_name, justify=tk.LEFT, anchor=tk.W).grid(row = 0,column = 0, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S) 
    tk.Label(self, text='Block label: %s' % self.__block_label, justify=tk.LEFT, anchor=tk.W).grid(row = 1,column = 0, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S) 

    Frame = tk.Frame(self, relief=tk.FLAT, padx=10, pady=5, borderwidth=0)
    Frame.grid(row = 3, column = 0, sticky=tk.E) 

    tk.Button(Frame, text = "OK", command = self.on_ok, width=5).grid(row = 0,column = 0, sticky=tk.E) 
    tk.Button(Frame, text = "Cancel", command = self.on_cancel, width=5).grid(row = 0,column = 1, sticky=tk.E) 

    self.populateDialouge()

    self.resizable(0, 0)

    # make dialog modal
    self.transient(self.__master)
    self.grab_set()
    self.protocol("WM_DELETE_WINDOW", self.on_cancel)
    # instead of mainloop call wait_window
    self.wait_window()

    pass
  # } setupDialouge func


  # populateDialouge func: function for populating the dialouge with properties
  # {
  def populateDialouge(self):
    """
    Populates the dialog with properties given in constructor.
    
    input: none
    output: none
    """

    Frame = tk.Frame(self, relief=tk.RAISED, padx=10, pady=5, borderwidth=1)

    Frame.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W+tk.E+tk.N+tk.S) 

#    self.__Vars = [None]*len(self.__proprties)
    
    for index, prop in enumerate(self.__properties):
      self.__defaults.append(prop[-1])
      PropName = prop[0]
      L = tk.Label(Frame, text=PropName+':')
      L.grid(row=index, column=0)

      PropType = prop[1]
      if PropType == 'd':
        var = tk.DoubleVar()
        var.trace("w", self.checkValues)
        self.__Vars.append(var)
        var.set(prop[-1])
        E = tk.Entry(Frame, textvariable=var)
        E.grid(row=index, column=1)
        pass
      elif PropType == 's':
        var = tk.StringVar()
        var.set(prop[-1])
        self.__Vars.append(var)
        E = tk.Entry(Frame, textvariable=var)
        E.grid(row=index, column=1)
        pass
      elif PropType == 'l':
        E = tk.Frame(Frame, relief=tk.FLAT)
        scrollbar = tk.Scrollbar(E, orient=tk.VERTICAL)
        listbox = tk.Listbox(E, selectmode=tk.SINGLE, height=4, yscrollcommand=scrollbar.set, exportselection=False)
        for item in prop[-2]: listbox.insert(tk.END, item)
        listbox.selection_set(0)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        E.grid(row=index, column=1)
        self.__Vars.append(listbox)
        pass

    pass


  # checkValues func: function to cancel edit property dialouge
  # {
  def checkValues(self, *args):
    """
    Message handler dealing with checking the values and their limits
    
    input:
        args = input argument, not used
    output: none
    """

    for index, var in enumerate(self.__Vars):

      prop = self.__properties[index]

      PropType = prop[1]
      PropRange = prop[2]

      if PropType == 'd':
        try:
          num = var.get()
          num = max(num, PropRange[0])
          num = min(num, PropRange[1])
          var.set(num)
          pass
        except:
          num = PropRange[0]
          var.set(num)
          pass          
      pass
  # } checkValues func

     
  # on_cancel func: function to cancel edit property dialouge
  # {
  def on_cancel(self):
    """
    Message handler dealing with canceling edit property dialog changes
    
    input: none
    output: none
    """

    
    self.std.Print('Canceling properties changes', fg, bg, style, src)
    self.__returnedValues = self.__defaults
    self.destroy()
    pass
  # } on_cancel func
    
  # on_ok func: function to accept edit property dialouge
  # {
  def on_ok(self):
    """
    Message handler dealing with accepting edit property dialog changes
    
    input: none
    output: none
    """

    self.std.Print('Accepting properties changes', fg, bg, style, src)

    self.__entries = []

    for index, var in enumerate(self.__Vars):

      prop = self.__properties[index]
      var = self.__Vars[index]

      PropType = prop[1]

      if PropType == 'd' or PropType == 's':
        self.__entries.append(var.get())
        pass
      elif PropType == 'l':
        self.__entries.append(var.curselection()[0])
        pass

    self.__returnedValues = self.__entries
    self.destroy()
    pass
  # } on_ok func
  
  # } populateDialouge func
  # < class functions section >
  
  # < getter and setter functions section >
  # property: returnedValues
  # returnedValues getter func: returned values getter
  # {
  @property
  def returnedValues(self):
    """
    Class property getter: returned property values
    """

    return self.__returnedValues
  # } returnedValues getter func
  # < getter and setter functions section >

# }  DlgEditProperty class


# main func: contains code to test DlgEditProperty class
# {
def main():
  CT = coloredtext.ColoredText()

  root = tk.Tk()
  root.geometry("500x500")
  root.title('Blodiator Base Test Bench')
  TestApp = DlgEditProperty(master=root, std=CT)

  print(TestApp.returnedValues)

  root.mainloop()
  pass
# } main func


if __name__ == '__main__':
  main()
