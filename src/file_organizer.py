from datetime import datetime
from datetime import date
from datetime import timedelta
import os
import shutil
import string
import platform

def organize(path, target_extension, flag_alphabetical, flag_by_date, flag_sub_folders, folder_count):
    '''
    1. List out all files in folder
    2. Create new folders based on extensions
    3. Move files into newly created folders
    4. Create new folders within each folder based on alphabetical sort or by_date sort

    '''
    file_names = os.listdir(path)
    
    #seperate files into folders based on extension(s)
    if (target_extension == '.*'):
        extensions = get_file_extensions(path)

        #In the case where '.*' is selected, and there arent any files at root level relative to path,
        #unpack all files within possible directories for fresh organization
        if not(extensions) and file_names: 
            print("Preparing for fresh organization...")
            for dir in file_names:
                rec_unpack_dir(path + f"/{dir}", path)
                os.rmdir(path + f"/{dir}")
            
            #update file_names and extensions now that they are available
            file_names = os.listdir(path)
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
    
    #Done
    print('Organized')
        
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
        else:
            #if directory already exists then unpack any sub directories within it for fresh organization
            rec_unpack_dir(dir, dir)

        for file in group:
            shutil.move(dest+f"/{file}", dir)

        #append dir to list
        sub_folders.append(dir)

    return sub_folders

def group_alphabetical(dir, count):
    start = 0
    end = 0
    moved_files = set()

    if count:
        step = 26//count
    else:
        return

    files = os.listdir(dir)

    #precedent upper_case over lower_case
    alphabet_upper = string.ascii_uppercase
    alphabet_lower = string.ascii_lowercase

    for x in range(count):
        #Remove already moved files from the list so we don't iter over again
        for file in moved_files:
            files.remove(file)

        if x == count - 1:
            #make last group include all left over characters as well
            end = -1
        else:
            end = start + step

        new_dir = dir + f"/files_{alphabet_upper[start]}_through_{alphabet_upper[end]}"

        if not os.path.isdir(new_dir):
            os.mkdir(new_dir)


        #Move files
        for file in files:
            if (not os.path.isdir(dir + f"/{file}")) and (file[0] in alphabet_upper[start:end] or file[0] in alphabet_lower[start:end]):
                shutil.move(dir + f"/{file}", new_dir)

                #Remove the moves file from the list of files so we don't iter over it again
                moved_files.add(file)
            
        start += step + 1

def group_by_date(dir, count):

    if not count:
        return

    #Find most recent file created and least recent file created
    files = os.listdir(dir)

    most_recent_time = latest_time = get_creation_date(dir + f"/{files[0]}")

    #Skip the first file since we already got the created time
    iterfiles = iter(files)
    next(iterfiles)

    for file in iterfiles:
        time_created = get_creation_date(dir + f"/{file}")
        if time_created > most_recent_time:
            most_recent_time = time_created
        elif time_created < latest_time:
            latest_time = time_created
        else: 
            continue

    #Get the most_recent created file and latest created file times into mm/dd/yyyy format
    most_recent_time = datetime.fromtimestamp(most_recent_time).date()
    latest_time = datetime.fromtimestamp(latest_time).date()
    
    delta = (most_recent_time - latest_time).days

    if delta == 0:
        #Case where its the same creation date for all files
        new_dir = dir + f"/Created_{most_recent_time}"

        for file in files:
            path = dir + f"/{file}"
            shutil.move(path, new_dir)
    else:
        step = delta//count

        if step == 1:
            #Create a folder for each of the days between delta
            for x in range(delta):
                new_dir = dir + f"/Created_{latest_time + timedelta(days=x)}"
                if not os.path.isdir(new_dir):
                    os.mkdir(new_dir)
                
            #Move each file into their folders based off of creation date
            for file in files:
                path = dir + f"/{file}"
                date_created = datetime.fromtimestamp(get_creation_date(path)).date()
                shutil.move(path, dir + f"/Created_{date_created}")

        else:
            #Make folder names match a range of dates within a step
            start_date = latest_time
            moved_files = set()

            for x in range(count):
                #Remove already moved files from the list so we don't iter over again
                for file in moved_files:
                    files.remove(file)

                if x == count - 1:
                    #Make last group include all left over dates
                    end_date = most_recent_time
                else:
                    end_date = start_date + timedelta(days=step)

                new_dir = dir + f"/Created_{start_date}_to_{end_date}"

                if not os.path.isdir(new_dir):
                    os.mkdir(new_dir)


                #Move Files
                for file in files:
                    path = dir + f"/{file}"
                    date_created = datetime.fromtimestamp(get_creation_date(path)).date()

                    #Move to folder if created date falls within range
                    if not(os.path.isdir(path)) and (start_date <= date_created <= end_date):
                        shutil.move(path, new_dir)

                        moved_files.add(file)

                start_date += timedelta(days=(step+1))

def get_creation_date(path):
    
    if platform.system() == 'Windows':
        return os.path.getctime(path)
    else:
        stat = os.stat(path)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux.
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def rec_unpack_dir(source, destination):
    #check for any subdirectories and unpack them
    files = os.listdir(source)
    for file in files:
        if os.path.isdir(source + f"/{file}"):
            rec_unpack_dir(source + f"/{file}", source)

            #delete empty directory
            os.rmdir(source + f"/{file}")
            continue
        
        shutil.move(source + f"/{file}", destination)
