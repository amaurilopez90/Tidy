from tkinter import filedialog
from tkinter import *
import json


class TidyInterface():

    def __init__(self, master):
        #Make initial frame for the base
        frame = Frame(master)
        frame.pack()

        #Required attributes
        self._master = master
        self._criteria = {}

        #Attributes that may be used throughout class
        self._target_directory = StringVar()
        self.target_extension = StringVar()
        self.alphabetical = IntVar().set(0)
        self.by_date = IntVar().set(0)
        self.sub_folders = IntVar().set(0)
        self.file_extensions = {''}
        self.ext_dropdown = OptionMenu(frame, self.target_extension, *self.file_extensions).grid(column=4, row=2)

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

        #Create layout for gui
        directory_entry = Entry(frame, textvariable=self._target_directory, width=26).grid(row=0, column=1, columnspan=3)
        
        directory_entry_label = Label(frame, text="Directory").grid(sticky=E, row=0)
        organize_method_label = Label(frame, text='Organize how?').grid(sticky=E, row=2)
        sub_folders_label = Label(frame, text='Sub Folders?').grid(sticky=E, row=3, column=0)
        ext_label = Label(frame, text='Target ext.').grid(column=3, row=2)
        
        browse_button = Button(frame, text='Browse', command=self.select_dir).grid(row=0, column=4)
        organize_button = Button(frame, text='Organize', command=self.organize).grid(columnspan=5, row=4)
        
        chk_alphabetical = Checkbutton(frame, text="A-z", variable=self.alphabetical).grid(row=2, column=1, sticky=W)
        chk_by_date = Checkbutton(frame, text="By Date", variable=self.by_date).grid(row=2, column=2, sticky=E)
        chk_sub_folders = Checkbutton(frame, variable = self.sub_folders).grid(row=3, column=1, sticky=W)


    def start(self):
        self._master.mainloop()

    def select_dir(self):
        #open a directory dialog box to ask for directory
        path = filedialog.askdirectory()
        self._target_directory.set(path)

        #get file extensions in directory and update extensions drop down
        self.file_extensions = self.get_file_extensions(path)
        self.update_ext_dropdown()

    def get_file_extensions(self, path):
        #Getset of file extensions that exist within directory path
        pass

    def update_ext_dropdown(self):
        #Delete existing drop down options
        menu = self.ext_dropdown['menu']
        menu.delete(0, 'end')

        #Re-establish new drop down options
        for ext in self.file_extensions:
            menu.add_command(label=ext, command=lambda value=ext: self.target_extension.set(value))


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

