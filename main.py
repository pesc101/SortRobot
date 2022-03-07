import argparse
import logging
from os import listdir
from os.path import isfile, join
import os
import shutil
import re
import yaml
from classes.watcher import Watcher
from classes.handler import EventHandler



# Ordner erstellen
def create_dirs(path, type_dict):
    os.chdir(path)
    [os.mkdir(name) for name in type_dict.keys() if not os.path.isdir(name)]


# Dateien sortieren
def sort_files(path: str, type_dict: dict):
    files = [f for f in listdir(path) if isfile(join(path, f))]
    files.remove('.DS_Store')
    if len(files) == 0:
        return print(f'No new Files in {path}')

    for file in files:
        src_path = path + file
        file_typ = file.split('.')[len(file.split('.')) - 1]

        for folder in type_dict.keys():
            if file_typ in type_dict.get(folder):
                dest_path = path + folder
                shutil.move(src_path, dest_path)
                shutil.move(os.path.join(path, folder), os.path.join(dest_path, file))
                print(src_path + '  >>>  ' + dest_path.split('/')[len(dest_path.split('/')) - 1])




        # for dict in range(len(type_dict.keys())):
        #     if file_typ in type.dict:
        #         print(src_path + '  >>>  ' + dest_path.split('/')[len(dest_path.split('/')) - 1])
        # if counter == 6:
        #     dest_path = path + dir_names[6]
        #     shutil.move(src_path, dest_path)
        #     print(src_path + '  >>>  ' + dest_path.split('/')[len(dest_path.split('/')) - 1])

    # Finish
    print('All Files got moved.')




# Ordner sortieren
def sort_dirs(mypath, dir_names):
    dirs = [f for f in next(os.walk(mypath))[1] if not re.search(r"^\d_", f)]
    if len(dirs) == 0:
        return print('No new Dirs in Download Dir')

    for dir in dirs:
        src_path = mypath + dir
        dest_path = mypath + dir_names[6]
        shutil.move(src_path, dest_path)
        print(src_path + '  >>>  ' + '6_rest')


if __name__ == "__main__":

    # Arg Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', help='Insert the path', default='/Users/jan/Downloads')
    parser.add_argument('--patterns', help='Insert Pattern', default='')
    args = parser.parse_args()


    # Logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%H:%M:%S %d-%m-%Y')

    # Import Config
    with open('config.yaml') as f:
        types = yaml.load(f, Loader=yaml.FullLoader)

    # Start Watcher
    w = Watcher(args.path, EventHandler())
    w.run(False)

    # create_dirs(download_dir, types)
    # sort_files(download_dir, types)
    # sort_dirs(download_dir, dirs)
    print('Done.')
