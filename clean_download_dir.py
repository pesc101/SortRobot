import datetime
from os import listdir
from os.path import isfile, join
import os
import shutil
import re
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileSystemEventHandler
import yaml




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


class Watcher:

    def __init__(self, directory, handler):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self, go_recursively):
        path = "/Users/jan/Downloads/"
        self.observer.schedule(self.handler, self.directory, recursive=go_recursively)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class EventHandler(PatternMatchingEventHandler):

    def __init__(self, *args, **kwargs):
        super(EventHandler, self).__init__(*args, **kwargs)

    def get_datetime(self):
        return datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")

    def on_created(self, event):
        print(f'{self.get_datetime()} CREATED: {event.src_path} created.')

    def on_deleted(self, event):
        print(f'{self.get_datetime()} DELETED: {event.src_path} deleted.')

    def on_modified(self, event):
        print(f'{self.get_datetime()} MODIFIED: {event.src_path} has been modified.')

    def on_moved(self, event):
        print(f'{self.get_datetime()} MOVED: {event.src_path} >> {event.dest_path}.')


if __name__ == "__main__":

    # Import Config
    with open('config.yaml') as f:
        types = yaml.load(f, Loader=yaml.FullLoader)
    print(types)

    # Start Watcher
    w = Watcher('/Users/jan/Downloads', EventHandler())
    w.run(False)

    # create_dirs(download_dir, types)
    # sort_files(download_dir, types)
    # sort_dirs(download_dir, dirs)
    print('Done.')
