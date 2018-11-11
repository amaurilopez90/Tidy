from tkinter import Tk
from tidy_interface import TidyInterface

import file_organizer

#Tkinter requires a root
root = Tk()
gui = TidyInterface(root)

#get organization method from gui
method = gui.start()

#analyze criteria and organize
file_organizer.organize(**method)