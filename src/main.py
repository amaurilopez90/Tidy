from tkinter import Tk
from tidy_interface import TidyInterface

import file_organizer

#Tkinter requires a root
root = Tk()
gui = TidyInterface(root)

#get organization method from gui
method = gui.start()
print(method)

#analyze criteria and organize
