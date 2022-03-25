import logging
import os
import shutil
import re


class SortingHandler:

    def __init__(self, path):
        self.path = path
        self.folder_path = self.get_folder_path()
        self.rest_folder = 'rest'
        self.name = self.get_name()
        self.num = 0

    def get_folder_path(self):
        return "/".join(str(x) for x in self.path.split('/')[0:len(self.path.split('/')) - 1])

    def get_name(self):
        return self.path.split('/')[len(self.path.split('/')) - 1]


class FileHandler(SortingHandler):

    def __init__(self, path):
        SortingHandler.__init__(self, path)
        self.typ = self.get_file_typ()

    def get_file_typ(self):
        return self.path.split('.')[len(self.path.split('.')) - 1]

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
                return

        # Rest Folder
        desc_path = os.path.join(self.folder_path, self.rest_folder, self.name)
        if os.path.exists(desc_path):
            desc_path = self.get_next_file(self.rest_folder)
        shutil.move(self.path, desc_path)

class FolderHandler(SortingHandler):

    def __init__(self, path):
        SortingHandler.__init__(self, path)

    def sort_dir(self, folders):
        dirs = [f for f in next(os.walk('.'))[1] if f not in folders and f != self.rest_folder]
        dirs = [f for f in dirs if not re.match('^\\.', f)]

        for dir in dirs:
            src_path = os.path.join(self.path, dir)
            dest_path = os.path.join(self.path, self.rest_folder)
            print(os.path.join(self.path, self.rest_folder, dir))
            if os.path.exists(os.path.join(self.path, self.rest_folder, dir)):
                dest_path = self.get_next_folder(dir)
            shutil.move(src_path, dest_path)
            logging.info(f'{src_path} >> {dest_path}')


    ## TODO Fixing get_next_folder
    def get_next_folder(self, folder):
        dest = os.path.join(self.folder_path, folder)
        while os.path.exists(os.path.join(dest, self.name)):
            self.num += 1

            period = self.name.rfind('.')
            if period == -1:
                period = len(self.name)

            new_file = f'{self.name[:period]}_{self.num}{self.name[period:]}'
            dest = os.path.join(dest, new_file)
        return dest

