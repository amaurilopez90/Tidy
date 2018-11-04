from tkinter import filedialog
from tkinter import *
import json
import sys
import os

def update_ext_dropdown(func):
    #decorator to update dropdown menu for file extensions
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)

        #Delete existing drop down options
        menu = self.ext_dropdown['menu']
        menu.delete(0, 'end')

        #Re-establish new drop down options
        for ext in self.file_extensions:
            menu.add_command(label=ext, command=lambda value=ext: self._criteria['target_extension'].set(value))

    return wrapper

class TidyInterface():

    def __init__(self, master):

        #Make initial frame for the base
        frame = Frame(master)
        frame.pack()

        #Required attributes
        self._master = master
        self._filename = ''
        self._criteria = {
            'target_directory': StringVar(),
            'target_extension': StringVar(),
            'flag_alphabetical': IntVar(),
            'flag_by_date': IntVar(),
            'flag_sub_folders': IntVar(),
            'folder_count': IntVar(),
        }

        self.file_extensions = {''}
        self.ext_dropdown = OptionMenu(frame, self._criteria['target_extension'], *self.file_extensions)
        self.ext_dropdown.grid(column=4, row=2)
        self.sub_folders_scale = Scale(frame, from_=0, to=4, orient=HORIZONTAL, variable=self._criteria['folder_count'], width=10, state=DISABLED)
        self.sub_folders_scale.grid(row=3, column=2, sticky=NE)

        #Set up the top menu configuration for gui
        menu = Menu(self._master)
        self._master.config(menu=menu)

        fileMenu = Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Open Criteria...', command=self.load_criteria)
        fileMenu.add_separator()
        fileMenu.add_command(label='Save', command=lambda func=self.save_criteria: func(self._criteria))
        fileMenu.add_command(label='Save Criteria As...', command=lambda func=self.save_criteria: func(self._criteria, save_as=True))
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=lambda code=0: sys.exit(code))

        #Create layout for gui
        directory_entry = Entry(frame, textvariable=self._criteria['target_directory'], width=26).grid(row=0, column=1, columnspan=3)
        
        directory_entry_label = Label(frame, text="Directory").grid(sticky=E, row=0)
        organize_method_label = Label(frame, text='Organize how?').grid(sticky=E, row=2)
        sub_folders_label = Label(frame, text='Sub Folders?').grid(sticky=E, row=3, column=0)
        ext_label = Label(frame, text='Target ext.').grid(column=3, row=2)
        
        browse_button = Button(frame, text='Browse', command=self.select_dir).grid(row=0, column=4)
        organize_button = Button(frame, text='Organize', command=self._master.destroy).grid(columnspan=5, row=5)
        
        chk_alphabetical = Checkbutton(frame, text="A-z", variable=self._criteria['flag_alphabetical']).grid(row=2, column=1, sticky=W)
        chk_by_date = Checkbutton(frame, text="By Date", variable=self._criteria['flag_by_date']).grid(row=2, column=2, sticky=E)
        chk_sub_folders = Checkbutton(frame, variable=self._criteria['flag_sub_folders'], command=self.toggle_slider).grid(row=3, column=1, sticky=W)

    def start(self):
        self._master.mainloop()
        criteria = self.get_criteria(self._criteria)
        return criteria

    def toggle_slider(self):
        if not self._criteria['flag_sub_folders'].get():
            self.sub_folders_scale.set(0)
            self.sub_folders_scale['state'] = DISABLED
            self._criteria['folder_count'].set(0)
        else:
            self.sub_folders_scale['state'] = NORMAL
            self.sub_folders_scale.set(self._criteria['folder_count'].get())

    def select_dir(self):
        #open a directory dialog box to ask for directory
        path = filedialog.askdirectory()
        self._criteria['target_directory'].set(path)

        #get file extensions in directory and update extensions drop down
        self.update_file_extensions(self.get_file_extensions(path))
        
    def load_criteria(self):
        file = filedialog.askopenfilename(initialdir='./criteria')

        if file:
            with open(file) as json_file:
                data = json.load(json_file)
                print(data)

            #Get new extensions
            self.update_file_extensions(self.get_file_extensions(os.path.dirname(file)))
            
            #load gui with new data
            for k,v in iter(data.items()):
                self._criteria[k].set(v)

            #toggleslider
            self.toggle_slider()

        else:
            return


    def save_criteria(self, class_criteria, save_as=False):
        data = self.get_criteria(class_criteria)

        #if file doesn't exist yet then do save_as
        if self._filename == '':
            save_as = True
        
        if(save_as):
            file = filedialog.asksaveasfile(mode='w', initialdir='./criteria', defaultextension='.json', title='Select File', filetypes=[('JSON files', ['.json'])])
            if file:
                with open(file.name, 'w') as output:
                    json.dump(data, output)

                self._filename = file.name
            else:
                return
        else:
            with open(self._filename, 'w') as output:
                json.dump(data, output)
                

    @update_ext_dropdown
    def update_file_extensions(self, extensions):
        self.file_extensions = extensions

    @staticmethod
    def get_criteria(class_criteria):
        formatted_criteria = {}
        for k,v in iter(class_criteria.items()):
            formatted_criteria[k] = v.get()

        return formatted_criteria

    @staticmethod
    def get_file_extensions(path):
        #return set of file extensions that exist within directory path
        extensions = set()
        for file in os.listdir(path):
            extensions.add(f".{file.split('.')[-1]}")

        return extensions
