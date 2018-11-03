from tkinter import Tk
from tidy_interface import TidyInterface


root = Tk()
gui = TidyInterface(root)
method = gui.start()
print(method)