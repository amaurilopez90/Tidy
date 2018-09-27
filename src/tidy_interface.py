from tkinter import *
import json


class TidyInterface():

    def __init__(self, master):
        self._master = master
        self._target_directory = ""
        self._criteria = {}

        frame = Frame(master)
        frame.pack()

        self.sel_dir_button = Button(frame, text='Print message', command=self.print_message)
        self.sel_dir_button.pack(side=LEFT)

        self.quit_button = Button(frame, text='Click here to quit', command=self._master.destroy)
        self.quit_button.pack(side=LEFT)

    def start(self):
        self._master.mainloop()

    def print_message(self):
        print('working')

    def generate_criteria(self):
        #Generation of criteria .json files
        #including 'load' and 'save' functionality to save or load an existing criteria into the GUI
        #for future usage
        pass


