import os
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
    
    #seperate files into folders based on extension(s)
    if (target_extension == '.*'):
        extensions = get_file_extensions(path)
        new_folders = group_extensions(path, file_names, extensions)
    else:
        new_folders = group_extensions(path, file_names, {f"{target_extension}"})

    #Create a new grouping within each new_folder based on alphabetical sort or by_date sort
    if flag_alphabetical:
        for folder in new_folders:
            group_alphabetical(folder, folder_count)
    elif flag_by_date:
        for folder in new_folders:
            group_by_date(folder, folder_count)
    else:
        #Done
        print('organized')

def sort_by_type(file):
    return os.path.splitext(file)[::-1]
        
def get_file_extensions(path):
        #return set of file extensions that exist within directory path
        extensions = set()
        for file in os.listdir(path):
            if not os.path.isdir(path+f"/{file}"):
                extensions.add(f".{file.split('.')[-1]}")

        return extensions

def group_extensions(dest, file_names, extensions):
    '''
    Creates groupings between file extensions and new sub_folder names

    '''
    #all folders to be made
    sub_folders = []
    
    #make groupings
    for ext in extensions:
        group = [f for f in file_names if f.endswith(ext)]
        dir = dest+f"/{ext.split('.')[-1]}_files"

        if not os.path.isdir(dir):
            os.mkdir(dir)

        for file in group:
            shutil.move(dest+f"/{file}", dir)

        #append dir to list
        sub_folders.append(dir)

    print('Folders by extensions made')
    return sub_folders

def group_alphabetical(dir, count):
    
    pass

def group_by_date(dir, count):
    pass
