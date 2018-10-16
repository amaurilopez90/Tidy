from tkinter import filedialog
from tkinter import *
import json


class TidyInterface():

    def __init__(self, master):
        self._master = master
        self._target_directory = ""
        self._criteria = {}
        self.entry_text = StringVar()
        self.alphabetical = IntVar()
        self.by_date = IntVar()
        self.sub_folders = IntVar()

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
        directory_entry = Entry(frame, textvariable=self.entry_text).grid(row=0, column=1)
        
        directory_entry_label = Label(frame, text="Directory").grid(sticky=E, row=0)
        organize_method_label = Label(frame, text='Organize how?').grid(sticky=E, row=2)
        sub_folders_label = Label(frame, text='Sub Folders?').grid(sticky=E, row=3, column=0)
        
        browse_button = Button(frame, text='Browse', command=self.select_dir).grid(row=0, column=2)
        organize_button = Button(frame, text='Organize', command=self.organize).grid(columnspan=3, row=4)
        
        chk_alphabetical = Checkbutton(frame, text="A-z", variable=self.alphabetical).grid(row=2, column=1, sticky=W)
        chk_by_date = Checkbutton(frame, text="By Date", variable=self.by_date).grid(row=2, column=1, sticky=E)
        chk_sub_folders = Checkbutton(frame, variable = self.sub_folders).grid(row=3, column=1, sticky=W)
        
        
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

