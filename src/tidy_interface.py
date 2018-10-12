from tkinter import filedialog
from tkinter import *
import json


class TidyInterface():

    def __init__(self, master):
        self._master = master
        self._target_directory = ""
        self._criteria = {}
        self.entry_text = StringVar()

        #Set up the top menu configuration for gui
        menu = Menu(self._master)
        self._master.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Open Criteria...', command=self.load_criteria)
        fileMenu.add_separator()
        fileMenu.add_command(label='Save', command=self.save_criteria)
        fileMenu.add_command(label='Save Criteria As...', command=self.save_criteria(save_as=True))
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self._master.destroy)

        #Make initial frame for the base
        frame = Frame(master)
        frame.pack()

        #Create layout for gui
        self.directory_entry = Entry(frame, textvariable=self.entry_text)
        self.directory_entry_label = Label(frame, text="Target")
        self.browse_button = Button(frame, text='Browse', command=self.select_dir)
        self.organize_button = Button(frame, text='Organize', command=self.organize)
        
        #Pack components into gui grid
        self.directory_entry_label.grid(sticky=E)
        self.directory_entry.grid(row=0, column=1)
        self.browse_button.grid(row=0, column=2)
        self.organize_button.grid(columnspan=3)


    def start(self):
        self._master.mainloop()

    def select_dir(self):
        path = filedialog.askdirectory()
        self.entry_text.set(path)

    def organize(self):
        print('working')

    def generate_criteria(self):
        #Generation of criteria .json files
        #including 'load' and 'save' functionality to save or load an existing criteria into the GUI
        #for future usage
        pass

    def load_criteria(self):
        pass
    
    def save_criteria(self, save_as=False):
        pass

