import os
import glob
import shutil

def organize(path, target_extension, flag_alphabetical, flag_by_date, flag_sub_folders, folder_count):
    '''
    1. List out all files in folder
    2. Create new folders based on extensions
    3. Move files into newly created folders
    4. Create new folders within each folder based on alphabetical sort or by_date sort

    '''
    file_names = os.listdir(path)
    
    #make this cleaner by sorting it
    file_names.sort(key=sort_by_type)
    
    if target_extension=='.*':
        extensions = get_file_extensions(path)
        make_folders(path, file_names, extensions)
    else:
        make_folders(path, file_names, {f"{target_extension}"})


def sort_by_type(file):
    return os.path.splitext(file)[::-1]
        
def get_file_extensions(path):
        #return set of file extensions that exist within directory path
        extensions = set()
        for file in os.listdir(path):
            if not os.path.isdir(path+f"/{file}"):
                extensions.add(f".{file.split('.')[-1]}")

        return extensions

def make_folders(dest, file_names, extensions):
    
    #make groupings
    for ext in extensions:
        group = [f for f in file_names if f.endswith(ext)]
        dir = dest+f"/{ext.split('.')[-1]}_files"

        if not os.path.isdir(dir):
            os.mkdir(dir)

        for file in group:
            shutil.move(dest+f"/{file}", dir)

    print('organized')
