import datetime
import shutil
import os
from watchdog.events import PatternMatchingEventHandler


def get_datetime():
    return datetime.datetime.now().strftime("%H:%M:%S %d-%m-%Y")


class EventHandler(PatternMatchingEventHandler):

    def __init__(self, folders, *args, **kwargs):
        self.folders = folders
        super(EventHandler, self).__init__(*args, **kwargs)

    def on_created(self, event):
        FileHandler(event.src_path).sort_file(folders=self.folders)
        print(f'{get_datetime()} CREATED: {event.src_path} created.')

    def on_deleted(self, event):
        print(f'{get_datetime()} DELETED: {event.src_path} deleted.')

    def on_modified(self, event):
        print(f'{get_datetime()} MODIFIED: {event.src_path} has been modified.')

    def on_moved(self, event):
        print(f'{get_datetime()} MOVED: {event.src_path} >> {event.dest_path}.')


class FileHandler:

    def __init__(self, path):
        self.path = path
        self.folder_path = self.get_folder_path()
        self.rest_folder = 'rest'
        self.typ = self.get_file_typ()
        self.name = self.get_name()
        self.num = 0

    def get_file_typ(self):
        return self.path.split('.')[len(self.path.split('.')) - 1]

    def get_folder_path(self):
        return "/".join(str(x) for x in self.path.split('/')[0:len(self.path.split('/')) - 1])

    def get_name(self):
        return self.path.split('/')[len(self.path.split('/')) - 1]

    def get_next_file(self, folder):
        dest = os.path.join(self.folder_path, folder)
        while os.path.exists(os.path.join(dest, self.name)):
            self.num += 1

            period = self.name.rfind('.')
            if period == -1:
                period = len(self.name)

            new_file = f'{self.name[:period]}_{self.num}{self.name[period:]}'
            dest = os.path.join(dest, new_file)
        return dest

    def sort_file(self, folders):
        for folder in folders.keys():
            if self.typ in folders.get(folder):
                desc_path = os.path.join(self.folder_path, folder, self.name)
                if os.path.exists(desc_path):
                    desc_path = self.get_next_file(folder)
                shutil.move(self.path, desc_path)
                print(f'{self.path} >>> {desc_path}')
                return

        # Rest Folder
        desc_path = os.path.join(self.folder_path, self.rest_folder, self.name)
        if os.path.exists(desc_path):
            desc_path = self.get_next_file(self.rest_folder)
        shutil.move(self.path, desc_path)
        print(f'{self.path} >>> {desc_path}')
